# GitHub Repository Setup Guide

## 🚀 Quick Setup Steps

### 1. Create GitHub Repository

```bash
# On GitHub.com, create a new repository named: face-swapper-app
# Initialize with README: No (we'll push our own)
# Add .gitignore: Python
# Add license: MIT
```

### 2. Clone and Setup Local Repository

```bash
# Clone the empty repository
git clone https://github.com/Zwe-MDynamix/FaceSwapper_App.git
cd face-swapper-app

# Initialize git if needed
git init
git remote add origin https://github.com/Zwe-MDynamix/FaceSwapper_App.git
```

### 3. Create Project Structure

Create this directory structure in your project:

```
face-swapper-app/
├── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml
│   │   └── docker-publish.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── src/
│   ├── __init__.py
│   ├── face_swapper.py
│   ├── utils.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_face_swapper.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
├── docker/
│   ├── Dockerfile.dev
│   └── docker-compose.override.yml
├── .gitignore
├── .dockerignore
├── LICENSE
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── docker-compose.yml
├── app.py
└── setup.py
```

### 4. Create Essential Files

Let's create the key files for your repository:

#### `.gitignore`
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
PIPFILE.lock

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Models and data
models/*.pkl
models/*.h5
models/*.pb
data/
uploads/
temp/
*.log

# Docker
docker-compose.override.yml
```

#### `requirements-dev.txt`
```txt
# Development dependencies
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.11.1
black==23.7.0
flake8==6.0.0
isort==5.12.0
pre-commit==3.3.3
mypy==1.5.1

# Documentation
mkdocs==1.5.2
mkdocs-material==9.1.21

# Testing tools
requests-mock==1.11.0
factory-boy==3.3.0

# Include production requirements
-r requirements.txt
```

#### `LICENSE` (MIT License)
```
MIT License

Copyright (c) 2024 Zwelakhe Mthembu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  face-swapper:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
      - STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Development service
  face-swapper-dev:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    ports:
      - "8502:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=false
      - STREAMLIT_SERVER_RUN_ON_SAVE=true
    volumes:
      - .:/app
      - /app/__pycache__
    profiles:
      - dev
```

#### `docker-compose.test.yml`
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - ENVIRONMENT=test
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - .:/app
    command: python -m pytest tests/ -v
    
  test-runner:
    build: .
    environment:
      - ENVIRONMENT=test
    volumes:
      - .:/app
    command: |
      sh -c "
        python -m pytest tests/unit/ --cov=src --cov-report=xml &&
        python -m pytest tests/integration/ -v
      "
    depends_on:
      - app
```

### 5. Create GitHub Actions Workflows

#### `.github/workflows/ci-cd.yml`
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
        
    - name: Format check with black
      run: black --check .
      
    - name: Import sort check
      run: isort --check-only .
      
    - name: Test with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=html
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
        
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: Zwe-MDynamix/FaceSwapper_App
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=raw,value=latest,enable={{is_default_branch}}
          
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
        
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

#### `.github/workflows/docker-publish.yml`
```yaml
name: Publish Docker Image

on:
  release:
    types: [published]
  push:
    branches: [ main ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: Zwe-MDynamix/FaceSwapper_App

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### 6. Create Issue and PR Templates

#### `.github/ISSUE_TEMPLATE/bug_report.md`
```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Docker Version: [e.g. 20.10.21]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
```

#### `.github/ISSUE_TEMPLATE/feature_request.md`
```markdown
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

#### `.github/PULL_REQUEST_TEMPLATE.md`
```markdown
## Description

Brief description of the changes in this PR.

## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?

Please describe the tests that you ran to verify your changes.

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist:

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### 7. Commit and Push Everything

```bash
# Add all files
git add .

# Commit with a descriptive message
git commit -m "Initial project setup with CI/CD pipeline

- Add comprehensive README with features and usage
- Configure multi-stage Docker build for production
- Set up GitHub Actions for CI/CD
- Add GitLab CI/CD pipeline configuration  
- Include issue and PR templates
- Add development and testing configurations"

# Push to GitHub
git push -u origin main

# Create and push develop branch
git checkout -b develop
git push -u origin develop
```

### 8. Configure Repository Settings

#### Repository Settings:
1. Go to Settings → General
2. Enable "Automatically delete head branches"
3. Set default branch to `main`

#### Branch Protection Rules:
1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

#### Secrets Configuration:
Go to Settings → Secrets and variables → Actions and add:
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

### 9. Enable GitHub Pages (Optional)

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs`
4. This will host your documentation

### 10. Add Repository Topics

Go to the main repository page and add topics:
- `streamlit`
- `face-swapping`
- `computer-vision`
- `docker`
- `python`
- `ai`
- `machine-learning`
- `insightface`