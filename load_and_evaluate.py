import sys
import os
import tensorflow as tf
from ml.config import RESULTS_DIR
from ml.dataset import get_data_generators
from ml.evaluation import evaluate_model

def load_and_evaluate():
    name = 'mobilenetv2'
    model_path = os.path.join('ml/models', f'{name}.h5')
    
    print(f"Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("Getting data generators...")
    # Assume training data is available for validation
    _, val_gen = get_data_generators()
    
    print("Evaluating model...")
    metrics = evaluate_model(model, val_gen, name)
    print(f"Evaluation complete. Metrics: {metrics}")

if __name__ == "__main__":
    load_and_evaluate()
