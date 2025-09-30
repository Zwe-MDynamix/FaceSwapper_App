#!/usr/bin/env python3
"""
Face Swapper App Setup Configuration
"""

import os
import re
from setuptools import setup, find_packages

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version from __init__.py
def get_version():
    """Extract version from src/__init__.py"""
    version_file = os.path.join(here, 'src', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
            version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
            if version_match:
                return version_match.group(1)
    return "0.1.0"  # Fallback version

# Read requirements from requirements.txt
def get_requirements():
    """Get requirements from requirements.txt"""
    requirements_file = os.path.join(here, 'requirements.txt')
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Read development requirements
def get_dev_requirements():
    """Get development requirements from requirements-dev.txt"""
    dev_requirements_file = os.path.join(here, 'requirements-dev.txt')
    if os.path.exists(dev_requirements_file):
        with open(dev_requirements_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#') and not line.startswith('-r')]
    return []

setup(
    # Basic package information
    name='face-swapper-app',
    version=get_version(),
    description='A professional-grade face swapping application built with Streamlit and InsightFace',
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    # URLs
    url='https://github.com/Zwe-MDynamix/FaceSwapper_App',
    download_url='https://github.com/Zwe-MDynamix/FaceSwapper_App/archive/v{}.tar.gz'.format(get_version()),
    
    # Author information
    author='Zwelakhe Mthembu',
    author_email='your-email@example.com',
    
    # License
    license='MIT',
    
    # Classifiers
    classifiers=[
        # Development Status
        'Development Status :: 4 - Beta',
        
        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        
        # Topic
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        
        # License
        'License :: OSI Approved :: MIT License',
        
        # Programming Language
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        
        # Operating System
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        
        # Environment
        'Environment :: Web Environment',
        'Environment :: Console',
    ],
    
    # Keywords
    keywords='face-swapping computer-vision ai machine-learning streamlit insightface opencv deepfake',
    
    # Package configuration
    packages=find_packages(exclude=['tests*', 'docs*']),
    package_dir={'': '.'},
    
    # Python version requirement
    python_requires='>=3.9',
    
    # Dependencies
    install_requires=get_requirements(),
    
    # Extra dependencies
    extras_require={
        'dev': get_dev_requirements(),
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-mock>=3.10.0',
            'requests-mock>=1.10.0',
        ],
        'docs': [
            'mkdocs>=1.4.0',
            'mkdocs-material>=9.0.0',
            'mkdocs-mermaid2-plugin>=0.6.0',
        ],
        'gpu': [
            'onnxruntime-gpu>=1.15.0',
        ],
        'all': get_dev_requirements() + [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'mkdocs>=1.4.0',
            'mkdocs-material>=9.0.0',
        ]
    },
    
    # Entry points
    entry_points={
        'console_scripts': [
            'face-swapper=src.cli:main',
        ],
    },
    
    # Package data
    package_data={
        'src': [
            'models/*.onnx',
            'templates/*.html',
            'static/*.css',
            'static/*.js',
        ],
    },
    
    # Include additional files
    include_package_data=True,
    
    # Zip safe
    zip_safe=False,
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/Zwe-MDynamix/FaceSwapper_App/issues',
        'Source': 'https://github.com/Zwe-MDynamix/FaceSwapper_App',
        'Documentation': 'https://zwelakhem.github.io/face-swapper-app/',
        'Docker Hub': 'https://hub.docker.com/r/Zwe-MDynamix/FaceSwapper_App',
        'Funding': 'https://github.com/sponsors/zwelakhem',
    },
)