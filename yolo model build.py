import os
import cv2
import yaml
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def load_and_preprocess_data(dataset_path):
    with open(dataset_path, 'r') as file:
        data = yaml.safe_load(file)

    images = []
    labels = []

    for entry in data:
        image = cv2.imread(entry['image_path'])
        if image is None:
            raise ValueError(f"Image not found at {entry['image_path']}")
        image = cv2.resize(image, (512, 512))  
        image = image / 255.0  


        label = [1.0] + [entry['x_center'], entry['y_center'], entry['width'], entry['height']]

        images.append(image)
        labels.append(label)

    return np.array(images), np.array(labels)

def build_yolo_model(input_shape=(512, 512, 3)): 
    model = keras.Sequential()

  
    model.add(layers.Conv2D(16, (3, 3), strides=(1, 1), padding='same', activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))


    model.add(layers.Flatten())
    model.add(layers.Dense(5, activation='sigmoid'))  

    return model


dataset_path = '/content/drive/MyDrive/project1/dataset.yaml/dataset.yaml'
images, labels = load_and_preprocess_data(dataset_path)


yolo_model = build_yolo_model()


yolo_model.compile(optimizer='adam', loss='mse',metrics=['accuracy'])  


yolo_model.fit(images, labels, epochs=10, batch_size=32)  


model_save_path = '/content/drive/MyDrive/project1/dataset.yaml/model.h5'
yolo_model.save(model_save_path)  
