# GIF Inpainter Studio - Examples

This directory contains example GIFs and test cases for the GIF Inpainter Studio.

## Test Cases

### Basic Test
1. Small animated GIF (10-20 frames)
2. Simple object to remove
3. Solid background

### Medium Complexity
1. Medium GIF (50-100 frames)
2. Moving object to remove
3. Textured background

### High Complexity
1. Large GIF (100+ frames)
2. Multiple objects
3. Complex background

## Sample Data

Place your test GIFs here for development and testing:

- `test_simple.gif` - Basic test case
- `test_watermark.gif` - Watermark removal test
- `test_person.gif` - Person removal test
- `test_text.gif` - Text overlay removal test

## Usage

1. Copy GIFs from this folder to `ComfyUI/input/`
2. Load in ComfyUI using Load GIF node
3. Process and compare results

## Contributing Tests

If you have interesting test cases, please contribute:
1. Anonymize if needed
2. Document the challenge
3. Share expected results
4. Submit PR with test case
