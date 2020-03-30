from io import BytesIO

from fastapi import FastAPI, File, status, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw

from .faces import detect_faces

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

@app.get('/')
async def meth():
    return "Hello"

@app.post("/detect")
async def faces_bbox(file: bytes = File(...)):
    im = Image.open(BytesIO(file))
    faces = detect_faces(im)
    return {'faces' : faces}

@app.post('/detect/preview')
async def detect_prevew(file: bytes = File(...)):
    im = Image.open(BytesIO(file))
    faces = detect_faces(im)
    drawer = ImageDraw.Draw(im)
    for i in faces:
        drawer.rectangle(i, fill=None, outline='blue', width=4)
    out = BytesIO()
    im.save(out, format='JPEG')
    return Response(content=out.getvalue(), media_type="image/jpeg")
    
@app.get('/meta')
async def meta():
    return {}