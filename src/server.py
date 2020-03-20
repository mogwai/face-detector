from io import BytesIO

from fastapi import FastAPI, File, status
from PIL import Image

from src import faces

app = FastAPI()

@app.get('/')
async def meth():
    return "Hello"

@app.post("/detect")
async def detect_faces(file: bytes = File(...)):
    im = Image.open(BytesIO(file))
    return {'faces' : faces.detect_faces(im).tolist()}