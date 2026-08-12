import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input
from tensorflow.keras.models import Model
from ml.config import IMG_SIZE

def get_model(num_classes):
    inputs = Input(shape=(*IMG_SIZE, 3))
    
    x = Flatten()(inputs)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    return Model(inputs=inputs, outputs=outputs)
