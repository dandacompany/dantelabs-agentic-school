# Model Evaluation Plugin

학습된 모델의 성능을 종합적으로 평가하고 시각화하는 플러그인입니다.

## 📋 개요

이 플러그인은 데이터 사이언스 파이프라인에서 모델 평가 단계를 담당하며, 다음을 제공합니다:

### 주요 기능
- ✅ **특성 중요도 분석** (상위 20개 특성)
- ✅ **학습 곡선 시각화** (과적합/과소적합 진단)
- ✅ **교차 검증** (K-Fold CV)
- ✅ **성능 메트릭 계산** (분류/회귀)
- ✅ **고해상도 시각화** (PNG 150 DPI)
- ✅ **Markdown 리포트 자동 생성**

### 지원 태스크
- 🎯 **분류 (Classification)**: Accuracy, Precision, Recall, F1, ROC AUC
- 📊 **회귀 (Regression)**: MAE, MSE, RMSE, R²

## 🚀 빠른 시작

### 1. 의존성 설치

**uv 사용 (권장 - 10-100배 빠름)**:
```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 macOS
brew install uv

# 패키지 설치
cd plugins/model-evaluation/skills/evaluation
uv pip install -r requirements.txt
```

**pip 사용 (기존 방식)**:
```bash
cd plugins/model-evaluation/skills/evaluation
pip install -r requirements.txt
```

### 2. 모델 평가

```bash
# Claude Code에서 실행
/evaluate-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class"

# 또는 Python 스크립트 직접 실행
cd plugins/model-evaluation/skills/evaluation/scripts
python evaluate_model.py \
  --model-path "../../../../../projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "../../../../../projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class"
```

**출력**: `projects/creditcard-fraud-detection/outputs/evaluations/` 폴더에 모든 시각화 및 리포트 저장

## 📁 플러그인 구조

```
plugins/model-evaluation/
├── plugin.json                      # 플러그인 메타데이터
├── README.md                        # 플러그인 문서
├── agents/
│   └── model-evaluator.md          # 모델 평가 에이전트
├── commands/
│   └── evaluate-model.md           # 평가 커맨드
└── skills/
    └── evaluation/
        ├── requirements.txt         # Python 패키지 의존성
        └── scripts/
            └── evaluate_model.py   # 평가 스크립트
```

## 🎯 주요 기능

### 1. 특성 중요도 분석
- Tree-based 모델의 `feature_importances_`
- Linear 모델의 `coef_` 절댓값
- 상위 20개 특성 막대 그래프
- 콘솔에 상위 10개 출력

### 2. 학습 곡선
- 훈련 세트 크기별 성능 변화
- 훈련/검증 스코어 비교
- 신뢰구간 (±표준편차) 표시
- 과적합/과소적합 진단

### 3. 교차 검증
- K-Fold 교차 검증 (기본 5-Fold)
- 분류: F1-Score (Weighted)
- 회귀: R² Score
- 폴드별 스코어 및 통계

### 4. 분류 모델 평가
- **기본 메트릭**: Accuracy, Precision, Recall, F1
- **상세 리포트**: 클래스별 지표
- **혼동 행렬**: 히트맵 시각화
- **ROC 곡선**: AUC 포함 (이진 분류)
- **PR 곡선**: Precision-Recall (이진 분류)

### 5. 회귀 모델 평가
- **기본 메트릭**: MAE, MSE, RMSE, R²
- **Actual vs Predicted**: 산점도 + 대각선
- **잔차 플롯**: 예측 오차 분포

### 6. 시각화 저장
- 모든 그래프를 고해상도 PNG (150 DPI)로 저장
- 명확한 레이블 및 제목
- 그리드 및 범례 포함

## 📊 사용 예시

### Example 1: 기본 평가
```bash
/evaluate-model \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target"
```

### Example 2: 회귀 모델 명시
```bash
/evaluate-model \
  --model-path "projects/house-price-prediction/models/rf_model.pkl" \
  --test-data "projects/house-price-prediction/data/test.csv" \
  --target-column "price" \
  --task-type regression
```

### Example 3: 10-Fold 교차 검증
```bash
/evaluate-model \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --cv 10
```

## 🔧 파라미터

### 필수 파라미터
- `--model-path`: 학습된 모델 파일 경로 (.pkl)
- `--test-data`: 테스트 데이터 파일 경로
- `--target-column`: 타겟 컬럼명

### 선택 파라미터
- `--task-type`: 태스크 타입 (classification/regression/auto, 기본값: auto)
- `--cv`: 교차 검증 폴드 수 (기본값: 5)
- `--output-dir`: 출력 디렉토리 (기본값: projects/{project-name}/outputs/evaluations)

## 📤 출력

### 시각화 파일 (PNG)
**공통**:
- `feature_importance.png`: 상위 20개 특성 중요도
- `learning_curves.png`: 학습 곡선

**분류 모델**:
- `confusion_matrix.png`: 혼동 행렬
- `roc_curve.png`: ROC 곡선 (이진 분류)
- `precision_recall_curve.png`: PR 곡선 (이진 분류)

**회귀 모델**:
- `actual_vs_predicted.png`: 예측 vs 실제
- `residuals.png`: 잔차 플롯

### Markdown 리포트
- `{model_name}_evaluation_report.md`
- 모든 메트릭 수치
- 생성된 시각화 파일 목록

### 콘솔 출력
```
═══════════════════════════════════════════════════════════
모델 평가 시작
═══════════════════════════════════════════════════════════

✓ 출력 디렉토리: projects/creditcard-fraud-detection/outputs/evaluations
✓ 데이터 로드 중: projects/creditcard-fraud-detection/data/processed/test.csv
✓ 데이터 로드 완료: 56,962건, 30개 특성
✓ 모델 로드 중: projects/creditcard-fraud-detection/models/xgboost_model.pkl
✓ 모델 로드 완료: XGBClassifier

✓ 자동 태스크 타입 감지: classification

────────────────────────────────────────────────────────
특성 중요도 분석
────────────────────────────────────────────────────────

상위 10개 중요 특성:
   1. V17                          : 0.1245
   2. V14                          : 0.0987
   3. V12                          : 0.0856
   ...

✓ 특성 중요도 시각화 저장: projects/.../feature_importance.png

────────────────────────────────────────────────────────
학습 곡선 분석
────────────────────────────────────────────────────────

⏳ 학습 곡선 계산 중 (시간이 소요될 수 있습니다)...
✓ 학습 곡선 저장: projects/.../learning_curves.png
  최종 학습 스코어: 0.9234 (±0.0123)
  최종 검증 스코어: 0.8987 (±0.0234)

────────────────────────────────────────────────────────
교차 검증
────────────────────────────────────────────────────────

⏳ 5-Fold 교차 검증 수행 중...

F1-Score (Weighted) 스코어 (5-Fold CV):
  Fold 1: 0.8956
  Fold 2: 0.9012
  Fold 3: 0.8845
  Fold 4: 0.9087
  Fold 5: 0.8923

  평균: 0.8965 (±0.0091)

────────────────────────────────────────────────────────
분류 모델 성능 평가
────────────────────────────────────────────────────────

기본 메트릭:
  Accuracy:  0.9995
  Precision: 0.9234
  Recall:    0.8567
  F1-Score:  0.8887

상세 리포트:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     56864
           1       0.92      0.86      0.89        98

    accuracy                           1.00     56962
   macro avg       0.96      0.93      0.94     56962
weighted avg       1.00      1.00      1.00     56962

✓ 혼동 행렬 저장: projects/.../confusion_matrix.png
✓ ROC 곡선 저장: projects/.../roc_curve.png
  ROC AUC: 0.9812
✓ Precision-Recall 곡선 저장: projects/.../precision_recall_curve.png

✓ 평가 리포트 저장: projects/.../xgboost_model_evaluation_report.md

═══════════════════════════════════════════════════════════
모델 평가 완료
═══════════════════════════════════════════════════════════

📁 모든 결과가 저장되었습니다: projects/creditcard-fraud-detection/outputs/evaluations/
   - 시각화: *.png
   - 리포트: xgboost_model_evaluation_report.md
```

## 🔍 지원 파일 형식

| 형식 | 확장자 | 지원 여부 |
|------|--------|---------|
| CSV | `.csv` | ✅ |
| Excel | `.xlsx`, `.xls` | ✅ |
| Parquet | `.parquet` | ✅ |
| Pickle | `.pkl` (모델) | ✅ |

## 🐛 트러블슈팅

### 문제: "특성 중요도를 지원하지 않습니다"
- 일부 모델(KNN, SVM 등)은 기본 특성 중요도 미지원
- **해결**: `/analyze-shap` 사용

### 문제: 학습 곡선 계산이 너무 느림
- 대용량 데이터의 경우 시간 소요
- **해결**: `--cv 3`으로 폴드 수 줄이기

### 문제: 메모리 부족
```bash
# 테스트 데이터 샘플링
import pandas as pd
df = pd.read_csv("test.csv")
df.sample(n=10000).to_csv("test_sample.csv", index=False)
```

### 문제: ROC 곡선이 생성되지 않음
- 다중 클래스 분류 또는 회귀 모델
- ROC 곡선은 이진 분류만 지원

## 📚 관련 문서

- [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Agent 정의](./agents/model-evaluator.md)
- [Command 문서](./commands/evaluate-model.md)

## 🔗 관련 플러그인

- `model-selection`: 여러 모델 학습 및 비교
- `hyperparameter-tuning`: 하이퍼파라미터 최적화
- `shap-analysis`: SHAP 값 분석
- `model-monitoring`: 프로덕션 모델 모니터링
- `model-deployment`: 모델 API 배포

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0
