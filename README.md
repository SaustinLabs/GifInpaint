# 🎬 GIF Inpainter Studio

![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom_Node-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Automated content removal tool for animated GIFs** - A comprehensive ComfyUI custom node package for removing unwanted objects/people from animated GIFs using advanced inpainting techniques.

## 🎯 Core Features

✨ **Fully Automated** - No manual frame-by-frame editing required  
🎬 **Batch Processing** - Process all frames simultaneously  
🎭 **Multiple Mask Types** - Manual, box, color range, and more  
🔄 **Frame Interpolation** - Smooth animations with artificial frames  
👁️ **Live Preview** - See mask overlay before inpainting  
💾 **Direct Export** - Save as optimized animated GIF  

## 🎨 Manual Mask Painting (NEW!)

**Paint your masks in Photoshop/GIMP, load them in ComfyUI!**

The most requested feature is here: **true manual mask painting**. Instead of relying on automated box/color masks, you can now:

- ✏️ **Paint masks in your favorite image editor** (Photoshop, GIMP, Krita, Paint.NET)
- 📥 **Load with LoadPaintedMask node** - drag and drop
- 🎯 **Full precision control** - zoom, layers, soft brushes, selections
- 🔄 **Apply to all frames** - paint once, masks entire GIF

**Quick Start:**
1. Extract first frame from your GIF
2. Paint white over areas to remove (in any image editor)
3. Save as PNG to `ComfyUI/input/` folder
4. Use `LoadPaintedMask` node → apply to all frames!

See **[MANUAL_MASK_GUIDE.md](MANUAL_MASK_GUIDE.md)** for complete tutorial and workflow.

## 📋 Problem Solved

Creators struggle with unwanted elements in GIFs that require tedious manual removal. Existing solutions either:
- ❌ Require expensive software (Adobe After Effects)
- ❌ Are limited to static images (Photoshop Content-Aware Fill)
- ❌ Lack automation for animated content
- ❌ Have poor quality inpainting results

**GIF Inpainter Studio** integrates directly into ComfyUI, leveraging existing SD inpainting models for high-quality automated results.

## 🚀 Installation

### Method 1: ComfyUI Manager (Recommended)

1. Open ComfyUI Manager
2. Search for "GIF Inpainter Studio"
3. Click Install

### Method 2: Manual Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/SaustinLabs/GifInpaint.git
cd GifInpaint
pip install -r requirements.txt
```

Or use the install script:

```bash
cd ComfyUI/custom_nodes/GifInpaint
python install.py
```

### Method 3: Direct Copy

1. Copy the entire `GifInpaint` folder to `ComfyUI/custom_nodes/`
2. Restart ComfyUI
3. Dependencies will be installed automatically on first load

## 📦 Requirements

- Python 3.8+
- ComfyUI (latest version)
- PyTorch 2.0+
- Pillow 10.0+
- NumPy 1.24+
- SciPy 1.11+

## 🎨 Available Nodes

### 🎬 Load GIF
Load animated GIF and extract frames as batch tensor.

**Inputs:**
- `gif`: GIF file from input folder

**Outputs:**
- `frames`: Batch tensor [B, H, W, C]
- `frame_count`: Total number of frames
- `width`: Frame width
- `height`: Frame height

### 💾 Save GIF
Save batch of frames as animated GIF.

**Inputs:**
- `frames`: Batch tensor to save
- `filename_prefix`: Output filename prefix (default: "inpainted")
- `duration`: Frame duration in ms (default: 100)
- `loop`: Loop count (0 = infinite)
- `optimize`: Enable optimization

### 🎭 Batch Mask Generator
Generate masks for batch processing.

**Mask Types:**
- **manual**: Use custom mask input
- **center_box**: Box at specified position/center
- **color_range**: Color-based selection
- **edge_detection**: Edge-based mask

**Inputs:**
- `frames`: Input frames
- `mask_type`: Type of mask to generate
- `x, y, width, height`: Box parameters
- `feather`: Edge softness

**Outputs:**
- `MASK`: Batch mask tensor

### 🎞️ GIF Frame Selector
Select specific frames or ranges from batch.

**Inputs:**
- `frames`: Input batch
- `start_frame`: Starting frame index
- `end_frame`: Ending frame index (-1 = last)
- `step`: Frame skip interval

### 🔄 Frame Interpolator
Interpolate frames to increase frame count and smooth animation.

**Inputs:**
- `frames`: Input batch
- `interpolation_factor`: Frames to add between each pair
- `method`: Interpolation method (linear/cubic)

### 👁️ Batch Inpaint Preview
Preview frames with mask overlay before inpainting.

**Inputs:**
- `frames`: Input frames
- `masks`: Mask batch
- `frame_index`: Frame to preview
- `mask_opacity`: Overlay opacity

### ℹ️ GIF Info
Display information about loaded GIF (frames, size, memory).

---

## 🎨 Manual Painting Nodes (NEW!)

### 🖼️ Load Painted Mask ⭐ RECOMMENDED
Load hand-painted masks from external image editors (Photoshop, GIMP, etc.).

**Inputs:**
- `reference_image`: Frame for size matching
- `mask_image_path`: Filename in input folder (e.g., "my_mask.png")
- `invert_mask`: Swap black/white if needed (yes/no)

**Outputs:**
- `MASK`: Loaded and auto-resized mask

**Workflow:** Paint white = remove, black = keep. See `workflows/true_manual_painting.json`

### ✏️ Simple Mask Drawer
Draw masks using coordinate points (for testing).

**Inputs:**
- `reference_image`: Frame for sizing
- `brush_strokes`: Coordinates like "100,100;150,150;200,200"
- `brush_size`: Thickness (5-200px)

**Outputs:**
- `MASK`: Drawn mask

### 🖌️ Manual Mask Painter
Programmatic mask generation via coordinates.

**Inputs:**
- `reference_image`: Frame reference
- `brush_size`: Circle radius at each point
- `mask_data`: Semicolon-separated x,y coordinates

**Outputs:**
- `MASK`: Generated mask

---

## 🎯 Basic Workflow

### Simple Inpainting Workflow

```
1. Load GIF → Extract frames
2. Generate Mask → Define removal area
3. Preview → Verify mask placement
4. Inpaint → Use SD inpainting model
5. Save GIF → Export result
```

### Detailed Example

1. **Load your GIF**
   - Add `Load GIF` node
   - Select GIF from input folder
   - Frames are extracted automatically

2. **Create mask**
   - Add `Batch Mask Generator` node
   - Choose mask type (e.g., "center_box")
   - Adjust position and size
   - Set feather for smooth edges

3. **Preview (optional)**
   - Add `Batch Inpaint Preview` node
   - Check different frames
   - Adjust mask if needed

4. **Inpaint frames**
   - Connect to `VAEEncode` node
   - Use `SetLatentNoiseMask` with your mask
   - Connect to `KSampler` with inpainting model
   - Decode with `VAEDecode`

5. **Save result**
   - Add `Save GIF` node
   - Set duration (ms per frame)
   - Click Queue Prompt

## 📚 Example Workflows

### Basic Inpaint
Located in: `workflows/basic_inpaint_workflow.json`

Complete workflow showing:
- GIF loading
- Mask generation
- SD inpainting
- GIF export

### Advanced Features

**Selective Frame Processing:**
```
Load GIF → Frame Selector (0-50) → Inpaint → Save GIF
```

**Smooth Animation:**
```
Load GIF → Inpaint → Frame Interpolator (2x) → Save GIF
```

**Multi-Region Removal:**
```
Load GIF → Mask Generator 1 → Mask Generator 2 → Combine Masks → Inpaint
```

## 🎓 Tips & Best Practices

### Mask Creation
- Use **feathering** for seamless blending
- **Preview** multiple frames to ensure coverage
- Larger masks = slower processing but better context

### Inpainting Settings
- Use **SD 1.5 Inpainting model** for best results
- Set denoise strength: 0.6-0.8 for most cases
- Lower CFG (5-8) for more natural fills
- Prompt: "clean background, seamless, empty space"

### Performance
- Process fewer frames for faster testing
- Use `Frame Selector` to limit range
- Optimize GIF on save for smaller files
- Consider resolution (smaller = faster)

### Quality Enhancement
- Use `Frame Interpolator` after inpainting for smoother motion
- Apply multiple masks for complex removals
- Experiment with different inpainting models

## 🔧 Integration with ComfyUI

This package integrates seamlessly with existing ComfyUI workflows:

**Compatible with:**
- All VAE models
- All inpainting checkpoints
- ControlNet (for guided inpainting)
- LoRA models
- Image processing nodes

**Works alongside:**
- AnimateDiff
- Video processing nodes
- Batch image processors
- Custom samplers

## 🛠️ Technical Details

### Frame Format
- Frames are stored as `torch.Tensor` in format `[B, H, W, C]`
- Color space: RGB
- Value range: [0.0, 1.0] (normalized)
- Compatible with all ComfyUI image nodes

### Mask Format
- Masks are `torch.Tensor` in format `[B, H, W]`
- Value range: [0.0, 1.0] (0 = keep, 1 = inpaint)
- Supports per-frame masks or single mask for all frames

### Memory Considerations
- Large GIFs (many frames or high resolution) use significant VRAM
- Process in batches using `Frame Selector` if needed
- Consider downscaling before processing

## 🐛 Troubleshooting

**GIF not loading:**
- Ensure GIF is in ComfyUI input folder
- Check file is valid animated GIF
- Try converting with online tool

**Out of memory:**
- Reduce frame count with `Frame Selector`
- Lower resolution before processing
- Process in smaller batches

**Poor inpainting quality:**
- Adjust denoise strength
- Try different inpainting model
- Use better prompt
- Increase mask feather

**Slow processing:**
- Reduce frame count
- Lower resolution
- Use faster sampler (e.g., DPM++ 2M)
- Decrease sampling steps

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional mask generation methods
- Optical flow-based tracking
- Better interpolation algorithms  
- UI improvements
- Performance optimizations

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- ComfyUI team for the excellent framework
- Stable Diffusion for inpainting models
- Community for feedback and testing

## 📧 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions  
- **Updates**: Watch this repository

---

**Made with ❤️ for the ComfyUI community**

*Automate your GIF editing workflow today!* 🎬✨