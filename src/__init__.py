"""
Face Swapper App - A professional face swapping application

This package provides face swapping functionality using InsightFace AI models.
"""

__version__ = "1.0.0"
__author__ = "Zwelakhe Mthembu"
__email__ = "your-email@example.com"
__license__ = "MIT"
__description__ = "A professional-grade face swapping application built with Streamlit and InsightFace"

# Package metadata
__title__ = "face-swapper-app"
__url__ = "https://github.com/Zwe-MDynamix/FaceSwapper_App"
__download_url__ = f"https://github.com/Zwe-MDynamix/FaceSwapper_App/archive/v{__version__}.tar.gz"
__bugtrack_url__ = "https://github.com/Zwe-MDynamix/FaceSwapper_App/issues"
__docker_url__ = "https://hub.docker.com/r/Zwe-MDynamix/FaceSwapper_App"

# Import main components for easy access
try:
    from .face_swapper import FaceSwapper
    from .utils import (
        ImageProcessor,
        FileHandler,
        calculate_face_similarity,
        create_thumbnail
    )
    
    # Define what gets imported with "from src import *"
    __all__ = [
        'FaceSwapper',
        'ImageProcessor',
        'FileHandler',
        'calculate_face_similarity',
        'create_thumbnail',
        '__version__',
        '__author__',
    ]
    
except ImportError as e:
    # Handle case where dependencies are not installed yet
    import warnings
    warnings.warn(
        f"Could not import all modules: {str(e)}. "
        "Some dependencies may not be installed. "
        "Run: pip install -r requirements.txt",
        ImportWarning
    )
    __all__ = []


def get_version():
    """Return the current version of the package"""
    return __version__


def get_package_info():
    """Return package information as a dictionary"""
    return {
        'name': __title__,
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'license': __license__,
        'description': __description__,
        'url': __url__,
        'docker_url': __docker_url__,
    }


# Print package info when imported (optional - can remove if too verbose)
if __name__ != '__main__':
    pass  # Silent import
    # Uncomment below to show info on import:
    # print(f"Face Swapper App v{__version__} loaded successfully!")
