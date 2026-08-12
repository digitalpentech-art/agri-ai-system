import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import os
import json
from ml.config import MODELS_DIR, EPOCHS, LEARNING_RATE
from ml.dataset import get_data_generators

def train_and_save_model(model_name, model_fn):
    print(f"Training {model_name}...")
    train_gen, val_gen = get_data_generators()
    num_classes = len(train_gen.class_indices)
    
    model = model_fn(num_classes)
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS
    )
    
    save_path = os.path.join(MODELS_DIR, f"{model_name}.h5")
    model.save(save_path)
    
    # Save training history
    history_path = os.path.join(MODELS_DIR, f"{model_name}_history.json")
    with open(history_path, 'w') as f:
        json.dump(history.history, f)
        
    print(f"{model_name} saved to {save_path}")
    return model, val_gen
