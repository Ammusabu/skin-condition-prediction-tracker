"""
Image preprocessing for skin condition model
"""
import numpy as np
from PIL import Image
import traceback

class ImagePreprocessor:
    """Preprocess images for model prediction"""
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        
    def preprocess_image(self, image_input):
        """Preprocess image for model prediction"""
        try:
            if image_input is None:
                print("❌ No image input provided")
                return None
            
            # Convert to PIL Image
            if isinstance(image_input, str):
                print(f"📂 Loading image from path: {image_input}")
                img = Image.open(image_input).convert('RGB')
            elif isinstance(image_input, np.ndarray):
                image_input = np.flip(image_input, axis=1)
                if image_input.max() <= 1.0:
                    image_input = (image_input * 255).astype("uint8")
                img = Image.fromarray(image_input).convert("RGB")
            elif hasattr(image_input, 'convert'):
                img = image_input.convert('RGB')
            else:
                print(f"❌ Invalid image input type: {type(image_input)}")
                return None
            
            print(f"📐 Original image size: {img.size}")
            
            # Resize to target size
            img = img.resize(self.target_size, Image.BILINEAR)
            print(f"📐 Resized image size: {img.size}")
            
            # Convert to numpy array
            img_array = np.array(img).astype(np.float32)
            print(f"🔍 Image array shape: {img_array.shape}")
            print(f"🔍 Original pixel range: [{img_array.min():.0f}, {img_array.max():.0f}]")
            
            # Normalize to [0, 1] — MUST exactly match training preprocessing
            img_array = img_array / 255.0
            print(f"🔍 Normalized pixel range: [{img_array.min():.3f}, {img_array.max():.3f}]")
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            print(f"🔍 Final array shape: {img_array.shape}")
            if img_array.shape != (1, 224, 224, 3):
                raise ValueError(f"Invalid input shape: {img_array.shape}")
            
    
            return img_array
            
        except Exception as e:
            print(f"❌ Preprocessing error: {e}")
            traceback.print_exc()
            return None