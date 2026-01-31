# 빠른 시작 가이드 (Quick Start)

## 1️⃣ 환경 설정

### uv 패키지 매니저 설치 (권장 ⚡)

```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 macOS
brew install uv
```

### 패키지 설치

**방법 1: uv 사용 (권장 - 10-100배 빠름)**:
```bash
cd samples/datascience

# requirements.txt로 한 번에 설치
uv pip install -r requirements.txt
```

**방법 2: pip 사용 (기존 방식)**:
```bash
cd samples/datascience

# requirements.txt로 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install pandas numpy matplotlib seaborn plotly \
    scikit-learn xgboost lightgbm catboost optuna \
    imbalanced-learn shap lime ydata-profiling \
    jupyter notebook ipywidgets
```

**💡 팁**: uv를 사용하면 ydata-profiling 같은 대용량 패키지도 10초 안에 설치됩니다!

---

## 2️⃣ 데이터 확인

### 데이터 위치
```
samples/datascience/data/raw/creditcard.csv
```

### 기본 정보 확인
```bash
cd samples/datascience
python -c "
import pandas as pd
df = pd.read_csv('data/raw/creditcard.csv')
print(f'전체 거래: {len(df):,}건')
print(f'사기 거래: {df[\"Class\"].sum():,}건 ({df[\"Class\"].mean()*100:.2f}%)')
"
```

**출력 예시**:
```
전체 거래: 284,807건
사기 거래: 492건 (0.17%)
```

---

## 3️⃣ 데이터 프로파일링

### 자동화된 EDA 리포트 생성
```bash
python scripts/01_data_profiling.py
```

**출력**:
- `outputs/reports/data_profile_report.html`
- 브라우저에서 열기: `open outputs/reports/data_profile_report.html`

**포함 내용**:
- 각 변수별 분포, 통계
- 상관관계 매트릭스
- 결측치 분석
- 이상치 탐지
- 시계열 패턴

---

## 4️⃣ 간단한 베이스라인 모델

### Python 스크립트로 실행
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# 데이터 로드
df = pd.read_csv('data/raw/creditcard.csv')
X = df.drop('Class', axis=1)
y = df['Class']

# Train/Test 분리 (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 베이스라인 모델 (Logistic Regression)
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

# 평가
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("=" * 60)
print("베이스라인 모델 성능 (Logistic Regression)")
print("=" * 60)
print(classification_report(y_test, y_pred))
print(f"\nROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
```

**예상 출력**:
```
              precision    recall  f1-score   support

           0       1.00      0.98      0.99     56864
           1       0.06      0.92      0.11        98

    accuracy                           0.98     56962
   macro avg       0.53      0.95      0.55     56962
weighted avg       1.00      0.98      0.99     56962

ROC-AUC: 0.9763
```

⚠️ **주의**: Precision이 낮은 이유는 불균형 때문. 다음 단계에서 개선!

---

## 5️⃣ SMOTE 적용 예시

```python
from imblearn.over_sampling import SMOTE

# SMOTE 적용
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# 모델 재학습
model_smote = LogisticRegression(max_iter=1000)
model_smote.fit(X_train_balanced, y_train_balanced)

# 평가
y_pred_smote = model_smote.predict(X_test)
y_proba_smote = model_smote.predict_proba(X_test)[:, 1]

print("=" * 60)
print("SMOTE 적용 후 성능")
print("=" * 60)
print(classification_report(y_test, y_pred_smote))
print(f"\nROC-AUC: {roc_auc_score(y_test, y_proba_smote):.4f}")
```

**개선 효과**:
- Precision ⬆️
- Recall 유지
- F1-Score ⬆️

---

## 6️⃣ XGBoost 모델

```python
import xgboost as xgb

# 클래스 불균형 비율 계산
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# XGBoost 모델
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_pos_weight,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# 평가
y_pred_xgb = xgb_model.predict(X_test)
y_proba_xgb = xgb_model.predict_proba(X_test)[:, 1]

print("=" * 60)
print("XGBoost 모델 성능")
print("=" * 60)
print(classification_report(y_test, y_pred_xgb))
print(f"\nROC-AUC: {roc_auc_score(y_test, y_proba_xgb):.4f}")
```

---

## 7️⃣ Jupyter 노트북으로 실습

```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/
```

**추천 실습 순서**:
1. `01_exploratory_data_analysis.ipynb` - EDA
2. `02_feature_engineering.ipynb` - 특성 엔지니어링
3. `03_imbalance_handling.ipynb` - 불균형 처리
4. `04_modeling.ipynb` - 모델 학습
5. `05_evaluation_and_interpretation.ipynb` - 평가 및 해석

---

## 8️⃣ 모델 비교 스크립트

```python
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb

models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    "XGBoost": xgb.XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42),
    "LightGBM": lgb.LGBMClassifier(is_unbalance=True, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    results[name] = auc
    print(f"{name}: ROC-AUC = {auc:.4f}")

# 결과 정렬
import pandas as pd
results_df = pd.DataFrame.from_dict(results, orient='index', columns=['ROC-AUC'])
results_df = results_df.sort_values('ROC-AUC', ascending=False)
print("\n모델 성능 순위:")
print(results_df)
```

---

## 9️⃣ 평가 지표 시각화

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_xgb)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['정상', '사기'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix - XGBoost')
plt.savefig('outputs/figures/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# Precision-Recall Curve
precision, recall, thresholds = precision_recall_curve(y_test, y_proba_xgb)
plt.figure(figsize=(10, 6))
plt.plot(recall, precision, marker='.')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve - XGBoost')
plt.grid(True)
plt.savefig('outputs/figures/pr_curve.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 🔟 다음 단계

### 고급 기법 적용
- [ ] SHAP으로 모델 해석
- [ ] Optuna로 하이퍼파라미터 튜닝
- [ ] Isolation Forest (이상탐지)
- [ ] Autoencoder (딥러닝 이상탐지)
- [ ] Threshold 최적화 (비용 함수 고려)

### 프로덕션 배포
- [ ] FastAPI로 REST API 구축
- [ ] Docker 컨테이너화
- [ ] 모델 모니터링 대시보드
- [ ] A/B 테스트 설계

---

## 📚 참고 명령어

```bash
# 프로젝트 구조 확인
tree -L 2

# 특정 스크립트 실행
python scripts/01_data_profiling.py

# Jupyter 실행
jupyter notebook

# 패키지 버전 확인
pip list | grep -E "pandas|scikit|xgboost|lightgbm"
```

---

**문제 발생 시**:
- 데이터가 없으면: `README.md`의 Kaggle 다운로드 지침 확인
- 패키지 에러: 가상환경 생성 후 재설치 권장
- 메모리 부족: 데이터 샘플링 적용 (`df.sample(50000)`)

**생성일**: 2026-01-31
