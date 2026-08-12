import os
from ml.inference.predictor import ProductionPredictor
from factory import Config

class DiseasePredictor:
    def __init__(self, model_path=None, classes_path=None):
        # model_path and classes_path are ignored now, as ProductionPredictor handles loading
        self.predictor = ProductionPredictor()

    def predict(self, image_path):
        # ProductionPredictor.predict returns (class_name, confidence)
        class_name, confidence = self.predictor.predict(image_path)
        
        # Heatmap generation is currently disabled/limited due to architecture differences.
        # This preserves the original signature but returns empty heatmap.
        return class_name, confidence, "" 
