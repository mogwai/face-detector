# Face AI Service

A simple Flask server to responsd to image results with faces detected

## Installation
- Install docker

```sh
cp .env.example .env
docker build -t face-detector .
docker run -it -p 3000:3000  face-detector 
```

## Example Usage
curl -X POST -F 'data=@./picture.jpg' localhost:5000/detect

```json
{
    "results": [
        // x, y, width, height
        [150, 140, 50, 50]
    ]
}
```