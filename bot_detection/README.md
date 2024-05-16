# Bot Detection

This project contains a bot detection system that uses a conformal predictor to make predictions. The main implementation can be found in the `bot_detection\bot_detection.py` file.

## Classes
#### ConformalPredictor
This class is used to calibrate a model and make predictions. It has the following methods:

`__init__`: Initializes the ConformalPredictor object.
`calibrate`: Calibrates the model using the provided calibration samples and alpha value.
`conformal_predict`: Makes predictions on the provided test samples.


#### BotDetection
This class is used to run the bot detection system. It has the following methods:

`__init__`: Initializes the BotDetection object.
`get_binary_predictions`: Returns binary predictions for the provided test samples and threshold.
`get_conformal_prediction`: Returns conformal predictions for the provided test samples, calibration samples, and alpha value.
`run`: Runs the bot detection system. It loads the data, prepares the model, gets binary and conformal predictions, measures detection performance, and reports detection performance.

## Usage
To use the bot detection system, create a BotDetection object and call the run method. The run method takes the following parameters:

`num_calibration_samples`: The number of calibration samples to use (default is 1000).
`alpha`: The alpha value to use for calibration (default is 0.03).
`binary_threshold`: The threshold to use for binary predictions (default is 0.5).
