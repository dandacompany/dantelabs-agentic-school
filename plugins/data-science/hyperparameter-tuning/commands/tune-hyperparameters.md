---
name: tune-hyperparameters
description: Optuna를 사용하여 자동으로 최적의 하이퍼파라미터를 찾습니다.
arguments:
  - name: X-train-path
    description: Train 특성 데이터 파일 경로
    required: true
  - name: y-train-path
    description: Train 타겟 데이터 파일 경로
    required: true
  - name: algorithm
    description: 튜닝할 알고리즘 (xgboost, lightgbm, random_forest)
    required: false
    default: "xgboost"
  - name: metric
    description: 최적화 지표 (f1, roc_auc, pr_auc)
    required: false
    default: "f1"
  - name: n-trials
    description: 최적화 시도 횟수
    required: false
    default: "50"
  - name: timeout
    description: 최적화 제한 시간 (초)
    required: false
  - name: output-dir
    description: 모델 저장 디렉토리
    required: false
    default: "projects/{project-name}/outputs/models"
---

# /tune-hyperparameters

Optuna를 사용하여 자동으로 최적의 하이퍼파라미터를 찾고 최고 성능의 모델을 학습합니다.

## Usage

```bash
# XGBoost 튜닝 (기본값)
/tune-hyperparameters \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv"

# LightGBM 튜닝 with PR-AUC
/tune-hyperparameters \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --algorithm lightgbm \
  --metric pr_auc

# 100회 시도
/tune-hyperparameters \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --algorithm xgboost \
  --n-trials 100

# 시간 제한 (3600초 = 1시간)
/tune-hyperparameters \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --timeout 3600
```

## What This Command Does

### 1. Optuna 최적화 프레임워크
- **TPE Sampler**: Tree-structured Parzen Estimator (효율적 탐색)
- **Median Pruner**: 성능 낮은 시도 조기 종료
- **Stratified K-Fold CV**: 5-Fold 교차 검증

### 2. 최적화 대상 하이퍼파라미터

#### XGBoost
```python
{
    'n_estimators': [50, 300],        # 트리 개수
    'max_depth': [3, 10],             # 트리 깊이
    'learning_rate': [0.01, 0.3],     # 학습률
    'subsample': [0.6, 1.0],          # 샘플 비율
    'colsample_bytree': [0.6, 1.0],   # 특성 비율
    'reg_alpha': [1e-8, 10.0],        # L1 정규화
    'reg_lambda': [1e-8, 10.0],       # L2 정규화
    'min_child_weight': [1, 10]       # 최소 샘플 가중치
}
```

#### LightGBM
```python
{
    'n_estimators': [50, 300],
    'max_depth': [3, 10],
    'learning_rate': [0.01, 0.3],
    'num_leaves': [20, 100],          # 리프 개수
    'subsample': [0.6, 1.0],
    'colsample_bytree': [0.6, 1.0],
    'reg_alpha': [1e-8, 10.0],
    'reg_lambda': [1e-8, 10.0],
    'min_child_samples': [5, 50]      # 최소 샘플 수
}
```

#### Random Forest
```python
{
    'n_estimators': [50, 300],
    'max_depth': [5, 30],
    'min_samples_split': [2, 20],     # 분할 최소 샘플
    'min_samples_leaf': [1, 10],      # 리프 최소 샘플
    'max_features': ['sqrt', 'log2', None]
}
```

### 3. 최적화 지표

| 지표 | 사용 시기 | 설명 |
|------|---------|------|
| **f1** | 불균형 데이터 (기본 권장) | Precision-Recall 균형 |
| **pr_auc** | 극심한 불균형 | PR 곡선 아래 면적 |
| **roc_auc** | 균형 데이터 | ROC 곡선 아래 면적 |

### 4. 출력

#### 튜닝된 모델
```
projects/{project-name}/outputs/models/
├── xgboost_tuned_model.pkl         # 최적 모델
├── xgboost_tuning_history.csv      # 최적화 이력
└── xgboost_best_params.txt         # 최적 파라미터
```

#### 콘솔 출력
```
============================================================
하이퍼파라미터 튜닝 시작
============================================================

데이터 로드 중...
✓ Train: 250,196건 × 33개 특성

최적화 시작 (알고리즘: xgboost, 지표: f1)
시도 횟수: 50

[I 2026-01-31 12:00:00,000] Trial 0 finished with value: 0.8156
[I 2026-01-31 12:01:15,000] Trial 1 finished with value: 0.8234
[I 2026-01-31 12:02:30,000] Trial 2 finished with value: 0.8312
...
[I 2026-01-31 13:00:00,000] Trial 49 finished with value: 0.8567

============================================================
최적화 완료
============================================================

최고 F1: 0.8567

최적 하이퍼파라미터:
  n_estimators: 150
  max_depth: 6
  learning_rate: 0.0856
  subsample: 0.85
  colsample_bytree: 0.92
  reg_alpha: 0.0023
  reg_lambda: 1.234
  min_child_weight: 3

최적 파라미터로 최종 모델 학습 중...
✓ 학습 완료

✓ 모델 저장: projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl
✓ 최적화 이력 저장: projects/creditcard-fraud-detection/outputs/models/xgboost_tuning_history.csv
✓ 최적 파라미터 저장: projects/creditcard-fraud-detection/outputs/models/xgboost_best_params.txt

============================================================
하이퍼파라미터 튜닝 완료
============================================================

📊 최고 성능: F1 = 0.8567
📁 모델: projects/creditcard-fraud-detection/outputs/models/xgboost_tuned_model.pkl
📁 이력: projects/creditcard-fraud-detection/outputs/models/xgboost_tuning_history.csv
📁 파라미터: projects/creditcard-fraud-detection/outputs/models/xgboost_best_params.txt
```

## Optimization Strategy

### TPE (Tree-structured Parzen Estimator)
- 베이지안 최적화 기반
- 이전 시도 결과를 학습하여 효율적 탐색
- Random Search보다 10-100배 빠름

### Median Pruning
- 성능 낮은 시도 조기 종료
- 계산 자원 절약
- 빠른 수렴

### 5-Fold Cross Validation
- 과적합 방지
- 안정적인 성능 추정
- Stratified로 클래스 비율 유지

## Performance Tips

### n-trials 설정 가이드

| 데이터 크기 | 권장 trials | 예상 시간 (XGBoost) |
|-----------|------------|-------------------|
| < 10,000건 | 100 | ~30분 |
| 10K - 100K | 50 | ~1시간 |
| 100K - 1M | 30 | ~2시간 |
| > 1M | 20 | ~3시간 |

### 빠른 튜닝 (프로토타입)
```bash
/tune-hyperparameters \
  --X-train-path "..." \
  --y-train-path "..." \
  --n-trials 20 \
  --timeout 1800  # 30분
```

### 정밀 튜닝 (프로덕션)
```bash
/tune-hyperparameters \
  --X-train-path "..." \
  --y-train-path "..." \
  --n-trials 100 \
  --metric pr_auc
```

## Examples

### Example 1: 신용카드 사기 탐지
```bash
/tune-hyperparameters \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --algorithm xgboost \
  --metric pr_auc \
  --n-trials 50
```

**예상 개선**:
- 기본 모델 F1: 0.83 → 튜닝 후: 0.85-0.87
- 약 2-4% 성능 향상

### Example 2: LightGBM 빠른 튜닝
```bash
/tune-hyperparameters \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --algorithm lightgbm \
  --n-trials 30 \
  --timeout 3600
```

### Example 3: Random Forest 정밀 튜닝
```bash
/tune-hyperparameters \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --algorithm random_forest \
  --metric f1 \
  --n-trials 100
```

## Tuning History Analysis

### CSV 파일 구조
```csv
number,value,datetime_start,datetime_complete,duration,params_n_estimators,params_max_depth,...
0,0.8156,2026-01-31 12:00:00,2026-01-31 12:01:15,75.2,100,6,...
1,0.8234,2026-01-31 12:01:15,2026-01-31 12:02:30,75.1,150,5,...
...
```

### 시각화 예제
```python
import pandas as pd
import matplotlib.pyplot as plt

# 이력 로드
df = pd.read_csv('xgboost_tuning_history.csv')

# 최적화 진행 과정
plt.figure(figsize=(10, 6))
plt.plot(df['number'], df['value'])
plt.xlabel('Trial')
plt.ylabel('F1 Score')
plt.title('Hyperparameter Optimization Progress')
plt.savefig('optimization_progress.png')
```

## Troubleshooting

### 문제: 최적화가 너무 오래 걸림
**해결**:
- `--timeout` 설정 (예: 3600초)
- `--n-trials` 줄이기 (50 → 20)
- LightGBM 사용 (XGBoost보다 빠름)

### 문제: 메모리 부족
**해결**:
- K-Fold 수 줄이기 (스크립트 수정: 5 → 3)
- 데이터 샘플링
- LightGBM 사용

### 문제: 성능 개선 없음
**해결**:
- `--n-trials` 늘리기 (50 → 100)
- 다른 `--metric` 시도
- 데이터 전처리 재확인

## Related Commands

- `/train-model`: 기본 모델 학습
- `/balance-data`: 클래스 불균형 처리 (튜닝 전)
- `/engineer-features`: 특성 엔지니어링 (튜닝 전)

## Agents Used

- `hyperparameter-tuner` (필수): Optuna 기반 자동 최적화

## Notes

⚠️ **주의사항**:
- 튜닝은 시간이 오래 걸림 (1-3시간)
- 충분한 메모리 확보 필요
- 튜닝 전 `/balance-data` 필수

💡 **팁**:
- 프로토타입: 20 trials, 30분
- 프로덕션: 50-100 trials, 1-3시간
- PR-AUC로 최적화 (불균형 데이터)
- 튜닝 이력 CSV로 분석

## Best Practices

### 1. 튜닝 전 준비
- [ ] 데이터 전처리 완료
- [ ] 클래스 불균형 처리
- [ ] 베이스라인 모델 성능 확인

### 2. 튜닝 중
- [ ] n-trials 적절히 설정 (20-100)
- [ ] timeout 설정 (과도한 시간 방지)
- [ ] 적절한 metric 선택

### 3. 튜닝 후
- [ ] 최적 파라미터 확인
- [ ] 튜닝 이력 분석
- [ ] Test 데이터로 최종 검증
- [ ] 과적합 여부 확인
