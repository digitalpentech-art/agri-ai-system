# Agri-AI-System

An agricultural disease detection web application built with Flask, TensorFlow, and Keras.

## Features
- AI-based disease prediction for plant images.
- Grad-CAM heatmaps for visual explainability.
- User management and authentication.

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`

## Evaluation (Google Colab)
To evaluate the pre-trained `mobilenetv2` model in a Google Colab notebook, use the following commands in a single cell:

```bash
# Clone the repository
git clone https://github.com/digitalpentech-art/agri-ai-system.git
cd agri-ai-system

# Install dependencies
pip install tensorflow numpy matplotlib scikit-learn --quiet

# Run the evaluation script
PYTHONPATH=. python3 scripts/evaluate_mobilenetv2.py
```
