"""
Manual Mask Painting Node for GifInpaint
Allows drawing masks directly in ComfyUI interface
"""

import torch
import numpy as np
from PIL import Image, ImageDraw
import base64
import io
import json

class ManualMaskPainter:
    """
    Node that allows manual mask painting in ComfyUI.
    Paint white areas to mark regions for removal.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reference_image": ("IMAGE",),
                "brush_size": ("INT", {
                    "default": 50,
                    "min": 1,
                    "max": 500,
                    "step": 1
                }),
                "mask_data": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "create_mask"
    CATEGORY = "GifInpaint"
    
    def create_mask(self, reference_image, brush_size, mask_data):
        """
        Create a mask from painted data.
        If mask_data is empty, returns a blank mask.
        """
        # Get dimensions from reference image
        batch_size = reference_image.shape[0]
        height = reference_image.shape[1]
        width = reference_image.shape[2]
        
        # Initialize blank mask
        mask = torch.zeros((height, width), dtype=torch.float32)
        
        # Parse mask_data if provided
        if mask_data and mask_data.strip():
            try:
                # Expect comma-separated x,y coordinates
                points = mask_data.strip().split(';')
                
                # Create PIL image for drawing
                mask_pil = Image.new('L', (width, height), 0)
                draw = ImageDraw.Draw(mask_pil)
                
                # Draw circles at each point
                for point in points:
                    if point.strip():
                        x, y = map(int, point.split(','))
                        # Draw circle (brush)
                        radius = brush_size // 2
                        draw.ellipse(
                            [(x - radius, y - radius), 
                             (x + radius, y + radius)],
                            fill=255
                        )
                
                # Convert to tensor
                mask_np = np.array(mask_pil).astype(np.float32) / 255.0
                mask = torch.from_numpy(mask_np)
                
            except Exception as e:
                print(f"Error parsing mask data: {e}")
                # Return blank mask on error
                pass
        
        return (mask,)


class SimpleMaskDrawer:
    """
    Simpler approach: Create mask from coordinates.
    Use with external painting or coordinate specification.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reference_image": ("IMAGE",),
                "use_color_picker": (["no", "yes"],),
            },
            "optional": {
                "brush_strokes": ("STRING", {
                    "default": "100,100;150,150;200,200",
                    "multiline": True
                }),
                "brush_size": ("INT", {
                    "default": 50,
                    "min": 5,
                    "max": 200,
                    "step": 5
                }),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "draw_mask"
    CATEGORY = "GifInpaint"
    
    def draw_mask(self, reference_image, use_color_picker, brush_strokes="", brush_size=50):
        """Create mask from brush stroke coordinates."""
        
        # Get dimensions from reference image
        height = reference_image.shape[1]
        width = reference_image.shape[2]
        
        # Create blank mask
        mask_pil = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask_pil)
        
        if brush_strokes and brush_strokes.strip():
            # Parse coordinates
            strokes = brush_strokes.strip().split(';')
            points = []
            
            for stroke in strokes:
                if ',' in stroke:
                    try:
                        x, y = map(float, stroke.split(','))
                        points.append((int(x), int(y)))
                    except:
                        continue
            
            # Draw each point as a circle
            radius = brush_size // 2
            for x, y in points:
                draw.ellipse(
                    [(x - radius, y - radius), 
                     (x + radius, y + radius)],
                    fill=255
                )
            
            # If we have multiple points, draw connecting lines
            if len(points) > 1:
                for i in range(len(points) - 1):
                    draw.line([points[i], points[i + 1]], 
                             fill=255, width=brush_size)
        
        # Convert to tensor
        mask_np = np.array(mask_pil).astype(np.float32) / 255.0
        mask = torch.from_numpy(mask_np)
        
        return (mask,)


class LoadPaintedMask:
    """
    Load a pre-painted mask from an image file.
    EASIEST METHOD: Paint mask in external tool, load it here.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "reference_image": ("IMAGE",),
                "mask_image_path": ("STRING", {
                    "default": "mask.png",
                    "multiline": False
                }),
                "invert_mask": (["no", "yes"],),
            }
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "load_mask"
    CATEGORY = "GifInpaint"
    
    def load_mask(self, reference_image, mask_image_path, invert_mask):
        """Load mask from a painted image file."""
        import folder_paths
        import os
        
        # Get dimensions
        height = reference_image.shape[1]
        width = reference_image.shape[2]
        
        # Try to find the image
        input_dir = folder_paths.get_input_directory()
        mask_path = os.path.join(input_dir, mask_image_path)
        
        if not os.path.exists(mask_path):
            print(f"Mask file not found: {mask_path}")
            print(f"Creating blank mask. Please place your mask image in: {input_dir}")
            mask = torch.zeros((height, width), dtype=torch.float32)
            return (mask,)
        
        try:
            # Load the mask image
            mask_img = Image.open(mask_path).convert('L')
            
            # Resize to match reference
            mask_img = mask_img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to tensor
            mask_np = np.array(mask_img).astype(np.float32) / 255.0
            
            # Invert if requested
            if invert_mask == "yes":
                mask_np = 1.0 - mask_np
            
            mask = torch.from_numpy(mask_np)
            
            print(f"✓ Loaded mask from: {mask_path}")
            return (mask,)
            
        except Exception as e:
            print(f"Error loading mask: {e}")
            mask = torch.zeros((height, width), dtype=torch.float32)
            return (mask,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "ManualMaskPainter": ManualMaskPainter,
    "SimpleMaskDrawer": SimpleMaskDrawer,
    "LoadPaintedMask": LoadPaintedMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ManualMaskPainter": "Manual Mask Painter",
    "SimpleMaskDrawer": "Simple Mask Drawer",
    "LoadPaintedMask": "Load Painted Mask",
}
