from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io, cv2
import sys
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

sys.stdout.reconfigure(encoding='utf-8')

class Tumor(BaseModel):
    name: str


class Tumors(BaseModel):
    tumors: List[Tumor]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

try:
    model = tf.keras.models.load_model('app/braintumor.h5')
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")
# Preprocessing function to handle image inputs
def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGB")
    original_image = np.array(image)
    image = image.resize((150, 150))
    img_array = np.array(image)
    img_array = img_array.reshape(1, 150, 150, 3)
    img_array.shape

    return img_array, original_image


memory_db = []

@app.get("/predict")
def get_tumor():
    Tumors = memory_db
    return Tumors

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

        image_data = await file.read()
        processed_image, original_image = preprocess_image(image_data)
        resultname = {0: 'glioma tumor', 1: 'meningioma tumor', 2: 'no tumor', 3: 'pituitary tumor'}

        prediction = model.predict(processed_image)

        prediction_class = np.argmax(prediction, axis=1)[0]
        result = resultname[prediction_class]

        memory_db.clear()
        memory_db.append(result)
        print(memory_db)

        return JSONResponse(content={"prediction": result})
