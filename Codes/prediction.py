# Authors: Julien Choukroun, Jessica Gourdon, Luc Sagnes

# This code is used to predict the steering angle.
# When the car is running, we take frames thanks to the camera.
# Then we put frames into the neural network to predict the steering angle.

#!/usr/bin/python3

import sys
sys.path.append(r'/opt/ezblock')

from ezblock import __reset_mcu__
__reset_mcu__()

import numpy as np
import random
from vilib import Vilib
import picarmini
from picarmini import forward
from picarmini import set_dir_servo_angle
from ezblock import WiFi
import cv2
import time

WiFi().write('CN', 'MIA06', 'MaisonIA06!2020') # We set the MIA Wifi
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import model_from_json

# load json and create model
json_file = open("model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_weights.h5")


camera = cv2.VideoCapture(Vilib.video_source)

camera.set(3,320)
camera.set(4,240)
 
camera.set(cv2.CAP_PROP_BUFFERSIZE,1)
cv2.setUseOptimized(True)

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]  # remove top half of the image, as it is not relavant for lane following
    image = image / 255 # normalizing the image
    return image


def forever():
    _, img = camera.read()
    
    img = img_preprocess(img) # Preprocess the image
    img = np.reshape(img,(-1,120,320,3)) # Reshape the image to put it in the neural network

    t1 = time.time()
    prediction = loaded_model.predict(img) # Use the neural network to predict the steering angle
    t2 = time.time()
    temps = t2-t1
    file = open("times.txt", "a")
    file.write(str(temps)) # Write the execution time for a prediction
    file.write("\n")
    file.flush()
    
    if (prediction[0][0]*45 > 35): # We cut the steering angle above 35
    	angle = 30
    elif (prediction[0][0]*45 < -35): # We cut the steering angle bellow -35
    	angle = -30
    else:
    	angle = prediction[0][0]*45 # We de-normalize the steering angle (multiply by 45)

    forward(1) # We set the speed at the minimum
    set_dir_servo_angle(angle+10) # We set the steering angle with the predicted angle

if __name__ == "__main__":
    while True: # While the car is running
        forever()
