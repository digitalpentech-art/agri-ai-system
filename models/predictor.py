import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import os
import json
import cv2
from factory import Config

class DiseasePredictor:
    def __init__(self, model_path, classes_path):
        try:
            with open(classes_path, 'r') as f:
                self.class_indices = json.load(f)
            self.classes = {v: k for k, v in self.class_indices.items()}
            num_classes = len(self.classes)
            
            # Manually construct architecture
            base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224, 224, 3))
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dropout(0.2)(x)
            predictions = Dense(num_classes, activation='softmax')(x)
            self.model = Model(inputs=base_model.input, outputs=predictions)
            
            # Load weights
            self.model.load_weights(model_path)
            
            # Identify the last convolutional layer (MobileNetV2 specific)
            self.last_conv_layer = 'out_relu'
        except Exception as e:
            print(f"Warning: Failed to load model: {e}")
            self.model = None

    def predict(self, image_path):
        if not self.model:
            raise RuntimeError("Model is not loaded.")
        img = Image.open(image_path).resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = self.model.predict(img_array)
        predicted_index = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions, axis=1)[0]
        
        heatmap_path = self.generate_heatmap(img_array, predicted_index, image_path)
        
        return self.classes[predicted_index], float(confidence), heatmap_path

    def generate_heatmap(self, img_array, class_index, original_path):
        grad_model = tf.keras.models.Model(
            [self.model.inputs], [self.model.get_layer(self.last_conv_layer).output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, class_index]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()

        # Resize and overlay
        img = cv2.imread(original_path)
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
        
        heatmap_filename = "heatmap_" + os.path.basename(original_path)
        heatmap_path = os.path.join(Config.UPLOAD_FOLDER, heatmap_filename)
        cv2.imwrite(heatmap_path, overlay)
        
        return heatmap_filename
