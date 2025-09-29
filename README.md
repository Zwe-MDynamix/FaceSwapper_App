# Face Swapper App 🎭 
🌟 Docker Images/Containers, GitLab CI-CD Pipeline & README created and written by: 

| **Zwelakhe Msuthu** | DevOps, SecDevOps & Cloud Infrastructure Engineer |

| **Zwe_M Dynamix** | e: zwenix@gmail.com |

[![Docker Pulls](https://img.shields.io/docker/pulls/zwelakhem/face-swapper-app)](https://hub.docker.com/r/zwelakhem/face-swapper-app)
[![Docker Image Size](https://img.shields.io/docker/image-size/zwelakhem/face-swapper-app)](https://hub.docker.com/r/zwelakhem/face-swapper-app)
[![Build Status](https://github.com/Zwe-MDynamix/FaceSwapper_App/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/Zwe-MDynamix/FaceSwapper_App/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional-grade face swapping application built with Streamlit and powered by InsightFace. This application enables real-time face swapping with high-quality results using state-of-the-art deep learning models.

## 🌟 Features

- **Real-time Face Swapping**: Swap faces between multiple images with high accuracy
- **Multiple Face Detection**: Automatically detects and processes multiple faces in images
- **High-Quality Results**: Utilizes InsightFace's advanced neural networks for realistic face swapping
- **User-Friendly Interface**: Clean, intuitive Streamlit web interface
- **Dockerized Deployment**: Easy deployment with Docker containers
- **Batch Processing**: Process multiple images simultaneously
- **Download Results**: Save processed images directly from the web interface

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image
docker run -p 8501:8501 zwelakhem/face-swapper-app:latest

# Or run with custom port
docker run -p 3000:8501 zwelakhem/face-swapper-app:latest
```

Visit `http://localhost:8501` to access the application.

### Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/Zwe-MDynamix/FaceSwapper_App.git
cd face-swapper-app

# Start the application
docker-compose up
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/Zwe-MDynamix/FaceSwapper_App.git
cd face-swapper-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 📋 Prerequisites

- **Docker**: Version 20.10 or later
- **Python**: Version 3.9 or later (for local development)
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: At least 2GB free space for models and processing

## 🛠️ Installation

### Option 1: Docker (Production)

```bash
# Build from source
git clone https://github.com/Zwe-MDynamix/FaceSwapper_App.git
cd face-swapper-app
docker build -t face-swapper-app .
docker run -p 8501:8501 face-swapper-app
```

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/Zwe-MDynamix/FaceSwapper_App.git
cd face-swapper-app

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3.9 python3-pip libglib2.0-0

# Install Python dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 📖 Usage

1. **Upload Source Image**: Upload the image containing the face you want to use
2. **Upload Target Image**: Upload the image where you want to swap the face
3. **Select Faces**: The app automatically detects faces - select which ones to swap
4. **Process**: Click "Swap Faces" to generate the result
5. **Download**: Save the processed image to your device

### API Usage

The application also exposes a simple API for programmatic access:

```python
import requests

# Upload images and get result
files = {
    'source': open('source_face.jpg', 'rb'),
    'target': open('target_image.jpg', 'rb')
}

response = requests.post('http://localhost:8501/api/swap', files=files)
```

## 🏗️ Architecture

```
face-swapper-app/
├── app.py                 # Main Streamlit application
├── src/
│   ├── face_swapper.py    # Core face swapping logic
│   ├── utils.py           # Utility functions
│   └── models.py          # Model loading and management
├── models/                # Pre-trained model storage
├── tests/                 # Unit and integration tests
├── docker/                # Docker-related files
├── .github/               # GitHub Actions workflows
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker build instructions
└── README.md             # Project documentation
```

## 🔧 Configuration

### Environment Variables

```bash
# Application settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Model configuration
MODEL_PATH=/app/models
FACE_DETECTION_CONFIDENCE=0.5
FACE_SWAPPING_QUALITY=high

# Performance settings
MAX_IMAGE_SIZE=2048
ENABLE_GPU=false
```

### Model Configuration

The application uses InsightFace models. You can configure which models to use:

```python
# In src/models.py
AVAILABLE_MODELS = {
    'buffalo_l': 'High accuracy, slower processing',
    'buffalo_m': 'Balanced accuracy and speed',
    'buffalo_s': 'Fast processing, lower accuracy'
}
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=src tests/
```

## 📊 Performance

- **Processing Time**: 2-5 seconds per face swap (CPU)
- **Memory Usage**: ~2GB RAM during processing
- **Supported Formats**: JPG, PNG, WEBP
- **Maximum Resolution**: 4K images supported
- **Concurrent Users**: Up to 10 simultaneous users

## 🐛 Troubleshooting

### Common Issues

**1. Out of Memory Error**
```bash
# Increase Docker memory limit
docker run --memory=4g -p 8501:8501 zwelakhem/face-swapper-app:latest
```

**2. Model Loading Issues**
```bash
# Clear model cache
docker run --rm -v face_swapper_models:/app/models busybox rm -rf /app/models/*
```

**3. Poor Face Detection**
```bash
# Adjust detection confidence in app settings
FACE_DETECTION_CONFIDENCE=0.3  # Lower = more sensitive
```

### Debug Mode

```bash
# Run with debug logging
docker run -e STREAMLIT_LOGGER_LEVEL=debug -p 8501:8501 zwelakhem/face-swapper-app:latest
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/face-swapper-app.git
cd face-swapper-app

# Create development environment
python -m venv dev-env
source dev-env/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [InsightFace](https://github.com/deepinsight/insightface) - Face analysis toolkit
- [Streamlit](https://streamlit.io/) - Web application framework
- [OpenCV](https://opencv.org/) - Computer vision library
- [ONNX Runtime](https://onnxruntime.ai/) - Machine learning inference

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Zwe-MDynamix/FaceSwapper_App/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Zwe-MDynamix/FaceSwapper_App/discussions)
- **Email**: zwenix@gmail.com

## 🔄 Changelog

### v1.0.0 (2024-12-XX)
- Initial release
- Basic face swapping functionality
- Docker support
- Web interface

### v0.9.0 (2024-12-XX)
- Beta release
- Core functionality implemented
- Testing and optimization

---

**⭐ If this project helped you, please give it a star on GitHub!**

