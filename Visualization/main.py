import keras
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras import models  
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation, Dropout
import visualkeras
from PIL import ImageFont

model = Sequential()
model.add(Conv2D(6, kernel_size=5, activation='relu', input_shape=(256, 256, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(16, kernel_size=5, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(120))
model.add(Dense(84))
model.add(Dense(3))  # Assuming 3 output classes

# Generate the visualization
model_image = visualkeras.layered_view(model, spacing=25, legend=True, font=ImageFont.truetype("arial.ttf", size=32))

# Save the visualization to a file
model_image.save('model_visualization.png')