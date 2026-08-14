from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import numpy as np

def calculate_metrics(y_true, y_pred):
    """
    Calculates multiclass evaluation metrics using macro averaging.
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

def get_classification_report(y_true, y_pred, target_names):
    return classification_report(y_true, y_pred, target_names=target_names, output_dict=True)

def get_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)

def get_per_class_metrics(cm):
    """
    Calculates TP, TN, FP, FN for each class from a confusion matrix.
    cm: confusion matrix (N x N)
    returns: dict of dicts {class_idx: {'TP': ..., 'TN': ..., 'FP': ..., 'FN': ...}}
    """
    per_class_metrics = {}
    total_sum = np.sum(cm)
    for i in range(cm.shape[0]):
        tp = cm[i, i]
        fn = np.sum(cm[i, :]) - tp
        fp = np.sum(cm[:, i]) - tp
        tn = total_sum - (tp + fp + fn)
        
        per_class_metrics[i] = {
            'TP': tp,
            'TN': tn,
            'FP': fp,
            'FN': fn
        }
    return per_class_metrics
