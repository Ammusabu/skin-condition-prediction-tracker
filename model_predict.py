"""
Model prediction module for skin condition classification
"""
import numpy as np
import json
from pathlib import Path
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')

class SkinConditionPredictor:
    def __init__(self, model_path="model/skin_model.keras", labels_path="model/class_labels.json"):
        self.model_path = model_path
        self.labels_path = labels_path
        self.model = None
        self.label_mapping = {}
        self.conditions = []
        
        # Load labels
        self._load_labels()
    
    def _load_labels(self):
        
        try:
            with open(self.labels_path, "r") as f:
                labels_data = json.load(f)

            self.label_mapping = {int(v): k for k, v in labels_data.items()}
            self.conditions = [self.label_mapping[i] for i in sorted(self.label_mapping)]
            print(f"✅ Loaded labels (index → class): {self.label_mapping}")

        except Exception as e:
            raise RuntimeError("class_labels.json missing or corrupted") from e
    
    def load_model(self):
        """Load the trained model"""
        try:
            if Path(self.model_path).exists():
                print(f"🔄 Loading model from {self.model_path}...")
                self.model = tf.keras.models.load_model(self.model_path, compile=False)
                print("✅ Model loaded successfully")
                print(f"✅ Model input shape: {self.model.input_shape}")
                print(f"✅ Model output shape: {self.model.output_shape}")
                return True
            else:
                print(f"❌ Model file not found: {self.model_path}")
                print("ℹ️ Please check if skin_model.h5 exists in the model/ directory")
                return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def predict(self, image_array):
        """Make prediction on image array"""
        try:
            if self.model is not None and image_array is not None:
                print(f"🔍 Making prediction on image with shape: {image_array.shape}")
                print(f"🔍 Image array range: [{image_array.min():.3f}, {image_array.max():.3f}]")
                
                # Make prediction
                predictions = self.model(image_array, training=False).numpy()
                print(f"🔍 Raw predictions shape: {predictions.shape}")
                print(f"🔍 Raw predictions: {predictions}")
                
                predicted_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_idx])
                predicted_condition = self.label_mapping.get(predicted_idx, "Unknown")
                # Get all predictions
                all_predictions = {
                    self.label_mapping[i]: float(predictions[0][i])
                    for i in range(len(predictions[0]))
                }
                return predicted_condition, confidence, all_predictions
                
                print(f"✅ Prediction complete:")
                print(f"   Condition: {predicted_condition}")
                print(f"   Confidence: {confidence:.2%}")
                print(f"   Index: {predicted_idx}")
                
                return predicted_condition, confidence, all_predictions
            else:
                raise RuntimeError("❌ MODEL NOT LOADED OR IMAGE ARRAY IS NONE")

                
        except Exception as e:
            raise RuntimeError("Prediction failed") from e

# Helper functions for backward compatibility
def load_model():
    """Load model for backward compatibility"""
    predictor = SkinConditionPredictor()
    if predictor.load_model():
        return predictor.model
    return None

def load_class_labels():
    """Load class labels for backward compatibility"""
    predictor = SkinConditionPredictor()
    return predictor.label_mapping