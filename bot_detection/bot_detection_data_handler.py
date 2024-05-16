from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

import sys
sys.path.append('../')
from utils.costum_keys import CustomKeys as ck


class BotDetectionDataHandler(object):
    def __init__(
            self, 
            num_calibration_samples=1000,
            num_folds=4,
            data_path='data/bot_detection_dataset.csv',
        ):
        super(BotDetectionDataHandler, self).__init__()
        self.num_folds = num_folds
        self.data_path = data_path
        self.num_calibration_samples = num_calibration_samples

    def load_data(self):
        df = pd.read_csv(self.data_path)
        df = df.drop(columns=[
            ck.ADDRESS, 
            ck.ERC20_MOST_REC_TOKEN_TYPE, 
            ck.ERC20_MOST_SENT_TOKEN_TYPE,
            ck.DATA_SOURCE,
            ck.LABEL_SOURCE,
            ]).astype(np.float64)
        df = df.dropna()
        self.negatives = df[df[ck.FLAG] == ck.NEGATIVE_FLAG]
        self.kaggle_labeled_bots = df[df[ck.FLAG] == ck.KAGGLE_LABELED_BOT_FLAG]
        self.mev_bots = df[df[ck.FLAG] == ck.MEV_BOT_FLAG]
        self.spams = df[df[ck.FLAG] == ck.SPAM_FLAG]
        self.positives = self.kaggle_labeled_bots.copy()
        return self.negatives, self.positives

    def separate_calibration_samples(self):
        num_samples = self.num_calibration_samples
        self.negatives = self.negatives.sample(frac=1)
        self.negatives = self.negatives.iloc[:-num_samples] 
        self.calibration_samples = self.negatives.iloc[-num_samples:]
        return self.calibration_samples

    def prepare_folds(self):
        self.negatives = self.negatives.sample(frac=1)
        self.positives = self.positives.sample(frac=1)
        positive_folds = np.array_split(self.positives.values, self.num_folds)
        negative_folds = np.array_split(self.negatives.values, self.num_folds)
        self.folds = []
        for i in range(self.num_folds):
            fold = np.concatenate([positive_folds[i], negative_folds[i]])
            np.random.shuffle(fold)
            self.folds.append(fold)
        return self.folds

    def split_data(self):
        cal_samples = self.separate_calibration_samples()
        folds = self.prepare_folds()
        test_data = np.copy(folds[0])
        train_data = np.concatenate(folds[1:])
        return train_data, cal_samples, test_data
     
    def scale_features(self, train_x, cal_x, test_x):
        scaler = StandardScaler()
        train_x_scaled = scaler.fit_transform(train_x)
        cal_x_scaled = scaler.transform(cal_x)
        test_x_scaled = scaler.transform(test_x)   
        return train_x_scaled, cal_x_scaled, test_x_scaled
    
    def get_features_with_labels(self):
        self.load_data()
        train_data, cal_samples, test_data = self.split_data()
        train_x, train_y = train_data[:, 1:], train_data[:, 0]
        cal_x, cal_y = cal_samples.values[:, 1:], cal_samples.values[:, 0]
        test_x, test_y = test_data[:, 1:], test_data[:, 0]
        train_x, cal_x, test_x = self.scale_features(train_x, cal_x, test_x)
        return train_x, train_y, cal_x, cal_y, test_x, test_y
