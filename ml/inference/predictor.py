import json
import os
import tensorflow as tf
import numpy as np
from ml.preprocessing import preprocess_image
from factory import Config

class ProductionPredictor:
    def __init__(self):
        self.model = None
        self.class_names = None
        self._load_model()

    def _load_model(self):
        if not os.path.exists(Config.MODEL_PATH):
            print(f"Model not found at {Config.MODEL_PATH}")
            return

        self.model = tf.keras.models.load_model(Config.MODEL_PATH)
        
        classes_path = os.path.join(os.path.dirname(Config.MODEL_PATH), 'classes.json')
        if os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                class_indices = json.load(f)
                self.class_names = {v: k for k, v in class_indices.items()}
            
    def predict(self, image_path):
        if not self.model:
            return "Predictor not initialized", 0.0, ""
            
        img_array = preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_index = int(tf.argmax(predictions, axis=1)[0])
        confidence = float(tf.reduce_max(predictions, axis=1)[0])
        
        # Placeholder for Grad-CAM logic
        heatmap_filename = "" 
        
        return self.class_names[predicted_index], confidence, heatmap_filename
