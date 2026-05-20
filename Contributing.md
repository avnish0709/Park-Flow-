# Contributing to MallPark 360

Thank you for your interest in contributing! Please read these guidelines before making contributions.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Use the bug report template
3. Provide:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Your environment (Python version, OS, etc.)

### Suggesting Features

1. Check if the feature is already requested
2. Use the feature request template
3. Explain the use case and benefits
4. Provide examples if possible

### Submitting Code

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Follow code style**:
   - Backend: Follow PEP 8
   - Frontend: Use consistent naming and formatting
4. **Test your changes** thoroughly
5. **Commit with clear messages**: 
   ```
   git commit -m "Add: Brief description of changes"
   ```
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Explanation of changes

## Pull Request Process

1. Ensure code follows project conventions
2. Update documentation as needed
3. Add tests for new features
4. Ensure all tests pass
5. Link any related issues
6. Wait for review and address feedback

## Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
(python -m uvicorn app.main:app --reload)
(-uvicorn app.main:app --reload)

# Frontend
cd frontend
npm install
npm run dev
```

## Commit Message Guidelines

- Use imperative mood ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues when applicable: "Fixes #123"
- Examples:
  - `Add: Parking slot validation`
  - `Fix: CORS headers issue`
  - `Docs: Update API documentation`

## Questions?

Feel free to open an issue with the `question` label.

Thank you for contributing!
