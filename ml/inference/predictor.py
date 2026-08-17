import json
import os
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
from ml.preprocessing import preprocess_image
from factory import Config

class ProductionPredictor:
    _instance = None
    _model = None
    _class_names = None
    _last_conv_layer_name = 'out_relu' # For MobileNetV2

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductionPredictor, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        if not os.path.exists(Config.MODEL_PATH):
            print(f"Model not found at {Config.MODEL_PATH}")
            return
        
        classes_path = os.path.join(os.path.dirname(Config.MODEL_PATH), 'classes.json')
        if not os.path.exists(classes_path):
            print("Classes file not found.")
            return
            
        with open(classes_path, 'r') as f:
            class_indices = json.load(f)
            self._class_names = {v: k for k, v in class_indices.items()}
        
        from ml.models.mobilenetv2 import get_model
        self._model = get_model(num_classes=len(self._class_names))
        
        try:
            self._model.load_weights(Config.MODEL_PATH)
            print("Weights loaded successfully.")
        except Exception as e:
            print(f"Error loading weights: {e}")
            self._model = None

    @property
    def model(self):
        return self._model

    def _make_gradcam_heatmap(self, img_array, pred_index=None):
        grad_model = tf.keras.models.Model(
            [self._model.inputs], [self._model.get_layer(self._last_conv_layer_name).output, self._model.output]
        )

        with tf.GradientTape() as tape:
            last_conv_layer_output, preds = grad_model(img_array)
            if pred_index is None:
                pred_index = tf.argmax(preds[0])
            class_channel = preds[:, pred_index]

        grads = tape.gradient(class_channel, last_conv_layer_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()

    def predict(self, image_path):
        if not self._model:
            return "Predictor not initialized", 0.0, ""
            
        img_array = preprocess_image(image_path)
        predictions = self._model.predict(img_array)
        predicted_index = int(tf.argmax(predictions, axis=1)[0])
        confidence = float(tf.reduce_max(predictions, axis=1)[0])
        
        # Grad-CAM
        heatmap = self._make_gradcam_heatmap(img_array, predicted_index)
        
        # Save Heatmap
        heatmap_filename = f"heatmap_{os.path.basename(image_path)}"
        heatmap_path = os.path.join(Config.UPLOAD_FOLDER, heatmap_filename)
        
        # Resize heatmap to original image size and apply colormap
        heatmap = np.uint8(255 * heatmap)
        jet = plt.get_cmap("jet")
        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]
        jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((224, 224))
        jet_heatmap.save(heatmap_path)
        
        return self._class_names[predicted_index], confidence, heatmap_filename

