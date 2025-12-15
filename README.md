# 🌱 Dr. Green: AI 기반 식물 질병 진단 웹 서비스

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-ResNet50-EE4C2C?logo=pytorch)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)

> **"식물이 아픈가요? Dr. Green에게 물어보세요!"** > 딥러닝(ResNet50)을 활용하여 38종의 식물 질병을 진단하고, 맞춤형 대처 방안을 제공하는 웹 서비스입니다.

---

## 📸 프로젝트 시연 (Demo)

| 메인 화면 & 이미지 업로드 | AI 진단 결과 & 솔루션 |
| :---: | :---: |
| ![Main Screen](./assets/main_screen.png) | ![Result Screen](./assets/result_screen.png) |

**📺 [유튜브 시연 영상 보러가기](https://youtu.be/TTor1DFvPoY)**

---

## 💡 프로젝트 소개 (Overview)

최근 홈 가드닝(Home Gardening) 인구가 늘어나면서 비전문가도 쉽게 식물의 질병을 파악하고 대처할 필요성이 커졌습니다.  
**Dr. Green**은 스마트폰이나 PC로 잎 사진을 찍어 올리면, AI가 즉시 질병명을 판독하고 **"어떻게 치료해야 하는지"** 해결책까지 원스톱으로 제공하는 서비스입니다.

### ✨ 주요 기능
1.  **이미지 업로드**: 드래그 앤 드롭으로 간편하게 식물 잎 사진 입력
2.  **AI 질병 진단**: 38개의 질병 클래스 중 하나를 89% 정확도로 분류
3.  **솔루션 제공**: 진단된 병명에 맞는 원인, 증상, 치료법 데이터(JSON) 출력
4.  **반응형 웹**: PC 및 모바일 환경 지원

---

## 🛠 기술 스택 (Tech Stack)

### AI & Data
* **Model**: ResNet50 (Pre-trained on ImageNet -> Fine-tuned)
* **Framework**: PyTorch
* **Dataset**: New Plant Diseases Dataset (Kaggle)
* **Environment**: Google Colab (T4 GPU)

### Backend
* **Framework**: FastAPI
* **Server**: Uvicorn
* **Library**: Pillow (이미지 처리), Python-multipart

### Frontend
* **Library**: React.js
* **HTTP Client**: Axios
* **Styling**: CSS3

---

## 📂 프로젝트 구조 (Structure)

```bash
Dr-Green-Project
├── backend
│   ├── main.py          # FastAPI 서버 메인 (API 엔드포인트)
│   ├── plant_model.pth  # 학습된 PyTorch 모델 파일
│   ├── solutions.json   # 질병별 대처 방안 데이터베이스
│   └── requirements.txt # 백엔드 의존성 목록
├── frontend
│   ├── src
│   │   ├── App.js       # React 메인 로직 (UI 및 API 연동)
│   │   └── App.css      # 스타일 시트
│   └── package.json     # 프론트엔드 의존성 목록
└── README.md
```bash
## 💡 핵심 기술 및 개발 내용 (Key Features)

### 1. AI 모델링 (Deep Learning)
* **Base Model**: ResNet50 (ImageNet Pre-trained)
* **Transfer Learning (전이 학습)**:
    * 마지막 Fully Connected Layer(FC)를 38개 출력 노드로 교체하였습니다.
    * **Fine-tuning**: 초기 층은 동결(Freeze)하고, 상위 레이어만 학습시켜 학습 효율을 극대화했습니다.
* **Data Augmentation**: 데이터 불균형 해소를 위해 회전, 뒤집기, 밝기 조절 등을 적용했습니다.

### 2. 백엔드 개발 (FastAPI)
* **비동기 처리**: `async/await` 문법을 사용하여 다중 접속 환경에서도 빠른 응답 속도를 보장합니다.
* **경량 데이터베이스**: 복잡한 RDBMS 대신 `solutions.json`을 NoSQL 형태로 활용하여 조회 속도를 높였습니다.

### 3. 프론트엔드 개발 (React)
* **사용자 경험(UX) 최적화**: 이미지 드래그 앤 드롭, 로딩 인디케이터, 결과 카드 UI를 구현했습니다.
* **Axios 연동**: 백엔드와의 비동기 통신을 안정적으로 처리합니다.

---

## 📊 AI 모델 성능 (Model Performance)

* **데이터셋**: New Plant Diseases Dataset (Kaggle)
* **학습 데이터**: 10,000장 (Subset) / **검증 데이터**: 2,000장
* **최종 정확도 (Validation Accuracy)**: **89.2%**
* **손실 값 (Loss)**: 0.34 (안정적으로 수렴)

| Metric | Score | 비고 |
| :--- | :--- | :--- |
| **Top-1 Accuracy** | **89.2%** | 가장 높은 확률의 예측이 정답일 확률 |
| **Inference Time** | **0.8s** | 이미지 1장당 평균 추론 시간 (CPU 기준) |

---

## 🛠 기술적 챌린지 및 해결 (Troubleshooting)

프로젝트 진행 중 발생한 주요 문제와 해결 과정입니다.

### 1. Colab I/O 병목 현상 (학습 속도 저하)
* **문제 상황**: Google Drive에 저장된 7만 장의 이미지를 직접 불러와 학습시킬 때, **1 Epoch당 15분 이상** 소요되는 I/O Latency 발생.
* **원인 분석**: 네트워크를 통해 드라이브의 파일을 개별적으로 읽어오는 과정에서 병목 발생.
* **해결 방안**:
    1. 전체 데이터셋을 `.zip`으로 압축.
    2. `!cp` 명령어로 Colab의 로컬 런타임 디스크(`/content`)로 복사.
    3. `!unzip`으로 로컬에서 압축 해제 후 학습 수행.
* **결과**: 1 Epoch 소요 시간을 **15분 → 50초**로 단축 (약 18배 성능 향상).

### 2. CORS (Cross-Origin Resource Sharing) 보안 이슈
* **문제 상황**: React(Port 3000)에서 FastAPI(Port 8000)로 API 요청 시 브라우저가 보안상의 이유로 차단.
* **해결 방안**: FastAPI의 `CORSMiddleware`를 미들웨어 스택에 추가하고, `allow_origins` 리스트에 프론트엔드 주소를 명시적으로 허용함.

## 🏁 결론 및 느낀점 (Conclusion)

본 프로젝트인 **Dr. Green**은 단순한 인공지능 모델 학습을 넘어, 실제 사용자가 활용할 수 있는 **완성된 웹 서비스**를 구축하는 것을 목표로 하였습니다.

### 💡 프로젝트 성과 및 배운 점
1.  **End-to-End AI 서비스 구현**: 데이터 전처리부터 모델 학습(PyTorch), 백엔드 API(FastAPI), 프론트엔드(React)까지 이어지는 전체 개발 파이프라인을 직접 구축하며 **풀스택 AI 개발 역량**을 확보하였습니다.
2.  **실질적인 문제 해결 능력**:
    * Google Colab의 I/O 병목 현상을 로컬 압축 해제 방식으로 해결하며 클라우드 자원 활용에 대한 이해도를 높였습니다.
    * CORS 설정 및 비동기 통신 처리 등 서로 다른 기술 스택을 연동하며 발생하는 실무적인 이슈들을 주도적으로 해결하였습니다.
3.  **사용자 중심의 설계**: 단순히 질병을 '분류'하는 것에 그치지 않고, 구체적인 '대처 방안(Solution)'을 제공함으로써 서비스의 실용성을 높였습니다.

이번 프로젝트를 통해 **"기술을 통해 실생활의 문제를 해결하고 가치를 창출하는 과정"**을 경험하였으며, 향후 객체 탐지(Object Detection) 기술 도입 및 클라우드 배포를 통해 서비스를 지속적으로 고도화할 계획입니다.
