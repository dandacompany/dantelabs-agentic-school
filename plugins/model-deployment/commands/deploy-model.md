---
name: deploy-model
description: 학습된 모델을 FastAPI 기반 REST API로 배포하고 Docker 컨테이너화합니다.
arguments:
  - name: model-path
    description: 학습된 모델 파일 경로 (.pkl)
    required: true
  - name: feature-names
    description: 특성 이름 (쉼표로 구분)
    required: false
  - name: sample-data
    description: 샘플 데이터 경로 (특성 이름 자동 추출)
    required: false
  - name: target-column
    description: 타겟 컬럼명
    required: false
  - name: task-type
    description: 태스크 타입 (classification, regression, auto)
    required: false
    default: "auto"
  - name: output-dir
    description: 출력 디렉토리
    required: false
    default: "projects/{project-name}/deployment"
---

# /deploy-model

학습된 모델을 FastAPI 기반 REST API로 배포하고 Docker 컨테이너화합니다.

## Usage

```bash
# 샘플 데이터로 특성 추출
/deploy-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --sample-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --target-column "Class"

# 특성 이름 직접 지정
/deploy-model \
  --model-path "projects/my-project/models/model.pkl" \
  --feature-names "age,income,score,credit_history"

# 태스크 타입 명시
/deploy-model \
  --model-path "projects/house-price/models/rf_model.pkl" \
  --sample-data "projects/house-price/data/train.csv" \
  --target-column "price" \
  --task-type regression

# 출력 디렉토리 지정
/deploy-model \
  --model-path "./models/model.pkl" \
  --feature-names "f1,f2,f3" \
  --output-dir "projects/my-project/deployment"
```

## What This Command Does

### 1. FastAPI 애플리케이션 생성
완전한 REST API를 자동으로 생성합니다:

#### 엔드포인트
- `GET /`: API 정보
- `GET /health`: 헬스 체크
- `POST /predict`: 단일 예측
- `POST /batch_predict`: 배치 예측

#### 기능
- **Pydantic 입력 검증**: 자동 타입 체크
- **Swagger UI**: 자동 API 문서 (`/docs`)
- **ReDoc**: 대체 문서 (`/redoc`)
- **에러 핸들링**: 명확한 에러 메시지

### 2. Docker 설정 생성
프로덕션 배포를 위한 Docker 파일 생성:

#### Dockerfile
- Python 3.10-slim 베이스
- 최적화된 레이어 캐싱
- 최소 이미지 크기

#### docker-compose.yml
- 원클릭 배포
- 헬스 체크 설정
- 자동 재시작

### 3. 의존성 관리
`requirements.txt` 자동 생성:
- FastAPI & Uvicorn
- scikit-learn, pandas, numpy
- XGBoost, LightGBM (선택)

### 4. README 생성
완전한 배포 가이드:
- 로컬 실행
- Docker 실행
- API 사용 예시
- 프로덕션 팁

### 5. 모델 복사
모델 파일을 배포 디렉토리로 복사

## Output Structure

```
projects/{project-name}/deployment/
├── app.py                    # FastAPI 애플리케이션
├── model.pkl                 # 학습된 모델 (복사본)
├── Dockerfile                # Docker 이미지 빌드
├── docker-compose.yml        # Docker Compose 설정
├── requirements.txt          # Python 패키지
└── README.md                 # 배포 가이드
```

## Examples

### Example 1: 신용카드 사기 탐지 API
```bash
/deploy-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --sample-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --target-column "Class"
```

**결과**:
- API 엔드포인트: `POST /predict`
- 입력: 30개 특성 (V1-V28, Time, Amount)
- 출력: `{"prediction": 0, "probability": [0.999, 0.001]}`

### Example 2: 주택 가격 예측 API
```bash
/deploy-model \
  --model-path "projects/house-price/models/rf_model.pkl" \
  --sample-data "projects/house-price/data/train.csv" \
  --target-column "price" \
  --task-type regression
```

**결과**:
- API 엔드포인트: `POST /predict`
- 출력: `{"prediction": 325000.50}`

### Example 3: 수동 특성 지정
```bash
/deploy-model \
  --model-path "projects/my-project/models/model.pkl" \
  --feature-names "age,income,credit_score,loan_amount"
```

## API Usage

### 로컬 실행
```bash
cd projects/{project-name}/deployment
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**접속**: http://localhost:8000/docs

### Docker 실행
```bash
cd projects/{project-name}/deployment
docker-compose up -d
```

### API 호출 예시

#### 헬스 체크
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

#### 단일 예측
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "V1": -1.234,
    "V2": 0.567,
    ...
    "Amount": 149.62
  }'
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

#### 배치 예측
```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "Content-Type: application/json" \
  -d '[
    {"V1": -1.234, "V2": 0.567, ...},
    {"V1": 2.345, "V2": -0.123, ...}
  ]'
```

## Swagger UI

FastAPI는 자동으로 인터랙티브 API 문서를 생성합니다:

**URL**: http://localhost:8000/docs

**기능**:
- 모든 엔드포인트 목록
- 요청/응답 스키마
- "Try it out" 버튼으로 테스트
- 자동 생성된 예시

## Production Deployment

### 성능 튜닝
```bash
# 멀티 워커 (CPU 코어 수에 맞게 조정)
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### 환경 변수
```bash
export PORT=8000
export WORKERS=4
export LOG_LEVEL=info
```

### HTTPS 설정
```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 443 \
  --ssl-keyfile=/path/to/key.pem \
  --ssl-certfile=/path/to/cert.pem
```

### Gunicorn 사용 (프로덕션)
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Docker Commands

### 이미지 빌드
```bash
docker build -t my-model-api:latest .
```

### 컨테이너 실행
```bash
docker run -d -p 8000:8000 --name model-api my-model-api:latest
```

### 로그 확인
```bash
docker logs -f model-api
```

### 컨테이너 중지
```bash
docker stop model-api
```

## Security Best Practices

### 1. API 키 인증
```python
from fastapi import Header, HTTPException

@app.post("/predict")
async def predict(request: PredictionRequest, api_key: str = Header(...)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ... 예측 수행
```

### 2. Rate Limiting
```bash
pip install slowapi
```

### 3. CORS 설정
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

## Monitoring

### Prometheus 메트릭
```bash
pip install prometheus-fastapi-instrumentator
```

### 로깅
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Related Commands

- `/evaluate-model`: 배포 전 모델 평가
- `/monitor-model`: 배포 후 모델 모니터링
- `/analyze-shap`: 예측 설명 API 추가

## Agents Used

- `deployment-engineer` (필수): API 코드 생성 및 Docker 설정

## Troubleshooting

### 문제: "모듈을 찾을 수 없습니다"
- requirements.txt 누락
- 해결: `pip install -r requirements.txt`

### 문제: 포트가 이미 사용 중
- 다른 서비스가 8000 포트 사용
- 해결: `--port 8001`로 포트 변경

### 문제: Docker 빌드 실패
- 모델 파일이 너무 큼
- 해결: `.dockerignore` 파일 생성, 불필요한 파일 제외

### 문제: 예측이 느림
- 단일 워커 사용
- 해결: `--workers 4`로 멀티 워커 실행

## Notes

⚠️ **주의사항**:
- 프로덕션 배포 시 API 키 인증 필수
- 대용량 배치 예측은 타임아웃 설정 필요
- 모델 파일 크기가 크면 Docker 이미지도 커짐

💡 **팁**:
- Swagger UI로 API 테스트 후 배포
- Docker로 로컬에서 먼저 테스트
- 멀티 워커로 성능 향상
- 모니터링 설정 필수 (Prometheus, Grafana)
- CI/CD 파이프라인 구축 (GitHub Actions, Jenkins)

🎯 **활용 사례**:
- 웹 애플리케이션과 통합
- 모바일 앱 백엔드
- 마이크로서비스 아키텍처
- Serverless 배포 (AWS Lambda, Google Cloud Run)
