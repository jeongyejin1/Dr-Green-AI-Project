from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
import json

# --- 1. FastAPI 앱 초기화 및 CORS 설정 ---
app = FastAPI()

origins = [
    "http://localhost:3000", # React 앱(프론트엔드) 주소
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. ⭐️ (필수!) Colab에서 복사한 클래스 이름 리스트 ---
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
    'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
] # (Colab 로그에서 복사한 38개 리스트)

# --- 3. 모델 구조 정의 및 가중치 로드 ---
model = models.resnet50(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))

# ⭐️ 로컬에 저장된 'plant_model.pth' 파일 로드
model.load_state_dict(torch.load('plant_model.pth', map_location=torch.device('cpu')))
model.eval()

# --- 4. 이미지 변환 정의 ---
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# --- 5. 솔루션 DB 로드 ---
with open('solutions.json', 'r', encoding='utf-8') as f:
    solutions_db = json.load(f)

# --- 6. 예측 함수 ---
def predict(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

        predicted_class_name = CLASS_NAMES[predicted_idx.item()]
        confidence_score = confidence.item() * 100

    return predicted_class_name, confidence_score

# --- 7. API 엔드포인트 정의 ---
@app.post("/analyze")
async def analyze_plant(file: UploadFile = File(...)):
    image_bytes = await file.read()
    predicted_class, confidence = predict(image_bytes)

    # ⭐️ DB에서 대처 방안 조회
    solution_data = solutions_db.get(predicted_class, {
        "disease_name": "정보 없음",
        "solution": "아직 데이터베이스에 등록되지 않은 질병입니다."
    })

    return {
        "predicted_class": predicted_class,
        "confidence": f"{confidence:.2f}%",
        "disease_name": solution_data.get("disease_name"),
        "solution": solution_data.get("solution")
    }