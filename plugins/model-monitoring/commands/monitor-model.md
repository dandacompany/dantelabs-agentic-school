---
name: monitor-model
description: 프로덕션 환경에서 모델 성능을 모니터링하고 데이터 드리프트를 탐지합니다.
arguments:
  - name: model-path
    description: 학습된 모델 파일 경로 (.pkl)
    required: true
  - name: reference-data
    description: 참조 데이터 경로 (학습 데이터)
    required: true
  - name: current-data
    description: 현재 데이터 경로 (프로덕션 데이터)
    required: true
  - name: target-column
    description: 타겟 변수 컬럼명
    required: false
  - name: task-type
    description: 태스크 타입 (classification, regression, auto)
    required: false
    default: "auto"
  - name: alert-threshold
    description: 드리프트 알림 임계값 (PSI)
    required: false
    default: "0.1"
  - name: output-dir
    description: 출력 디렉토리
    required: false
    default: "projects/{project-name}/outputs/monitoring"
---

# /monitor-model

프로덕션 환경에서 모델 성능을 지속적으로 모니터링하고 데이터 드리프트를 탐지합니다.

## Usage

```bash
# 기본 사용법
/monitor-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --reference-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --current-data "projects/creditcard-fraud-detection/data/production/prod_2024_01.csv" \
  --target-column "Class"

# 드리프트 임계값 조정
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod.csv" \
  --target-column "target" \
  --alert-threshold 0.15

# 타겟 없이 드리프트만 탐지
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod.csv"

# 출력 디렉토리 지정
/monitor-model \
  --model-path "./models/model.pkl" \
  --reference-data "./data/train.csv" \
  --current-data "./data/prod.csv" \
  --target-column "target" \
  --output-dir "projects/my-project/outputs/monitoring"
```

## What This Command Does

### 1. 데이터 드리프트 탐지
프로덕션 데이터가 학습 데이터와 얼마나 다른지 측정합니다.

#### PSI (Population Stability Index)
- 0.0 - 0.1: 변화 없음 (안정)
- 0.1 - 0.2: 약간의 변화 (주의)
- 0.2+: 큰 변화 (알림)

#### KS Test (Kolmogorov-Smirnov)
- p-value < 0.05: 분포가 유의미하게 다름
- p-value >= 0.05: 분포 유사

### 2. 예측 분포 모니터링
- 참조 데이터 vs 현재 데이터 예측 분포 비교
- 히스토그램으로 시각화
- KS 통계량으로 차이 정량화

### 3. 성능 추적 (타겟이 있는 경우)
**분류**:
- Accuracy, Precision, Recall, F1-Score

**회귀**:
- MAE, MSE, RMSE, R²

### 4. 알림 시스템
다음 경우 자동 알림 생성:
- 데이터 드리프트 발생
- 성능 저하 (F1 < 0.7 또는 R² < 0.7)
- JSON 형식으로 저장

### 5. 모니터링 리포트 생성
- Markdown 형식 종합 리포트
- 알림 요약
- 성능 메트릭
- 드리프트 상세 정보

## Output Structure

```
projects/{project-name}/outputs/monitoring/
├── drift_summary.png                    # 드리프트 요약 시각화
├── drift_report.csv                     # 드리프트 상세 데이터
├── prediction_distribution.png          # 예측 분포 비교
├── alerts.json                          # 알림 목록 (JSON)
└── {model_name}_monitoring_report.md    # 종합 리포트
```

## Examples

### Example 1: 정기 모니터링
```bash
/monitor-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --reference-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --current-data "projects/creditcard-fraud-detection/data/production/prod_2024_01.csv" \
  --target-column "Class"
```

### Example 2: 타겟 없이 드리프트만 확인
```bash
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod_unlabeled.csv"
```

### Example 3: 엄격한 드리프트 임계값
```bash
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod.csv" \
  --target-column "target" \
  --alert-threshold 0.05
```

## Drift Detection Metrics

### PSI 해석
| PSI 값 | 의미 | 조치 |
|--------|------|------|
| 0.0 - 0.1 | 변화 없음 | 정상 |
| 0.1 - 0.2 | 약간의 변화 | 모니터링 강화 |
| 0.2+ | 큰 변화 | 재학습 고려 |

### KS Test 해석
| p-value | 의미 | 조치 |
|---------|------|------|
| >= 0.05 | 분포 유사 | 정상 |
| < 0.05 | 분포 다름 | 조사 필요 |
| < 0.01 | 분포 매우 다름 | 재학습 권장 |

## Alert Types

### DATA_DRIFT
- **심각도**: WARNING
- **조건**: PSI > threshold 또는 p-value < 0.05
- **조치**: 특성 분포 조사, 필요 시 재학습

### PERFORMANCE_DEGRADATION
- **심각도**: CRITICAL
- **조건**: F1 < 0.7 또는 R² < 0.7
- **조치**: 즉시 재학습 또는 모델 교체

## Monitoring Strategy

### 일일 모니터링
```bash
# 매일 자동 실행 (cron)
0 2 * * * /path/to/monitor_model.sh
```

### 주간 리포트
```bash
# 일주일 데이터 수집 후 분석
/monitor-model \
  --reference-data "train.csv" \
  --current-data "prod_week_$(date +%U).csv"
```

### 월간 재평가
```bash
# 한 달 누적 데이터로 성능 평가
/monitor-model \
  --reference-data "train.csv" \
  --current-data "prod_month_$(date +%m).csv" \
  --target-column "target"
```

## When to Retrain

다음 경우 모델 재학습을 고려하세요:
1. **심각한 드리프트**: PSI > 0.2 또는 여러 특성 드리프트
2. **성능 저하**: 주요 메트릭 10% 이상 하락
3. **예측 분포 변화**: KS p-value < 0.01
4. **비즈니스 요구**: 새로운 패턴, 계절성 등

## Related Commands

- `/evaluate-model`: 모델 성능 평가
- `/select-model`: 모델 재학습
- `/tune-hyperparameters`: 하이퍼파라미터 재조정
- `/analyze-shap`: 드리프트 원인 분석

## Agents Used

- `model-monitor` (필수): 모델 모니터링 및 드리프트 탐지 실행

## Troubleshooting

### 문제: "컬럼이 현재 데이터에 없습니다"
- 프로덕션 데이터의 컬럼이 학습 데이터와 다름
- 해결: 전처리 파이프라인 동기화

### 문제: 모든 특성에서 드리프트 발생
- 임계값이 너무 낮음
- 해결: `--alert-threshold 0.15` 또는 더 높게 조정

### 문제: 성능 추적이 건너뛰어짐
- 타겟 컬럼이 없음
- 해결: `--target-column` 지정 또는 드리프트만 모니터링

## Notes

⚠️ **주의사항**:
- 참조 데이터는 일반적으로 학습 데이터 사용
- PSI 계산은 숫자형 특성만 지원
- 범주형 특성은 사전 인코딩 필요

💡 **팁**:
- 정기적 모니터링 설정 (일/주/월)
- 드리프트 발생 시 원인 특성 조사
- 알림 JSON을 모니터링 대시보드와 연동
- 시간 경과에 따른 메트릭 추이 추적
- 계절성 고려 (연말, 휴가 등)

🎯 **모범 사례**:
- 최소 주 1회 모니터링
- 드리프트 임계값은 비즈니스 요구에 맞게 조정
- 알림 발생 시 근본 원인 분석
- 재학습 전 A/B 테스트
