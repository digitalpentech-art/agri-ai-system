import sys
import os
import shutil
from ml.models.mobilenetv2 import get_model as get_mobilenetv2
from ml.training.trainer import train_and_save_model
from ml.evaluation import evaluate_model
from ml.config import RESULTS_DIR

def run_pipeline():
    # 1. Mount Drive if in Colab
    if 'google.colab' in sys.modules:
        from google.colab import drive
        drive.mount('/content/drive')
        drive_results_dir = '/content/drive/MyDrive/agri_ai_results/'
        os.makedirs(drive_results_dir, exist_ok=True)
    else:
        print("Not running in Colab, skipping drive mount.")
        drive_results_dir = RESULTS_DIR
        os.makedirs(drive_results_dir, exist_ok=True)

    print("Initializing MobileNetV2 Training...")
    
    # Only training MobileNetV2
    name = 'mobilenetv2'
    model_fn = get_mobilenetv2
    
    # Train and Evaluate
    model, val_gen = train_and_save_model(name, model_fn)
    metrics = evaluate_model(model, val_gen, name)
    
    # 2. Persist results to Drive immediately
    source_model_results = os.path.join(RESULTS_DIR, name)
    dest_model_results = os.path.join(drive_results_dir, name)
    
    if os.path.exists(source_model_results):
        shutil.copytree(source_model_results, dest_model_results, dirs_exist_ok=True)
        print(f"Results for {name} saved to Drive.")
    
    print("Pipeline complete. Results safely on Drive.")

if __name__ == "__main__":
    run_pipeline()
