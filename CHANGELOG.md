# Changelog

All notable changes to GIF Inpainter Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-08

### Added
- Initial release of GIF Inpainter Studio
- Core nodes for GIF loading and saving
- Batch mask generation with multiple types
- Frame selector for processing subsets
- Frame interpolator for smooth animations
- Inpaint preview with mask overlay
- GIF info display node
- Advanced nodes package:
  - Advanced Mask Editor (dilate, erode, smooth, invert)
  - Motion Mask Generator (automatic motion detection)
  - Color Range Mask Generator (green screen removal)
  - Mask Combiner (union, intersection, difference, xor, average)
  - Temporal Smoother (reduce flickering)
  - Batch Frame Resizer
- Comprehensive documentation and examples
- Quick start guide
- Example workflows
- Utility functions for advanced processing
- Test suite with sample GIF generators

### Features
- ✨ Fully automated frame-by-frame processing
- 🎬 Batch processing of all frames simultaneously
- 🎭 Multiple mask generation methods
- 🔄 Frame interpolation for smoother animations
- 👁️ Live preview with mask overlay
- 💾 Direct GIF export with optimization
- 🎨 Color-based masking (green screen)
- 🎯 Motion-based mask generation
- ✏️ Advanced mask editing tools
- 📊 Temporal smoothing to reduce flicker
- 📐 Batch frame resizing

### Documentation
- Complete README with features and installation
- Quick start guide with step-by-step tutorial
- Example workflows in JSON format
- Technical documentation for developers
- Troubleshooting guide
- Tips and best practices

### Compatibility
- ComfyUI latest version
- Python 3.8+
- PyTorch 2.0+
- Works with all SD inpainting models
- Compatible with ControlNet, LoRA, and other extensions

## [Unreleased]

### Planned Features
- Object tracking across frames
- Optical flow-based masking
- AI-powered automatic object detection
- Batch processing optimization
- GPU memory management improvements
- Multi-threading support
- Real-time preview mode
- Integration with Segment Anything Model (SAM)
- Custom brush tool for manual masking
- Timeline editor for frame-specific adjustments
- Export to video formats (MP4, WebM)
- Undo/redo functionality
- Preset mask templates
- Batch folder processing

### Future Enhancements
- Performance optimizations
- Better memory handling for large GIFs
- Enhanced interpolation algorithms
- UI improvements
- Additional mask generation methods
- Cloud processing support
- API for external integrations

---

[1.0.0]: https://github.com/SaustinLabs/GifInpaint/releases/tag/v1.0.0
