"""
Advanced nodes for GIF Inpainter Studio
These nodes provide additional functionality for complex use cases
"""

import torch
import numpy as np
from typing import Tuple


class AdvancedMaskEditor:
    """
    Advanced mask editing with brush, eraser, and shape tools
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "operation": (["dilate", "erode", "smooth", "invert"], {"default": "dilate"}),
                "strength": ("INT", {"default": 3, "min": 1, "max": 20}),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "edit_mask"
    CATEGORY = "GifInpaint/Advanced"
    
    def edit_mask(self, mask, operation, strength):
        from scipy.ndimage import binary_dilation, binary_erosion, gaussian_filter
        
        if operation == "dilate":
            if mask.dim() == 3:
                result = []
                for m in mask:
                    dilated = binary_dilation(m.numpy(), iterations=strength)
                    result.append(torch.from_numpy(dilated.astype(np.float32)))
                return (torch.stack(result),)
            else:
                dilated = binary_dilation(mask.numpy(), iterations=strength)
                return (torch.from_numpy(dilated.astype(np.float32)),)
        
        elif operation == "erode":
            if mask.dim() == 3:
                result = []
                for m in mask:
                    eroded = binary_erosion(m.numpy(), iterations=strength)
                    result.append(torch.from_numpy(eroded.astype(np.float32)))
                return (torch.stack(result),)
            else:
                eroded = binary_erosion(mask.numpy(), iterations=strength)
                return (torch.from_numpy(eroded.astype(np.float32)),)
        
        elif operation == "smooth":
            if mask.dim() == 3:
                result = []
                for m in mask:
                    smoothed = gaussian_filter(m.numpy(), sigma=strength)
                    result.append(torch.from_numpy(smoothed))
                return (torch.stack(result),)
            else:
                smoothed = gaussian_filter(mask.numpy(), sigma=strength)
                return (torch.from_numpy(smoothed),)
        
        elif operation == "invert":
            return (1.0 - mask,)
        
        return (mask,)


class MotionMaskGenerator:
    """
    Generate masks based on motion detection between frames
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "threshold": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "blur": ("INT", {"default": 5, "min": 0, "max": 20}),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "detect_motion"
    CATEGORY = "GifInpaint/Advanced"
    
    def detect_motion(self, frames, threshold, blur):
        from scipy.ndimage import gaussian_filter
        
        masks = []
        
        for i in range(len(frames) - 1):
            # Calculate frame difference
            diff = torch.abs(frames[i + 1] - frames[i])
            motion = torch.mean(diff, dim=2)  # Average across channels
            
            # Apply blur
            if blur > 0:
                motion_np = gaussian_filter(motion.numpy(), sigma=blur)
                motion = torch.from_numpy(motion_np)
            
            # Threshold
            mask = (motion > threshold).float()
            masks.append(mask)
        
        # Add last frame (copy of previous)
        masks.append(masks[-1] if masks else torch.zeros(frames.shape[1:3]))
        
        return (torch.stack(masks),)


class ColorRangeMaskGenerator:
    """
    Generate masks based on color similarity (like green screen removal)
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "red": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "green": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "blue": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "tolerance": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 1.0, "step": 0.01}),
                "feather": ("INT", {"default": 5, "min": 0, "max": 50}),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "color_mask"
    CATEGORY = "GifInpaint/Advanced"
    
    def color_mask(self, frames, red, green, blue, tolerance, feather):
        from scipy.ndimage import gaussian_filter
        
        target = torch.tensor([red, green, blue]).reshape(1, 1, 1, 3)
        
        masks = []
        for frame in frames:
            # Calculate color distance
            distance = torch.sqrt(torch.sum((frame - target) ** 2, dim=2))
            mask = (distance < tolerance).float()
            
            # Apply feathering
            if feather > 0:
                mask_np = gaussian_filter(mask.numpy(), sigma=feather)
                mask = torch.from_numpy(mask_np)
            
            masks.append(mask)
        
        return (torch.stack(masks),)


class MaskCombiner:
    """
    Combine multiple masks with various operations
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask1": ("MASK",),
                "mask2": ("MASK",),
                "operation": (["union", "intersection", "difference", "xor", "average"], 
                             {"default": "union"}),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "combine"
    CATEGORY = "GifInpaint/Advanced"
    
    def combine(self, mask1, mask2, operation):
        if operation == "union":
            result = torch.maximum(mask1, mask2)
        elif operation == "intersection":
            result = torch.minimum(mask1, mask2)
        elif operation == "difference":
            result = torch.clamp(mask1 - mask2, 0, 1)
        elif operation == "xor":
            result = torch.abs(mask1 - mask2)
        elif operation == "average":
            result = (mask1 + mask2) / 2.0
        else:
            result = mask1
        
        return (result,)


class TemporalSmoother:
    """
    Apply temporal smoothing to reduce flickering
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "window_size": ("INT", {"default": 3, "min": 1, "max": 11, "step": 2}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "smooth"
    CATEGORY = "GifInpaint/Advanced"
    
    def smooth(self, frames, window_size, strength):
        if window_size % 2 == 0:
            window_size += 1
        
        half_window = window_size // 2
        smoothed = []
        
        for i in range(len(frames)):
            start_idx = max(0, i - half_window)
            end_idx = min(len(frames), i + half_window + 1)
            window_frames = frames[start_idx:end_idx]
            
            # Calculate weighted average
            smoothed_frame = torch.mean(window_frames, dim=0)
            
            # Blend with original based on strength
            blended = frames[i] * (1 - strength) + smoothed_frame * strength
            smoothed.append(blended)
        
        return (torch.stack(smoothed),)


class BatchFrameResizer:
    """
    Resize all frames in batch
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 8}),
                "method": (["bilinear", "bicubic", "nearest"], {"default": "bilinear"}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("frames", "width", "height")
    FUNCTION = "resize"
    CATEGORY = "GifInpaint/Advanced"
    
    def resize(self, frames, width, height, method):
        import torch.nn.functional as F
        
        # Convert to [B, C, H, W]
        frames_transposed = frames.permute(0, 3, 1, 2)
        
        # Resize
        resized = F.interpolate(
            frames_transposed,
            size=(height, width),
            mode=method,
            align_corners=False if method != 'nearest' else None
        )
        
        # Convert back to [B, H, W, C]
        result = resized.permute(0, 2, 3, 1)
        
        return (result, width, height)


# Register advanced nodes
ADVANCED_NODE_CLASS_MAPPINGS = {
    "AdvancedMaskEditor": AdvancedMaskEditor,
    "MotionMaskGenerator": MotionMaskGenerator,
    "ColorRangeMaskGenerator": ColorRangeMaskGenerator,
    "MaskCombiner": MaskCombiner,
    "TemporalSmoother": TemporalSmoother,
    "BatchFrameResizer": BatchFrameResizer,
}

ADVANCED_NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedMaskEditor": "Advanced Mask Editor ✏️",
    "MotionMaskGenerator": "Motion Mask Generator 🎯",
    "ColorRangeMaskGenerator": "Color Range Mask 🎨",
    "MaskCombiner": "Mask Combiner ➕",
    "TemporalSmoother": "Temporal Smoother 📊",
    "BatchFrameResizer": "Batch Frame Resizer 📐",
}
