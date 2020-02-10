import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from keras.models import load_model
import os
import pdb

def train(epochs):
    train_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    test_datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    batch_size = 32
    target_size = (28,28)

    train_generator = train_datagen.flow_from_directory(
        "train/",
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        color_mode="grayscale"
    )
    validation_generator = test_datagen.flow_from_directory(
        "test/",
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        color_mode="grayscale"

    )
    model = Sequential() 
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1))) 
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))  
    model.add(Dropout(0.25))  
    model.add(Flatten())  
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
    model.load_weights("with_other.h5")
    history = model.fit_generator(train_generator, epochs=epochs, validation_data=validation_generator, verbose=1)
    model.save_weights("with_other.h5")
    print(model.summary())
    return  history.history

def make_prediction(filepath):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
    model.load_weights("with_other.h5")
    img = image.load_img(filepath, target_size=(28, 28, 1), color_mode="grayscale")
    img = image.img_to_array(img)
    img /= 255
    prediction = model.predict_classes(np.array([img]))
    return prediction[0]

def results():
    test_img = []
    test_dir = []
    t_d = os.listdir(os.path.join("test", "pneumonia"))
    _sum=0
    for i in t_d:
        if make_prediction(os.path.join("test", "pneumonia", i))==2:
            _sum+=1
    print(_sum/len(t_d))
    t_d = os.listdir(os.path.join("test", "other"))
    _sum=0
    for i in t_d:
        if make_prediction(os.path.join("test", "other", i))==1:
            _sum+=1
    print(_sum/len(t_d))
    t_d = os.listdir(os.path.join("test", "normal"))
    _sum=0
    for i in t_d:
        if make_prediction(os.path.join("test", "normal", i))==0:
            _sum+=1
    print(_sum/len(t_d))

if __name__ == "__main__":
    print(train(5))
    print(make_prediction(os.path.join("train", "other", "264413683_190662.jpg")),
          make_prediction(os.path.join("train", "normal", "IM-0115-0001.jpeg")),
          make_prediction(os.path.join("train", "pneumonia", "person1164_virus_1958.jpeg")))
   


