# Debugging Installation Issues

## Quick Checklist

### 1. Verify Installation Location
Your folder structure should look like:
```
ComfyUI/
├── custom_nodes/
│   ├── GifInpaint/          ← THIS FOLDER
│   │   ├── __init__.py
│   │   ├── nodes.py
│   │   ├── requirements.txt
│   │   └── ...
│   └── (other custom nodes)
├── models/
├── input/
└── main.py
```

**Check:**
```bash
# You should be in ComfyUI/custom_nodes/GifInpaint
pwd
# Should show: /path/to/ComfyUI/custom_nodes/GifInpaint
```

### 2. Run Debug Script
```bash
cd /path/to/ComfyUI/custom_nodes/GifInpaint
python debug_install.py
```

### 3. Check ComfyUI Console Output
When you start ComfyUI, look for:
- `🎬 GIF Inpainter Studio v1.0.0 loaded successfully!` ✓ Good!
- Any error messages with "GifInpaint" ✗ Problem
- Python import errors ✗ Problem

### 4. Common Issues & Fixes

#### Issue: "Nodes don't appear in menu"
**Fix:**
1. Completely restart ComfyUI (not just refresh browser)
2. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
3. Check console for errors

#### Issue: "Import Error: No module named 'folder_paths'"
**Fix:**
- You're not running from ComfyUI environment
- Make sure ComfyUI is starting the node correctly

#### Issue: "Import Error: No module named 'PIL'"
**Fix:**
```bash
pip install Pillow
# or
pip install -r requirements.txt
```

#### Issue: "Import Error: No module named 'torch'"
**Fix:**
```bash
pip install torch
# or install from PyTorch website for your system
```

#### Issue: "Import Error: No module named 'scipy'"
**Fix:**
```bash
pip install scipy
```

### 5. Manual Verification

#### Test 1: Can __init__.py be imported?
```bash
cd /path/to/ComfyUI/custom_nodes/GifInpaint
python3 -c "import __init__"
```

Should show: `🎬 GIF Inpainter Studio v1.0.0 loaded successfully!`

If you get errors, that's the problem!

#### Test 2: Check nodes.py syntax
```bash
python3 -m py_compile nodes.py
```

No output = good. Errors = syntax problem.

#### Test 3: Verify dependencies
```bash
python3 -c "import torch; import PIL; import numpy; import scipy; print('All deps OK')"
```

### 6. Where are the nodes?

In ComfyUI:
1. Right-click in the workflow canvas
2. Look for category: **"GifInpaint"**
3. Should see nodes like:
   - Load GIF 🎬
   - Save GIF 💾
   - Batch Mask Generator 🎭
   - etc.

If not there:
- Check ComfyUI console for errors
- Try refreshing the page (full refresh)
- Restart ComfyUI completely

### 7. Check ComfyUI is Finding the Folder

Look at ComfyUI console output when it starts. It should list custom nodes being loaded.

If you don't see GifInpaint mentioned at all:
- Folder might be in wrong location
- Folder name might be wrong (should be `GifInpaint`)
- __init__.py might have errors

### 8. Nuclear Option: Clean Install

```bash
# Remove the folder
rm -rf /path/to/ComfyUI/custom_nodes/GifInpaint

# Re-clone
cd /path/to/ComfyUI/custom_nodes/
git clone https://github.com/SaustinLabs/GifInpaint.git

# Install dependencies
cd GifInpaint
pip install -r requirements.txt

# Restart ComfyUI completely (kill the process and start again)
```

### 9. Check Python Version

```bash
python3 --version
```

Must be 3.8 or higher!

## Still Not Working?

Run the debug script and share the output:

```bash
cd /path/to/ComfyUI/custom_nodes/GifInpaint
python debug_install.py > debug_output.txt 2>&1
```

Then check `debug_output.txt` for clues.

## Expected Working State

When working correctly, you should see:
1. On ComfyUI startup: `🎬 GIF Inpainter Studio v1.0.0 loaded successfully!`
2. In node menu: Category "GifInpaint" with 13 nodes
3. No error messages in console

## Quick Test

Try adding this to a text file in ComfyUI folder and run:

```python
# test_nodes.py
import sys
sys.path.append('./custom_nodes/GifInpaint')

try:
    from nodes import NODE_CLASS_MAPPINGS
    print(f"✓ Found {len(NODE_CLASS_MAPPINGS)} nodes:")
    for name in NODE_CLASS_MAPPINGS.keys():
        print(f"  - {name}")
except Exception as e:
    print(f"✗ Error: {e}")
```

```bash
cd /path/to/ComfyUI
python test_nodes.py
```
