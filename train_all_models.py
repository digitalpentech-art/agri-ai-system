import sys
import os

# Add agri-ai-system directory to path
sys.path.append(os.path.join(os.getcwd(), 'agri-ai-system'))

from ml.models.cnn import get_model as get_cnn
from ml.models.dnn import get_model as get_dnn
from ml.models.mobilenetv2 import get_model as get_mobilenetv2
from ml.training.trainer import train_and_save_model
from ml.evaluation import evaluate_model, compare_models

def run_pipeline():
    print("Initializing Training Pipeline...")
    
    models_to_train = [
        ('cnn', get_cnn),
        ('dnn', get_dnn),
        ('mobilenetv2', get_mobilenetv2)
    ]
    
    results = []
    
    for name, model_fn in models_to_train:
        model, val_gen = train_and_save_model(name, model_fn)
        metrics = evaluate_model(model, val_gen, name)
        results.append({'model_name': name, 'metrics': metrics})
        
    compare_models(results)
    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
