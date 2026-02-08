# Contributing to GIF Inpainter Studio

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include ComfyUI version
- Provide error messages and logs
- Share example GIF if possible (anonymized)
- Describe expected vs actual behavior

### Suggesting Features
- Open a GitHub Issue with [Feature Request] tag
- Describe the use case
- Explain why it would be useful
- Include mockups or examples if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test with various GIF sizes
   - Verify memory usage
   - Check compatibility with existing nodes

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: New mask generation method"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Use type hints where applicable

### Development Setup

```bash
# Clone repository
git clone https://github.com/SaustinLabs/GifInpaint.git
cd GifInpaint

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_utils.py
```

### Node Development Guidelines

When creating new nodes:

1. **Follow ComfyUI conventions**
   - Use INPUT_TYPES classmethod
   - Define RETURN_TYPES and RETURN_NAMES
   - Set appropriate CATEGORY
   - Implement the FUNCTION method

2. **Handle edge cases**
   - Check tensor dimensions
   - Validate input ranges
   - Provide sensible defaults
   - Add error handling

3. **Document thoroughly**
   - Add docstrings
   - Explain parameters
   - Provide usage examples

4. **Register properly**
   - Add to NODE_CLASS_MAPPINGS
   - Add to NODE_DISPLAY_NAME_MAPPINGS
   - Use descriptive display name with emoji

### Areas for Contribution

We especially welcome contributions in these areas:

- **Performance**: Optimization for large GIFs
- **Algorithms**: Better interpolation and smoothing
- **Masks**: New mask generation methods
- **Tracking**: Object tracking across frames
- **UI**: Better previews and controls
- **Documentation**: Tutorials and examples
- **Testing**: More test cases and benchmarks

### Questions?

Feel free to:
- Open a GitHub Discussion
- Comment on existing issues
- Reach out to maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make GIF Inpainter Studio better!** 🙌
