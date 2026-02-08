"""
ComfyUI Custom Nodes for GIF Inpainting
"""

import torch
import numpy as np
from PIL import Image, ImageSequence
import io
import folder_paths
import os


class LoadGIF:
    """
    Load animated GIF and extract frames as batch
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if f.endswith('.gif')]
        return {
            "required": {
                "gif": (sorted(files), {"image_upload": True}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("frames", "frame_count", "width", "height")
    FUNCTION = "load_gif"
    CATEGORY = "GifInpaint"
    
    def load_gif(self, gif):
        input_dir = folder_paths.get_input_directory()
        gif_path = os.path.join(input_dir, gif)
        
        img = Image.open(gif_path)
        frames = []
        
        for frame in ImageSequence.Iterator(img):
            # Convert to RGB (GIFs might be in palette mode)
            frame_rgb = frame.convert("RGB")
            # Convert to numpy array and normalize to [0, 1]
            frame_np = np.array(frame_rgb).astype(np.float32) / 255.0
            frames.append(frame_np)
        
        # Stack frames into batch tensor [B, H, W, C]
        frames_tensor = torch.from_numpy(np.stack(frames))
        
        frame_count = len(frames)
        height, width = frames[0].shape[:2]
        
        return (frames_tensor, frame_count, width, height)


class SaveGIF:
    """
    Save batch of frames as animated GIF
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "inpainted"}),
                "duration": ("INT", {"default": 100, "min": 10, "max": 1000, "step": 10}),
                "loop": ("INT", {"default": 0, "min": 0, "max": 100}),
                "optimize": ("BOOLEAN", {"default": True}),
            },
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_gif"
    OUTPUT_NODE = True
    CATEGORY = "GifInpaint"
    
    def save_gif(self, frames, filename_prefix="inpainted", duration=100, loop=0, optimize=True):
        output_dir = folder_paths.get_output_directory()
        
        # Convert tensor frames to PIL Images
        pil_frames = []
        for frame in frames:
            # Convert from [H, W, C] tensor to numpy array
            frame_np = frame.cpu().numpy()
            # Denormalize from [0, 1] to [0, 255]
            frame_np = (frame_np * 255).astype(np.uint8)
            pil_frame = Image.fromarray(frame_np)
            pil_frames.append(pil_frame)
        
        # Generate filename
        counter = 1
        while True:
            filename = f"{filename_prefix}_{counter:04d}.gif"
            filepath = os.path.join(output_dir, filename)
            if not os.path.exists(filepath):
                break
            counter += 1
        
        # Save as animated GIF
        pil_frames[0].save(
            filepath,
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration,
            loop=loop,
            optimize=optimize
        )
        
        return {"ui": {"gifs": [{"filename": filename, "type": "output"}]}}


class GIFFrameSelector:
    """
    Select specific frames or range from GIF batch
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "start_frame": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "end_frame": ("INT", {"default": -1, "min": -1, "max": 10000}),
                "step": ("INT", {"default": 1, "min": 1, "max": 100}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("frames", "frame_count")
    FUNCTION = "select_frames"
    CATEGORY = "GifInpaint"
    
    def select_frames(self, frames, start_frame=0, end_frame=-1, step=1):
        total_frames = frames.shape[0]
        
        if end_frame == -1 or end_frame > total_frames:
            end_frame = total_frames
        
        selected_frames = frames[start_frame:end_frame:step]
        new_count = selected_frames.shape[0]
        
        return (selected_frames, new_count)


class BatchMaskGenerator:
    """
    Generate masks for batch processing with various methods
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "mask_type": (["manual", "color_range", "center_box", "edge_detection"], {"default": "center_box"}),
            },
            "optional": {
                "mask": ("MASK",),  # For manual mask
                "x": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "y": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "width": ("INT", {"default": 100, "min": 1, "max": 4096}),
                "height": ("INT", {"default": 100, "min": 1, "max": 4096}),
                "feather": ("INT", {"default": 0, "min": 0, "max": 100}),
            },
        }
    
    RETURN_TYPES = ("MASK",)
    FUNCTION = "generate_mask"
    CATEGORY = "GifInpaint"
    
    def generate_mask(self, frames, mask_type, mask=None, x=0, y=0, width=100, height=100, feather=0):
        batch_size, h, w, _ = frames.shape
        
        if mask_type == "manual" and mask is not None:
            # Use provided mask for all frames
            if mask.dim() == 2:
                # Single mask, broadcast to all frames
                masks = mask.unsqueeze(0).repeat(batch_size, 1, 1)
            else:
                masks = mask
        
        elif mask_type == "center_box":
            # Create box mask in center or at specified position
            masks = torch.zeros((batch_size, h, w))
            
            # Clamp coordinates
            x1 = max(0, min(x, w))
            y1 = max(0, min(y, h))
            x2 = max(0, min(x + width, w))
            y2 = max(0, min(y + height, h))
            
            masks[:, y1:y2, x1:x2] = 1.0
            
            # Apply feathering if requested
            if feather > 0:
                from scipy.ndimage import gaussian_filter
                for i in range(batch_size):
                    masks[i] = torch.from_numpy(
                        gaussian_filter(masks[i].numpy(), sigma=feather)
                    )
        
        elif mask_type == "color_range":
            # Simple edge-based mask (fallback)
            masks = torch.zeros((batch_size, h, w))
            masks[:, h//4:3*h//4, w//4:3*w//4] = 1.0
        
        else:
            # Default: small center box
            masks = torch.zeros((batch_size, h, w))
            center_x, center_y = w // 2, h // 2
            box_size = min(w, h) // 4
            masks[:, 
                  center_y - box_size:center_y + box_size,
                  center_x - box_size:center_x + box_size] = 1.0
        
        return (masks,)


class GIFInfo:
    """
    Display information about loaded GIF
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_info"
    CATEGORY = "GifInpaint"
    OUTPUT_NODE = True
    
    def get_info(self, frames):
        batch_size, height, width, channels = frames.shape
        
        info = f"""GIF Information:
- Frame Count: {batch_size}
- Dimensions: {width}x{height}
- Channels: {channels}
- Total Pixels: {batch_size * height * width * channels:,}
- Memory Size: {frames.element_size() * frames.nelement() / 1024 / 1024:.2f} MB
"""
        
        return {"ui": {"text": [info]}, "result": (info,)}


class FrameInterpolator:
    """
    Interpolate frames to increase frame count (smooth animation)
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "interpolation_factor": ("INT", {"default": 2, "min": 2, "max": 10}),
                "method": (["linear", "cubic"], {"default": "linear"}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("frames", "frame_count")
    FUNCTION = "interpolate_frames"
    CATEGORY = "GifInpaint"
    
    def interpolate_frames(self, frames, interpolation_factor=2, method="linear"):
        import torch.nn.functional as F
        
        batch_size = frames.shape[0]
        
        # Simple linear interpolation between frames
        new_frames = []
        
        for i in range(batch_size - 1):
            new_frames.append(frames[i])
            
            # Add interpolated frames between current and next
            for j in range(1, interpolation_factor):
                alpha = j / interpolation_factor
                interpolated = frames[i] * (1 - alpha) + frames[i + 1] * alpha
                new_frames.append(interpolated)
        
        # Add last frame
        new_frames.append(frames[-1])
        
        result = torch.stack(new_frames)
        new_count = result.shape[0]
        
        return (result, new_count)


class BatchInpaintPreview:
    """
    Preview frames with mask overlay
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "masks": ("MASK",),
                "frame_index": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "mask_opacity": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "preview"
    CATEGORY = "GifInpaint"
    
    def preview(self, frames, masks, frame_index=0, mask_opacity=0.5):
        batch_size = frames.shape[0]
        frame_index = min(frame_index, batch_size - 1)
        
        frame = frames[frame_index].clone()
        mask = masks[frame_index] if masks.dim() > 2 else masks
        
        # Create red overlay for mask
        mask_overlay = torch.zeros_like(frame)
        mask_overlay[:, :, 0] = mask  # Red channel
        
        # Blend frame with mask overlay
        preview_frame = frame * (1 - mask_opacity) + mask_overlay * mask_opacity
        preview_frame = torch.clamp(preview_frame, 0, 1)
        
        return (preview_frame.unsqueeze(0),)


# Node registration
NODE_CLASS_MAPPINGS = {
    "LoadGIF": LoadGIF,
    "SaveGIF": SaveGIF,
    "GIFFrameSelector": GIFFrameSelector,
    "BatchMaskGenerator": BatchMaskGenerator,
    "GIFInfo": GIFInfo,
    "FrameInterpolator": FrameInterpolator,
    "BatchInpaintPreview": BatchInpaintPreview,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadGIF": "Load GIF 🎬",
    "SaveGIF": "Save GIF 💾",
    "GIFFrameSelector": "GIF Frame Selector 🎞️",
    "BatchMaskGenerator": "Batch Mask Generator 🎭",
    "GIFInfo": "GIF Info ℹ️",
    "FrameInterpolator": "Frame Interpolator 🔄",
    "BatchInpaintPreview": "Batch Inpaint Preview 👁️",
}
