import numpy as np
from sklearn.metrics import accuracy_score, f1_score

def calculate_metrics(y_true, y_pred, confidences):
    """
    Calculate required evaluation metrics.
    """
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    mean_conf = np.mean(confidences)
    gap = np.abs(mean_conf - acc)
    
    return {
        'accuracy': acc,
        'macro_f1': macro_f1,
        'mean_confidence': mean_conf,
        'confidence_accuracy_gap': gap
    }
