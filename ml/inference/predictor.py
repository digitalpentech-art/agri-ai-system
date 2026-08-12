import json
import os
import tensorflow as tf
from ml.config import BEST_MODEL_JSON, MODELS_DIR, CLASSES_JSON
from ml.preprocessing import preprocess_image

class ProductionPredictor:
    def __init__(self):
        self.model = None
        self.class_names = None
        self._load_best_model()

    def _load_best_model(self):
        if not os.path.exists(BEST_MODEL_JSON):
            print("No best model found. Please train models first.")
            return

        with open(BEST_MODEL_JSON, 'r') as f:
            best_model_info = json.load(f)
            model_name = best_model_info['model_name']
            
        model_path = os.path.join(MODELS_DIR, f"{model_name}.h5")
        self.model = tf.keras.models.load_model(model_path)
        
        with open(CLASSES_JSON, 'r') as f:
            self.class_indices = json.load(f)
            self.class_names = {v: k for k, v in self.class_indices.items()}
            
    def predict(self, image_path):
        if not self.model:
            return "Predictor not initialized", 0.0
            
        img_array = preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_index = int(tf.argmax(predictions, axis=1)[0])
        confidence = float(tf.reduce_max(predictions, axis=1)[0])
        
        return self.class_names[predicted_index], confidence
