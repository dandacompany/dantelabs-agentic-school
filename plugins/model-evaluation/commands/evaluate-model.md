---
name: evaluate-model
description: 학습된 모델의 성능을 종합적으로 평가하고 시각화 리포트를 생성합니다.
arguments:
  - name: model-path
    description: 학습된 모델 파일 경로 (.pkl)
    required: true
  - name: test-data
    description: 테스트 데이터 파일 경로 (CSV, Excel, Parquet)
    required: true
  - name: target-column
    description: 타겟 변수 컬럼명
    required: true
  - name: task-type
    description: 태스크 타입 (classification, regression, auto)
    required: false
    default: "auto"
  - name: cv
    description: 교차 검증 폴드 수
    required: false
    default: "5"
  - name: output-dir
    description: 출력 디렉토리
    required: false
    default: "projects/{project-name}/outputs/evaluations"
---

# /evaluate-model

학습된 모델의 성능을 종합적으로 평가하고 상세한 시각화 리포트를 생성합니다.

## Usage

```bash
# 기본 사용법
/evaluate-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class"

# 태스크 타입 명시
/evaluate-model \
  --model-path "projects/house-price-prediction/models/rf_model.pkl" \
  --test-data "projects/house-price-prediction/data/processed/test.csv" \
  --target-column "price" \
  --task-type regression

# 교차 검증 폴드 수 조정
/evaluate-model \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --cv 10

# 출력 디렉토리 지정
/evaluate-model \
  --model-path "./models/model.pkl" \
  --test-data "./data/test.csv" \
  --target-column "target" \
  --output-dir "projects/my-project/outputs/evaluations"
```

## What This Command Does

### 1. 모델 및 데이터 로드
- 학습된 모델 파일 로드 (.pkl 형식)
- 테스트 데이터 로드 (CSV, Excel, Parquet 지원)
- 태스크 타입 자동 감지 (분류 vs 회귀)

### 2. 특성 중요도 분석
- **상위 20개 중요 특성 시각화**
- Tree-based 모델: feature_importances_
- Linear 모델: coefficient 절댓값
- 막대 그래프로 직관적 표현

### 3. 학습 곡선 분석
- **훈련/검증 스코어 변화 추이**
- 데이터 크기별 성능 평가
- 과적합/과소적합 진단
- 신뢰구간 표시

### 4. 교차 검증
- **K-Fold 교차 검증 수행**
- 분류: F1-Score (Weighted)
- 회귀: R² Score
- 폴드별 스코어 및 평균±표준편차

### 5. 성능 메트릭 계산

**분류 모델**:
- Accuracy, Precision, Recall, F1-Score
- Classification Report (클래스별 상세 지표)
- Confusion Matrix (혼동 행렬)
- ROC Curve & AUC (이진 분류)
- Precision-Recall Curve (이진 분류)

**회귀 모델**:
- MAE, MSE, RMSE, R²
- Actual vs Predicted 산점도
- Residual Plot (잔차 분석)

### 6. 시각화 생성
모든 시각화는 고해상도 PNG (150 DPI)로 저장:
- `feature_importance.png`: 특성 중요도
- `learning_curves.png`: 학습 곡선
- `confusion_matrix.png`: 혼동 행렬 (분류)
- `roc_curve.png`: ROC 곡선 (이진 분류)
- `precision_recall_curve.png`: PR 곡선 (이진 분류)
- `actual_vs_predicted.png`: 예측 vs 실제 (회귀)
- `residuals.png`: 잔차 플롯 (회귀)

### 7. 평가 리포트 생성
- Markdown 형식 종합 리포트
- 모든 메트릭 수치 정리
- 생성된 시각화 파일 목록

## Output Structure

```
projects/{project-name}/outputs/evaluations/
├── feature_importance.png
├── learning_curves.png
├── confusion_matrix.png              # 분류 모델
├── roc_curve.png                     # 이진 분류
├── precision_recall_curve.png        # 이진 분류
├── actual_vs_predicted.png           # 회귀 모델
├── residuals.png                     # 회귀 모델
└── {model_name}_evaluation_report.md
```

## Examples

### Example 1: 신용카드 사기 탐지 (분류)
```bash
/evaluate-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class"
```

**예상 출력**:
```
기본 메트릭:
  Accuracy:  0.9995
  Precision: 0.9234
  Recall:    0.8567
  F1-Score:  0.8887

ROC AUC: 0.9812

교차 검증:
  평균: 0.8845 (±0.0234)
```

### Example 2: 주택 가격 예측 (회귀)
```bash
/evaluate-model \
  --model-path "projects/house-price-prediction/models/rf_model.pkl" \
  --test-data "projects/house-price-prediction/data/processed/test.csv" \
  --target-column "price" \
  --task-type regression
```

**예상 출력**:
```
기본 메트릭:
  MAE:  15234.56
  MSE:  456789012.34
  RMSE: 21372.62
  R²:   0.8745

교차 검증:
  평균: 0.8623 (±0.0412)
```

### Example 3: 10-Fold 교차 검증
```bash
/evaluate-model \
  --model-path "projects/my-project/models/lgbm_model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --cv 10
```

## Performance Metrics Explained

### 분류 메트릭
| 메트릭 | 설명 | 언제 중요한가 |
|--------|------|-------------|
| **Accuracy** | 전체 정확도 | 클래스 균형이 잘 맞을 때 |
| **Precision** | 양성 예측의 정확도 | 거짓 양성(FP) 비용이 클 때 |
| **Recall** | 실제 양성의 탐지율 | 거짓 음성(FN) 비용이 클 때 |
| **F1-Score** | Precision과 Recall의 조화평균 | 불균형 데이터 |
| **ROC AUC** | 분류 임계값 전반의 성능 | 모델 전체 성능 평가 |

### 회귀 메트릭
| 메트릭 | 설명 | 특징 |
|--------|------|------|
| **MAE** | 평균 절대 오차 | 이상치에 덜 민감 |
| **MSE** | 평균 제곱 오차 | 큰 오차에 페널티 |
| **RMSE** | MSE의 제곱근 | 타겟과 같은 스케일 |
| **R²** | 설명력 (0~1) | 모델 적합도 |

## Feature Importance Insights

**해석 방법**:
- 상위 특성들이 모델 예측에 가장 큰 영향
- 중요도가 매우 낮은 특성은 제거 고려
- 도메인 지식과 일치하는지 확인

**활용**:
- 특성 선택 (Feature Selection)
- 도메인 전문가와 검증
- 모델 설명력 향상

## Learning Curves Interpretation

**과적합 (Overfitting)**:
- 훈련 스코어 >> 검증 스코어
- 격차가 크고 좁혀지지 않음
- 해결: 정규화, 데이터 추가, 복잡도 감소

**과소적합 (Underfitting)**:
- 훈련 스코어와 검증 스코어 모두 낮음
- 해결: 모델 복잡도 증가, 특성 추가

**적절한 학습**:
- 훈련/검증 스코어가 비슷하고 높음
- 데이터 증가 시 수렴

## Cross-Validation Strategy

| CV 폴드 | 데이터 크기 | 권장 상황 |
|---------|-----------|---------|
| **3-5** | 소형 (<10k) | 빠른 평가 |
| **5-10** | 중형 (10k-100k) | 표준 평가 |
| **10+** | 대형 (>100k) | 정밀 평가 |

## Related Commands

- `/select-model`: 여러 모델 학습 및 비교
- `/tune-hyperparameters`: 하이퍼파라미터 최적화
- `/analyze-shap`: SHAP 값 분석
- `/monitor-model`: 모델 성능 모니터링

## Agents Used

- `model-evaluator` (필수): 모델 평가 및 시각화 실행

## Troubleshooting

### 문제: "특성 중요도를 지원하지 않습니다"
- 일부 모델(KNN, SVM 등)은 기본 특성 중요도 미지원
- 해결: SHAP 분석 사용 (`/analyze-shap`)

### 문제: 학습 곡선 계산 시간이 너무 김
- 대용량 데이터셋의 경우 시간 소요
- 해결: CV 폴드 수 줄이기 (`--cv 3`)

### 문제: 메모리 부족
- 데이터가 너무 큰 경우
- 해결: 테스트 데이터 샘플링 또는 청크 처리

### 문제: ROC 곡선이 생성되지 않음
- 다중 클래스 분류 또는 회귀 모델
- ROC 곡선은 이진 분류만 지원

## Notes

⚠️ **주의사항**:
- 모델 파일은 joblib 또는 pickle로 저장되어야 함
- 테스트 데이터는 학습 시와 동일한 전처리 필요
- 타겟 컬럼명은 정확히 일치해야 함

💡 **팁**:
- 먼저 학습 곡선으로 과적합/과소적합 확인
- 교차 검증 스코어로 일반화 성능 평가
- 특성 중요도로 모델 해석력 확보
- 여러 메트릭을 종합적으로 고려
