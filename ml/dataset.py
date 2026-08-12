import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os
from ml.config import DATA_DIR, IMG_SIZE, BATCH_SIZE, SEED, CLASSES_JSON

def get_data_generators():
    """
    Creates train and validation data generators with reproducible splits.
    """
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        seed=SEED,
        shuffle=True
    )

    validation_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        seed=SEED,
        shuffle=False # Important for evaluation/confusion matrix
    )

    # Save classes
    os.makedirs(os.path.dirname(CLASSES_JSON), exist_ok=True)
    with open(CLASSES_JSON, 'w') as f:
        json.dump(train_generator.class_indices, f)
        
    return train_generator, validation_generator
