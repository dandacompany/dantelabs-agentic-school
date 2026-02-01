# Model Selection Plugin

머신러닝 모델 학습 및 평가를 수행하는 플러그인입니다.

## 📋 개요

이 플러그인은 전처리 및 리샘플링 완료된 데이터로 머신러닝 모델을 학습하고 평가합니다:

- ✅ **알고리즘**: XGBoost, LightGBM, Random Forest
- ✅ **평가 지표**: ROC-AUC, PR-AUC, F1-Score, Confusion Matrix
- ✅ **모델 저장**: Joblib로 재사용 가능
- ✅ **Feature Importance**: 중요 변수 분석 (예정)
- ✅ **하이퍼파라미터 튜닝**: Optuna 통합 (예정)

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd plugins/model-selection/skills/model-selection
uv pip install --system -r requirements.txt
```

### 2. 모델 학습

```bash
# XGBoost 학습 (기본값, 권장)
python scripts/train_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --algorithm xgboost
```

## 📁 플러그인 구조

```
plugins/model-selection/
├── plugin.json
├── README.md
├── agents/
│   └── model-trainer.md
├── commands/
│   └── train-model.md
└── skills/
    └── model-selection/
        ├── requirements.txt
        └── scripts/
            └── train_model.py
```

## 🎯 지원 알고리즘

### 1. XGBoost (기본값, 권장)
```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)
```

**장점**:
- ✅ 높은 성능
- ✅ 불균형 데이터 처리 강점
- ✅ Feature importance 제공
- ✅ 정규화 내장

**사용 시기**: 대부분의 경우 (기본 추천)

### 2. LightGBM
```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)
```

**장점**:
- ✅ XGBoost보다 빠름
- ✅ 메모리 효율적
- ✅ 범주형 변수 직접 처리

**사용 시기**: 대용량 데이터 (100만 건+)

### 3. Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
```

**장점**:
- ✅ 해석 가능
- ✅ 안정적
- ✅ 과적합 덜함

**사용 시기**: 베이스라인 모델, 해석 중요 시

## 📊 출력

### 학습된 모델
```
projects/{project-name}/outputs/models/
├── xgboost_model.pkl           # 학습된 모델
└── preprocessing_pipeline.pkl  # 전처리 파이프라인
```

### 콘솔 출력
```
============================================================
모델 학습 시작
============================================================

데이터 로드 중...
✓ Train: 250,196건
✓ Test: 56,962건

모델 학습 중 (알고리즘: xgboost)...
✓ 학습 완료

모델 평가 중...

============================================================
분류 리포트
============================================================
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     56864
           1       0.81      0.85      0.83        98

    accuracy                           1.00     56962
   macro avg       0.90      0.92      0.91     56962
weighted avg       1.00      1.00      1.00     56962

ROC-AUC: 0.9760
PR-AUC: 0.8701

Confusion Matrix:
                Predicted
              0        1
Actual 0  56,844      20
Actual 1      15      83

✓ 모델 저장: projects/creditcard-fraud-detection/outputs/models/xgboost_model.pkl

============================================================
모델 학습 완료
============================================================

📊 최종 성능:
   ROC-AUC: 0.9760
   PR-AUC: 0.8701
```

## 🔧 사용 예시

### Example 1: 신용카드 사기 탐지 (XGBoost)
```bash
python train_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --algorithm xgboost
```

**예상 성능**:
- ROC-AUC: 0.97+
- PR-AUC: 0.87+
- F1-Score: 0.83+

### Example 2: 고객 이탈 예측 (LightGBM)
```bash
python train_model.py \
  --X-train-path "projects/customer-churn/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/customer-churn/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/customer-churn/data/processed/X_test.csv" \
  --y-test-path "projects/customer-churn/data/processed/y_test.csv" \
  --algorithm lightgbm
```

### Example 3: 베이스라인 모델 (Random Forest)
```bash
python train_model.py \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --algorithm random_forest
```

## 📈 평가 지표 가이드

### 불균형 데이터 (사기 탐지, 이상 탐지)

| 지표 | 사용 여부 | 이유 |
|------|----------|------|
| **Accuracy** | ❌ 금지 | 불균형에서 무의미 |
| **Precision** | ✅ 중요 | FP 비용 고려 |
| **Recall** | ✅ 매우 중요 | FN 비용 고려 |
| **F1-Score** | ✅ 핵심 | Precision-Recall 균형 |
| **PR-AUC** | ✅ 최적 | 불균형 데이터 최적 지표 |
| **ROC-AUC** | ⚠️ 참고 | PR-AUC보다 덜 유용 |

### Confusion Matrix 해석

```
                Predicted
              0        1
Actual 0  56,844      20    # TN, FP
Actual 1      15      83    # FN, TP
```

- **TP (True Positive)**: 사기를 사기로 정확히 예측
- **TN (True Negative)**: 정상을 정상으로 정확히 예측
- **FP (False Positive)**: 정상을 사기로 오판 (Type I Error)
- **FN (False Negative)**: 사기를 정상으로 오판 (Type II Error) ⚠️

**비즈니스 영향**:
- **FN (사기 놓침)**: 금전적 손실 → Recall 중요
- **FP (정상 오판)**: 고객 불편 → Precision 고려

## 🔍 모델 활용

### 학습된 모델 로드 & 예측
```python
import joblib
import pandas as pd

# 모델 로드
model = joblib.load('projects/creditcard-fraud-detection/outputs/models/xgboost_model.pkl')
scaler = joblib.load('projects/creditcard-fraud-detection/outputs/models/preprocessing_pipeline.pkl')

# 신규 데이터 전처리
X_new = pd.read_csv('new_data.csv')
X_new_scaled = scaler.transform(X_new)

# 예측
y_pred = model.predict(X_new_scaled)
y_proba = model.predict_proba(X_new_scaled)[:, 1]

print(f"사기 확률: {y_proba[0]:.2%}")
```

### Threshold 최적화
```python
from sklearn.metrics import precision_recall_curve
import numpy as np

# 최적 임계값 찾기
precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_threshold = thresholds[np.argmax(f1_scores)]

print(f"최적 임계값: {optimal_threshold:.3f}")

# 적용
y_pred_optimized = (y_proba >= optimal_threshold).astype(int)
```

## 🐛 트러블슈팅

### 문제: 과적합 (Train >> Test 성능)
**해결**:
```python
# max_depth 줄이기
model = xgb.XGBClassifier(max_depth=3)

# 정규화 강화
model = xgb.XGBClassifier(reg_alpha=1.0, reg_lambda=10.0)

# 앙상블 크기 줄이기
model = xgb.XGBClassifier(n_estimators=50)
```

### 문제: 저성능 (F1-Score < 0.5)
**해결**:
- 리샘플링 비율 조정 (`/balance-data --ratio 0.2`)
- 전처리 재확인 (`/engineer-features`)
- 알고리즘 변경 (RF → XGBoost)
- 하이퍼파라미터 튜닝

### 문제: 메모리 부족
**해결**:
- LightGBM 사용
- n_estimators 줄이기
- 청크 단위 학습

## 📊 알고리즘 비교

| 알고리즘 | 속도 | 성능 | 메모리 | 해석성 | 추천 순위 |
|---------|------|------|--------|--------|----------|
| **XGBoost** | 보통 | 매우 우수 | 보통 | 중간 | ⭐⭐⭐ |
| **LightGBM** | 빠름 | 매우 우수 | 우수 | 중간 | ⭐⭐ |
| **Random Forest** | 느림 | 우수 | 나쁨 | 우수 | ⭐ |

## 🔗 관련 플러그인

- `data-profiling`: 데이터 분석
- `feature-engineering`: 특성 엔지니어링
- `imbalance-handling`: 클래스 불균형 처리 (학습 전)

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0

## 💡 Best Practices

### 학습 전 체크리스트
- [ ] 데이터 전처리 완료 (`/engineer-features`)
- [ ] 클래스 불균형 처리 (`/balance-data`)
- [ ] Train/Test 분리 확인
- [ ] 특성 개수 일치 확인

### 학습 후 체크리스트
- [ ] Confusion Matrix 분석
- [ ] F1-Score, PR-AUC 기록
- [ ] 과적합 여부 확인
- [ ] 모델 파일 저장 확인

### 프로덕션 배포 전
- [ ] 모델 + 전처리 파이프라인 함께 저장
- [ ] Threshold 최적화
- [ ] 성능 벤치마크 기록
- [ ] 예측 속도 측정

## 🚀 다음 단계

모델 학습 후 권장 단계:

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
   - 비즈니스 인사이트 도출
