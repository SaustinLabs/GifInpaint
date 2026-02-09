#!/usr/bin/env python3
"""
Debug script to diagnose installation issues
Run this from the GifInpaint directory
"""

import sys
import os
from pathlib import Path

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def check_location():
    """Check if we're in the right location"""
    print_section("1. Checking Installation Location")
    
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if we're in GifInpaint folder
    if current_dir.name != "GifInpaint":
        print("⚠ WARNING: Current folder is not named 'GifInpaint'")
        print(f"  Current: {current_dir.name}")
        print("  Expected: GifInpaint")
    else:
        print("✓ Folder name is correct: GifInpaint")
    
    # Check if parent is custom_nodes
    if current_dir.parent.name != "custom_nodes":
        print("⚠ WARNING: Parent folder is not 'custom_nodes'")
        print(f"  Current: {current_dir.parent.name}")
        print("  Expected: custom_nodes")
        print("\n  → You should move this folder to ComfyUI/custom_nodes/")
    else:
        print("✓ Located in custom_nodes folder")
        
        # Try to find ComfyUI root
        comfyui_root = current_dir.parent.parent
        main_py = comfyui_root / "main.py"
        if main_py.exists():
            print(f"✓ Found ComfyUI root: {comfyui_root}")
        else:
            print(f"⚠ Could not find main.py in {comfyui_root}")

def check_files():
    """Check if all required files exist"""
    print_section("2. Checking Required Files")
    
    required_files = [
        "__init__.py",
        "nodes.py",
        "requirements.txt",
        "README.md",
    ]
    
    all_good = True
    for filename in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} ({size} bytes)")
        else:
            print(f"✗ {filename} MISSING")
            all_good = False
    
    return all_good

def check_python():
    """Check Python version"""
    print_section("3. Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
        return True
    else:
        print("✗ Python version too old. Need 3.8+")
        return False

def check_dependencies():
    """Check if dependencies are installed"""
    print_section("4. Checking Dependencies")
    
    deps = {
        'torch': 'PyTorch',
        'numpy': 'NumPy', 
        'PIL': 'Pillow',
        'scipy': 'SciPy',
    }
    
    missing = []
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError as e:
            print(f"✗ {name} NOT installed")
            print(f"  Error: {e}")
            missing.append(name)
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("\nTo install:")
        print("  pip install -r requirements.txt")
        return False
    return True

def check_imports():
    """Try importing the nodes"""
    print_section("5. Testing Node Imports")
    
    try:
        print("Attempting to import nodes...")
        from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        print(f"✓ Successfully imported nodes module")
        print(f"✓ Found {len(NODE_CLASS_MAPPINGS)} core nodes:")
        for name, display_name in NODE_DISPLAY_NAME_MAPPINGS.items():
            print(f"  - {display_name}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import nodes")
        print(f"  Error: {e}")
        print("\n  This is usually because:")
        print("  1. Missing dependencies (see section 4)")
        print("  2. Syntax error in nodes.py")
        print("  3. Missing required files")
        return False
    except Exception as e:
        print(f"✗ Error importing nodes: {e}")
        return False

def check_advanced_nodes():
    """Try importing advanced nodes"""
    print_section("6. Testing Advanced Nodes")
    
    try:
        from advanced_nodes import ADVANCED_NODE_CLASS_MAPPINGS
        print(f"✓ Found {len(ADVANCED_NODE_CLASS_MAPPINGS)} advanced nodes:")
        for name in ADVANCED_NODE_CLASS_MAPPINGS.keys():
            print(f"  - {name}")
        return True
    except ImportError as e:
        print(f"⚠ Advanced nodes not available: {e}")
        return False
    except Exception as e:
        print(f"✗ Error with advanced nodes: {e}")
        return False

def check_comfyui_compatibility():
    """Check if ComfyUI modules can be imported"""
    print_section("7. Testing ComfyUI Compatibility")
    
    # Try to import ComfyUI's folder_paths
    try:
        # Add parent directories to path to simulate ComfyUI environment
        parent = Path.cwd().parent.parent
        if parent not in sys.path:
            sys.path.insert(0, str(parent))
        
        import folder_paths
        print("✓ Can import folder_paths (ComfyUI module)")
        return True
    except ImportError:
        print("⚠ Cannot import folder_paths")
        print("  This is expected if not running from ComfyUI")
        print("  The nodes will work once ComfyUI loads them")
        return None  # Not a failure, just informational

def test_init():
    """Test the __init__.py file"""
    print_section("8. Testing Package Initialization")
    
    try:
        # Import without triggering ComfyUI-specific code
        with open('__init__.py', 'r') as f:
            content = f.read()
            print("✓ __init__.py is readable")
            
            # Check for key elements
            if 'NODE_CLASS_MAPPINGS' in content:
                print("✓ Exports NODE_CLASS_MAPPINGS")
            if 'NODE_DISPLAY_NAME_MAPPINGS' in content:
                print("✓ Exports NODE_DISPLAY_NAME_MAPPINGS")
            if '__version__' in content:
                print("✓ Has version info")
                
        return True
    except Exception as e:
        print(f"✗ Error reading __init__.py: {e}")
        return False

def main():
    print("\n" + "🔍 GIF Inpainter Studio - Installation Diagnostic Tool" + "\n")
    print("This script checks your installation for common issues.\n")
    
    results = {
        'location': check_location(),
        'files': check_files(),
        'python': check_python(),
        'dependencies': check_dependencies(),
        'imports': check_imports(),
        'advanced': check_advanced_nodes(),
        'comfyui': check_comfyui_compatibility(),
        'init': test_init(),
    }
    
    # Final summary
    print_section("DIAGNOSTIC SUMMARY")
    
    critical_passed = results['files'] and results['python'] and results['dependencies'] and results['imports']
    
    if critical_passed:
        print("✅ INSTALLATION LOOKS GOOD!")
        print("\nIf nodes still don't appear in ComfyUI:")
        print("1. Make sure this folder is in ComfyUI/custom_nodes/")
        print("2. Completely restart ComfyUI (kill and restart process)")
        print("3. Clear browser cache (Ctrl+Shift+R)")
        print("4. Check ComfyUI console for error messages")
        print("\nYou should see: '🎬 GIF Inpainter Studio v1.0.0 loaded successfully!'")
    else:
        print("⚠ ISSUES DETECTED")
        print("\nProblems found:")
        if not results['files']:
            print("  - Missing required files")
        if not results['python']:
            print("  - Python version too old")
        if not results['dependencies']:
            print("  - Missing dependencies - run: pip install -r requirements.txt")
        if not results['imports']:
            print("  - Cannot import nodes - check errors above")
        
        print("\nFix these issues and run this script again.")
    
    print("\n" + "="*60)
    print("For more help, see: DEBUG.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
