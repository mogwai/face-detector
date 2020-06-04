import base64
from io import BytesIO
from typing import List

from fastapi import FastAPI, File, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

from .faces import detect_faces

with open(".version") as f:
    VERSION = f.read()

app = FastAPI(version=VERSION, title="Face Detection", docs_url="/", redoc_url=None)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load font to use to show percentages
with open("./font.ttf", "rb") as f:
    FONT = ImageFont.truetype(BytesIO(f.read()), 15)


@app.get("/")
def hello(res: Response):
    """A route for health checking"""
    return Response(status_code=status.HTTP_204_NO_CONTENT)


class BBoxResponse(BaseModel):
    faces: List[List[int]]
    confidence: List[float]


@app.post("/detect", response_model=BBoxResponse)
async def faces_bbox(file: UploadFile = File(...)):
    """Gets the bounding boxes of faces in a given image"""
    file = await file.read()
    im = Image.open(BytesIO(file))
    faces, conf = detect_faces(im)
    return {"faces": faces.tolist(), "confidence": conf.tolist()}


def _detect_preview(file: bytes):
    im = Image.open(BytesIO(file))
    drawer = ImageDraw.Draw(im)
    faces, confidence = detect_faces(im)
    for i, c in zip(faces, confidence):
        drawer.rectangle(i, fill=None, outline="blue", width=4)
        pos = i[:2]
        pos[0] += 5
        drawer.text(pos, str(c * 100)[:4], (0, 0, 255), FONT)
    out = BytesIO()
    im.save(out, format="JPEG")
    return out, faces, confidence


@app.post("/detect/preview")
async def detect_prevew(file: UploadFile = File(...)):
    """Returns a jpeg of the visualised results"""
    data = await file.read()
    out, _, __ = _detect_preview(data)
    return Response(content=out.getvalue(), media_type="image/jpeg")


class Base64BBoxResponse(BBoxResponse):
    image: str


@app.post("/detect/preview/base64", response_model=Base64BBoxResponse)
async def detect_base64_preview(file: UploadFile = File(...)):
    """Returns the base64 encoded image with the results"""
    file = await file.read()
    out, faces, confidence = _detect_preview(file)
    res = {
        "faces": faces.tolist(),
        "confidence": confidence.tolist(),
        "image": base64.encodebytes(out.getvalue()),
    }
    return res


@app.get("/meta")
async def meta():
    """ Meta information about the models being exposed such as classes"""
    return {}
