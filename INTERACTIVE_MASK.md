# Using ComfyUI's Built-in Mask Editor

## YES! You can right-click and paint directly in ComfyUI!

Here's the complete workflow:

## Method 1: Using LoadImage with Mask Capability (EASIEST)

### Step-by-Step:

1. **Extract first frame from GIF:**
   ```
   LoadGIF → GIFFrameSelector (0-1) → SaveImage
   ```
   This saves frame to `ComfyUI/output/`

2. **Load that frame with mask support:**
   ```
   Add Node → image → Load Image
   - Select your saved frame
   - Upload: "choose file to upload" (select the frame you just saved)
   ```

3. **Right-click on the image preview:**
   - Right-click on the preview thumbnail
   - Select **"Open in MaskEditor"** or **"Edit Mask"**
   - Paint white over areas you want to REMOVE
   - Click "Save" or close the editor

4. **Use ImageToMask node (NEW!):**
   ```
   LoadImage (with painted mask) → ImageToMask → BatchMaskGenerator (manual)
   ```

5. **Apply to all GIF frames:**
   ```
   BatchMaskGenerator (manual mode) → receives your painted mask
   → applies to all frames in your GIF
   ```

---

## Method 2: Using GIF Mask Editor Node (NEW!)

We added a new node: **GIFMaskEditor**

### Workflow:

```
LoadGIF → GIFFrameSelector (0-1) → GIFMaskEditor
                                           ↓
                                   [Right-click preview]
                                   [Open in MaskEditor]
                                   [Paint mask]
                                           ↓
                                    mask output
                                           ↓
                            BatchMaskGenerator (manual)
                                           ↓
                                    [All frames masked]
```

### How it works:

1. **Add GIF Mask Editor node**
   - Right-click → Add Node → GifInpaint → GIF Mask Editor

2. **Connect your GIF frame** (just first frame)
   - LoadGIF → GIF Frame Selector (0-1) → GIF Mask Editor

3. **Right-click on the preview image**
   - Click "Generate" once to see the preview
   - Right-click on the image
   - Select "Open in MaskEditor"

4. **Paint your mask**
   - White = areas to REMOVE
   - Black = areas to KEEP
   - Use brush size controls
   - Click Save when done

5. **Mask output connects to BatchMaskGenerator**
   - The mask automatically goes to BatchMaskGenerator
   - Set it to "manual" mode
   - It broadcasts your mask to all frames!

---

## Method 3: Load + ComfyUI's Native Mask Editor

This uses ComfyUI's built-in **LoadImage** node which has mask support:

### Complete Workflow:

```
1. LoadGIF → GIFFrameSelector (0-1) → SaveImage
   └─ Save first frame as PNG

2. Load Image node (ComfyUI built-in)
   └─ Load that PNG
   └─ Has built-in mask upload support

3. In ComfyUI UI:
   └─ Right-click on LoadImage preview
   └─ "Open in MaskEditor"
   └─ Paint mask directly
   └─ Save

4. LoadImage → mask output → ImageToMask (if needed)
   └─ Connect to BatchMaskGenerator (manual mode)
   └─ Apply to all GIF frames
```

---

## New Nodes Added

### 🎨 GIF Mask Editor
**Purpose:** Interactive mask editing for GIF frames

**Usage:**
- Connect a single GIF frame
- Right-click preview → Open in MaskEditor
- Paint directly in ComfyUI
- Outputs both image and mask

**Workflow:**
```
GIFFrameSelector → GIFMaskEditor → mask → BatchMaskGenerator
```

---

### 🔄 Image to Mask Converter
**Purpose:** Convert any image to a mask

**Usage:**
- Takes any IMAGE input
- Selects channel (red/green/blue/alpha/luminance)
- Outputs MASK

**Why:** ComfyUI's LoadImage can have a mask, but it needs conversion to work with our nodes.

**Workflow:**
```
LoadImage (with painted mask) → ImageToMask → BatchMaskGenerator
```

---

## Complete Paint-in-ComfyUI Workflow

### Option A: Direct Painting (Recommended)

```json
Workflow steps:
1. LoadGIF → your_gif.gif
2. GIF Frame Selector → frame 0 to 1 (just first frame)
3. GIF Mask Editor → connected to frame
   ├─ Generates preview
   ├─ Right-click → Open in MaskEditor
   ├─ Paint mask (white = remove)
   └─ Outputs mask
4. Batch Mask Generator (manual mode)
   ├─ frames: from LoadGIF (all frames)
   ├─ mask: from GIF Mask Editor
   └─ Outputs batch mask for all frames
5. Continue with standard inpainting pipeline
```

### Option B: Using LoadImage Node

```json
Workflow steps:
1. LoadGIF → GIFFrameSelector → SaveImage (save first frame)
2. LoadImage → load saved frame
   ├─ Right-click preview → Open in MaskEditor
   └─ Paint and save
3. LoadImage → second output (mask) → ImageToMask
4. ImageToMask → BatchMaskGenerator (manual)
5. LoadGIF (original, all frames) → BatchMaskGenerator
6. Continue to inpainting
```

---

## How to Right-Click and Paint

### In ComfyUI UI:

1. **Run workflow once** (Queue Prompt)
   - This generates the preview image

2. **Find the image preview**
   - Look for the small thumbnail in the node
   - It shows your GIF frame

3. **Right-click on the preview**
   - Context menu appears
   - Look for "Open in MaskEditor" or similar option

4. **Paint in the mask editor**
   - **White brush** = mark for REMOVAL (inpainting)
   - **Black brush** = mark to KEEP (preserved)
   - Adjust brush size with controls
   - Use eraser if needed

5. **Save and close**
   - Click "Save" or just close
   - Mask is now connected to your workflow

6. **Re-run workflow**
   - The mask you painted is now used
   - Applies to all GIF frames via BatchMaskGenerator

---

## Important Notes

### About ComfyUI's Mask Editor:

- ✅ **Built into ComfyUI** - no extensions needed
- ✅ **Works with image previews** - right-click any image
- ✅ **Painting is intuitive** - white = mask, black = keep
- ⚠️ **Must run once first** - need preview to appear before editing
- ⚠️ **Some nodes support it better** - LoadImage has best support

### Mask Format:

- **White (255)** = Will be inpainted (removed)
- **Black (0)** = Will be preserved (kept)
- **Gray** = Partial masking (50% gray = 50% effect)

### Tips:

1. **Use GIF Mask Editor** for direct integration
2. **Use LoadImage method** if you prefer ComfyUI's native tools
3. **Soft brush edges** = better blending
4. **Feather your mask** for seamless results
5. **Preview before full run** - check mask coverage

---

## Comparison

| Method | Complexity | Integration | Best For |
|--------|-----------|-------------|----------|
| **GIF Mask Editor** | Simple | Direct | Quick painting in ComfyUI |
| **LoadImage + Mask** | Medium | Native ComfyUI | Using existing workflows |
| **Load Painted Mask** | Simple | External tool | Photoshop/GIMP users |
| **SimpleMaskDrawer** | Easy | Coordinates | Testing/automation |

---

## Troubleshooting

### "I don't see Open in MaskEditor option"

- Make sure you ran the workflow once (Queue Prompt)
- The preview needs to generate first
- Try the LoadImage node - it has better mask support

### "My mask isn't being applied"

- Check BatchMaskGenerator is set to "manual" mode
- Verify mask connection (wire from mask output to mask input)
- Re-run workflow after painting

### "Mask is inverted (removing wrong parts)"

- Use ImageToMask node with `invert: yes`
- Or repaint with opposite colors
- Check BatchMaskGenerator's mask input

---

## Summary

**YES, you can right-click → paint → process!**

**Easiest workflow:**
1. LoadGIF → GIFFrameSelector → **GIFMaskEditor**
2. Run once → right-click preview → **Open in MaskEditor**
3. Paint white over areas to remove → Save
4. GIFMaskEditor → mask → **BatchMaskGenerator (manual)**
5. Continue to inpainting → SaveGIF

**New nodes enable this:**
- `GIFMaskEditor` - Interactive editing support
- `ImageToMask` - Convert images to masks

**Restart ComfyUI** to load these new nodes!
