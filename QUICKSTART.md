# Quick Start Guide

## 🚀 Getting Started with GIF Inpainter Studio

### Prerequisites
- ComfyUI installed and working
- SD 1.5 Inpainting model (recommended: `sd_v1-5_inpainting.ckpt`)
- A GIF you want to edit

### Step-by-Step Tutorial

#### 1. Installation
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/SaustinLabs/GifInpaint.git
cd GifInpaint
pip install -r requirements.txt
```

Restart ComfyUI after installation.

#### 2. Prepare Your GIF
- Place your GIF in `ComfyUI/input/` folder
- Recommended: GIFs under 500 frames, resolution under 512x512 for best performance

#### 3. Basic Workflow Setup

Open ComfyUI and create this workflow:

**a) Load GIF**
- Add `Load GIF 🎬` node
- Select your GIF from dropdown

**b) Create Mask**
- Add `Batch Mask Generator 🎭` node
- Connect frames from Load GIF
- Settings:
  - Mask Type: `center_box`
  - X, Y: Position of unwanted object
  - Width, Height: Size of removal area
  - Feather: 5-10 for smooth edges

**c) Preview (Optional)**
- Add `Batch Inpaint Preview 👁️` node
- Connect frames and mask
- Check frame 0, middle frame, and last frame
- Adjust mask if needed

**d) Encode for Inpainting**
- Add `VAEEncode` node
- Connect frames from Load GIF
- Add `VAELoader` node → load `sd_vae_ft_mse.safetensors`

**e) Apply Mask**
- Add `SetLatentNoiseMask` node
- Connect latent from VAEEncode
- Connect mask from Batch Mask Generator

**f) Inpaint**
- Add `CheckpointLoaderSimple` → load `sd_v1-5_inpainting.ckpt`
- Add `KSampler` node
  - Connect model from checkpoint
  - Connect latent from SetLatentNoiseMask
  - Settings:
    - Steps: 20-30
    - CFG: 6-8
    - Denoise: 0.7-0.8
    - Sampler: euler or dpm++_2m

**g) Decode & Save**
- Add `VAEDecode` node
- Connect samples from KSampler
- Add `Save GIF 💾` node
- Connect frames from VAEDecode
- Settings:
  - Filename prefix: "my_cleaned_gif"
  - Duration: 100 (adjust for speed)
  - Loop: 0 (infinite)
  - Optimize: true

#### 4. Run the Workflow
- Click "Queue Prompt"
- Wait for processing (time depends on frame count)
- Find output in `ComfyUI/output/` folder

### 📊 Example Use Cases

#### Remove Person from Background
```
Settings:
- Mask: center_box around person
- Feather: 10
- Prompt: "empty room, clean background"
- Denoise: 0.75
```

#### Remove Watermark
```
Settings:
- Mask: small box over watermark
- Feather: 5
- Prompt: "seamless, clean"
- Denoise: 0.8
```

#### Remove Text Overlay
```
Settings:
- Mask: rectangle covering text
- Feather: 8
- Prompt: "clear surface, no text"
- Denoise: 0.7
```

### ⚡ Performance Tips

**For Large GIFs:**
1. Use `GIF Frame Selector` to process in chunks
2. Example: Process frames 0-50, then 51-100, etc.

**For Better Quality:**
1. Increase sampling steps (30-40)
2. Use higher resolution inpainting model
3. Apply `Frame Interpolator` after inpainting

**For Speed:**
1. Reduce frame count
2. Lower resolution before processing
3. Use faster sampler (euler_a)
4. Fewer steps (15-20)

### 🎨 Advanced Techniques

#### Multi-Object Removal
Create multiple masks and combine them:
1. Generate mask for object 1
2. Generate mask for object 2
3. Use mask addition node to combine
4. Apply combined mask

#### Tracking Object Across Frames
For objects that move:
1. Use `Frame Selector` to split into sections
2. Adjust mask position per section
3. Process separately
4. Recombine frames

#### Creating Smooth Animations
After inpainting:
1. Add `Frame Interpolator 🔄` node
2. Set factor to 2 or 3
3. This doubles/triples frame count
4. Results in smoother motion

### 🐛 Common Issues

**"GIF not found"**
- Check GIF is in `ComfyUI/input/` folder
- Refresh ComfyUI

**"Out of memory"**
- Reduce frame count with Frame Selector
- Lower CFG and steps
- Process in smaller batches

**"Poor inpainting quality"**
- Increase feather on mask
- Adjust denoise (try 0.6-0.9 range)
- Improve prompt
- Use better inpainting model

**"Flickering in output"**
- Increase mask feather
- Lower denoise slightly
- Use consistent seed (not "fixed")
- Apply temporal smoothing

### 📖 Next Steps

1. **Load Example Workflow**: Import `workflows/basic_inpaint_workflow.json`
2. **Experiment**: Try different mask types and sizes
3. **Optimize**: Find best settings for your use case
4. **Share**: Join the discussion and share results!

### 🔗 Resources

- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI)
- [SD Inpainting Models](https://huggingface.co/runwayml/stable-diffusion-inpainting)
- [Example GIFs for Testing](https://giphy.com/)

---

**Need help?** Open an issue on GitHub!

Happy inpainting! 🎬✨
