from ml.inference.predictor import ProductionPredictor
import os

# Create dummy image for testing
from PIL import Image
img = Image.new('RGB', (224, 224), color = 'red')
img.save('test_img.jpg')

predictor = ProductionPredictor()
print("Predictor initialized:", predictor._model is not None)

if predictor._model:
    try:
        disease, confidence, heatmap = predictor.predict('test_img.jpg')
        print(f"Prediction: {disease}, Confidence: {confidence}")
    except Exception as e:
        print(f"Prediction failed: {e}")
else:
    print("Model not loaded.")
