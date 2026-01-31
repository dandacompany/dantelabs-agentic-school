# Model Deployment Plugin

학습된 모델을 FastAPI 기반 REST API로 배포하고 Docker 컨테이너화하는 플러그인입니다.

## 📋 개요

이 플러그인은 모델 배포를 자동화하여 다음을 제공합니다:

### 주요 기능
- ✅ **FastAPI 자동 생성**: REST API 코드 자동 생성
- ✅ **Pydantic 검증**: 입력 데이터 자동 검증
- ✅ **Swagger UI**: 인터랙티브 API 문서
- ✅ **Docker 컨테이너화**: Dockerfile & docker-compose.yml
- ✅ **배치 예측**: 다중 샘플 동시 처리
- ✅ **헬스 체크**: API 상태 모니터링

### 왜 이 플러그인인가?
- **빠른 배포**: 한 번의 명령으로 완전한 API 생성
- **프로덕션 준비**: Docker로 어디서나 실행 가능
- **표준화**: FastAPI 모범 사례 적용
- **문서화**: 자동 Swagger UI 생성

## 🚀 빠른 시작

### 1. 의존성 설치

**uv 사용 (권장)**:
```bash
cd plugins/model-deployment/skills/deployment
uv pip install -r requirements.txt
```

**pip 사용**:
```bash
pip install -r requirements.txt
```

### 2. API 생성

```bash
# Claude Code에서 실행
/deploy-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --sample-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --target-column "Class"

# 또는 Python 스크립트 직접 실행
cd plugins/model-deployment/skills/deployment/scripts
python deploy_api.py \
  --model-path "../../../../../projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --sample-data "../../../../../projects/creditcard-fraud-detection/data/processed/train.csv" \
  --target-column "Class"
```

### 3. API 실행

```bash
cd projects/creditcard-fraud-detection/deployment
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**API 문서**: http://localhost:8000/docs

### 4. Docker 실행

```bash
cd projects/creditcard-fraud-detection/deployment
docker-compose up -d
```

## 📁 플러그인 구조

```
plugins/model-deployment/
├── plugin.json
├── README.md
├── agents/
│   └── deployment-engineer.md
├── commands/
│   └── deploy-model.md
└── skills/
    └── deployment/
        ├── requirements.txt
        └── scripts/
            └── deploy_api.py
```

## 🎯 주요 기능

### 1. FastAPI 애플리케이션 생성
자동으로 다음을 포함하는 완전한 API 생성:

#### 엔드포인트
- `GET /`: API 정보
- `GET /health`: 헬스 체크
- `POST /predict`: 단일 예측
- `POST /batch_predict`: 배치 예측

#### 기능
- Pydantic 모델로 입력 검증
- 자동 타입 체크
- 에러 핸들링
- Swagger UI (`/docs`)
- ReDoc (`/redoc`)

### 2. Docker 컨테이너화
프로덕션 배포를 위한 Docker 설정:

#### Dockerfile
- Python 3.10-slim 베이스
- 최적화된 레이어 캐싱
- 최소 이미지 크기

#### docker-compose.yml
- 원클릭 배포
- 헬스 체크
- 자동 재시작

### 3. 의존성 관리
`requirements.txt` 자동 생성:
- FastAPI & Uvicorn
- scikit-learn 생태계
- XGBoost, LightGBM

### 4. 배포 가이드
`README.md` 자동 생성:
- 로컬 실행
- Docker 실행
- API 사용 예시
- 프로덕션 팁

### 5. 모델 복사
모델 파일을 배포 디렉토리로 자동 복사

## 📊 사용 예시

### Example 1: 분류 모델 배포
```bash
/deploy-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --sample-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --target-column "Class"
```

### Example 2: 회귀 모델 배포
```bash
/deploy-model \
  --model-path "projects/house-price/models/rf_model.pkl" \
  --sample-data "projects/house-price/data/train.csv" \
  --target-column "price" \
  --task-type regression
```

### Example 3: 수동 특성 지정
```bash
/deploy-model \
  --model-path "projects/my-project/models/model.pkl" \
  --feature-names "age,income,credit_score,loan_amount"
```

## 🔧 파라미터

### 필수 파라미터
- `--model-path`: 학습된 모델 파일 경로

### 선택 파라미터 (둘 중 하나 필수)
- `--feature-names`: 특성 이름 (쉼표로 구분)
- `--sample-data`: 샘플 데이터 (자동 추출)

### 기타 선택 파라미터
- `--target-column`: 타겟 컬럼명
- `--task-type`: 태스크 타입 (classification/regression/auto)
- `--output-dir`: 출력 디렉토리

## 📤 출력

생성되는 파일:
- `app.py`: FastAPI 애플리케이션
- `model.pkl`: 모델 복사본
- `Dockerfile`: Docker 이미지 빌드
- `docker-compose.yml`: Docker Compose 설정
- `requirements.txt`: Python 패키지
- `README.md`: 배포 가이드

## 🌐 API 사용

### 헬스 체크
```bash
curl http://localhost:8000/health
```

**응답**:
```json
{
  "status": "healthy",
  "model_type": "XGBClassifier",
  "feature_count": 30
}
```

### 단일 예측
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"V1": -1.234, "V2": 0.567, "Amount": 149.62}'
```

**응답 (분류)**:
```json
{
  "prediction": 0,
  "probability": [0.9995, 0.0005]
}
```

**응답 (회귀)**:
```json
{
  "prediction": 325000.50
}
```

### 배치 예측
```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "Content-Type: application/json" \
  -d '[
    {"V1": -1.234, "V2": 0.567},
    {"V1": 2.345, "V2": -0.123}
  ]'
```

## 🐳 Docker 사용

### 이미지 빌드
```bash
cd projects/{project-name}/deployment
docker build -t my-model-api:latest .
```

### 컨테이너 실행
```bash
docker run -d -p 8000:8000 --name model-api my-model-api:latest
```

### Docker Compose
```bash
docker-compose up -d
```

### 로그 확인
```bash
docker logs -f model-api
```

## 🔐 프로덕션 팁

### 1. 성능 튜닝
```bash
# 멀티 워커 (CPU 코어 수)
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Gunicorn 사용 (프로덕션)
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 2. API 키 인증
```python
from fastapi import Header, HTTPException

@app.post("/predict")
async def predict(request: PredictionRequest, api_key: str = Header(...)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
```

### 3. Rate Limiting
```bash
pip install slowapi
```

### 4. HTTPS 설정
```bash
uvicorn app:app --ssl-keyfile=/path/to/key.pem --ssl-certfile=/path/to/cert.pem
```

### 5. 모니터링
```bash
pip install prometheus-fastapi-instrumentator
```

## 🐛 트러블슈팅

### 문제: "모듈을 찾을 수 없습니다"
- **해결**: `pip install -r requirements.txt`

### 문제: 포트가 이미 사용 중
- **해결**: `uvicorn app:app --port 8001`

### 문제: Docker 빌드 실패
- **해결**: `.dockerignore` 파일 생성

### 문제: 예측이 느림
- **해결**: `--workers 4`로 멀티 워커 실행

## 📚 관련 문서

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Docker 공식 문서](https://docs.docker.com/)
- [Uvicorn 문서](https://www.uvicorn.org/)

## 🔗 관련 플러그인

- `model-evaluation`: 배포 전 모델 평가
- `model-monitoring`: 배포 후 모델 모니터링
- `shap-analysis`: 예측 설명 API 추가

## 💡 활용 사례

### 웹 애플리케이션
React/Vue.js에서 API 호출

### 모바일 앱
iOS/Android 앱 백엔드

### 마이크로서비스
Kubernetes에서 오케스트레이션

### Serverless
AWS Lambda, Google Cloud Run

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0
