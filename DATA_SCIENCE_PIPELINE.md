# 데이터 사이언스 파이프라인 가이드

DanteLabs Agentic School의 완전 자동화된 데이터 사이언스 파이프라인입니다.

## 📋 파이프라인 개요

```
원본 데이터
    ↓
1️⃣ 데이터 프로파일링 (data-profiling)
    ↓
2️⃣ EDA 분석 (data-profiling)
    ↓
3️⃣ 특성 엔지니어링 (feature-engineering)
    ↓
4️⃣ 클래스 불균형 처리 (imbalance-handling)
    ↓
5️⃣ 모델 학습 (model-selection)
    ↓
학습된 모델 + 평가 리포트
```

## 🚀 빠른 시작

### Step 0: 프로젝트 초기화

```bash
# 새 프로젝트 생성
python scripts/init_project.py --name my-ml-project

# 프로젝트 구조
projects/my-ml-project/
├── data/
│   ├── raw/              # 원본 데이터
│   ├── processed/        # 전처리 데이터
│   └── interim/          # 중간 데이터
├── outputs/
│   ├── models/           # 학습된 모델
│   ├── reports/          # 분석 리포트
│   └── figures/          # 시각화
└── notebooks/            # Jupyter 노트북
```

### Step 1: 원본 데이터 준비

```bash
# 데이터를 data/raw/에 저장
cp /path/to/your/data.csv projects/my-ml-project/data/raw/
```

### Step 2-6: 파이프라인 실행

#### 2️⃣ 데이터 프로파일링
```bash
python plugins/data-profiling/skills/profiling/scripts/generate_profile.py \
  --data-path "projects/my-ml-project/data/raw/data.csv" \
  --target-column "target" \
  --output-dir "projects/my-ml-project/outputs/reports" \
  --mode explorative
```

**출력**:
- `projects/my-ml-project/outputs/reports/data_profile_report.html` (브라우저 자동 오픈)

**확인 사항**:
- 결측치 비율
- 클래스 분포 (불균형 여부)
- 변수 간 상관관계
- 이상치

#### 3️⃣ EDA 분석
```bash
python plugins/data-profiling/skills/profiling/scripts/analyze_eda.py \
  --data-path "projects/my-ml-project/data/raw/data.csv" \
  --target-column "target" \
  --output-dir "projects/my-ml-project/outputs/reports"
```

**출력**:
- `projects/my-ml-project/outputs/reports/data_eda_report.md` (A4 한 장)

**확인 사항**:
- 데이터 전처리 지침 (우선순위별)
- 추가 분석 권고사항
- 모델링 전략

#### 4️⃣ 특성 엔지니어링
```bash
python plugins/feature-engineering/skills/feature-engineering/scripts/transform_features.py \
  --data-path "projects/my-ml-project/data/raw/data.csv" \
  --target-column "target" \
  --time-features "hour,day,cyclical" \
  --scaling-strategy "robust" \
  --output-dir "projects/my-ml-project/data/processed"
```

**출력**:
- `projects/my-ml-project/data/processed/data_processed_X.csv`
- `projects/my-ml-project/data/processed/data_processed_y.csv`
- `outputs/models/data_preprocessing_pipeline.pkl`

**수행 작업**:
- 스케일링 (RobustScaler, StandardScaler, MinMaxScaler)
- 시간 특성 추출 (Hour, Day, Cyclical encoding)
- 전처리 파이프라인 저장

#### 5️⃣ 클래스 불균형 처리
```bash
python plugins/imbalance-handling/skills/imbalance-handling/scripts/balance_data.py \
  --X-path "projects/my-ml-project/data/processed/data_processed_X.csv" \
  --y-path "projects/my-ml-project/data/processed/data_processed_y.csv" \
  --method smote \
  --ratio 0.1 \
  --output-dir "projects/my-ml-project/data/processed"
```

**출력**:
- `projects/my-ml-project/data/processed/X_train_balanced.csv`
- `projects/my-ml-project/data/processed/y_train_balanced.csv`
- `projects/my-ml-project/data/processed/X_test.csv`
- `projects/my-ml-project/data/processed/y_test.csv`

**리샘플링 방법**:
- SMOTE (기본값, 권장)
- ADASYN (정교한 샘플링)
- BorderlineSMOTE (경계선 중심)
- RandomUnderSampler (대용량)
- SMOTE-Tomek (하이브리드)

#### 6️⃣ 모델 학습
```bash
python plugins/model-selection/skills/model-selection/scripts/train_model.py \
  --X-train-path "projects/my-ml-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-ml-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-ml-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-ml-project/data/processed/y_test.csv" \
  --algorithm xgboost \
  --output-dir "projects/my-ml-project/outputs/models"
```

**출력**:
- `projects/my-ml-project/outputs/models/xgboost_model.pkl`
- 콘솔에 Classification Report, ROC-AUC, PR-AUC, Confusion Matrix

**지원 알고리즘**:
- XGBoost (기본값, 권장)
- LightGBM (대용량 데이터)
- Random Forest (베이스라인)

## 📊 실전 예제: 신용카드 사기 탐지

### 데이터셋 특징
- 284,807건
- 31개 특성 (Time, V1-V28, Amount, Class)
- 극심한 클래스 불균형: 1:578 (사기 0.17%)

### 전체 파이프라인 실행

```bash
# 0. 프로젝트 생성
python scripts/init_project.py --name creditcard-fraud-detection

# 1. 데이터 복사
cp samples/datascience/data/raw/creditcard.csv \
   projects/creditcard-fraud-detection/data/raw/

# 2. 프로파일링 (약 5분)
python plugins/data-profiling/skills/profiling/scripts/generate_profile.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --output-dir "projects/creditcard-fraud-detection/outputs/reports"

# 3. EDA 분석
python plugins/data-profiling/skills/profiling/scripts/analyze_eda.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --output-dir "projects/creditcard-fraud-detection/outputs/reports"

# 4. 특성 엔지니어링
python plugins/feature-engineering/skills/feature-engineering/scripts/transform_features.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical" \
  --output-dir "projects/creditcard-fraud-detection/data/processed"

# 5. 불균형 처리 (1:578 → 1:10)
python plugins/imbalance-handling/skills/imbalance-handling/scripts/balance_data.py \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1 \
  --output-dir "projects/creditcard-fraud-detection/data/processed"

# 6. 모델 학습 (XGBoost)
python plugins/model-selection/skills/model-selection/scripts/train_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --algorithm xgboost \
  --output-dir "projects/creditcard-fraud-detection/outputs/models"
```

### 예상 결과

```
ROC-AUC: 0.9760
PR-AUC: 0.8701
F1-Score: 0.83

Confusion Matrix:
                Predicted
              0        1
Actual 0  56,844      20    (99.96% 정확도)
Actual 1      15      83    (84.7% Recall)
```

**핵심 성과**:
- ✅ 사기 거래의 84.7% 탐지 (Recall)
- ✅ 정상 거래 오탐률 0.04% (Precision)
- ✅ 균형 잡힌 성능 (F1-Score: 0.83)

## 🎯 플러그인별 역할

| 플러그인 | 역할 | 핵심 기능 | 출력 |
|---------|------|---------|------|
| **data-profiling** | 데이터 분석 | 프로파일링, EDA | HTML, Markdown 리포트 |
| **feature-engineering** | 특성 변환 | 스케일링, 시간 특성 | 전처리 데이터, 파이프라인 |
| **imbalance-handling** | 불균형 해결 | SMOTE, ADASYN | 균형 데이터 (Train/Test) |
| **model-selection** | 모델 학습 | XGBoost, LightGBM, RF | 학습된 모델, 평가 리포트 |

## 📈 평가 지표 가이드

### 불균형 데이터 (사기 탐지, 이상 탐지)

| 지표 | 중요도 | 설명 |
|------|--------|------|
| **PR-AUC** | ⭐⭐⭐⭐⭐ | 불균형 데이터 최적 지표 |
| **F1-Score** | ⭐⭐⭐⭐⭐ | Precision-Recall 균형 |
| **Recall** | ⭐⭐⭐⭐ | 사기 놓치지 않기 (FN 최소화) |
| **Precision** | ⭐⭐⭐ | 오탐 최소화 (FP 최소화) |
| **ROC-AUC** | ⭐⭐ | 참고용 (불균형에 덜 민감) |
| **Accuracy** | ❌ | 사용 금지 (불균형에서 무의미) |

### 균형 데이터

| 지표 | 중요도 |
|------|--------|
| **F1-Score** | ⭐⭐⭐⭐⭐ |
| **ROC-AUC** | ⭐⭐⭐⭐ |
| **Accuracy** | ⭐⭐⭐ |

## 🔧 파라미터 최적화 가이드

### 리샘플링 비율 (ratio)

| 원본 불균형 | 권장 ratio | 최종 비율 | 비고 |
|-----------|-----------|----------|------|
| 1:500+ | 0.05-0.1 | 1:20 ~ 1:10 | 극심한 불균형 |
| 1:100 | 0.1-0.2 | 1:10 ~ 1:5 | 심한 불균형 |
| 1:50 | 0.2-0.5 | 1:5 ~ 1:2 | 중간 불균형 |
| 1:10 | 0.5-1.0 | 1:2 ~ 1:1 | 가벼운 불균형 |

### 스케일링 전략

| 전략 | 사용 시기 | 특징 |
|------|---------|------|
| **RobustScaler** | 이상치 많음 (기본 권장) | 중앙값, IQR 사용 |
| **StandardScaler** | 정규분포 | 평균 0, 분산 1 |
| **MinMaxScaler** | 0-1 범위 필요 | 이상치에 민감 |

### 알고리즘 선택

| 상황 | 추천 알고리즘 | 이유 |
|------|-------------|------|
| 기본 시작 | **XGBoost** | 높은 성능, 불균형 처리 강점 |
| 대용량 데이터 (100만 건+) | **LightGBM** | 빠른 속도, 메모리 효율 |
| 베이스라인 | **Random Forest** | 안정적, 해석 가능 |

## 💡 Best Practices

### 1. 프로젝트 조직
- ✅ 프로젝트별 폴더 분리 (`projects/{name}/`)
- ✅ 원본 데이터는 `data/raw/`에만 (절대 수정 금지)
- ✅ Git에 데이터/모델 커밋 금지 (`.gitignore` 설정)

### 2. 데이터 전처리
- ✅ Train/Test 분리 **후** 리샘플링 (Data leakage 방지)
- ✅ 전처리 파이프라인 저장 (재사용)
- ✅ Test 데이터는 원본 유지 (리샘플링 X)

### 3. 모델 학습
- ✅ F1-Score, PR-AUC로 평가 (불균형 데이터)
- ✅ Stratified K-Fold CV 사용
- ✅ 모델 + 파이프라인 함께 저장

### 4. 성능 모니터링
- ✅ Confusion Matrix 분석
- ✅ Feature Importance 확인
- ✅ 과적합 여부 확인 (Train vs Test)

## 🐛 트러블슈팅

### 문제: 메모리 부족
**해결**:
- 프로파일링: `--mode minimal --sample-size 50000`
- 리샘플링: `--ratio 0.05` (낮은 비율)
- 모델: LightGBM 사용

### 문제: 과적합
**해결**:
- `max_depth` 줄이기 (6 → 3)
- 정규화 강화 (`reg_alpha`, `reg_lambda`)
- 리샘플링 비율 낮추기

### 문제: 저성능 (F1-Score < 0.5)
**해결**:
- 리샘플링 비율 조정 (0.1 → 0.2)
- 알고리즘 변경 (RF → XGBoost)
- 특성 엔지니어링 재검토

## 📚 관련 문서

- [프로젝트 구조 가이드](./PROJECTS.md)
- [data-profiling 플러그인](./plugins/data-profiling/README.md)
- [feature-engineering 플러그인](./plugins/feature-engineering/README.md)
- [imbalance-handling 플러그인](./plugins/imbalance-handling/README.md)
- [model-selection 플러그인](./plugins/model-selection/README.md)

## 🔗 다음 단계

파이프라인 완료 후 권장 단계:

1. **Feature Importance 분석** (예정)
   - 중요 변수 Top 20 파악
   - 불필요한 변수 제거

2. **하이퍼파라미터 튜닝** (예정)
   - Optuna, GridSearch
   - F1-Score 최적화

3. **Ensemble** (예정)
   - XGBoost + LightGBM + RF
   - Voting, Stacking

4. **SHAP 분석** (예정)
   - 예측 설명
   - 비즈니스 인사이트

5. **프로덕션 배포** (예정)
   - API 서버 구축
   - 모니터링 시스템

---

**생성일**: 2026-01-31
**작성자**: Dante Labs
**버전**: 1.0.0
