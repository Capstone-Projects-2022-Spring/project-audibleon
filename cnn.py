import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import tensorflow as tf

from tensorflow.keras.utils import to_categorical
from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , BatchNormalization, Input, Activation
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix ,classification_report
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score

trainFile = "sign_mnist_train.csv"
testFile = "sign_mnist_test.csv"

df = pd.read_csv(trainFile)
#  remove this comment
train = df.values[0:, 1:]
labels = df.values[0:, 0]
labels = to_categorical(labels)
sample = train[1]
plt.imshow(sample.reshape((28, 28)))
train = train/255
train = train.reshape((27455, 28, 28, 1))
plt.imshow(train[1].reshape((28, 28)))
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=(28, 28, 1), activation='relu', padding='same'))
model.add(MaxPool2D((2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'))
model.add(MaxPool2D(2, 2))
model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(25, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
h = model.fit(train, labels, validation_split=0.3, epochs=6, batch_size=64)
plt.plot(h.history['accuracy'])
plt.plot(h.history['val_accuracy'])
plt.title('Model accuracy')
plt.show()
plt.plot(h.history['loss'])
plt.plot(h.history['val_loss'])
plt.title('Model Loss')
plt.show()