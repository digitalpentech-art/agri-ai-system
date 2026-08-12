import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data/plantvillage')
# Directory to save trained models
MODELS_DIR = os.path.join(BASE_DIR, 'ml/models')
# Directory to save evaluation results and training curves
RESULTS_DIR = os.path.join(BASE_DIR, 'ml/results')
# Directory for production model registration
PRODUCTION_DIR = os.path.join(MODELS_DIR, 'production')

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
SEED = 42

# Metadata paths
CLASSES_JSON = os.path.join(MODELS_DIR, 'classes.json')
BEST_MODEL_JSON = os.path.join(RESULTS_DIR, 'best_model.json')
MODEL_COMPARISON_CSV = os.path.join(RESULTS_DIR, 'model_comparison.csv')

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PRODUCTION_DIR, exist_ok=True)
