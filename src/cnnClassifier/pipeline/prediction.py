import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
from cnnClassifier.config.configuration import ConfigurationManager


class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename
        self.config_manager = ConfigurationManager()
        self.prediction_config = self.config_manager.get_prediction_config()

    def predict(self):
        # load model using path from config
        model = load_model(self.prediction_config.model_path)

        # load and preprocess image using size from params
        test_image = image.load_img(
            self.filename, 
            target_size=self.prediction_config.params_image_size[:-1]
        )
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        # scale image if necessary (standard practice for VGG16)
        test_image = test_image / 255.0

        result = np.argmax(model.predict(test_image), axis=1)
        print(result)

        if result[0] == 1:
            prediction = 'Tumor'
            return [{"image": prediction}]
        else:
            prediction = 'Normal'
            return [{"image": prediction}]
