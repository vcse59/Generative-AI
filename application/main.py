from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os


# Initialize FastAPI app
app = FastAPI(
    title="Image Classifier",
    description="Predicts label from an input image using a Keras model",
    version="1.0.0"
)

# Load the trained Keras model
model_path = os.path.join("model-training", "models", "model.h5")
model = tf.keras.models.load_model(model_path)

# Optionally, define class labels if available
class_labels = {'Cat': 0, 'Dog': 1}
inv_class_labels = {v: k for k, v in class_labels.items()}

def preprocess_image(image_bytes):
    """Preprocess uploaded image for model prediction"""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((150, 150))  # Update size as per your model input
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict label from uploaded image
    """
    contents = await file.read()
    img_array = preprocess_image(contents)
    preds = model.predict(img_array)
    predicted_class = int(preds[0] > 0.5)
    pred_idx = int(np.argmax(preds, axis=1)[0])
    pred_label = inv_class_labels[predicted_class]
    confidence = float(np.max(preds))
    return JSONResponse({
        "predicted_label": pred_label,
        "confidence": round(confidence, 4)
    })

@app.get("/")
def health_check():
    return {"status": "healthy", "model": "image_classifier_v1"}
