import streamlit as st
import cv2
import numpy as np
from PIL import Image
import insightface
from insightface.app import FaceAnalysis
import os

# Page configuration
st.set_page_config(
    page_title="Face Swapper App",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .upload-text {
        text-align: center;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'face_swapper' not in st.session_state:
    st.session_state.face_swapper = None
if 'result_image' not in st.session_state:
    st.session_state.result_image = None

@st.cache_resource
def load_face_swapper():
    """Load and cache the face swapper model"""
    try:
        app = FaceAnalysis(name='buffalo_l')
        app.prepare(ctx_id=0, det_size=(640, 640))
        
        # Load face swapper model
        model_path = os.path.join(insightface.model_zoo.get_model_dir(), 'inswapper_128.onnx')
        if not os.path.exists(model_path):
            st.warning("Downloading face swapper model... This may take a few minutes on first run.")
        
        from insightface.model_zoo import get_model
        swapper = get_model('inswapper_128.onnx', download=True, download_zip=True)
        
        return app, swapper
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

def process_image(image_file):
    """Convert uploaded file to numpy array"""
    try:
        image = Image.open(image_file)
        image_np = np.array(image)
        # Convert RGB to BGR for OpenCV
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        return image_np
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def swap_faces(source_img, target_img, app, swapper):
    """Perform face swapping"""
    try:
        # Detect faces in source image
        source_faces = app.get(source_img)
        if len(source_faces) == 0:
            st.error("❌ No face detected in source image!")
            return None
        
        # Detect faces in target image
        target_faces = app.get(target_img)
        if len(target_faces) == 0:
            st.error("❌ No face detected in target image!")
            return None
        
        # Use the first detected face from source
        source_face = source_faces[0]
        
        # Swap faces in target image
        result = target_img.copy()
        for target_face in target_faces:
            result = swapper.get(result, target_face, source_face, paste_back=True)
        
        return result
    except Exception as e:
        st.error(f"Error during face swapping: {str(e)}")
        return None

# Main App
def main():
    # Header
    st.title("🎭 Face Swapper App")
    st.markdown("### Swap faces between images using AI")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This app uses InsightFace AI to detect and swap faces between images.
        
        **How to use:**
        1. Upload a source image (face to extract)
        2. Upload a target image (where to place the face)
        3. Click 'Swap Faces' button
        4. Download the result!
        """)
        
        st.header("⚙️ Settings")
        confidence_threshold = st.slider(
            "Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Higher values = stricter face detection"
        )
        
        st.header("📊 Stats")
        if st.session_state.result_image is not None:
            st.success("✅ Face swap completed!")
        else:
            st.info("⏳ Waiting for images...")
    
    # Main content
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.subheader("📸 Source Image")
        st.markdown('<p class="upload-text">Upload the face you want to use</p>', unsafe_allow_html=True)
        source_file = st.file_uploader(
            "Choose source image",
            type=['jpg', 'jpeg', 'png'],
            key="source",
            label_visibility="collapsed"
        )
        
        if source_file:
            source_image = Image.open(source_file)
            st.image(source_image, caption="Source Face", use_container_width=True)
    
    with col2:
        st.subheader("🎯 Target Image")
        st.markdown('<p class="upload-text">Upload the image to modify</p>', unsafe_allow_html=True)
        target_file = st.file_uploader(
            "Choose target image",
            type=['jpg', 'jpeg', 'png'],
            key="target",
            label_visibility="collapsed"
        )
        
        if target_file:
            target_image = Image.open(target_file)
            st.image(target_image, caption="Target Image", use_container_width=True)
    
    with col3:
        st.subheader("✨ Result")
        if st.session_state.result_image is not None:
            # Convert BGR to RGB for display
            result_rgb = cv2.cvtColor(st.session_state.result_image, cv2.COLOR_BGR2RGB)
            st.image(result_rgb, caption="Swapped Result", use_container_width=True)
            
            # Download button
            result_pil = Image.fromarray(result_rgb)
            from io import BytesIO
            buf = BytesIO()
            result_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="📥 Download Result",
                data=byte_im,
                file_name="face_swap_result.png",
                mime="image/png"
            )
        else:
            st.info("Result will appear here after face swapping")
    
    # Action button
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        if st.button("🔄 Swap Faces", type="primary", use_container_width=True):
            if source_file is None or target_file is None:
                st.error("⚠️ Please upload both source and target images!")
            else:
                with st.spinner("🔮 Loading AI models..."):
                    # Load models
                    app, swapper = load_face_swapper()
                    
                    if app is None or swapper is None:
                        st.error("Failed to load face swapper models!")
                        return
                
                with st.spinner("🎨 Swapping faces... This may take a few seconds..."):
                    # Process images
                    source_np = process_image(source_file)
                    target_np = process_image(target_file)
                    
                    if source_np is None or target_np is None:
                        st.error("Failed to process images!")
                        return
                    
                    # Perform face swap
                    result = swap_faces(source_np, target_np, app, swapper)
                    
                    if result is not None:
                        st.session_state.result_image = result
                        st.success("✅ Face swap completed successfully!")
                        st.rerun()
    
    # Clear button
    with col_btn3:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.result_image = None
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with ❤️ using Streamlit and InsightFace</p>
        <p>⚠️ Please use responsibly and ethically</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
