"""
Core face swapping functionality
"""

import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
import os
from typing import Optional, List, Tuple


class FaceSwapper:
    """
    Face swapping class using InsightFace models
    """
    
    def __init__(self, model_name: str = 'buffalo_l', det_size: Tuple[int, int] = (640, 640)):
        """
        Initialize the face swapper
        
        Args:
            model_name: Name of the face analysis model
            det_size: Detection size for face detection
        """
        self.model_name = model_name
        self.det_size = det_size
        self.app = None
        self.swapper = None
        
    def load_models(self):
        """Load face analysis and swapper models"""
        try:
            # Load face analysis model
            self.app = FaceAnalysis(name=self.model_name)
            self.app.prepare(ctx_id=0, det_size=self.det_size)
            
            # Load face swapper model
            self.swapper = get_model('inswapper_128.onnx', download=True, download_zip=True)
            
            return True
        except Exception as e:
            print(f"Error loading models: {str(e)}")
            return False
    
    def detect_faces(self, image: np.ndarray) -> List:
        """
        Detect faces in an image
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of detected faces
        """
        if self.app is None:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        faces = self.app.get(image)
        return faces
    
    def swap_face(
        self,
        source_img: np.ndarray,
        target_img: np.ndarray,
        source_face_index: int = 0,
        target_face_index: Optional[int] = None
    ) -> Optional[np.ndarray]:
        """
        Swap a single face from source to target
        
        Args:
            source_img: Source image containing the face to extract
            target_img: Target image where the face will be placed
            source_face_index: Index of face to use from source (default: 0)
            target_face_index: Index of face to replace in target (None = all faces)
            
        Returns:
            Image with swapped face, or None if swap failed
        """
        if self.app is None or self.swapper is None:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        try:
            # Detect faces
            source_faces = self.detect_faces(source_img)
            target_faces = self.detect_faces(target_img)
            
            if len(source_faces) == 0:
                print("No face detected in source image")
                return None
            
            if len(target_faces) == 0:
                print("No face detected in target image")
                return None
            
            # Get source face
            if source_face_index >= len(source_faces):
                print(f"Source face index {source_face_index} out of range")
                return None
            
            source_face = source_faces[source_face_index]
            
            # Perform swap
            result = target_img.copy()
            
            if target_face_index is None:
                # Swap all faces in target
                for target_face in target_faces:
                    result = self.swapper.get(result, target_face, source_face, paste_back=True)
            else:
                # Swap specific face
                if target_face_index >= len(target_faces):
                    print(f"Target face index {target_face_index} out of range")
                    return None
                
                target_face = target_faces[target_face_index]
                result = self.swapper.get(result, target_face, source_face, paste_back=True)
            
            return result
            
        except Exception as e:
            print(f"Error during face swap: {str(e)}")
            return None
    
    def swap_faces_batch(
        self,
        source_images: List[np.ndarray],
        target_image: np.ndarray
    ) -> List[Optional[np.ndarray]]:
        """
        Swap faces from multiple source images onto a target image
        
        Args:
            source_images: List of source images
            target_image: Target image
            
        Returns:
            List of result images
        """
        results = []
        
        for source_img in source_images:
            result = self.swap_face(source_img, target_image)
            results.append(result)
        
        return results
    
    def get_face_info(self, image: np.ndarray) -> List[dict]:
        """
        Get information about detected faces
        
        Args:
            image: Input image
            
        Returns:
            List of dictionaries containing face information
        """
        faces = self.detect_faces(image)
        
        face_info = []
        for i, face in enumerate(faces):
            info = {
                'index': i,
                'bbox': face.bbox.tolist(),
                'det_score': float(face.det_score),
                'landmark': face.landmark.tolist() if hasattr(face, 'landmark') else None,
                'age': int(face.age) if hasattr(face, 'age') else None,
                'gender': 'male' if hasattr(face, 'gender') and face.gender == 1 else 'female'
            }
            face_info.append(info)
        
        return face_info
    
    def visualize_faces(self, image: np.ndarray) -> np.ndarray:
        """
        Draw bounding boxes around detected faces
        
        Args:
            image: Input image
            
        Returns:
            Image with face bounding boxes drawn
        """
        faces = self.detect_faces(image)
        result = image.copy()
        
        for face in faces:
            bbox = face.bbox.astype(int)
            cv2.rectangle(result, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # Draw landmarks if available
            if hasattr(face, 'landmark'):
                for point in face.landmark:
                    cv2.circle(result, (int(point[0]), int(point[1])), 2, (0, 0, 255), -1)
        
        return result
