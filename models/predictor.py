import os
import json
from factory import Config

class DiseasePredictor:
    def __init__(self, model_path, classes_path):
        self.model_path = model_path
        self.classes_path = classes_path
        self.model = None
        self.tf = None
        self.np = None
        self.Image = None
        self.cv2 = None
        self.classes = {}

    def _load_model(self):
        """Lazy load the model and dependencies."""
        if self.model is not None:
            return

        try:
            import tensorflow as tf
            from tensorflow.keras.applications import MobileNetV2
            from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
            from tensorflow.keras.models import Model
            import numpy as np
            from PIL import Image
            import cv2
            
            self.np = np
            self.Image = Image
            self.cv2 = cv2
            self.tf = tf
            
            with open(self.classes_path, 'r') as f:
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
            self.model.load_weights(self.model_path)
            
            # Identify the last convolutional layer (MobileNetV2 specific)
            self.last_conv_layer = 'out_relu'
        except Exception as e:
            print(f"Warning: Failed to load model: {e}")
            self.model = False # Mark as failed to avoid retries
            
    def predict(self, image_path):
        self._load_model()
        if not self.model:
            return "Error: Predictor not loaded", 0.0, ""
        
        img = self.Image.open(image_path).resize((224, 224))
        img_array = self.np.array(img) / 255.0
        img_array = self.np.expand_dims(img_array, axis=0)
        
        predictions = self.model.predict(img_array)
        predicted_index = self.np.argmax(predictions, axis=1)[0]
        confidence = self.np.max(predictions, axis=1)[0]
        
        heatmap_path = self.generate_heatmap(img_array, predicted_index, image_path)
        
        return self.classes[predicted_index], float(confidence), heatmap_path

    def generate_heatmap(self, img_array, class_index, original_path):
        self._load_model()
        if not self.model:
            return ""
        
        grad_model = self.tf.keras.models.Model(
            [self.model.inputs], [self.model.get_layer(self.last_conv_layer).output, self.model.output]
        )

        with self.tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, class_index]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = self.tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., self.tf.newaxis]
        heatmap = self.tf.squeeze(heatmap)
        heatmap = self.tf.maximum(heatmap, 0) / self.tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()

        # Resize and overlay
        img = self.cv2.imread(original_path)
        heatmap = self.cv2.resize(heatmap, (img.shape[1], img.shape[0]))
        heatmap = self.np.uint8(255 * heatmap)
        heatmap = self.cv2.applyColorMap(heatmap, self.cv2.COLORMAP_JET)
        overlay = self.cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
        
        heatmap_filename = "heatmap_" + os.path.basename(original_path)
        heatmap_path = os.path.join(Config.UPLOAD_FOLDER, heatmap_filename)
        self.cv2.imwrite(heatmap_path, overlay)
        
        return heatmap_filename
