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

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Version info
__version__ = "1.0.0"
__author__ = "SaustinLabs"
__description__ = "Automated GIF inpainting tool for ComfyUI"

print(f"🎬 GIF Inpainter Studio v{__version__} loaded successfully!")
