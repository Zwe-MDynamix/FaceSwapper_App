"""
Face Swapper App - A professional face swapping application
"""

__version__ = "1.0.0"
__author__ = "Zwelakhe Mthembu"
__email__ = "your-email@example.com"
__license__ = "MIT"
__description__ = "A professional-grade face swapping application built with Streamlit and InsightFace"

# Import main components
try:
    from .face_swapper import FaceSwapper
    from .utils import ImageProcessor, ModelManager
    from .models import load_face_analysis_model
    
    __all__ = [
        'FaceSwapper',
        'ImageProcessor', 
        'ModelManager',
        'load_face_analysis_model'
    ]
except ImportError:
    # Handle case where dependencies are not installed
    __all__ = []

# Package metadata
__title__ = "face-swapper-app"
__url__ = "https://github.com/zwelakhem/face-swapper-app"
__download_url__ = f"https://github.com/zwelakhem/face-swapper-app/archive/v{__version__}.tar.gz"
__bugtrack_url__ = "https://github.com/zwelakhem/face-swapper-app/issues"