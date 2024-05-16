import numpy as np


class ConformalPredictor(object):
    def __init__(self):
        super(ConformalPredictor, self).__init__()
        self.conformal_threshold = None
        self.model = None

    def calibrate(self, model, calibration_samples, alpha=0.1):
        n = len(calibration_samples)
        calibration_scores = model.predict(calibration_samples)
        qhat = np.quantile(calibration_scores, np.ceil((n+1)*(1-alpha))/n)
        self.conformal_threshold = qhat
        return self.conformal_threshold
    
    def conformal_predict(self, test_samples):
        test_scores = self.model.predict(test_samples)
        predictions = test_scores > self.conformal_threshold
        return predictions.astype(int)
    