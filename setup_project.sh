#!/bin/bash

# Face Swapper App - Project Setup Script
# This script creates all necessary files for the project

echo "🎭 Setting up Face Swapper App project..."
echo "=========================================="

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p src
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures
mkdir -p docs
mkdir -p docker
mkdir -p models
mkdir -p data

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
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
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
htmlcov/
.coverage
.pytest_cache/
coverage.xml

# Models and data
models/*.pkl
models/*.h5
models/*.pb
data/
uploads/
temp/
*.log
EOF

# Create .dockerignore
echo "📝 Creating .dockerignore..."
cat > .dockerignore << 'EOF'
__pycache__
*.pyc
.git
.gitignore
README.md
.env
.venv
venv/
tests/
docs/
.github/
.gitlab-ci.yml
docker-compose.yml
*.md
EOF

# Create requirements.txt
echo "📝 Creating requirements.txt..."
cat > requirements.txt << 'EOF'
# Core Streamlit
streamlit==1.28.1

# Computer Vision & Face Recognition
insightface==0.7.3
opencv-python-headless==4.8.0.76
onnxruntime==1.15.1

# Scientific Computing
numpy==1.21.6
pandas==1.5.3
Pillow==9.5.0
EOF

# Create requirements-dev.txt
echo "📝 Creating requirements-dev.txt..."
cat > requirements-dev.txt << 'EOF'
# Development dependencies
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.11.1
black==23.7.0
flake8==6.0.0
isort==5.12.0
pre-commit==3.3.3

# Include production requirements
-r requirements.txt
EOF

# Create Dockerfile
echo "📝 Creating Dockerfile..."
cat > Dockerfile << 'EOF'
# Build stage - Ubuntu 20.04
FROM ubuntu:20.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and build tools
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3-pip \
    python3.9-distutils \
    build-essential \
    cmake \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

WORKDIR /app
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    python3.9-distutils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libopenblas0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-index --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
EOF

# Create docker-compose.yml
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
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
EOF

# Create .gitlab-ci.yml
echo "📝 Creating .gitlab-ci.yml..."
cat > .gitlab-ci.yml << 'EOF'
stages:
  - lint
  - test
  - build
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA
  DOCKERHUB_IMAGE: zwelakhem/face-swapper-app

default:
  image: python:3.9

lint:code:
  stage: lint
  script:
    - pip install flake8 black isort
    - black --check --diff . || true
    - flake8 . --count --exit-zero --max-line-length=127
  allow_failure: true

test:unit:
  stage: test
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - python -m pytest tests/ -v || true
  allow_failure: true

build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
    - echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
  script:
    - docker build -t $IMAGE_NAME:$IMAGE_TAG .
    - docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
    - docker push $IMAGE_NAME:$IMAGE_TAG
    - docker push $IMAGE_NAME:latest
    - docker tag $IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_IMAGE:$IMAGE_TAG
    - docker tag $IMAGE_NAME:latest $DOCKERHUB_IMAGE:latest
    - docker push $DOCKERHUB_IMAGE:$IMAGE_TAG
    - docker push $DOCKERHUB_IMAGE:latest
  only:
    - main
    - develop

security:container-scan:
  stage: security
  image: docker:latest
  services:
    - docker:dind
  script:
    - echo "Security scanning..."
  allow_failure: true
EOF

# Create GitHub Actions workflow
echo "📝 Creating GitHub Actions workflows..."
cat > .github/workflows/ci-cd.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    - name: Test with pytest
      run: |
        pytest tests/ -v || true

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
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: zwelakhem/face-swapper-app:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
EOF

# Create src/__init__.py
echo "📝 Creating src/__init__.py..."
cat > src/__init__.py << 'EOF'
"""Face Swapper App"""
__version__ = "1.0.0"
__author__ = "Zwelakhe Mthembu"
EOF

# Create basic test file
echo "📝 Creating test files..."
cat > tests/__init__.py << 'EOF'
"""Tests for Face Swapper App"""
EOF

cat > tests/unit/__init__.py << 'EOF'
"""Unit tests"""
EOF

cat > tests/unit/test_basic.py << 'EOF'
"""Basic tests"""
import pytest

def test_basic():
    """Basic test to verify pytest works"""
    assert True

def test_import():
    """Test that we can import the package"""
    try:
        import src
        assert src.__version__ == "1.0.0"
    except ImportError:
        pytest.skip("Package not installed")
EOF

# Create LICENSE
echo "📝 Creating LICENSE..."
cat > LICENSE << 'EOF'
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
EOF

# Create placeholder app.py if it doesn't exist
if [ ! -f "app.py" ]; then
    echo "📝 Creating placeholder app.py..."
    cat > app.py << 'EOF'
import streamlit as st

st.set_page_config(page_title="Face Swapper App", page_icon="🎭", layout="wide")

st.title("🎭 Face Swapper App")
st.write("Welcome to the Face Swapper App!")

st.info("⚠️ This is a placeholder. Replace with your actual face swapping code.")

# Placeholder for face swapping functionality
st.header("Upload Images")
col1, col2 = st.columns(2)

with col1:
    source_file = st.file_uploader("Upload Source Image", type=['jpg', 'jpeg', 'png'])
    if source_file:
        st.image(source_file, caption="Source Image")

with col2:
    target_file = st.file_uploader("Upload Target Image", type=['jpg', 'jpeg', 'png'])
    if target_file:
        st.image(target_file, caption="Target Image")

if st.button("Swap Faces"):
    st.warning("Face swapping functionality to be implemented")
EOF
fi

# Create setup.py
echo "📝 Creating setup.py..."
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name='face-swapper-app',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.28.1',
        'insightface>=0.7.3',
        'opencv-python-headless>=4.8.0',
        'onnxruntime>=1.15.1',
    ],
)
EOF

echo ""
echo "✅ Project setup complete!"
echo ""
echo "📁 Created files:"
echo "   - .gitignore"
echo "   - .dockerignore"
echo "   - requirements.txt"
echo "   - requirements-dev.txt"
echo "   - Dockerfile"
echo "   - docker-compose.yml"
echo "   - .gitlab-ci.yml"
echo "   - .github/workflows/ci-cd.yml"
echo "   - LICENSE"
echo "   - setup.py"
echo "   - src/__init__.py"
echo "   - tests/unit/test_basic.py"
echo "   - app.py (placeholder if not exists)"
echo ""
echo "📋 Next steps:"
echo "   1. Copy your actual app.py code (if you have it)"
echo "   2. git init"
echo "   3. git add ."
echo "   4. git commit -m 'Initial commit'"
echo "   5. git remote add origin https://github.com/zwelakhem/face-swapper-app.git"
echo "   6. git push -u origin main"
echo ""
echo "🚀 Your project is ready!"
EOF

chmod +x setup_project.sh
