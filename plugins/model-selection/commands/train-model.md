---
name: train-model
description: 전처리된 데이터로 머신러닝 모델을 학습하고 평가합니다.
arguments:
  - name: X-train-path
    description: Train 특성 데이터 파일 경로
    required: true
  - name: y-train-path
    description: Train 타겟 데이터 파일 경로
    required: true
  - name: X-test-path
    description: Test 특성 데이터 파일 경로
    required: true
  - name: y-test-path
    description: Test 타겟 데이터 파일 경로
    required: true
  - name: algorithm
    description: 학습할 알고리즘 (xgboost, lightgbm, random_forest)
    required: false
    default: "xgboost"
  - name: tune
    description: 하이퍼파라미터 튜닝 활성화 (true/false)
    required: false
    default: "false"
  - name: output-dir
    description: 모델 저장 디렉토리
    required: false
    default: "projects/{project-name}/outputs/models"
---

# /train-model

전처리 및 리샘플링 완료된 데이터로 머신러닝 모델을 학습하고 평가합니다.

## Usage

```bash
# XGBoost 학습 (기본값)
/train-model \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv"

# LightGBM 사용
/train-model \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --algorithm lightgbm

# Random Forest 사용
/train-model \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --algorithm random_forest

# 하이퍼파라미터 튜닝 포함 (예정)
/train-model \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --algorithm xgboost \
  --tune true

# 출력 디렉토리 지정
/train-model \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --output-dir "projects/my-project/outputs/experiment_1"
```

## What This Command Does

### 1. 데이터 로드 및 검증
- Train/Test 데이터 로드
- Shape 확인 (특성 수 일치 여부)
- 클래스 분포 확인

### 2. 모델 학습

#### XGBoost (기본값, 권장)
```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=100,      # 트리 개수
    max_depth=6,           # 트리 깊이
    learning_rate=0.1,     # 학습률
    random_state=42,
    eval_metric='logloss'
)
model.fit(X_train, y_train)
```

**장점**:
- ✅ 높은 성능
- ✅ 불균형 데이터 처리 강점 (`scale_pos_weight`)
- ✅ Feature importance 제공
- ✅ 정규화 내장

**사용 시기**: 대부분의 경우 (기본 추천)

#### LightGBM
```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    verbose=-1
)
model.fit(X_train, y_train)
```

**장점**:
- ✅ XGBoost보다 빠름 (대용량 데이터)
- ✅ 메모리 효율적
- ✅ 범주형 변수 직접 처리

**사용 시기**: 대용량 데이터 (100만 건 이상)

#### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
```

**장점**:
- ✅ 해석 가능
- ✅ 안정적
- ✅ 과적합 덜함

**사용 시기**: 베이스라인 모델, 해석 중요 시

### 3. 모델 평가

#### Classification Report
```
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     56864
           1       0.81      0.85      0.83        98

    accuracy                           1.00     56962
   macro avg       0.90      0.92      0.91     56962
weighted avg       1.00      1.00      1.00     56962
```

#### ROC-AUC & PR-AUC
```python
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc

# ROC-AUC
roc_auc = roc_auc_score(y_test, y_proba)

# PR-AUC (불균형 데이터에 더 적합)
precision, recall, _ = precision_recall_curve(y_test, y_proba)
pr_auc = auc(recall, precision)
```

#### Confusion Matrix
```
                Predicted
              0        1
Actual 0  56,844      20    # TN=56844, FP=20
Actual 1      15      83    # FN=15, TP=83
```

**해석**:
- **TP (True Positive)**: 83 - 사기를 사기로 정확히 예측
- **TN (True Negative)**: 56,844 - 정상을 정상으로 정확히 예측
- **FP (False Positive)**: 20 - 정상을 사기로 오판 (Type I Error)
- **FN (False Negative)**: 15 - 사기를 정상으로 오판 (Type II Error) ⚠️

### 4. 모델 저장
```python
import joblib

joblib.dump(model, 'projects/{project-name}/outputs/models/xgboost_model.pkl')
```

## Output Structure

```
projects/{project-name}/outputs/models/
├── xgboost_model.pkl           # 학습된 모델
└── preprocessing_pipeline.pkl  # 전처리 파이프라인 (이전 단계에서 생성)
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

## Algorithm Comparison

| 알고리즘 | 속도 | 성능 | 메모리 | 해석성 | 추천 순위 |
|---------|------|------|--------|--------|----------|
| **XGBoost** | 보통 | 매우 우수 | 보통 | 중간 | ⭐⭐⭐ |
| **LightGBM** | 빠름 | 매우 우수 | 우수 | 중간 | ⭐⭐ |
| **Random Forest** | 느림 | 우수 | 나쁨 | 우수 | ⭐ |

## Evaluation Metrics Guide

### 불균형 데이터 (사기 탐지, 이상 탐지)

| 지표 | 사용 여부 | 이유 |
|------|----------|------|
| **Accuracy** | ❌ 금지 | 99.83% 불균형에서 무의미 |
| **Precision** | ✅ 중요 | FP 비용 고려 |
| **Recall** | ✅ 매우 중요 | FN 비용 고려 (사기 놓치면 손실) |
| **F1-Score** | ✅ 핵심 | Precision-Recall 균형 |
| **PR-AUC** | ✅ 최적 | 불균형 데이터 최적 지표 |
| **ROC-AUC** | ⚠️ 참고 | PR-AUC보다 덜 유용 |

### 균형 데이터 (고객 이탈, 분류)

| 지표 | 사용 여부 |
|------|----------|
| **Accuracy** | ✅ 사용 가능 |
| **F1-Score** | ✅ 권장 |
| **ROC-AUC** | ✅ 권장 |

## Examples

### Example 1: 신용카드 사기 탐지 (XGBoost)
```bash
/train-model \
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
/train-model \
  --X-train-path "projects/customer-churn/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/customer-churn/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/customer-churn/data/processed/X_test.csv" \
  --y-test-path "projects/customer-churn/data/processed/y_test.csv" \
  --algorithm lightgbm
```

### Example 3: 베이스라인 모델 (Random Forest)
```bash
/train-model \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-project/data/processed/y_test.csv" \
  --algorithm random_forest
```

## Model Loading & Prediction

### 학습된 모델 로드
```python
import joblib

# 모델 로드
model = joblib.load('projects/creditcard-fraud-detection/outputs/models/xgboost_model.pkl')

# 전처리 파이프라인 로드
scaler = joblib.load('projects/creditcard-fraud-detection/outputs/models/preprocessing_pipeline.pkl')

# 신규 데이터 전처리
X_new_scaled = scaler.transform(X_new)

# 예측
y_pred = model.predict(X_new_scaled)
y_proba = model.predict_proba(X_new_scaled)[:, 1]
```

### Threshold 최적화
```python
from sklearn.metrics import precision_recall_curve
import numpy as np

# 최적 임계값 찾기 (F1-Score 최대화)
precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]

print(f"최적 임계값: {optimal_threshold:.3f}")
print(f"F1-Score: {f1_scores[optimal_idx]:.3f}")

# 예측 시 적용
y_pred_optimized = (y_proba >= optimal_threshold).astype(int)
```

## Performance Tips

### 과적합 방지
```python
# XGBoost
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,           # 너무 깊지 않게
    learning_rate=0.1,
    subsample=0.8,         # 샘플 비율
    colsample_bytree=0.8,  # 특성 비율
    reg_alpha=0.1,         # L1 정규화
    reg_lambda=1.0,        # L2 정규화
)
```

### 대용량 데이터
```python
# LightGBM 사용
model = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.1,
    num_leaves=31,        # 트리 복잡도
    max_bin=255,          # 히스토그램 bin 수
)
```

### 성능 향상
```python
# Stratified K-Fold CV
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='f1')
print(f"CV F1-Score: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

## Feature Importance Analysis

```python
import matplotlib.pyplot as plt
import xgboost as xgb

# XGBoost Feature Importance
xgb.plot_importance(model, max_num_features=20)
plt.tight_layout()
plt.savefig('projects/{project-name}/outputs/figures/feature_importance.png')

# 상위 변수 추출
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
top_features = X_train.columns[indices[:20]]
print("상위 20개 중요 변수:")
for i, feat in enumerate(top_features):
    print(f"{i+1}. {feat}: {importances[indices[i]]:.4f}")
```

## Troubleshooting

### 문제: "ValueError: Number of features mismatch"
- Train/Test 특성 개수 불일치
- 전처리 파이프라인 동일하게 적용 확인

### 문제: 과적합 (Train 성능 >> Test 성능)
```python
# max_depth 줄이기
model = xgb.XGBClassifier(max_depth=3)

# 정규화 강화
model = xgb.XGBClassifier(reg_alpha=1.0, reg_lambda=10.0)
```

### 문제: 저성능 (F1-Score < 0.5)
- 리샘플링 비율 조정 (`/balance-data --ratio 0.2`)
- 전처리 재확인 (`/engineer-features`)
- 알고리즘 변경 (Random Forest → XGBoost)

### 문제: 메모리 부족
- LightGBM 사용
- n_estimators 줄이기 (100 → 50)
- 청크 단위 학습

## Related Commands

- `/balance-data`: 클래스 불균형 처리 (학습 전 필수)
- `/engineer-features`: 특성 엔지니어링 (전처리)
- `/profile-data`: 데이터 분석

## Agents Used

- `model-trainer` (필수): 모델 학습 및 평가

## Notes

⚠️ **주의사항**:
- Train/Test 데이터 분리 확인
- 불균형 데이터는 Accuracy 지표 금지
- 전처리 파이프라인과 모델 함께 저장

💡 **팁**:
- XGBoost부터 시작 (기본 추천)
- F1-Score로 평가 (Precision-Recall 균형)
- Feature importance 확인하여 중요 변수 파악
- Threshold 최적화로 성능 향상

## Best Practices

### 1. 학습 전 체크리스트
- [ ] 데이터 전처리 완료 (`/engineer-features`)
- [ ] 클래스 불균형 처리 (`/balance-data`)
- [ ] Train/Test 분리 확인
- [ ] 특성 개수 일치 확인

### 2. 학습 후 체크리스트
- [ ] Confusion Matrix 확인
- [ ] F1-Score, PR-AUC 기록
- [ ] Feature importance 분석
- [ ] 과적합 여부 확인 (Train vs Test 성능)

### 3. 프로덕션 배포 전
- [ ] 모델 파일 저장 확인
- [ ] 전처리 파이프라인 저장 확인
- [ ] Threshold 최적화
- [ ] 성능 벤치마크 기록

## Next Steps

모델 학습 후 권장 단계:

1. **Feature Importance 분석**
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
