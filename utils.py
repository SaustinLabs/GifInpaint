"""
Utility functions for GIF processing
"""

import torch
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional


def resize_frames(frames: torch.Tensor, target_size: Tuple[int, int]) -> torch.Tensor:
    """
    Resize batch of frames to target size
    
    Args:
        frames: Tensor of shape [B, H, W, C]
        target_size: (width, height) tuple
        
    Returns:
        Resized frames tensor
    """
    import torch.nn.functional as F
    
    # Convert to [B, C, H, W] for torch resize
    frames_transposed = frames.permute(0, 3, 1, 2)
    
    # Resize
    resized = F.interpolate(
        frames_transposed,
        size=(target_size[1], target_size[0]),
        mode='bilinear',
        align_corners=False
    )
    
    # Convert back to [B, H, W, C]
    return resized.permute(0, 2, 3, 1)


def apply_mask_smoothing(mask: torch.Tensor, kernel_size: int = 5) -> torch.Tensor:
    """
    Apply Gaussian smoothing to mask edges
    
    Args:
        mask: Mask tensor [B, H, W] or [H, W]
        kernel_size: Size of smoothing kernel
        
    Returns:
        Smoothed mask
    """
    from scipy.ndimage import gaussian_filter
    
    if mask.dim() == 2:
        # Single mask
        smoothed = gaussian_filter(mask.numpy(), sigma=kernel_size/2)
        return torch.from_numpy(smoothed)
    else:
        # Batch of masks
        smoothed_batch = []
        for m in mask:
            smoothed = gaussian_filter(m.numpy(), sigma=kernel_size/2)
            smoothed_batch.append(torch.from_numpy(smoothed))
        return torch.stack(smoothed_batch)


def create_gradient_mask(
    height: int,
    width: int,
    x: int,
    y: int,
    mask_width: int,
    mask_height: int,
    feather: int = 10
) -> torch.Tensor:
    """
    Create mask with gradient edges for seamless blending
    
    Args:
        height, width: Frame dimensions
        x, y: Top-left corner of mask
        mask_width, mask_height: Mask dimensions
        feather: Gradient width in pixels
        
    Returns:
        Mask tensor [H, W]
    """
    mask = np.zeros((height, width), dtype=np.float32)
    
    # Create solid center
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(width, x + mask_width), min(height, y + mask_height)
    mask[y1:y2, x1:x2] = 1.0
    
    if feather > 0:
        from scipy.ndimage import distance_transform_edt
        
        # Create distance transform
        distance = distance_transform_edt(mask)
        inverse_distance = distance_transform_edt(1 - mask)
        
        # Apply gradient
        gradient = np.minimum(distance, feather) / feather
        mask = np.clip(gradient, 0, 1)
    
    return torch.from_numpy(mask)


def detect_motion_mask(
    frames: torch.Tensor,
    threshold: float = 0.1
) -> torch.Tensor:
    """
    Create masks based on motion detection between frames
    
    Args:
        frames: Frame batch [B, H, W, C]
        threshold: Motion detection threshold
        
    Returns:
        Motion masks [B, H, W]
    """
    masks = []
    
    for i in range(len(frames) - 1):
        # Calculate frame difference
        diff = torch.abs(frames[i + 1] - frames[i])
        motion = torch.mean(diff, dim=2)  # Average across channels
        
        # Threshold
        mask = (motion > threshold).float()
        masks.append(mask)
    
    # Add last frame (copy of second-to-last)
    masks.append(masks[-1] if masks else torch.zeros(frames.shape[1:3]))
    
    return torch.stack(masks)


def color_range_mask(
    frame: torch.Tensor,
    target_color: Tuple[float, float, float],
    tolerance: float = 0.1
) -> torch.Tensor:
    """
    Create mask based on color similarity
    
    Args:
        frame: Single frame [H, W, C]
        target_color: RGB color in range [0, 1]
        tolerance: Color matching tolerance
        
    Returns:
        Color mask [H, W]
    """
    target = torch.tensor(target_color).reshape(1, 1, 3)
    distance = torch.sqrt(torch.sum((frame - target) ** 2, dim=2))
    mask = (distance < tolerance).float()
    
    return mask


def combine_masks(masks: List[torch.Tensor], method: str = 'union') -> torch.Tensor:
    """
    Combine multiple masks
    
    Args:
        masks: List of mask tensors
        method: 'union' (OR), 'intersection' (AND), or 'average'
        
    Returns:
        Combined mask
    """
    if method == 'union':
        combined = torch.zeros_like(masks[0])
        for mask in masks:
            combined = torch.maximum(combined, mask)
    elif method == 'intersection':
        combined = torch.ones_like(masks[0])
        for mask in masks:
            combined = torch.minimum(combined, mask)
    elif method == 'average':
        combined = torch.mean(torch.stack(masks), dim=0)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return combined


def dilate_mask(mask: torch.Tensor, iterations: int = 1) -> torch.Tensor:
    """
    Expand mask boundaries (dilation)
    
    Args:
        mask: Input mask
        iterations: Number of dilation iterations
        
    Returns:
        Dilated mask
    """
    from scipy.ndimage import binary_dilation
    
    if mask.dim() == 2:
        dilated = binary_dilation(mask.numpy(), iterations=iterations)
        return torch.from_numpy(dilated.astype(np.float32))
    else:
        dilated_batch = []
        for m in mask:
            dilated = binary_dilation(m.numpy(), iterations=iterations)
            dilated_batch.append(torch.from_numpy(dilated.astype(np.float32)))
        return torch.stack(dilated_batch)


def erode_mask(mask: torch.Tensor, iterations: int = 1) -> torch.Tensor:
    """
    Shrink mask boundaries (erosion)
    
    Args:
        mask: Input mask
        iterations: Number of erosion iterations
        
    Returns:
        Eroded mask
    """
    from scipy.ndimage import binary_erosion
    
    if mask.dim() == 2:
        eroded = binary_erosion(mask.numpy(), iterations=iterations)
        return torch.from_numpy(eroded.astype(np.float32))
    else:
        eroded_batch = []
        for m in mask:
            eroded = binary_erosion(m.numpy(), iterations=iterations)
            eroded_batch.append(torch.from_numpy(eroded.astype(np.float32)))
        return torch.stack(eroded_batch)


def get_bounding_box(mask: torch.Tensor) -> Tuple[int, int, int, int]:
    """
    Get bounding box of mask region
    
    Args:
        mask: Mask tensor [H, W]
        
    Returns:
        (x1, y1, x2, y2) bounding box coordinates
    """
    rows = torch.any(mask > 0, dim=1)
    cols = torch.any(mask > 0, dim=0)
    
    if not torch.any(rows) or not torch.any(cols):
        return (0, 0, 0, 0)
    
    y1, y2 = torch.where(rows)[0][[0, -1]]
    x1, x2 = torch.where(cols)[0][[0, -1]]
    
    return (int(x1), int(y1), int(x2), int(y2))


def temporal_smoothing(frames: torch.Tensor, window_size: int = 3) -> torch.Tensor:
    """
    Apply temporal smoothing to reduce flickering
    
    Args:
        frames: Frame batch [B, H, W, C]
        window_size: Smoothing window size (odd number)
        
    Returns:
        Smoothed frames
    """
    if window_size % 2 == 0:
        window_size += 1
    
    half_window = window_size // 2
    smoothed = []
    
    for i in range(len(frames)):
        start_idx = max(0, i - half_window)
        end_idx = min(len(frames), i + half_window + 1)
        window_frames = frames[start_idx:end_idx]
        smoothed.append(torch.mean(window_frames, dim=0))
    
    return torch.stack(smoothed)
