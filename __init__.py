"""
GIF Inpainter Studio - ComfyUI Custom Nodes
Automated content removal tool for animated GIFs
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Import advanced nodes
try:
    from .advanced_nodes import ADVANCED_NODE_CLASS_MAPPINGS, ADVANCED_NODE_DISPLAY_NAME_MAPPINGS
    NODE_CLASS_MAPPINGS.update(ADVANCED_NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(ADVANCED_NODE_DISPLAY_NAME_MAPPINGS)
except ImportError:
    print("Warning: Advanced nodes not available")

# Import manual mask painting nodes
try:
    from .mask_painter_node import NODE_CLASS_MAPPINGS as PAINTER_MAPPINGS
    from .mask_painter_node import NODE_DISPLAY_NAME_MAPPINGS as PAINTER_DISPLAY
    NODE_CLASS_MAPPINGS.update(PAINTER_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(PAINTER_DISPLAY)
    print(f"  + {len(PAINTER_MAPPINGS)} manual painting nodes loaded")
except ImportError as e:
    print(f"Warning: Manual painting nodes not available: {e}")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Version info
__version__ = "1.0.0"
__author__ = "SaustinLabs"
__description__ = "Automated GIF inpainting tool for ComfyUI"

print(f"🎬 GIF Inpainter Studio v{__version__} loaded successfully!")
