#!/usr/bin/env python3
"""
GIF Inpainter Studio - Setup and Verification Script

This script helps set up and verify the GIF Inpainter Studio installation.
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    
    required = {
        'torch': 'PyTorch',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
    }
    
    missing = []
    
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} not found")
            missing.append(name)
    
    return missing


def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("✗ requirements.txt not found")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def check_comfyui_path():
    """Check if running inside ComfyUI custom_nodes"""
    print("\nChecking ComfyUI installation...")
    
    current_path = Path(__file__).parent
    
    # Check if we're in custom_nodes directory
    if current_path.parent.name == "custom_nodes":
        print(f"✓ Located in ComfyUI custom_nodes")
        comfyui_path = current_path.parent.parent
        print(f"  ComfyUI path: {comfyui_path}")
        return True, comfyui_path
    else:
        print("⚠ Not in ComfyUI custom_nodes directory")
        print("  Please move this folder to ComfyUI/custom_nodes/")
        return False, None


def create_example_gifs():
    """Create example test GIFs"""
    print("\nCreating example test GIFs...")
    
    try:
        from test_utils import create_test_gif, create_test_watermark_gif
        
        examples_dir = Path(__file__).parent / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        create_test_gif(str(examples_dir / "test_simple.gif"), num_frames=10)
        create_test_watermark_gif(str(examples_dir / "test_watermark.gif"), num_frames=10)
        
        print("✓ Example GIFs created in examples/ folder")
        return True
    except Exception as e:
        print(f"✗ Failed to create examples: {e}")
        return False


def verify_nodes():
    """Verify nodes can be imported"""
    print("\nVerifying nodes...")
    
    try:
        from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        print(f"✓ Loaded {len(NODE_CLASS_MAPPINGS)} base nodes")
        
        try:
            from advanced_nodes import ADVANCED_NODE_CLASS_MAPPINGS
            print(f"✓ Loaded {len(ADVANCED_NODE_CLASS_MAPPINGS)} advanced nodes")
        except ImportError:
            print("⚠ Advanced nodes not available")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load nodes: {e}")
        return False


def print_next_steps(in_comfyui):
    """Print next steps for user"""
    print_header("Next Steps")
    
    if in_comfyui:
        print("1. Restart ComfyUI")
        print("2. Look for 'GifInpaint' category in node menu")
        print("3. Add 'Load GIF' node to start")
        print("4. Place your GIFs in ComfyUI/input/ folder")
        print("5. Check QUICKSTART.md for detailed tutorial")
    else:
        print("1. Move this folder to ComfyUI/custom_nodes/")
        print("2. Run this script again from that location")
        print("3. Restart ComfyUI")
    
    print("\n📚 Documentation:")
    print("   - README.md - Full documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - workflows/ - Example workflows")
    print("   - examples/ - Test GIFs")


def main():
    """Main setup and verification"""
    print_header("GIF Inpainter Studio - Setup & Verification")
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Python version too old. Please upgrade to Python 3.8+")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        response = input("\nInstall missing dependencies? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                print("\n❌ Installation failed")
                sys.exit(1)
        else:
            print("\n⚠ Skipping installation. Some features may not work.")
    
    # Check ComfyUI path
    in_comfyui, comfyui_path = check_comfyui_path()
    
    # Verify nodes
    verify_nodes()
    
    # Create examples
    create_example_gifs()
    
    # Print final status
    print_header("Setup Complete")
    
    if in_comfyui and not missing:
        print("✅ Everything is ready!")
    elif in_comfyui:
        print("⚠ Setup complete with warnings")
    else:
        print("⚠ Please move to ComfyUI custom_nodes folder")
    
    # Print next steps
    print_next_steps(in_comfyui)
    
    print("\n" + "=" * 60)
    print("For support, visit: https://github.com/SaustinLabs/GifInpaint")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
