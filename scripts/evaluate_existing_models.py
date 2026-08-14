import os
import tensorflow as tf
from ml.dataset import get_data_generators
from ml.evaluation import evaluate_model
from ml.config import MODELS_DIR

def run_evaluation():
    # 1. Get the validation generator
    _, val_gen = get_data_generators()

    # 2. Define the models to evaluate
    models_to_evaluate = ['cnn', 'dnn', 'mobilenetv2']

    for model_name in models_to_evaluate:
        model_path = os.path.join(MODELS_DIR, f"{model_name}.h5")
        
        if os.path.exists(model_path):
            print(f"Loading {model_name} from {model_path}...")
            model = tf.keras.models.load_model(model_path)
            
            # 3. This saves per_class_metrics.json in ml/results/{model_name}/
            evaluate_model(model, val_gen, model_name)
        else:
            print(f"Model file not found: {model_path}")

    print("Evaluation complete. Numerical metrics are saved in ml/results/{model}/per_class_metrics.json")

if __name__ == "__main__":
    run_evaluation()
