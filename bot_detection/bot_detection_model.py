from sklearn.utils import class_weight
import tensorflow as tf
import numpy as np


class BotDetectionModel(object):
    def __init__(self, n_features):
        super(BotDetectionModel, self).__init__()
        model = tf.keras.Sequential()
        Dense = tf.keras.layers.Dense
        model.add(Dense(64, input_shape=(n_features,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(
            loss='binary_crossentropy',
            optimizer='adam', 
            metrics=['accuracy'],
            )
        self.__model = model

    def __get_class_weights(self, train_y):
        class_weights = class_weight.compute_class_weight(
            class_weight = 'balanced', 
            classes = np.unique(train_y),
            y = train_y.flatten(),
        )
        class_weights = dict(enumerate(class_weights))
        return class_weights
    
    def train(self, train_x, train_y):
        class_weights = self.__get_class_weights(train_y)
        self.__model.fit(
            train_x,
            train_y, 
            epochs=30, 
            batch_size=32, 
            class_weight=class_weights,
        )
        return self.__model    
    
    def predict(self, test_x):
        return self.__model.predict(test_x)