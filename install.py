"""
Installation script for GIF Inpainter Studio
"""

import subprocess
import sys
import os


def install():
    """Install required dependencies"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    print("Installing GIF Inpainter Studio dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_path
        ])
        print("✓ Installation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Installation failed: {e}")
        return False


if __name__ == "__main__":
    install()
