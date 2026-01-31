# EDA 분석 리포트: creditcard

**생성일**: 2026-01-31 08:08
**분석 대상**: creditcard (284,807건)
**문제 유형**: Classification

---

## 📊 Executive Summary

- 극심한 클래스 불균형 (1:578)
- 변수 스케일 차이 (1143543배)
- 시간 변수 활용 가능

---

## 📋 데이터 개요

| 항목 | 값 |
|------|-----|
| 전체 건수 | 284,807건 |
| 특성 개수 | 31개 |
| 결측치 | 0개 |
| 중복 | 1,081건 |
| 메모리 | 67.4 MB |
| 수치형 변수 | 31개 |
| 범주형 변수 | 0개 |

**타겟 분포** (`Class`):
- 클래스 0: 284,315건 (99.83%)
- 클래스 1: 492건 (0.17%)
- 불균형 비율: **1:578** ⚠️

---

## 🔍 주요 발견사항

### 1. 클래스 불균형 (Critical)
사기 거래가 전체의 0.17%에 불과합니다. Accuracy 지표는 무의미하며, Precision-Recall 중심 평가가 필요합니다.

### 2. 변수 스케일 차이 (High)
변수 간 스케일 차이가 1143543배입니다. 스케일링 필수입니다.

---

## 📋 데이터 전처리 지침

### High Priority: 스케일링

변수 간 스케일 차이가 큽니다 (최대/최소 = 1143543배)

```python
from sklearn.preprocessing import RobustScaler

# 이상치에 강건한 RobustScaler 권장
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X[numeric_cols])
```

### Critical Priority: 클래스 불균형 처리

불균형 비율 1:578

```python
from imblearn.over_sampling import SMOTE

# SMOTE로 소수 클래스 오버샘플링
smote = SMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 또는 Class weights 조정
from xgboost import XGBClassifier
model = XGBClassifier(scale_pos_weight=578)
```

---

## 🔍 추가 분석 권고사항

### 1. Feature Importance 분석

중요 변수 식별 및 차원 축소

```python
import xgboost as xgb

model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# 변수 중요도 시각화
xgb.plot_importance(model, max_num_features=15)
plt.tight_layout()
plt.show()

# 상위 변수만 선택
from sklearn.feature_selection import SelectFromModel
selector = SelectFromModel(model, prefit=True, threshold='median')
X_selected = selector.transform(X)
```

### 2. 시간 특성 추출

Time 변수에서 유용한 파생 변수 생성

```python
# 시간대 추출
X['Hour'] = (X['Time'] / 3600) % 24
X['Day'] = (X['Time'] / 86400).astype(int)

# 주기성 인코딩 (Cyclical encoding)
X['Hour_sin'] = np.sin(2 * np.pi * X['Hour'] / 24)
X['Hour_cos'] = np.cos(2 * np.pi * X['Hour'] / 24)

# 시간대별 패턴 분석
fraud_by_hour = df.groupby('Hour')['Class'].mean()
fraud_by_hour.plot(kind='bar', title='Target Rate by Hour')
```

### 3. SHAP 분석 (모델 해석)

예측에 기여하는 변수와 방향성 이해

```python
import shap

# Tree 기반 모델용
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test)

# Force plot (개별 예측 설명)
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

---

## 🤖 모델링 전략

### 추천 알고리즘

**1순위: XGBoost**
- 선택 이유: 불균형 데이터 강점, Feature importance

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=578,  # 불균형 비율
    random_state=42
)
model.fit(X_train, y_train)
```

**2순위: LightGBM**
- 선택 이유: 빠른 학습 속도, 대용량 데이터 효율

```python
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    n_estimators=100,
    is_unbalance=True,  # 불균형 자동 처리
    random_state=42
)
model.fit(X_train, y_train)
```

**3순위: Random Forest**
- 선택 이유: 안정적 성능, 해석 가능

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)
```

### 평가 지표

- **F1-Score** (Precision-Recall 균형)
- **PR-AUC** (불균형 데이터 최적)
- **Recall** (False Negative 비용 높음)
- **Precision** (False Positive 비용 높음)
- ⚠️ Accuracy 사용 금지 (불균형으로 무의미)

### 교차 검증

```python
from sklearn.model_selection import StratifiedKFold

# 클래스 비율 유지하며 5-fold CV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

---

## 📌 다음 단계 (Next Steps)

### 우선순위 1 (즉시 실행)
- [ ] 데이터 전처리: `/engineer-features`
- [ ] 클래스 불균형 처리: `/handle-imbalance --method smote`
- [ ] 베이스라인 모델 학습: `/train-models --algorithms xgboost`

### 우선순위 2 (모델 학습 후)
- [ ] Feature importance 분석
- [ ] SHAP 분석으로 모델 해석
- [ ] Threshold 최적화

### 우선순위 3 (성능 개선)
- [ ] 하이퍼파라미터 튜닝 (Optuna)
- [ ] Ensemble 모델
- [ ] 추가 특성 엔지니어링

---

**생성 도구**: data-profiling plugin v1.0.0
**다음 커맨드**: `/engineer-features`, `/handle-imbalance`, `/train-models`
