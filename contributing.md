# Contributing to Face Swapper App

Thank you for your interest in contributing to the Face Swapper App! This document provides guidelines and instructions for contributing to this project.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- Git
- A GitHub/GitLab account

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/face-swapper-app.git
   cd face-swapper-app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

6. **Start Development Server**
   ```bash
   streamlit run app.py
   ```

## 📝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Bug Report Template:**
- Use a clear, descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples and expected vs actual behavior
- Include your environment details (OS, Python version, Docker version)
- Add screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please provide:
- A clear description of the feature
- The problem it solves or value it adds
- Possible implementation approaches
- Any alternatives you've considered

### Pull Requests

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run all tests
   pytest tests/ -v
   
   # Run linting
   flake8 src/ tests/
   black --check src/ tests/
   isort --check-only src/ tests/
   
   # Run with coverage
   pytest --cov=src tests/
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new face detection algorithm
   
   - Implement MTCNN face detection
   - Improve accuracy by 15%
   - Add unit tests for new functionality
   - Update documentation"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🎯 Development Guidelines

### Code Style

We use Black for code formatting and flake8 for linting:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

### Commit Message Convention

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ui): add face selection interface
fix(api): handle invalid image formats
docs: update installation instructions
test: add integration tests for face swapping
```

### Testing Guidelines

#### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Aim for >90% code coverage
- Place in `tests/unit/`

Example:
```python
# tests/unit/test_face_swapper.py
import pytest
from unittest.mock import Mock, patch
from src.face_swapper import FaceSwapper

def test_detect_faces():
    swapper = FaceSwapper()
    # Mock the face detection
    with patch('src.face_swapper.insightface') as mock_insight:
        mock_insight.app.FaceAnalysis.return_value.get.return_value = [Mock()]
        faces = swapper.detect_faces("test_image.jpg")
        assert len(faces) > 0
```

#### Integration Tests
- Test complete workflows
- Use real (small) test images
- Place in `tests/integration/`

Example:
```python
# tests/integration/test_api.py
import requests
import pytest

def test_face_swap_api():
    response = requests.post(
        "http://localhost:8501/api/swap",
        files={
            'source': open('tests/fixtures/source.jpg', 'rb'),
            'target': open('tests/fixtures/target.jpg', 'rb')
        }
    )
    assert response.status_code == 200
    assert 'image' in response.json()
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings for all functions and classes
- Include type hints
- Update API documentation in `docs/API.md`

Example:
```python
def swap_faces(source_img: np.ndarray, target_img: np.ndarray, 
               confidence: float = 0.5) ->
