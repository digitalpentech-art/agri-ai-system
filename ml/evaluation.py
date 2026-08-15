import numpy as np
import json
import os
import matplotlib.pyplot as plt
import csv
from ml.metrics import calculate_metrics, get_classification_report, get_confusion_matrix, get_per_class_metrics
from ml.config import RESULTS_DIR, MODEL_COMPARISON_CSV, BEST_MODEL_JSON

def evaluate_model(model, val_generator, model_name):
    print(f"Evaluating {model_name}...")
    # Get true labels and predictions
    val_generator.reset()
    y_true = val_generator.classes
    y_pred_probs = model.predict(val_generator)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Calculate metrics
    metrics = calculate_metrics(y_true, y_pred)
    
    # Save metrics
    model_results_dir = os.path.join(RESULTS_DIR, model_name)
    os.makedirs(model_results_dir, exist_ok=True)
    
    with open(os.path.join(model_results_dir, 'metrics.json'), 'w') as f:
        json.dump(metrics, f)
        
    # Classification Report
    report = get_classification_report(y_true, y_pred, target_names=list(val_generator.class_indices.keys()))
    with open(os.path.join(model_results_dir, 'classification_report.json'), 'w') as f:
        json.dump(report, f)
        
    # Per-Class Numerical Metrics (TP, TN, FP, FN)
    cm = get_confusion_matrix(y_true, y_pred)
    per_class_metrics = get_per_class_metrics(cm)
    with open(os.path.join(model_results_dir, 'per_class_metrics.json'), 'w') as f:
        json.dump(per_class_metrics, f)
        
    # Raw Confusion Matrix
    with open(os.path.join(model_results_dir, 'confusion_matrix.json'), 'w') as f:
        json.dump(cm.tolist(), f)
        
    # Confusion Matrix Plot
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.colorbar()
    plt.savefig(os.path.join(model_results_dir, 'confusion_matrix.png'))
    plt.close()
    
    print(f"Evaluation complete for {model_name}. Metrics: {metrics}")
    print(f"Numerical metrics saved to {os.path.join(model_results_dir, 'per_class_metrics.json')}")
    print(f"Raw confusion matrix saved to {os.path.join(model_results_dir, 'confusion_matrix.json')}")
    return metrics

def compare_models(results_list):
    """
    Compares models and selects the best based on Macro F1-score.
    results_list: list of dicts {'model_name': ..., 'metrics': ...}
    """
    with open(MODEL_COMPARISON_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Model', 'Accuracy', 'Precision', 'Recall', 'F1_Score'])
        
        best_model = None
        best_f1 = -1
        
        for res in results_list:
            metrics = res['metrics']
            writer.writerow([res['model_name'], metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['f1_score']])
            
            if metrics['f1_score'] > best_f1:
                best_f1 = metrics['f1_score']
                best_model = res
        
        with open(BEST_MODEL_JSON, 'w') as f:
            json.dump(best_model, f)
            
        print(f"Best model selected: {best_model['model_name']} with F1: {best_f1}")
        return best_model
