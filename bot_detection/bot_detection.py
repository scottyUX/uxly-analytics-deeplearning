import numpy as np

from bot_detection.bot_detection_data_handler import BotDetectionDataHandler
from bot_detection.bot_detection_model import BotDetectionModel
from bot_detection.detection_reporter import measure_detection_performance
from bot_detection.detection_reporter import report_detection_performance


class ConformalPredictor(object):
    def __init__(self):
        super(ConformalPredictor, self).__init__()
        self.conformal_threshold = None
        self.model = None

    def calibrate(self, model, calibration_samples, alpha=0.1):
        self.model = model
        n = len(calibration_samples)
        calibration_scores = model.predict(calibration_samples)
        qhat = np.quantile(calibration_scores, np.ceil((n+1)*(1-alpha))/n)
        self.conformal_threshold = qhat
        return self.conformal_threshold
    
    def conformal_predict(self, test_samples):
        if self.model is None:
            raise ValueError('Model is not calibrated')
        test_scores = self.model.predict(test_samples)
        predictions = test_scores > self.conformal_threshold
        return predictions.astype(int)
    

class BotDetection(object):
    def __init__(self):
        super(BotDetection, self).__init__()
        self.conformal_predictor = ConformalPredictor()
      
    def get_binary_predictions(self, test_x, threshold=0.5):
        test_scores = self.model.predict(test_x)
        predictions = test_scores > threshold
        return predictions.astype(int)
    
    def get_conformal_prediction(self, test_x, calibration_samples, alpha=0.1):
        self.conformal_predictor.calibrate(self.model, calibration_samples, alpha)
        return self.conformal_predictor.conformal_predict(test_x)

    def run(self):
        # Set hyperparameters
        num_calibration_samples = 1000
        alpha = 0.03
        binary_threshold = 0.5
        hyperparameters = (num_calibration_samples, alpha, binary_threshold)
        # Load data
        data_handler = BotDetectionDataHandler(num_calibration_samples)
        features_with_labels = data_handler.get_features_with_labels()
        train_x, train_y, cal_x, cal_y, test_x, test_y = features_with_labels
        # Prepare the model
        self.model = BotDetectionModel(n_features=train_x.shape[1])
        self.model.train(train_x, train_y)
        # Get binary and conformal predictions
        preds = self.get_binary_predictions(test_x, binary_threshold)
        conformal_preds = self.get_conformal_prediction(test_x, cal_x, alpha)
        # Measure detection performance
        scores = measure_detection_performance(test_y, preds)
        conformal_scores = measure_detection_performance(test_y, conformal_preds)
        # Report detection performance with initial hyperparameters
        hyperparameters += (self.conformal_predictor.conformal_threshold,)
        metrics_list = [scores, conformal_scores]
        report_detection_performance(metrics_list, hyperparameters)
        return
