# 신용카드 사기 탐지 (Credit Card Fraud Detection)

## 📊 데이터셋 개요

**출처**: [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
**라이선스**: DbCL-1.0
**데이터 기간**: 2013년 9월 (유럽 카드 소지자의 2일간 거래 데이터)

### 기본 통계
- **전체 거래 건수**: 284,807건
- **특성 개수**: 31개 (Time, V1-V28, Amount, Class)
- **결측치**: 0개
- **클래스 분포**:
  - 정상 거래 (Class 0): 284,315건 (99.83%)
  - 사기 거래 (Class 1): 492건 (0.17%)
  - **불균형 비율**: 1:578

---

## 📁 데이터 구조

### 특성 설명

| 특성 | 설명 | 비고 |
|------|------|------|
| **Time** | 첫 거래 이후 경과 시간(초) | 시계열 분석 가능 |
| **V1 ~ V28** | PCA 변환된 익명화 특성 | 개인정보 보호를 위한 변환 |
| **Amount** | 거래 금액 | 원본 값 (스케일링 필요) |
| **Class** | 타겟 변수 | 0: 정상, 1: 사기 |

⚠️ **주의**: V1~V28은 PCA로 변환되어 직접적인 비즈니스 해석이 어렵습니다. 보안상의 이유로 원본 특성명과 배경 정보가 제공되지 않습니다.

---

## 🎯 프로젝트 목표

이 데이터셋은 **고도로 불균형한 이진 분류 문제**를 다루는 데이터 사이언스 파이프라인 구축을 위한 샘플입니다.

### 주요 학습 포인트

#### 1. **데이터 프로파일링 (Data Profiling)**
- [ ] 탐색적 데이터 분석 (EDA)
- [ ] 클래스 불균형 시각화
- [ ] 특성 분포 분석
- [ ] 상관관계 분석
- [ ] 이상치 탐지

#### 2. **특성 엔지니어링 (Feature Engineering)**
- [ ] Time 특성 변환 (시간대, 요일 등)
- [ ] Amount 스케일링 (StandardScaler, RobustScaler)
- [ ] 특성 선택 (Correlation, Feature Importance)
- [ ] 파생 변수 생성

#### 3. **불균형 처리 (Imbalance Handling)**
- [ ] **리샘플링 기법**:
  - SMOTE (Synthetic Minority Over-sampling Technique)
  - Random Undersampling
  - ADASYN
  - SMOTETomek (Combined)
- [ ] **알고리즘 레벨 조정**:
  - class_weight='balanced'
  - scale_pos_weight (XGBoost)
  - sample_weight
- [ ] **앙상블 기법**:
  - BalancedRandomForest
  - EasyEnsemble
  - BalancedBagging

#### 4. **모델링 (Modeling)**
- [ ] **전통적 ML 알고리즘**:
  - Logistic Regression (베이스라인)
  - Random Forest
  - XGBoost
  - LightGBM
  - CatBoost
- [ ] **이상탐지 알고리즘**:
  - Isolation Forest
  - Local Outlier Factor (LOF)
  - One-Class SVM
  - Autoencoder
- [ ] 하이퍼파라미터 튜닝 (Optuna, GridSearchCV)

#### 5. **평가 및 해석 (Evaluation & Interpretation)**
- [ ] **적합한 평가지표 사용**:
  - ⚠️ Accuracy는 부적합 (99.83% 불균형)
  - ✅ Precision, Recall, F1-Score
  - ✅ PR-AUC (Precision-Recall AUC)
  - ✅ ROC-AUC
  - ✅ Confusion Matrix
  - ✅ Cost-Sensitive Metrics
- [ ] **임계값 최적화**:
  - Precision-Recall 트레이드오프
  - 비즈니스 비용 고려 (FP vs FN)
- [ ] **모델 해석**:
  - SHAP Values
  - Feature Importance
  - LIME
  - Partial Dependence Plots

#### 6. **보고서 작성 (Reporting)**
- [ ] 비기술 이해관계자용 요약
- [ ] 모델 성능 비교표
- [ ] 비즈니스 임팩트 계산
- [ ] 배포 권장사항

---

## 🚀 데이터 사이언스 파이프라인 구조

```
Raw Data (creditcard.csv)
    ↓
data-profiling → profile_report.html
    ↓
feature-engineering → preprocessing_pipeline.pkl
    ↓
imbalance-handling → X_train_balanced.csv
    ↓
model-selection → trained_models/
    ↓
evaluation-report → evaluation_report.pdf
    ↓
deployment-package → model_api/
```

---

## 💡 주요 도전 과제

### 1. 극심한 클래스 불균형 (1:578)
- Accuracy 지표는 무의미 (모든 거래를 정상으로 예측해도 99.83% 달성)
- Precision-Recall 곡선이 ROC 곡선보다 중요
- 소수 클래스(사기)에 대한 충분한 학습 필요

### 2. 비용 민감 분류 (Cost-Sensitive Learning)
- **False Negative (사기를 정상으로 오판)**: 금전적 손실
- **False Positive (정상을 사기로 오판)**: 고객 불편, 신뢰 하락
- 비즈니스 컨텍스트에 따라 FN/FP 비용 비율 결정 필요

### 3. PCA 변환된 특성
- 원본 특성명 불명 → 도메인 지식 활용 제한
- Feature Engineering 어려움
- 모델 해석성 저하

### 4. 시간적 의존성
- Time 변수 존재 → 시계열 특성 고려
- Train/Test Split 시 시간 순서 보존 필요
- 시간대별 사기 패턴 존재 가능성

---

## 📈 예상 성능 벤치마크

| 모델 | Precision | Recall | F1-Score | PR-AUC |
|------|-----------|--------|----------|--------|
| Baseline (모두 정상 예측) | - | 0% | - | - |
| Logistic Regression | ~0.85 | ~0.60 | ~0.70 | ~0.75 |
| Random Forest | ~0.90 | ~0.75 | ~0.82 | ~0.85 |
| XGBoost + SMOTE | ~0.92 | ~0.80 | ~0.86 | ~0.90 |
| Isolation Forest | ~0.25 | ~0.30 | ~0.27 | ~0.60 |

*실제 성능은 전처리, 하이퍼파라미터, 불균형 처리 전략에 따라 달라질 수 있습니다.*

---

## 🔧 사용 예시

### 데이터 로드
```python
import pandas as pd
import numpy as np

# 데이터 로드
df = pd.read_csv('creditcard.csv')

# 특성과 타겟 분리
X = df.drop('Class', axis=1)
y = df['Class']

# Train/Test 분리 (시간 순서 보존)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### SMOTE 적용
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

### 모델 학습 및 평가
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 모델 학습
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train_balanced, y_train_balanced)

# 예측 및 평가
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
```

---

## 📚 참고 자료

- [Kaggle 데이터셋 페이지](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- [imbalanced-learn 공식 문서](https://imbalanced-learn.org/)
- [SMOTE 논문](https://arxiv.org/abs/1106.1813)
- [Cost-Sensitive Learning](https://machinelearningmastery.com/cost-sensitive-learning-for-imbalanced-classification/)

---

## 📝 라이선스

데이터셋은 Database Contents License (DbCL v1.0) 하에 배포됩니다.

**인용**:
```
Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson and Gianluca Bontempi.
Calibrating Probability with Undersampling for Unbalanced Classification.
In Symposium on Computational Intelligence and Data Mining (CIDM), IEEE, 2015
```

---

**생성일**: 2026-01-31
**프로젝트**: DanteLabs Agentic School - Data Science Plugin
