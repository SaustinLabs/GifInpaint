# Manual Mask Painting Guide

## The Problem
The `BatchMaskGenerator` node creates **automatic** masks (boxes, color detection, etc). 
For **manual painting**, you need to use ComfyUI's UI features.

## Solution: Use BatchMaskGenerator + Adjust in UI

### Method 1: Start with Automated Mask, Then Refine

1. **Load your GIF**
   - Add `Load GIF` node
   - Select your GIF

2. **Create initial automated mask**
   - Add `BatchMaskGenerator` node
   - Set `mask_type: center_box` or `color_range`
   - This creates a starting mask
   
3. **View and refine the mask**
   - The workflow now has a working automated mask
   - Use the preview nodes to see what will be inpainted

### Method 2: Paint Masks Externally

**ComfyUI doesn't have a dedicated mask painting node.** Instead, you have two options:

**Option A: Use Image Editing Software**
1. Export first frame of your GIF
2. Open in Photoshop/GIMP/Paint.NET
3. Create a black-and-white mask (white = remove, black = keep)
4. Save mask as PNG
5. Use `LoadImageMask` node in ComfyUI to load your painted mask
6. Connect to `BatchMaskGenerator` with `mask_type: manual`

**Option B: Use ComfyUI-Manager Extensions**
Install mask painting extensions from ComfyUI-Manager:
- **ComfyUI_essentials** - has MaskFromColor, MaskFromBatch
- **rgthree-comfy** - has mask utilities
- **was-node-suite-comfyui** - has mask drawing tools

### Method 3: Automated Masking (Easiest)

**This is the recommended approach** - just use `BatchMaskGenerator` with:
- `mask_type: center_box` - creates a box mask (adjust x, y, width, height)
- `mask_type: color_range` - removes specific colors (great for green screens or solid backgrounds)

**Advantages:**
- Works immediately, no external tools needed
- Adjustable parameters in real-time
- Good for most use cases

## How Manual Masking ACTUALLY Works in ComfyUI

**Reality Check:** ComfyUI doesn't have a built-in mask painting node like Photoshop. The UI can display masks, but creating them requires either:
1. External image editing software
2. Installing additional custom node packages
3. Using automated methods (recommended)

The **manual_painting_workflow.json** uses automated masking (`center_box`) because:
- It works out of the box
- No additional extensions needed  
- You can adjust the box size/position in real-time
- For 80% of use cases, this is sufficient

## Complete Working Workflow

The included **manual_painting_workflow.json** demonstrates:

1. **LoadGIF** - Loads your animated GIF
2. **BatchMaskGenerator** - Creates masks using `center_box` method
   - Adjust the x, y, width, height parameters to position your mask
   - The mask is applied to ALL frames automatically
3. **BatchInpaintPreview** - Shows preview of what will be masked (optional)
4. **CheckpointLoader** - Uses regular SD 1.5 model (NOT inpainting model)
5. **VAEEncode** → **SetLatentNoiseMask** - Applies mask in latent space
6. **KSampler** - Generates inpainted content with your prompts
7. **VAEDecode** → **SaveGIF** - Output inpainted GIF

**To adjust the mask area:**
- Open Node #2 (BatchMaskGenerator)
- Change: `x, y` = top-left corner position
- Change: `width, height` = size of the area to remove
- Preview updates in Node #3

## The 4-Channel Error Fix (from previous workflow)

**Problem:** `expected input to have 4 channels, but got 3 channels`

**Cause:** Using regular SD model instead of inpainting model

**Solution:**
Use one of these inpainting models:
- `sd_v1-5_inpainting.ckpt` 
- `sd-v1-5-inpainting.safetensors`
- Any model with "inpainting" in the name

Download from: https://huggingface.co/runwayml/stable-diffusion-inpainting

## Alternative: Don't Use Inpainting Models

If you don't have an inpainting model, you can use **regular models** with a different approach:

### Workflow Without Inpainting Model

```
1. Load GIF frames
2. Create mask (manual or auto)
3. Use img2img approach instead of inpainting:
   - VAEEncode your frames
   - Use KSampler with high denoise (0.8-0.95)
   - Add image conditioning instead of inpainting
   - Mask limits where changes happen
```

This works with any SD 1.5 model!

## Complete Manual Painting Workflow

### What You Need:
- ComfyUI
- Regular SD 1.5 model (OR inpainting model)
- Your GIF in `ComfyUI/input/` folder

### Steps:

1. **Load GIF**
   ```
   Add Node → GifInpaint → Load GIF
   ```

2. **Extract Single Frame for Mask Creation**
   ```
   Add Node → GifInpaint → GIF Frame Selector
   - start_frame: 0
   - end_frame: 1
   (This gets just the first frame)
   ```

3. **Paint Your Mask**
   ```
   Add Node → mask → MaskEditor
   - Connect the single frame
   - Paint over what you want to remove (white = remove)
   - Black = keep, White = remove
   ```

4. **Apply Mask to All Frames**
   ```
   Add Node → GifInpaint → Batch Mask Generator
   - mask_type: manual
   - mask: connect from MaskEditor
   - frames: connect from Load GIF (all frames)
   ```

5. **Process with Regular Model (NOT inpainting)**
   ```
   Load GIF frames → VAEEncode → 
   SetLatentNoiseMask (with your mask) →
   KSampler (regular checkpoint, denoise 0.9) →
   VAEDecode → Save GIF
   ```

## Important Notes

### For Automatic Masks (No Painting):
- Use `BatchMaskGenerator` directly
- Set box coordinates (x, y, width, height)
- This creates masks automatically

### For Manual Painting:
- Use `MaskEditor` node (ComfyUI built-in)
- Paint once on one frame
- Broadcast to all frames with BatchMaskGenerator (manual mode)

## Quick Fix for Your Current Setup

Since you're getting errors, try this:

1. **Don't use sd_v1-5_inpainting.ckpt** - use a regular model instead
2. **Add proper text encoding:**
   - CheckpointLoader → CLIP output → CLIPTextEncode → "your prompt"
   - That creates CONDITIONING → connect to KSampler positive
   - Another CLIPTextEncode with "" → KSampler negative

3. **For manual mask:**
   - Get one frame from your GIF
   - Use MaskEditor to paint
   - Apply to all frames

## Why This is Confusing

The SD inpainting models expect:
- 4 channels: RGB + mask channel (baked together)
- Special preprocessing

Regular models with masked latents:
- 3 channels: Just RGB
- Mask applied separately in latent space
- **This is easier and works with any model!**

**Recommendation:** Use regular SD 1.5 models with latent masking (not inpainting-specific models).

## Example Working Workflow (No Inpainting Model)

```
[Load GIF] → frames → [GIF Frame Selector (0-1)] → [MaskEditor (paint here)]
                                                              ↓
[Load GIF] → frames → [Batch Mask Generator (manual)] ← mask from MaskEditor
       ↓                              ↓
   [VAEEncode] → latent → [SetLatentNoiseMask] ← mask
                                    ↓
                              [KSampler] ← regular checkpoint
                                    ↓        (like realisticVision, dreamshaper, etc)
                              [VAEDecode]
                                    ↓
                              [Save GIF]
```

This uses regular models and works great!
