# Import libraries
import tensorflow as tf
from tensorflow import keras
import pathlib
import numpy as np
import matplotlib.pyplot as plt

# Class names for the 10 different categories identifying whether a driver is impaired or not
class_names = ['Calling_left', 'Calling_right', 'Drinking', 'Head_turned', 'Infotainment',
               'Reaching', 'Safe_driver', 'Scratching', 'Texting_left', 'Texting_right']

num_classes = 10

# Image size used throughout the process
img_height, img_width = 480, 640

# Load the model
model = tf.keras.models.load_model('model.h5')

# Load the image
img = keras.preprocessing.image.load_img(
    "imgs/testing/test/img_65.jpg", target_size=(img_height, img_width)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

# Predict the image
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

# Print the results
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)