import numpy as np
import tensorflow as tf
from src.digit_data import getData

class Classifier:
    def fit(self, fromFile=False):
        if fromFile:
            model = tf.keras.models.load_model("src/model.tf")
            self.model = model
            return

        X, y, X_test, y_test = getData()

        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(16, (3,3), activation="relu", input_shape=(28,28,1)),
            tf.keras.layers.MaxPool2D(2,2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax")
        ])

        model.compile(optimizer="adam", loss="CategoricalCrossentropy", metrics=["accuracy"])
        model.fit(X, y, epochs=10)

        res = model.evaluate(X_test, y_test, verbose=2)
        print(res)
        model.save("src/model.tf")

        #model.summary()

        self.model = model

    def predict(self, img):
        preprocessed_image = self.preprocess_image(img)
        #TODO: check that array has right dims 
        cs = self.model.predict([preprocessed_image])
        c = cs[0]
        digit = c.argmax()
        print(f"predicted {digit}")
        return digit

    def preprocess_image(self, image):
        #one color channel
        image_with_channels = image[...,np.newaxis]
        image_resized = tf.keras.preprocessing.image.smart_resize(image_with_channels, (28,28))

        #add batch size
        return image_resized[np.newaxis,...]
