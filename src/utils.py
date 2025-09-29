import cv2
from src.utils import ImageProcessor, detect_image_quality

# Load an image
img = cv2.imread('test_photo.jpg')

# Check quality
quality = detect_image_quality(img)
print(f"Image Quality Report:")
print(f"  - Brightness: {quality['brightness']:.1f}")
print(f"  - Contrast: {quality['contrast']:.1f}")
print(f"  - Sharpness: {quality['sharpness']:.1f}")
print(f"  - Quality Score: {quality['quality_score']:.1f}/100")
print(f"  - Is Blurry: {quality['is_blurry']}")

# Resize and enhance
resized = ImageProcessor.resize_image(img, max_size=800)
enhanced = ImageProcessor.enhance_image(resized, brightness=1.2, contrast=1.1)

# Save result
cv2.imwrite('enhanced_photo.jpg', enhanced)
print("Enhanced image saved!")
