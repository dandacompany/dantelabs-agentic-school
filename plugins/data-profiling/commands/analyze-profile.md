---
name: analyze-profile
description: 프로파일링 리포트를 분석하여 데이터 전처리, 추가 분석, 모델링 지침이 담긴 EDA 레포트를 생성합니다.
arguments:
  - name: profile-path
    description: 프로파일링 HTML 리포트 파일 경로
    required: true
  - name: data-path
    description: 원본 데이터 파일 경로 (추가 분석용)
    required: true
  - name: target-column
    description: 타겟 변수 컬럼명
    required: false
  - name: output-format
    description: 출력 형식 (markdown, pdf)
    required: false
    default: "markdown"
  - name: output-dir
    description: 리포트 저장 디렉토리
    required: false
    default: "projects/{project-name}/outputs/reports"
---

# /analyze-profile

프로파일링 리포트를 심층 분석하여 실행 가능한 데이터 전처리, 추가 분석, 모델링 지침을 담은 A4 한 장 분량의 EDA 레포트를 생성합니다.

## Usage

```bash
# 기본 사용법
/analyze-profile \
  --profile-path "projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html" \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv"

# 타겟 컬럼 지정
/analyze-profile \
  --profile-path "projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html" \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# PDF 형식으로 출력
/analyze-profile \
  --profile-path "projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html" \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --output-format pdf
```

## What This Command Does

### 1. 프로파일링 리포트 분석
- HTML 리포트에서 주요 통계 정보 추출
- Alerts 섹션 분석 (데이터 품질 이슈)
- 변수별 분포 특성 파악
- 상관관계 매트릭스 분석

### 2. 원본 데이터 추가 분석
- 클래스 불균형 정량화
- 이상치 탐지 및 영향도 평가
- 변수 간 관계 심층 분석
- 시계열 패턴 확인 (해당되는 경우)

### 3. 실행 가능한 지침 생성
다음 3가지 관점에서 구체적인 액션 아이템 제시:

#### 📋 데이터 전처리 관점
- 결측치 처리 전략 (Imputation, Deletion)
- 이상치 처리 방법 (Capping, Transformation, Removal)
- 스케일링 전략 (StandardScaler, MinMaxScaler, RobustScaler)
- 인코딩 전략 (One-hot, Label, Target encoding)
- 데이터 타입 변환

#### 🔍 추가 분석 관점
- 변수 간 상호작용 탐색
- 파생 변수 생성 아이디어
- 세그먼트별 분석 (타겟별, 카테고리별)
- 시계열 분해 (Trend, Seasonality, Residual)
- 다변량 분석 (PCA, t-SNE)

#### 🤖 모델링 관점
- 적합한 알고리즘 추천 (분류/회귀/클러스터링)
- 클래스 불균형 처리 전략 (SMOTE, Undersampling, Class weights)
- Feature selection 방법
- 교차 검증 전략
- 평가 지표 선정 (Accuracy, Precision, Recall, F1, ROC-AUC)
- 하이퍼파라미터 튜닝 우선순위

### 4. A4 한 장 분량 레포트 생성
- **파일명**: `{dataset_name}_eda_report.md` (또는 `.pdf`)
- **위치**: `projects/{project-name}/outputs/reports/`
- **구조**:
  - Executive Summary (핵심 요약)
  - 데이터 개요
  - 주요 발견사항
  - 데이터 전처리 지침
  - 추가 분석 권고사항
  - 모델링 전략
  - 다음 단계 (Next Steps)

## Output Structure

### Markdown 리포트 예시

```markdown
# EDA 분석 리포트: 신용카드 사기 탐지

**생성일**: 2026-01-31
**분석 대상**: creditcard.csv (284,807건)

---

## 📊 Executive Summary

- **주요 과제**: 극심한 클래스 불균형 (1:578)
- **핵심 발견**: Amount 변수 스케일 차이, Time 변수 활용 가능
- **우선 조치**: SMOTE + RobustScaler + XGBoost 조합 권장
- **예상 성능**: F1-Score 0.85+ 달성 가능

---

## 📋 데이터 개요

| 항목 | 값 |
|------|-----|
| 전체 건수 | 284,807건 |
| 특성 개수 | 31개 (Time, V1-V28, Amount, Class) |
| 결측치 | 0개 |
| 중복 | 0건 |
| 메모리 | 67.4 MB |

**타겟 분포**:
- 정상 거래: 284,315건 (99.83%)
- 사기 거래: 492건 (0.17%)
- 불균형 비율: **1:578** ⚠️

---

## 🔍 주요 발견사항

### 1. 클래스 불균형 (Critical)
- 사기 거래가 전체의 0.17%에 불과
- Accuracy 지표는 무의미 (모두 정상으로 예측해도 99.83%)
- Precision-Recall 곡선 중심의 평가 필요

### 2. 변수 스케일 차이
- Amount: 0 ~ 25,691 (평균 88.3, 표준편차 250.1)
- V1-V28: PCA 변환됨 (표준화된 범위)
- **스케일 차이**: 최대/최소 = 1,143,543배

### 3. PCA 변환된 특성
- V1-V28은 원본 특성명 불명
- 직접적인 비즈니스 해석 어려움
- Feature importance 분석으로 중요 변수 식별 필요

### 4. 시간 정보
- Time: 첫 거래 이후 경과 시간(초)
- 0 ~ 172,792초 (약 48시간)
- 시간대별 사기 패턴 존재 가능성

---

## 📋 데이터 전처리 지침

### 1. 스케일링 (Priority: High)
```python
from sklearn.preprocessing import RobustScaler

# Amount 변수만 스케일링 (V1-V28은 이미 정규화됨)
scaler = RobustScaler()  # 이상치에 강건
X['Amount_scaled'] = scaler.fit_transform(X[['Amount']])
X = X.drop('Amount', axis=1)
```

**선택 이유**:
- RobustScaler: 이상치 영향 최소화 (Amount에 극단값 존재)
- V1-V28은 이미 PCA로 표준화되어 추가 스케일링 불필요

### 2. 특성 엔지니어링
```python
# Time을 시간대로 변환
X['Hour'] = (X['Time'] / 3600) % 24
X['Day'] = (X['Time'] / 86400).astype(int)

# 주기성 인코딩 (Cyclical encoding)
import numpy as np
X['Hour_sin'] = np.sin(2 * np.pi * X['Hour'] / 24)
X['Hour_cos'] = np.cos(2 * np.pi * X['Hour'] / 24)
```

### 3. 클래스 불균형 처리 (Priority: Critical)

**옵션 A: SMOTE (권장)**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

**옵션 B: Class weights**
```python
from sklearn.ensemble import RandomForestClassifier

# 불균형 비율 계산
scale_pos_weight = (y == 0).sum() / (y == 1).sum()  # 578

model = RandomForestClassifier(
    class_weight='balanced',  # 또는 {0: 1, 1: 578}
    random_state=42
)
```

**권장**: SMOTE + Class weights 조합

---

## 🔍 추가 분석 권고사항

### 1. Feature Importance 분석
```python
# XGBoost로 변수 중요도 파악
import xgboost as xgb

model = xgb.XGBClassifier(scale_pos_weight=578)
model.fit(X_train, y_train)

# 상위 10개 중요 변수 시각화
xgb.plot_importance(model, max_num_features=10)
```

**목적**: V1-V28 중 어떤 변수가 사기 탐지에 중요한지 파악

### 2. 시간대별 패턴 분석
```python
# 시간대별 사기 비율 분석
fraud_by_hour = df.groupby('Hour')['Class'].mean()
fraud_by_hour.plot(kind='bar', title='Fraud Rate by Hour')
```

**가설**: 특정 시간대(심야)에 사기 거래 집중 가능성

### 3. Amount 세그먼트별 분석
```python
# 금액대별 사기 비율
df['Amount_bin'] = pd.cut(df['Amount'], bins=[0, 10, 50, 100, 500, np.inf])
df.groupby('Amount_bin')['Class'].mean()
```

### 4. SHAP 분석 (모델 학습 후)
```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

**목적**: 사기 예측에 기여하는 변수와 방향성 이해

---

## 🤖 모델링 전략

### 1. 알고리즘 선택

**추천 순위**:
1. **XGBoost** (1순위)
   - 불균형 데이터 처리 강점 (`scale_pos_weight`)
   - Feature importance 제공
   - 높은 성능

2. **LightGBM** (2순위)
   - XGBoost보다 빠름
   - 대용량 데이터 효율적

3. **Random Forest** (베이스라인)
   - 해석 가능
   - 안정적 성능

**비추천**: Logistic Regression (선형 관계 가정, 불균형 취약)

### 2. 평가 지표

**절대 금지**: Accuracy (99.83% 불균형)

**권장 지표**:
- **Precision**: False Positive 비용 중요 시
- **Recall**: False Negative 비용 중요 시 (사기 놓치면 손실)
- **F1-Score**: Precision-Recall 균형
- **PR-AUC**: 불균형 데이터 최적 (ROC-AUC보다 유리)

**비즈니스 관점**:
- FN(사기를 정상으로 오판) > FP(정상을 사기로 오판)
- Recall 우선, 단 Precision 최소 0.8 이상 유지

### 3. 교차 검증

```python
from sklearn.model_selection import StratifiedKFold

# 클래스 비율 유지하며 5-fold CV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_idx, val_idx in cv.split(X, y):
    X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
    y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]
    # 학습 및 평가
```

### 4. 하이퍼파라미터 튜닝 (Optuna)

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'scale_pos_weight': 578,
    }
    model = xgb.XGBClassifier(**params)
    # ... 학습 및 평가
    return f1_score  # 최적화 목표

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
```

### 5. Threshold 최적화

```python
from sklearn.metrics import precision_recall_curve

# 최적 임계값 찾기
precision, recall, thresholds = precision_recall_curve(y_val, y_proba)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_threshold = thresholds[np.argmax(f1_scores)]

# 예측 시 적용
y_pred = (y_proba >= optimal_threshold).astype(int)
```

---

## 📌 다음 단계 (Next Steps)

### 우선순위 1 (즉시 실행)
- [ ] `/engineer-features`: Amount 스케일링, Time 특성 추출
- [ ] `/handle-imbalance`: SMOTE 적용 (sampling_strategy=0.1)
- [ ] `/train-models`: XGBoost 베이스라인 모델 학습

### 우선순위 2 (모델 학습 후)
- [ ] Feature importance 분석 → 상위 20개 변수 선택
- [ ] SHAP 분석 → 사기 패턴 이해
- [ ] Threshold 최적화 → Recall 0.9, Precision 0.8 목표

### 우선순위 3 (성능 개선)
- [ ] Optuna 하이퍼파라미터 튜닝
- [ ] Ensemble (XGBoost + LightGBM + RF)
- [ ] 시간대별 모델 (심야 vs 주간)

---

## 📈 예상 성능

| 모델 | 예상 F1-Score | 예상 PR-AUC |
|------|--------------|------------|
| Baseline (Logistic) | 0.65 | 0.70 |
| Random Forest + SMOTE | 0.80 | 0.85 |
| **XGBoost + SMOTE** | **0.85-0.90** | **0.90-0.95** |
| Ensemble | 0.90+ | 0.95+ |

**근거**: Kaggle 벤치마크 참조 (동일 데이터셋)

---

**생성일**: 2026-01-31
**분석 도구**: ydata-profiling v4.18.1
**다음 커맨드**: `/engineer-features`, `/handle-imbalance`, `/train-models`
```

---

## Related Commands

- `/profile-data`: 데이터 프로파일링 리포트 생성
- `/engineer-features`: 특성 엔지니어링
- `/handle-imbalance`: 클래스 불균형 처리
- `/train-models`: 모델 학습

## Agents Used

- `eda-analyst` (필수): 프로파일링 리포트 심층 분석

## Notes

⚠️ **주의사항**:
- HTML 리포트가 먼저 생성되어 있어야 함 (`/profile-data` 실행 필요)
- PDF 출력은 pandoc 설치 필요: `brew install pandoc`

💡 **팁**:
- 이 레포트를 기반으로 데이터 전처리 우선순위 결정
- 코드 스니펫을 복사하여 즉시 실행 가능
- 비즈니스 요구사항에 맞게 평가지표 조정
