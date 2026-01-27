# Contributing to BlackRoad OS Repository Index

Thank you for your interest in contributing to the BlackRoad OS Repository Index! 🖤

## Getting Started

1. **Fork the Repository**
   ```bash
   # Fork via GitHub UI, then clone your fork
   git clone https://github.com/YOUR_USERNAME/index.py.git
   cd index.py
   ```

2. **Set Up Development Environment**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Make Your Changes**
   ```bash
   # Create a feature branch
   git checkout -b feature/your-feature-name
   
   # Make your changes
   # ...
   
   # Run tests
   python tests/test_basic.py
   
   # Run linter
   flake8 .
   
   # Format code
   black .
   ```

4. **Submit a Pull Request**
   ```bash
   # Commit your changes
   git add .
   git commit -m "Description of your changes"
   
   # Push to your fork
   git push origin feature/your-feature-name
   
   # Open a PR on GitHub
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use `black` for code formatting
- Use type hints where appropriate
- Write descriptive docstrings

### Testing

- Add tests for new features
- Ensure all tests pass before submitting
- Run `python tests/test_basic.py` to verify

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep first line under 50 characters
- Add detailed description if needed

### Documentation

- Update README.md if adding new features
- Document new command-line options
- Keep examples up to date

## Types of Contributions

### Bug Fixes

If you find a bug:
1. Check if it's already reported in Issues
2. Create a new issue if not
3. Submit a PR with the fix

### New Features

Before adding a new feature:
1. Open an issue to discuss it
2. Get approval from maintainers
3. Implement the feature
4. Add tests and documentation

### Documentation

Documentation improvements are always welcome:
- Fix typos
- Improve clarity
- Add examples
- Update outdated information

### Repository Data

To update the repository catalog:
1. Update `repositories-static.json` if adding manual entries
2. Or run `python index.py --update` with GitHub token
3. Verify the output
4. Submit PR with updated data

## Setting Up GitHub Token

For fetching live repository data:

1. **Create a Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click "Generate new token"
   - Select `public_repo` scope
   - Generate and copy the token

2. **Use the Token**
   ```bash
   # Set as environment variable
   export GITHUB_TOKEN="your_token_here"
   
   # Or add to .env file (don't commit!)
   echo "GITHUB_TOKEN=your_token_here" > .env
   
   # Run with token
   python index.py --update
   ```

## Code Review Process

1. All PRs require review before merging
2. Address review feedback promptly
3. Keep PRs focused and small
4. Ensure CI checks pass

## Community

- Be respectful and inclusive
- Follow the [Code of Conduct](https://github.com/BlackRoad-OS/.github/blob/main/CODE_OF_CONDUCT.md)
- Help others in issues and discussions
- Share your knowledge

## Questions?

- Open an issue for questions
- Visit [developers.blackroad.io](https://developers.blackroad.io)
- Check [docs.blackroad.io](https://docs.blackroad.io)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

🖤 Thank you for contributing to BlackRoad OS!
