import pandas as pd
from bot_detection.bot_detection import BotDetection
from bot_detection.detection_reporter import get_rows


def conformal_prediction_evaluation(
    ):
    rows = get_rows()
    columns = ['Evaluation', 'Metric', 'Binary Prediction', 'Conformal Prediction']
    evaluation_table = pd.DataFrame(columns=columns)
    for i in range(100):
        bot_detection = BotDetection()
        metrics_list, hyperparameters = bot_detection.run(
            num_calibration_samples=1000,
            alpha=0.03,
            binary_threshold=0.5,
            print_results=False,
        )
        num_cal_samples, alpha, binary_threshold, qhat = hyperparameters
        scores, conformal_scores = metrics_list
        scores = ['N/A', 'N/A', binary_threshold] + list(scores)
        conformal_scores = [alpha, num_cal_samples, qhat] + list(conformal_scores)
        evaluation_index = f'Evaluation {i+1}'
        evaluation_index = [evaluation_index] * len(scores)
        df = pd.DataFrame(
            zip(evaluation_index, rows, scores, conformal_scores),
            columns=columns,
        )
        evaluation_table = pd.concat([evaluation_table, df], ignore_index=True)
        print(f'Evaluation {i+1} completed')
    evaluation_table.to_csv('data/conformal_prediction_evaluation.csv', index=False)
