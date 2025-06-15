from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)  # normalize
val_datagen = ImageDataGenerator(rescale=1./255)

import os

train_generator = train_datagen.flow_from_directory(
    os.path.join('model-training',  'output', 'train'),
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',  # or 'categorical' for >2 classes
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    os.path.join('model-training',  'output', 'val'),
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    shuffle=True
)

class_labels = train_generator.class_indices
print(class_labels)
inv_class_labels = {v: k for k, v in class_labels.items()}

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    MaxPooling2D(2,2),
    
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # or softmax for multiple classes
])

model.compile(
    loss='binary_crossentropy',  # or 'categorical_crossentropy'
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.legend()
plt.title('Accuracy over Epochs')
plt.show()

# Save model
model.save(os.path.join('model-training', 'models', 'model.h5'))


# Example of using the trained model to predict a single image

# Load later
from tensorflow.keras.models import load_model
model = load_model(os.path.join('model-training', 'models', 'model.h5'))

from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load and preprocess single image
img = image.load_img(os.path.join('model-training', 'test_image.jpg'), target_size=(150, 150))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
pred = model.predict(img_array)

# For binary classification
predicted_class = int(pred[0] > 0.5)
print("Predicted Label:", inv_class_labels[predicted_class])
