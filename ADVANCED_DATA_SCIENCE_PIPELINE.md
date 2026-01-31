# 고급 데이터 사이언스 파이프라인 가이드

DanteLabs Agentic School의 완전 자동화된 엔터프라이즈급 데이터 사이언스 파이프라인입니다.

## 📋 전체 파이프라인 개요

```
원본 데이터
    ↓
🔍 1️⃣ 데이터 프로파일링 (data-profiling)
    ↓
📊 2️⃣ EDA 분석 (data-profiling)
    ↓
⚙️  3️⃣ 특성 엔지니어링 (feature-engineering)
    ↓
⚖️  4️⃣ 클래스 불균형 처리 (imbalance-handling)
    ↓
🤖 5️⃣ 모델 학습 (model-selection)
    ↓
🔧 6️⃣ 하이퍼파라미터 튜닝 (hyperparameter-tuning) ⭐ NEW
    ↓
📈 7️⃣ 모델 평가 (model-evaluation) ⭐ NEW
    ↓
🔬 8️⃣ SHAP 분석 (shap-analysis) ⭐ NEW
    ↓
👁️  9️⃣ 모델 모니터링 (model-monitoring) ⭐ NEW
    ↓
🚀 🔟 모델 배포 (model-deployment) ⭐ NEW
    ↓
프로덕션 API 서버
```

## 🎯 플러그인 전체 목록 (9개)

### 기본 파이프라인 (4개)

| # | 플러그인 | 역할 | 핵심 기능 |
|---|---------|------|---------|
| 1 | **data-profiling** | 데이터 분석 | 자동 EDA, A4 레포트 |
| 2 | **feature-engineering** | 특성 변환 | 스케일링, 시간 특성 |
| 3 | **imbalance-handling** | 불균형 해결 | SMOTE, ADASYN |
| 4 | **model-selection** | 모델 학습 | XGBoost, LightGBM, RF |

### 고급 파이프라인 (5개) ⭐ NEW

| # | 플러그인 | 역할 | 핵심 기능 |
|---|---------|------|---------|
| 5 | **hyperparameter-tuning** | 자동 최적화 | Optuna, TPE, Pruning |
| 6 | **model-evaluation** | 성능 분석 | Feature Importance, Learning Curves |
| 7 | **shap-analysis** | 예측 설명 | SHAP Values, Waterfall Plot |
| 8 | **model-monitoring** | 성능 추적 | Drift Detection, Alerts |
| 9 | **model-deployment** | 프로덕션 배포 | FastAPI, Docker, Swagger |

## 🚀 완전 자동화 파이프라인 (신용카드 사기 탐지 예제)

### Step 0: 프로젝트 초기화

```bash
python scripts/init_project.py --name creditcard-fraud-detection
cp samples/datascience/data/raw/creditcard.csv \
   projects/creditcard-fraud-detection/data/raw/
```

### Step 1-4: 기본 파이프라인

```bash
# 1. 프로파일링
/profile-data \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# 2. EDA 분석
/analyze-profile \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# 3. 특성 엔지니어링
/engineer-features \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical"

# 4. 불균형 처리
/balance-data \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1
```

### Step 5-10: 고급 파이프라인 ⭐ NEW

```bash
# 5. 모델 학습 (베이스라인)
/train-model \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --algorithm xgboost

# 6. 하이퍼파라미터 튜닝 (50 trials, 약 1시간)
/tune-hyperparameters \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --algorithm xgboost \
  --metric pr_auc \
  --n-trials 50

# 7. 모델 평가 (Feature Importance, Learning Curves)
/evaluate-model \
  --model-path "projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv"

# 8. SHAP 분석 (예측 설명)
/analyze-shap \
  --model-path "projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --sample-size 1000

# 9. 모델 모니터링 (프로덕션 데이터로)
/monitor-model \
  --model-path "projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl" \
  --reference-data "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --current-data "projects/creditcard-fraud-detection/data/production/prod_2024_01.csv" \
  --target-column "Class"

# 10. API 배포
/deploy-model \
  --model-path "projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl" \
  --X-sample-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv"

# API 서버 실행
cd projects/creditcard-fraud-detection/deployment
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📊 각 단계별 출력

### 1-4. 기본 파이프라인
```
projects/creditcard-fraud-detection/
├── outputs/
│   ├── reports/
│   │   ├── creditcard_profile_report.html     # 프로파일링
│   │   └── creditcard_eda_report.md           # EDA 분석
│   └── models/
│       ├── xgboost_model.pkl                  # 베이스라인 모델
│       └── preprocessing_pipeline.pkl
└── data/
    └── processed/
        ├── X_train_balanced.csv
        ├── y_train_balanced.csv
        ├── X_test.csv
        └── y_test.csv
```

### 5-10. 고급 파이프라인 ⭐ NEW
```
projects/creditcard-fraud-detection/
├── outputs/
│   ├── models/
│   │   ├── xgboost_tuned_model.pkl            # 튜닝된 모델
│   │   ├── xgboost_tuning_history.csv         # 튜닝 이력
│   │   └── xgboost_best_params.txt            # 최적 파라미터
│   ├── evaluations/
│   │   ├── feature_importance.png             # 특성 중요도
│   │   ├── learning_curves.png                # 학습 곡선
│   │   ├── confusion_matrix.png               # Confusion Matrix
│   │   └── evaluation_report.md               # 평가 리포트
│   ├── shap/
│   │   ├── summary_plot.png                   # SHAP 요약
│   │   ├── waterfall_plot.png                 # Waterfall
│   │   ├── force_plot.html                    # Force Plot
│   │   └── shap_report.md                     # SHAP 리포트
│   └── monitoring/
│       ├── drift_summary.png                  # Drift 요약
│       ├── drift_report.csv                   # Drift 상세
│       ├── alerts.json                        # 알림
│       └── monitoring_report.md               # 모니터링 리포트
└── deployment/
    ├── app.py                                 # FastAPI 서버
    ├── Dockerfile                             # Docker 이미지
    ├── docker-compose.yml                     # Docker Compose
    ├── requirements.txt                       # API 의존성
    └── README.md                              # 배포 가이드
```

## 🎯 성능 개선 과정

### 신용카드 사기 탐지 (284,807건, 1:578 불균형)

| 단계 | F1-Score | PR-AUC | ROC-AUC | 개선 |
|-----|----------|--------|---------|------|
| **베이스라인** (XGBoost 기본값) | 0.83 | 0.87 | 0.976 | - |
| **+ 하이퍼파라미터 튜닝** | 0.86 | 0.89 | 0.981 | +3.6% |
| **+ Feature Selection** | 0.87 | 0.90 | 0.983 | +4.8% |
| **+ Threshold 최적화** | 0.88 | 0.91 | 0.983 | +6.0% |

## 🔧 플러그인별 상세 가이드

### 5️⃣ hyperparameter-tuning

**목적**: 베이지안 최적화로 자동 튜닝

**핵심 기능**:
- Optuna TPE Sampler (Random Search보다 10-100배 빠름)
- Median Pruner (성능 낮은 시도 조기 종료)
- Stratified K-Fold CV (5-Fold)

**예상 시간**: 50 trials = 1-2시간 (XGBoost)

**예상 개선**: +2-4% F1-Score

### 6️⃣ model-evaluation

**목적**: 모델 성능 심층 분석

**핵심 기능**:
- Feature Importance (Top 20 변수)
- Learning Curves (Train/Val 손실)
- Cross-Validation (K-Fold)
- Classification Report (Precision, Recall, F1)
- Confusion Matrix, ROC Curve, PR Curve

**출력**: PNG 시각화 + Markdown 리포트

### 7️⃣ shap-analysis

**목적**: 예측 설명 및 해석

**핵심 기능**:
- SHAP Values 계산 (TreeExplainer)
- Summary Plot (전체 데이터)
- Waterfall Plot (개별 예측)
- Force Plot (인터랙티브)
- Dependence Plot (특성 의존성)

**활용**:
- 모델 신뢰성 검증
- 비즈니스 인사이트 도출
- 규제 준수 (설명 가능한 AI)

### 8️⃣ model-monitoring

**목적**: 프로덕션 모델 성능 추적

**핵심 기능**:
- Data Drift Detection (PSI, KS Test)
- Prediction Distribution Shift
- Performance Degradation Alert
- Real-time Metrics Tracking

**알림 기준**:
- PSI > 0.1: 주의
- PSI > 0.25: 심각 (재학습 필요)
- KS Statistic > 0.1: Drift 발생

### 9️⃣ model-deployment

**목적**: 프로덕션 API 배포

**핵심 기능**:
- FastAPI REST API 자동 생성
- Pydantic 입력 검증
- Swagger UI (자동 문서화)
- Docker 컨테이너화
- Multi-worker 지원

**API Endpoints**:
- `GET /`: 웰컴 메시지
- `GET /health`: 헬스 체크
- `POST /predict`: 단일 예측
- `POST /batch_predict`: 배치 예측

**프로덕션 준비**:
- Health check
- Error handling
- Request validation
- API documentation
- Container support

## 🔍 실전 활용 시나리오

### 시나리오 1: 신속 프로토타입 (1일)

```bash
# 1-4. 기본 파이프라인 (2시간)
/profile-data → /analyze-profile → /engineer-features → /balance-data

# 5. 베이스라인 모델 (10분)
/train-model --algorithm xgboost

# 6. 빠른 튜닝 (30분)
/tune-hyperparameters --n-trials 20 --timeout 1800

# 7. 간단 평가 (5분)
/evaluate-model
```

**총 소요 시간**: ~3시간
**예상 성능**: F1-Score 0.80-0.85

### 시나리오 2: 프로덕션 모델 (3일)

```bash
# Day 1: 기본 파이프라인 + 베이스라인
/profile-data → /analyze-profile → /engineer-features → /balance-data → /train-model

# Day 2: 정밀 튜닝 + 평가
/tune-hyperparameters --n-trials 100  # 3-4시간
/evaluate-model
/analyze-shap

# Day 3: 배포 준비
/deploy-model
docker-compose up -d
/monitor-model (프로덕션 데이터로)
```

**총 소요 시간**: ~3일
**예상 성능**: F1-Score 0.85-0.90

### 시나리오 3: 엔터프라이즈 솔루션 (1주)

```bash
# Week 1 Plan:
# Mon-Tue: 데이터 분석 및 전처리
# Wed: 모델 학습 및 튜닝
# Thu: 모델 평가 및 SHAP 분석
# Fri: 배포 및 모니터링 설정

# 추가 작업:
- Feature Engineering 반복
- Ensemble 모델 (XGBoost + LightGBM + RF)
- A/B 테스트 설계
- 모니터링 대시보드 구축
```

**총 소요 시간**: ~1주
**예상 성능**: F1-Score 0.90+
**산출물**: 프로덕션 API + 모니터링 + 문서

## 💡 Best Practices

### 1. 파이프라인 실행 순서

**필수 순서**:
```
프로파일링 → EDA → 특성 엔지니어링 → 불균형 처리 → 모델 학습
```

**권장 순서** (고급):
```
↓ (위 단계 완료 후)
베이스라인 평가 → 하이퍼파라미터 튜닝 → 최종 평가 → SHAP 분석 → 배포 → 모니터링
```

### 2. 성능 최적화 팁

| 목표 | 방법 | 예상 개선 |
|------|------|----------|
| **빠른 실험** | n-trials=20, timeout=30min | +1-2% |
| **정밀 튜닝** | n-trials=100, pr_auc 최적화 | +3-5% |
| **Ensemble** | XGBoost + LightGBM + RF | +5-8% |
| **Feature Selection** | SHAP 기반 Top 20 선택 | +2-3% |

### 3. 프로덕션 체크리스트

- [ ] 하이퍼파라미터 튜닝 완료
- [ ] Feature Importance 분석
- [ ] SHAP 분석 (설명 가능성)
- [ ] Cross-Validation 검증
- [ ] Test 데이터 최종 평가
- [ ] Docker 컨테이너 빌드
- [ ] API 테스트 (단일 + 배치)
- [ ] 모니터링 설정 (PSI, KS)
- [ ] 알림 임계값 설정
- [ ] 문서화 (API, 모델 카드)

## 📚 관련 문서

- [기본 파이프라인 가이드](./DATA_SCIENCE_PIPELINE.md)
- [프로젝트 구조 가이드](./PROJECTS.md)
- [hyperparameter-tuning 플러그인](./plugins/hyperparameter-tuning/README.md)
- [model-evaluation 플러그인](./plugins/model-evaluation/README.md)
- [shap-analysis 플러그인](./plugins/shap-analysis/README.md)
- [model-monitoring 플러그인](./plugins/model-monitoring/README.md)
- [model-deployment 플러그인](./plugins/model-deployment/README.md)

## 🎓 학습 경로

### 초급: 기본 파이프라인 마스터
1. 데이터 프로파일링 이해
2. 특성 엔지니어링 기법
3. 클래스 불균형 처리
4. 기본 모델 학습

### 중급: 성능 최적화
5. 하이퍼파라미터 튜닝 (Optuna)
6. 모델 평가 및 분석
7. Feature Importance 해석

### 고급: 프로덕션 배포
8. SHAP 분석 및 설명
9. 모델 모니터링 전략
10. API 배포 및 운영

---

**생성일**: 2026-01-31
**작성자**: Dante Labs
**버전**: 2.0.0 (Advanced Pipeline)
**플러그인 수**: 9개 (기본 4 + 고급 5)
