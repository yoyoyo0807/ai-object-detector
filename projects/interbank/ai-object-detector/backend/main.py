from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import io
from PIL import Image
import numpy as np

# FastAPIのインスタンス化（これが "app" であることが重要です）
app = FastAPI()

# フロントエンド（Next.js）からのアクセスを許可する設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発時はすべて許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOLOv11モデルの読み込み（初回実行時に自動ダウンロードされます）
model = YOLO("yolo11n.pt")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Object Detector API is running"}

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    # 1. アップロードされた画像を読み込む
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # 2. YOLOで物体検出を実行
    results = model(image)
    
    # 3. 検出結果を整形して返す
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            })
    
    return {"detections": detections}