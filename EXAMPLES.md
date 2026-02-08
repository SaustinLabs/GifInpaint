# GIF Inpainter Studio - Usage Examples

## Example 1: Basic Object Removal

### Scenario
Remove a person from a GIF background.

### Workflow
```
Load GIF → Batch Mask Generator → Preview → VAE Encode → Inpaint → Save GIF
```

### Settings
- **Mask Type**: center_box
- **Position**: Where person is located
- **Feather**: 10 (smooth edges)
- **Denoise**: 0.75
- **Steps**: 25
- **Prompt**: "empty background, clean scene"

### Expected Result
Person removed with background filled in naturally.

---

## Example 2: Watermark Removal

### Scenario
Remove static watermark from corner of GIF.

### Workflow
```
Load GIF → Batch Mask Generator (small box) → Inpaint → Save GIF
```

### Settings
- **Mask Type**: center_box
- **X, Y**: Watermark position (e.g., bottom-right)
- **Width, Height**: Just cover watermark
- **Feather**: 5
- **Denoise**: 0.8
- **Prompt**: "clean surface, seamless"

### Tips
- Keep mask small for faster processing
- Higher denoise for complete removal
- Low feather since watermarks have sharp edges

---

## Example 3: Text Overlay Removal

### Scenario
Remove text overlays from educational GIF.

### Workflow
```
Load GIF → Batch Mask Generator → Frame Selector → Inpaint → Interpolate → Save
```

### Settings
- **Mask**: Rectangle covering text
- **Feather**: 8
- **Frame Selection**: Only frames with text
- **Interpolation**: 2x for smoothness
- **Prompt**: "clean background, no text"

---

## Example 4: Green Screen Removal

### Scenario
Remove green screen background.

### Workflow
```
Load GIF → Color Range Mask Generator → Inpaint → Save GIF
```

### Settings (Color Range Mask)
- **Red**: 0.0
- **Green**: 1.0
- **Blue**: 0.0
- **Tolerance**: 0.2
- **Feather**: 10

### Settings (Inpainting)
- **Prompt**: "natural background, outdoor scene"
- **Denoise**: 0.9
- **Steps**: 30

---

## Example 5: Multi-Object Removal

### Scenario
Remove multiple unwanted elements from GIF.

### Workflow
```
Load GIF → Mask Generator 1 → Mask Generator 2 → Mask Combiner → Inpaint → Save
```

### Settings
- **Two separate masks** for different objects
- **Mask Combiner**: Union operation
- **Feather both**: 8-10
- **Higher steps**: 35-40 for quality

---

## Example 6: Moving Object Removal

### Scenario
Remove object that moves across frames.

### Workflow
```
Load GIF → Motion Mask Generator → Advanced Mask Editor → Inpaint → Temporal Smoother → Save
```

### Settings (Motion Mask)
- **Threshold**: 0.15
- **Blur**: 10

### Settings (Advanced Editor)
- **Operation**: Dilate
- **Strength**: 5

### Settings (Temporal Smoother)
- **Window Size**: 5
- **Strength**: 0.7

---

## Example 7: High Quality Processing

### Scenario
Maximum quality inpainting for professional use.

### Workflow
```
Load GIF → Frame Selector (batch) → Resize Up → Mask → Inpaint (high steps) → 
Temporal Smooth → Resize Down → Interpolate → Save
```

### Settings
- **Upscale**: 1.5x before processing
- **Steps**: 50
- **CFG**: 7
- **Denoise**: 0.8
- **Multiple passes** if needed
- **Interpolate**: 2x final output

### Note
Much slower but professional results.

---

## Example 8: Quick Preview Workflow

### Scenario
Test settings before full processing.

### Workflow
```
Load GIF → Frame Selector (first 10) → Mask → Preview → Inpaint → Review
```

### Settings
- **Process only** 10 frames
- **Check different** frame indices (0, 5, 9)
- **Adjust mask** based on preview
- **Then process full** GIF

---

## Example 9: Batch Processing Multiple GIFs

### Scenario
Process many GIFs with same settings.

### Workflow
Create reusable workflow:
```
Load GIF (change file) → [Standard Processing Chain] → Save GIF (auto-number)
```

### Settings
- **Save filename prefix** with description
- **Auto-numbering** enabled
- **Same mask settings** for consistency
- **Queue multiple** in sequence

---

## Example 10: Creative Background Replacement

### Scenario
Replace entire background with AI-generated scene.

### Workflow
```
Load GIF → Motion Mask (detect subject) → Invert Mask → Inpaint → Save
```

### Settings
- **Motion Mask**: Detects moving subject
- **Mask Editor**: Invert operation
- **Prompt**: "beautiful sunset beach, golden hour"
- **High denoise**: 0.95
- **Creative prompt** for interesting backgrounds

---

## Performance Optimization Examples

### Large GIF (200+ frames)
```
Load → Frame Selector (0-50) → Process → Save as Part 1
Load → Frame Selector (51-100) → Process → Save as Part 2
...
Combine parts externally
```

### High Resolution GIF
```
Load → Batch Resize (512x512) → Process → Resize Up → Save
```

### Memory Constrained
```
Load → Frame Selector (step=2) → Process → Interpolate → Save
(Process every other frame, interpolate missing ones)
```

---

## Common Setting Presets

### Preset: Subtle Removal
- Denoise: 0.6
- Steps: 20
- CFG: 6
- Feather: 15

### Preset: Complete Removal
- Denoise: 0.85
- Steps: 30
- CFG: 8
- Feather: 10

### Preset: Fast Preview
- Denoise: 0.7
- Steps: 15
- CFG: 7
- Feather: 8

### Preset: Maximum Quality
- Denoise: 0.8
- Steps: 50
- CFG: 7.5
- Feather: 12

---

## Troubleshooting Through Examples

### Problem: Flickering Output
**Solution Workflow:**
```
[Normal Process] → Temporal Smoother (window=5, strength=0.8) → Save
```

### Problem: Visible Mask Edges
**Solution Workflow:**
```
Mask Generator (feather=20) → Advanced Editor (smooth, strength=10) → Use
```

### Problem: Artifacts in Output
**Solution Workflow:**
```
Increase mask feather + Lower denoise to 0.65 + Increase CFG to 9
```

### Problem: Background Doesn't Match
**Solution Workflow:**
```
Increase mask size + Better prompt + Multiple inpainting passes
```

---

## Tips for Each Use Case

### Commercial/Professional
- Always test on 10-frame subset first
- Use highest quality settings
- Apply temporal smoothing
- Check every frame manually
- Consider multiple passes

### Social Media
- Balance quality and speed
- 256x256 or 512x512 resolution
- 30 frames or less ideal
- Optimize GIF file size
- Fast turnaround more important

### Personal Projects
- Experiment with creative prompts
- Try different mask types
- Use interpolation for smooth motion
- Don't worry about perfect results

### Batch Production
- Create template workflow
- Document settings
- Use consistent naming
- Process overnight if needed
- Quality check samples

---

**Remember**: Every GIF is different. Start with these examples and adjust based on your specific content!
