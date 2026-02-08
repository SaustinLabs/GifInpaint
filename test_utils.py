"""
Test utilities for GIF Inpainter Studio
"""

import torch
import numpy as np
from PIL import Image
import os


def create_test_gif(
    filename: str = "test.gif",
    num_frames: int = 10,
    width: int = 256,
    height: int = 256,
    duration: int = 100
):
    """
    Create a simple test GIF with moving circle
    
    Args:
        filename: Output filename
        num_frames: Number of frames
        width, height: Dimensions
        duration: Frame duration in ms
    """
    frames = []
    
    for i in range(num_frames):
        # Create blank frame
        img = Image.new('RGB', (width, height), color=(200, 200, 255))
        pixels = img.load()
        
        # Draw moving circle
        center_x = int(width * (i / num_frames))
        center_y = height // 2
        radius = 30
        
        for y in range(height):
            for x in range(width):
                dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if dist < radius:
                    # Red circle
                    pixels[x, y] = (255, 100, 100)
        
        frames.append(img)
    
    # Save as GIF
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    
    print(f"Created test GIF: {filename}")
    return filename


def create_test_watermark_gif(
    filename: str = "test_watermark.gif",
    num_frames: int = 10,
    width: int = 256,
    height: int = 256,
    duration: int = 100
):
    """
    Create test GIF with watermark overlay
    """
    from PIL import ImageDraw, ImageFont
    
    frames = []
    
    for i in range(num_frames):
        # Gradient background
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            for x in range(width):
                color_value = int(150 + 50 * np.sin(2 * np.pi * (x + i * 10) / width))
                pixels[x, y] = (color_value, color_value, 255)
        
        # Add watermark text
        draw = ImageDraw.Draw(img)
        text = "WATERMARK"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = (width - text_width - 10, height - text_height - 10)
        draw.text(position, text, fill=(255, 255, 255))
        
        frames.append(img)
    
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    
    print(f"Created watermark test GIF: {filename}")
    return filename


def validate_node_outputs(node_class, inputs):
    """
    Test a node with given inputs
    
    Args:
        node_class: Node class to test
        inputs: Dictionary of input parameters
        
    Returns:
        Node outputs
    """
    node = node_class()
    
    # Get the function name
    func_name = node.FUNCTION
    func = getattr(node, func_name)
    
    # Call the function
    outputs = func(**inputs)
    
    print(f"✓ {node_class.__name__} executed successfully")
    print(f"  Outputs: {[type(o).__name__ if isinstance(o, torch.Tensor) else type(o) for o in outputs]}")
    
    return outputs


def test_basic_workflow():
    """
    Test basic GIF loading and saving workflow
    """
    print("\n=== Testing Basic Workflow ===\n")
    
    # Create test GIF
    test_file = create_test_gif("test_basic.gif", num_frames=5)
    
    # Test LoadGIF (would need actual ComfyUI environment)
    print("✓ Test GIF created successfully")
    print(f"  File: {test_file}")
    print(f"  Size: {os.path.getsize(test_file)} bytes")
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
        print("✓ Cleanup complete")


def benchmark_processing(num_frames: int, width: int, height: int):
    """
    Benchmark frame processing speed
    """
    import time
    
    print(f"\n=== Benchmarking {num_frames} frames at {width}x{height} ===\n")
    
    # Create dummy frames
    frames = torch.rand(num_frames, height, width, 3)
    
    # Test operations
    operations = [
        ("Frame creation", lambda: torch.rand(num_frames, height, width, 3)),
        ("Normalization", lambda: frames * 255),
        ("Mean calculation", lambda: torch.mean(frames, dim=0)),
        ("Frame stacking", lambda: torch.stack([frames[i] for i in range(len(frames))])),
    ]
    
    for name, operation in operations:
        start = time.time()
        result = operation()
        elapsed = time.time() - start
        print(f"  {name}: {elapsed*1000:.2f}ms")
    
    print("\n✓ Benchmark complete")


if __name__ == "__main__":
    # Run tests
    print("GIF Inpainter Studio - Test Suite")
    print("=" * 50)
    
    # Create test GIFs
    create_test_gif("examples/test_simple.gif", num_frames=10)
    create_test_watermark_gif("examples/test_watermark.gif", num_frames=10)
    
    # Run benchmark
    benchmark_processing(num_frames=20, width=256, height=256)
    
    print("\n" + "=" * 50)
    print("Testing complete!")
