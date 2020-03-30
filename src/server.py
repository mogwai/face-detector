from io import BytesIO

from fastapi import FastAPI, File, status, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw, ImageFont
import base64
from .faces import detect_faces

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


with open('./font.ttf','rb') as f:
    FONT = ImageFont.truetype(BytesIO(f.read()), 15)

@app.get('/')
def hello(res: Response):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.post("/detect")
async def faces_bbox(file: bytes = File(...)):
    im = Image.open(BytesIO(file))
    faces, conf = detect_faces(im)
    return {'faces' : faces.tolist(), 'confidence': conf.tolist()}

def _detect_preview(file):
    im = Image.open(BytesIO(file))
    drawer = ImageDraw.Draw(im)
    faces, confidence = detect_faces(im)
    for i, c in zip(faces,confidence):
        drawer.rectangle(i, fill=None, outline='blue', width=4)
        pos = i[:2]
        pos[0]+=5
        drawer.text(pos, str(c*100)[:4], (0,0,255), FONT)
    out = BytesIO()
    im.save(out, format='JPEG')
    return out, faces, confidence

@app.post('/detect/preview')
async def detect_prevew(file: bytes = File(...)):
    out,_,__ = _detect_preview(file)
    return Response(content=out.getvalue(), media_type="image/jpeg")

@app.post('/detect/preview/base64')
async def detect_base64_preview(file: bytes = File(...)):
    out,faces, confidence = _detect_preview(file)
    res = {
        'faces': faces.tolist(),
        'confidence': confidence.tolist(),
        'image': base64.encodebytes(out.getvalue()),
    }
    return res

@app.get('/meta')
async def meta():
    return {}