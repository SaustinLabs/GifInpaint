# TRUE Manual Mask Painting Guide

## The EASIEST Way: Paint in Photoshop/GIMP, Load in ComfyUI

This is the most practical approach for manual mask painting:

### Step-by-Step Process

#### 1. Export First Frame of Your GIF
```
ComfyUI Workflow:
LoadGIF → GIFFrameSelector (frame 0-1) → SaveImage
```
This saves your first frame as a PNG.

#### 2. Paint Your Mask in Any Image Editor

**In Photoshop:**
1. Open the saved frame
2. Create new layer
3. Paint WHITE over areas you want to REMOVE
4. Paint BLACK over areas you want to KEEP
5. Delete/hide the original frame layer (mask layer only)
6. Save as `my_mask.png`

**In GIMP:**
1. Open the saved frame
2. Create new layer (fill with black)
3. Use white brush to paint areas to remove
4. Export as `my_mask.png`

**In Paint.NET / Krita:**
- Same concept: Black = keep, White = remove
- Save as PNG

**Important:** 
- White = will be inpainted (removed)
- Black = will be preserved
- Gray = partial inpainting

#### 3. Move Mask to ComfyUI Input Folder

Place your `my_mask.png` in:
```
G:\ComfyUI\ComfyUI-master\input\
```

#### 4. Use the LoadPaintedMask Node

New workflow included: **true_manual_painting.json**

Node #3 is `LoadPaintedMask`:
- Set `mask_image_path` to your mask filename
- It automatically resizes to match your GIF
- Set `invert_mask` to "yes" if you painted it backwards

The mask is then applied to ALL frames of your GIF!

---

## Three Mask Painting Nodes Included

### 1. LoadPaintedMask (RECOMMENDED) ⭐
**Best for:** Real manual painting workflow

**How it works:**
- Paint mask in Photoshop/GIMP/etc
- Save to ComfyUI input folder
- Node loads and applies it
- Works perfectly, no complications

**Inputs:**
- `reference_image`: One frame from your GIF
- `mask_image_path`: Filename (e.g., "my_mask.png")
- `invert_mask`: Swap black/white if needed

**Example workflow:** `true_manual_painting.json`

---

### 2. SimpleMaskDrawer
**Best for:** Quick coordinate-based masks

**How it works:**
- Specify points as coordinates: `100,100;150,150;200,200`
- Node draws circles and lines between points
- Good for simple shapes

**Inputs:**
- `reference_image`: Frame for sizing
- `brush_strokes`: Semicolon-separated x,y coordinates
- `brush_size`: Thickness of the brush
- `use_color_picker`: Reserved for future use

**Use case:** Quick testing without external tools

---

### 3. ManualMaskPainter
**Best for:** Programmatic mask generation

**How it works:**
- Similar to SimpleMaskDrawer
- Takes coordinate data as string
- Draws circles at each point

**Inputs:**
- `reference_image`: Frame for sizing
- `brush_size`: Circle radius
- `mask_data`: Semicolon-separated coordinates

**Use case:** Advanced users, scripting, API integration

---

## Complete Workflow: true_manual_painting.json

This workflow demonstrates the full process:

1. **LoadGIF** (Node 1)
   - Loads your animated GIF
   
2. **GIFFrameSelector** (Node 2)
   - Extracts first frame (0-1)
   - This is your reference for mask painting

3. **LoadPaintedMask** (Node 3) ⭐ NEW!
   - Loads your hand-painted mask
   - Put mask PNG in `ComfyUI/input/` folder
   - Automatically resizes to match GIF

4. **BatchMaskGenerator** (Node 4)
   - Takes your painted mask
   - Applies it to ALL frames
   - `mask_type: manual`

5. **BatchInpaintPreview** (Node 5)
   - Shows preview of masked frames
   - Optional but helpful

6-13. **Standard Inpainting Pipeline**
   - CheckpointLoader → VAEEncode → SetLatentNoiseMask
   - KSampler → VAEDecode → SaveGIF
   - Uses regular SD 1.5 models (NOT inpainting-specific)

---

## Why This Approach is Best

### ✅ Advantages
- **Real manual painting** - use your favorite tools
- **Precise control** - zoom, undo, layers, filters
- **Familiar workflow** - use tools you already know
- **Works immediately** - no custom ComfyUI extensions needed
- **Flexible** - any image editor works

### ❌ Previous Approach Problems
- ComfyUI has no built-in mask painting
- Extensions are complicated/unreliable
- Coordinate-based drawing is awkward
- Automated masks too limited

---

## Quick Start

### Option A: Load Example Workflow
```
1. Copy true_manual_painting.json to ComfyUI
2. Load in ComfyUI interface
3. All nodes should be connected (green)
```

### Option B: Paint Your First Mask
```
1. Run workflow once with any GIF
2. Node 2 saves first frame
3. Open frame in Photoshop/GIMP
4. Paint white over what you want removed
5. Save as my_mask.png to input folder
6. Update Node 3 mask_image_path
7. Run workflow again → inpainted GIF!
```

---

## Troubleshooting

### "Mask file not found"
- Check the console - it shows the expected path
- Default: `G:\ComfyUI\ComfyUI-master\input\my_mask.png`
- Make sure filename in node matches actual file

### "Blank mask / nothing removed"
- Ensure white = areas to remove
- Try setting `invert_mask: yes`
- Check mask dimensions match (node auto-resizes)

### "Wrong area masked"
- Verify mask aligns with first frame
- GIFs with movement might need motion tracking
- Consider using MotionMaskGenerator for moving objects

### "Works on first frame but not others"
- This is expected! The mask is static
- All frames get the SAME mask position
- For moving targets, use MotionMaskGenerator or ColorRangeMaskGenerator

---

## Advanced: Mask Painting Tips

### Creating Perfect Masks

**1. Feathered Edges**
- Use soft brush (Photoshop: 0% hardness)
- Creates smooth transition
- Better inpainting results

**2. Multiple Objects**
- Paint all removal areas in one mask
- White = remove, all at once

**3. Partial Removal**
- Use gray values for transparency
- 50% gray = 50% inpainting strength
- Good for watermarks/logos

**4. Precision Editing**
- Work at 200-400% zoom
- Use selection tools then fill
- Cleaner edges = better results

### Mask Reuse

Save your masks! You can:
- Use same mask on different GIFs (if similar composition)
- Modify existing masks slightly
- Build a library of common shapes

---

## Comparison Chart

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **LoadPaintedMask** | Full control, familiar tools, precise | Requires external editor, extra step | Most use cases ⭐ |
| **SimpleMaskDrawer** | Quick, no external tools | Awkward coordinate input | Testing |
| **ManualMaskPainter** | Programmatic | Hard to use manually | Scripts / API |
| **BatchMaskGenerator (center_box)** | Instant | Only rectangles | Simple box removal |
| **ColorRangeMaskGenerator** | Automatic color detection | Limited to color-based | Green screen, solid backgrounds |
| **MotionMaskGenerator** | Tracks movement | Complex setup | Moving objects |

---

## Summary

**For manual mask painting, use this workflow:**

1. **Paint mask in Photoshop/GIMP** (white = remove)
2. **Save to ComfyUI input folder** (e.g., my_mask.png)
3. **Use LoadPaintedMask node** to load it
4. **BatchMaskGenerator** (manual mode) broadcasts to all frames
5. **Standard inpainting pipeline** removes the masked areas

This is the **simplest, most practical** approach for manual mask painting in ComfyUI.

**Workflow file:** `workflows/true_manual_painting.json`

**New nodes:** LoadPaintedMask, SimpleMaskDrawer, ManualMaskPainter
