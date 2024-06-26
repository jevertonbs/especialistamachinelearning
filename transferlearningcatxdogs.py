# -*- coding: utf-8 -*-
"""TransferLearningCatxDogs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1q5L0BAW_AGB0FP0SgJZ1lMA5gG_QDPlL
"""

!git clone https://github.com/cunhamaicon/catsxdogs

!pip install keras-preprocessing

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
#from keras.preprocessing import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import Dropout

model=MobileNet(weights='imagenet',include_top=False)

x=model.output
x=GlobalAveragePooling2D()(x)

x=Dense(50,activation='relu')(x)
preds=Dense(1,activation='sigmoid')(x)
model=Model(inputs=model.input,outputs=preds)

for i,layer in enumerate(model.layers):
  print(i,layer.name)

for layer in model.layers[:88]:
  layer.trainable=False
for layer in model.layers[88:]:
  layer.trainable=True

batch_size = 32

train_datagen= ImageDataGenerator(rescale = 1./255,
                                  shear_range = 0.4,
                                  zoom_range = 0.4,
                                  height_shift_range = 0.3,
                                  width_shift_range = 0.3,
                                  rotation_range = 50,
                                  horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('catsxdogs/training_set',
                                                target_size = (224,224),
                                                batch_size=batch_size,
                                                class_mode='binary')
test_set = test_datagen.flow_from_directory('catsxdogs/test_set',
                                                target_size = (224,224),
                                                batch_size=batch_size,
                                                class_mode='binary')

model.compile(optimizer=Adam(learning_rate = 0.0001), loss='binary_crossentropy',metrics=['accuracy'])

history = model.fit_generator(generator=training_set,
                              steps_per_epoch=8000/batch_size,
                              epochs = 10,
                              validation_data = test_set,
                              validation_steps = 2000/batch_size)

model.save('catsxdogs_mobilenet.h5')
from google.colab import files
files.download('catsxdogs_mobilenet.h5')

from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

ls catsxdogs/single_prediction

test_image = load_img('catsxdogs/single_prediction/floyd4.jpg', target_size=(224, 224))

test_image = img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
test_image = test_image/255

result = model.predict(test_image)

if result[0][0] > 0.5:
  prediction = 'Cachorro'
else:
  prediction = 'Gato'
print(prediction)