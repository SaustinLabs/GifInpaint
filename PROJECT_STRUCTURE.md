# Project Structure

```
GifInpaint/
├── __init__.py                 # Package initialization and node registration
├── nodes.py                    # Core ComfyUI nodes for GIF processing
├── advanced_nodes.py           # Advanced processing nodes
├── utils.py                    # Utility functions for image/mask processing
├── test_utils.py              # Testing utilities and sample GIF generators
├── setup.py                   # Setup and verification script
├── install.py                 # Dependency installation script
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── QUICKSTART.md              # Quick start tutorial
├── CHANGELOG.md               # Version history and changes
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── .gitignore                # Git ignore rules
├── workflows/                 # Example ComfyUI workflows
│   └── basic_inpaint_workflow.json
└── examples/                  # Example test GIFs and documentation
    └── README.md
```

## Core Files

### __init__.py
Package entry point that registers all nodes with ComfyUI.

### nodes.py
Main nodes:
- LoadGIF - Load and extract GIF frames
- SaveGIF - Export frames as animated GIF
- GIFFrameSelector - Select frame ranges
- BatchMaskGenerator - Generate masks
- GIFInfo - Display GIF information
- FrameInterpolator - Smooth animations
- BatchInpaintPreview - Preview with mask overlay

### advanced_nodes.py
Advanced functionality:
- AdvancedMaskEditor - Edit masks with operations
- MotionMaskGenerator - Detect motion between frames
- ColorRangeMaskGenerator - Color-based masking
- MaskCombiner - Combine multiple masks
- TemporalSmoother - Reduce flickering
- BatchFrameResizer - Resize frame batches

### utils.py
Helper functions for:
- Frame resizing
- Mask smoothing and gradients
- Motion detection
- Color range masking
- Mask operations (dilate, erode, combine)
- Temporal smoothing
- Bounding box calculation

### test_utils.py
Testing tools:
- create_test_gif() - Generate test GIFs
- create_test_watermark_gif() - Watermark test
- validate_node_outputs() - Node testing
- benchmark_processing() - Performance tests

## Installation Files

### setup.py
Complete setup and verification:
- Check Python version
- Verify dependencies
- Check ComfyUI installation
- Create example GIFs
- Verify node loading
- Display next steps

### install.py
Simple dependency installer for pip requirements.

### requirements.txt
Required packages:
- Pillow (image processing)
- NumPy (numerical operations)
- torch (tensor operations)
- scipy (scientific computing)

## Documentation

### README.md
Complete documentation including:
- Feature overview
- Installation instructions
- Node descriptions
- Workflow examples
- Tips and best practices
- Troubleshooting guide

### QUICKSTART.md
Step-by-step tutorial for:
- Installation
- Basic workflow setup
- Common use cases
- Performance tips
- Advanced techniques
- Common issues

### CHANGELOG.md
Version history and planned features.

### CONTRIBUTING.md
Guidelines for contributors.

## Workflows

### basic_inpaint_workflow.json
Complete example workflow showing:
1. GIF loading
2. Mask generation
3. Inpainting with SD
4. GIF export

Can be imported directly into ComfyUI.

## Usage

1. Copy entire folder to `ComfyUI/custom_nodes/`
2. Run `python setup.py` to verify installation
3. Restart ComfyUI
4. Find nodes under "GifInpaint" category
5. Import example workflow or build your own

## Development

To contribute or modify:
1. Edit nodes in `nodes.py` or `advanced_nodes.py`
2. Add utilities to `utils.py`
3. Register new nodes in `__init__.py`
4. Test with `test_utils.py`
5. Update documentation

## File Sizes

Typical file sizes:
- nodes.py: ~12KB (core functionality)
- advanced_nodes.py: ~10KB (advanced features)
- utils.py: ~8KB (utility functions)
- README.md: ~15KB (comprehensive docs)
- Total package: ~50KB (excluding dependencies)

Very lightweight and fast to load!
