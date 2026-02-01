# Hyperparameter Tuning Plugin

Optuna를 사용한 자동 하이퍼파라미터 최적화 플러그인입니다.

## 📋 개요

이 플러그인은 베이지안 최적화를 사용하여 자동으로 최적의 하이퍼파라미터를 찾습니다:

- ✅ **Optuna 프레임워크**: TPE Sampler + Median Pruner
- ✅ **알고리즘 지원**: XGBoost, LightGBM, Random Forest
- ✅ **최적화 지표**: F1-Score, ROC-AUC, PR-AUC
- ✅ **교차 검증**: Stratified 5-Fold CV
- ✅ **조기 종료**: 성능 낮은 시도 자동 중단

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd plugins/hyperparameter-tuning/skills/tuning
uv pip install --system -r requirements.txt
```

### 2. 하이퍼파라미터 튜닝

```bash
python scripts/tune_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --algorithm xgboost \
  --metric f1 \
  --n-trials 50
```

## 📁 플러그인 구조

```
plugins/hyperparameter-tuning/
├── plugin.json
├── README.md
├── commands/
│   └── tune-hyperparameters.md
└── skills/
    └── tuning/
        ├── requirements.txt
        └── scripts/
            └── tune_model.py
```

## 🎯 주요 기능

### 1. Optuna 최적화
- **TPE Sampler**: 효율적인 베이지안 최적화
- **Median Pruner**: 성능 낮은 시도 조기 종료
- **Random Search보다 10-100배 빠름**

### 2. 지원 알고리즘

| 알고리즘 | 튜닝 파라미터 수 | 권장 trials |
|---------|---------------|------------|
| **XGBoost** | 8개 | 50-100 |
| **LightGBM** | 9개 | 50-100 |
| **Random Forest** | 5개 | 30-50 |

### 3. 최적화 지표

| 지표 | 사용 시기 |
|------|---------|
| **f1** | 불균형 데이터 (기본 권장) |
| **pr_auc** | 극심한 불균형 |
| **roc_auc** | 균형 데이터 |

## 📊 출력

### 튜닝된 모델
```
projects/{project-name}/outputs/models/
├── xgboost_tuned_model.pkl         # 최적 모델
├── xgboost_tuning_history.csv      # 최적화 이력
└── xgboost_best_params.txt         # 최적 파라미터
```

### 최적 파라미터 파일
```
Algorithm: xgboost
Metric: f1
Best F1: 0.8567

Best Parameters:
  n_estimators: 150
  max_depth: 6
  learning_rate: 0.0856
  subsample: 0.85
  colsample_bytree: 0.92
  reg_alpha: 0.0023
  reg_lambda: 1.234
  min_child_weight: 3

Optimization Date: 2026-01-31 13:00:00
```

## 🔧 사용 예시

### Example 1: 신용카드 사기 탐지 튜닝
```bash
python tune_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --algorithm xgboost \
  --metric pr_auc \
  --n-trials 50
```

**예상 개선**:
- 기본 모델 F1: 0.83
- 튜닝 후 F1: 0.85-0.87
- **2-4% 성능 향상**

### Example 2: 빠른 프로토타입 (20 trials, 30분)
```bash
python tune_model.py \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --n-trials 20 \
  --timeout 1800
```

### Example 3: 정밀 튜닝 (100 trials, 3시간)
```bash
python tune_model.py \
  --X-train-path "projects/my-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-project/data/processed/y_train_balanced.csv" \
  --algorithm lightgbm \
  --n-trials 100 \
  --metric f1
```

## 📈 n-trials 가이드

| 데이터 크기 | 권장 trials | 예상 시간 (XGBoost) |
|-----------|------------|-------------------|
| < 10,000건 | 100 | ~30분 |
| 10K - 100K | 50 | ~1시간 |
| 100K - 1M | 30 | ~2시간 |
| > 1M | 20 | ~3시간 |

## 🎨 최적화 이력 시각화

### Python 예제
```python
import pandas as pd
import matplotlib.pyplot as plt

# 이력 로드
df = pd.read_csv('projects/my-project/outputs/models/xgboost_tuning_history.csv')

# 최적화 진행 과정
plt.figure(figsize=(10, 6))
plt.plot(df['number'], df['value'], marker='o')
plt.xlabel('Trial Number')
plt.ylabel('F1 Score')
plt.title('Hyperparameter Optimization Progress')
plt.grid(True)
plt.savefig('optimization_progress.png')

# 최고 성능 trial
best_trial = df.loc[df['value'].idxmax()]
print(f"Best Trial #{best_trial['number']}: F1 = {best_trial['value']:.4f}")
```

## 🐛 트러블슈팅

### 문제: 최적화가 너무 오래 걸림
**해결**:
```bash
# timeout 설정
--timeout 3600  # 1시간

# trials 줄이기
--n-trials 20

# LightGBM 사용 (더 빠름)
--algorithm lightgbm
```

### 문제: 메모리 부족
**해결**:
- 데이터 샘플링
- LightGBM 사용
- K-Fold 수 줄이기 (스크립트 수정)

### 문제: 성능 개선 없음
**해결**:
- trials 늘리기 (50 → 100)
- 다른 metric 시도
- 데이터 전처리 재확인

## 🔗 관련 플러그인

- `model-selection`: 기본 모델 학습
- `imbalance-handling`: 클래스 불균형 처리 (튜닝 전)
- `feature-engineering`: 특성 엔지니어링 (튜닝 전)

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0

## 💡 Best Practices

### 튜닝 전 준비
- [ ] 데이터 전처리 완료
- [ ] 클래스 불균형 처리
- [ ] 베이스라인 모델 성능 기록

### 튜닝 전략
- [ ] 프로토타입: 20 trials, 30분
- [ ] 일반: 50 trials, 1-2시간
- [ ] 프로덕션: 100 trials, 3-4시간

### 튜닝 후 검증
- [ ] 최적 파라미터 확인
- [ ] Test 데이터로 검증
- [ ] 과적합 여부 확인
- [ ] 베이스라인 대비 개선율 기록
