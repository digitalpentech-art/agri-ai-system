import os
import json
from factory import Config

class DiseasePredictor:
    def __init__(self, model_path, classes_path):
        self.model = True # Mock
        
    def predict(self, image_path):
        # Mock prediction
        return "Healthy", 0.95, "heatmap_mock.jpg"
    
    def generate_heatmap(self, img_array, class_index, original_path):
        return "heatmap_mock.jpg"
