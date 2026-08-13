import os
import sys

import tensorflow as tf
from ml.dataset import get_data_generators
from ml.evaluation import evaluate_model
from ml.config import MODELS_DIR

def evaluate_saved_model():
    name = 'mobilenetv2'
    model_path = os.path.join(MODELS_DIR, f"{name}.h5")

    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading trained model from: {model_path}")
    model = tf.keras.models.load_model(model_path)

    print("Preparing validation data...")
    # get_data_generators() returns (train_gen, val_gen)
    _, val_gen = get_data_generators()

    print(f"Evaluating {name}...")
    # evaluate_model saves metrics.json, classification_report.json, and confusion_matrix.png
    # to os.path.join(RESULTS_DIR, model_name)
    metrics = evaluate_model(model, val_gen, name)
    print(f"Evaluation complete. Metrics saved.")

if __name__ == "__main__":
    evaluate_saved_model()
