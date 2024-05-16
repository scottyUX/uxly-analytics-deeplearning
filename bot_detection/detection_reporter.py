from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, auc
from sklearn.metrics import accuracy_score
from math import sqrt


__labels = [
    'Accuracy',
    'Balanced Accuracy',
    'Precision',
    'Recall',
    'F1 Score',
    'MCC',
    'Cohen\'s Kappa',
    'G-Mean',
    'AUC-ROC',
    'AUC-PR',
    'True negatives',
    'False positives',
    'False negatives',
    'True positives',
    'False Positive Rate',
    'False Negative Rate',
]

def __calculate_mcc(tp, tn, fp, fn):
    numerator = tp * tn - fp * fn
    denominator = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = numerator / denominator if denominator else 0
    return mcc

def __calculate_cohen_kappa(tn, fp, fn, tp):
    total = tp + fp + fn + tn
    p0 = (tp + tn) / total
    pe = ((tp + fp) * (tp + fn) + (tn + fp) * (tn + fn)) / (total * total)
    kappa = (p0 - pe) / (1 - pe)
    return kappa

def __calculate_scores(tn, fp, fn, tp):
    balanced_accuracy = (tp / (tp + fn) + tn / (tn + fp)) / 2
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * (precision * recall) / (precision + recall)
    mcc = __calculate_mcc(tp, tn, fp, fn)
    cohen_kappa = __calculate_cohen_kappa(tn, fp, fn, tp)
    g_mean = sqrt((tp / (tp + fn)) * (tn / (tn + fp)))
    return balanced_accuracy, precision, recall, f1_score, mcc, \
        cohen_kappa, g_mean

def measure_detection_performance(ground_truth, predictions):
    accuracy = accuracy_score(ground_truth, predictions)
    tn, fp, fn, tp = confusion_matrix(ground_truth, predictions).ravel()
    fpr, tpr, _ = roc_curve(ground_truth, predictions)
    auc_pr = auc(fpr, tpr)
    fpr = fp / (fp + tn) if (fp + tn) else 0
    fnr = fn / (fn + tp) if (fn + tp) else 0
    auc_roc = roc_auc_score(ground_truth, predictions)
    scores =  __calculate_scores(tn, fp, fn, tp)
    return (accuracy, *scores, auc_pr, auc_roc, tn, fp, fn, tp, fpr, fnr)
    
def print_hyperparameters(hyperparameters):
    num_calibration_samples, alpha, binary_threshold, qhat = hyperparameters
    print(f'Conformal alpha,N/A,{alpha:.4f}')
    print(f'Calibration Samples,N/A,{num_calibration_samples}')
    print(f'Binary threshold,{binary_threshold:.4f},{qhat:.4f}')
    return
    
def report_detection_performance(metrics_list, hyperparameters=None):
    if hyperparameters:
        print_hyperparameters(hyperparameters)
    if not isinstance(metrics_list[0], tuple):
        metrics_list = [metrics_list]   
    global __labels
    int_labels = __labels[10:14]
    for label, values in zip(__labels, zip(*metrics_list)):
        line = f'{label},'
        for value in values:
            line += f'{value:.0f},' if label in int_labels else f'{value:.4f},'
        print(line[:-1])
    return

def get_rows():
    global __labels
    hyperparameters = ['Conformal alpha', 'Calibration Samples', 'Binary threshold']
    return hyperparameters + __labels