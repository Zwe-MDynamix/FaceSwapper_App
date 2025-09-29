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
