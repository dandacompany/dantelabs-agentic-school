---
name: analyze-shap
description: SHAP(SHapley Additive exPlanations)를 사용하여 모델 예측을 설명하고 해석합니다.
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
  - name: sample-size
    description: SHAP 계산에 사용할 샘플 크기
    required: false
    default: "1000"
  - name: instance-idx
    description: 설명할 인스턴스 인덱스
    required: false
    default: "0"
  - name: output-dir
    description: 출력 디렉토리
    required: false
    default: "projects/{project-name}/outputs/shap"
---

# /analyze-shap

SHAP(SHapley Additive exPlanations)를 사용하여 모델 예측을 상세하게 설명합니다.

## Usage

```bash
# 기본 사용법
/analyze-shap \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class"

# 샘플 크기 지정
/analyze-shap \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --sample-size 2000

# 특정 인스턴스 설명
/analyze-shap \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --instance-idx 42

# 출력 디렉토리 지정
/analyze-shap \
  --model-path "./models/model.pkl" \
  --test-data "./data/test.csv" \
  --target-column "target" \
  --output-dir "projects/my-project/outputs/shap"
```

## What This Command Does

### 1. SHAP Explainer 생성
- **TreeExplainer**: Tree-based 모델 (XGBoost, LightGBM, RF)
- **LinearExplainer**: Linear 모델 (LogisticRegression, LinearRegression)
- **KernelExplainer**: 범용 모델 (model-agnostic, 느림)

### 2. SHAP 값 계산
- 각 특성이 예측에 미치는 영향 정량화
- 게임 이론 기반 Shapley 값 사용
- 모델 예측을 특성별 기여도로 분해

### 3. 전역 설명 (Global Explanation)

#### Summary Plot
- 모든 샘플에 대한 SHAP 값 분포
- 특성 중요도 + 영향 방향
- 색상: 특성 값 (빨강=높음, 파랑=낮음)

#### Bar Plot
- 평균 절댓값 SHAP 값
- 특성 중요도 순위
- 단순하고 직관적

### 4. 지역 설명 (Local Explanation)

#### Waterfall Plot
- 개별 예측의 특성별 기여도
- Base value → Final prediction 경로
- 양수/음수 기여 시각화

#### Force Plot
- 개별 예측의 시각적 설명
- 양성/음성 기여 색상 구분
- Interactive (HTML) 또는 Static (PNG)

#### Dependence Plot
- 특성 값과 SHAP 값의 관계
- 비선형 관계 탐지
- 상호작용 효과 시각화

### 5. 개별 인스턴스 설명
- 실제 레이블 vs 예측 레이블
- 상위 5개 영향 특성
- 각 특성의 값 및 SHAP 기여도
- 텍스트 설명 파일 생성

### 6. SHAP 리포트 생성
- Markdown 형식 종합 리포트
- 전역 특성 중요도 테이블
- 생성된 시각화 파일 목록
- SHAP 값 해석 가이드

## Output Structure

```
projects/{project-name}/outputs/shap/
├── shap_summary_plot.png                  # 전역: Summary Plot
├── shap_bar_plot.png                      # 전역: Bar Plot
├── shap_waterfall_plot_instance_0.png     # 지역: Waterfall
├── shap_force_plot_instance_0.png         # 지역: Force
├── shap_dependence_plot_{feature}.png     # 특성 의존성
├── instance_0_explanation.txt             # 텍스트 설명
└── {model_name}_shap_report.md            # 종합 리포트
```

## Examples

### Example 1: 신용카드 사기 탐지
```bash
/analyze-shap \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --test-data "projects/creditcard-fraud-detection/data/processed/test.csv" \
  --target-column "Class" \
  --sample-size 1000
```

**예상 출력**:
```
인스턴스 0 예측 설명
실제 레이블: 1 (사기)
예측 레이블: 1 (사기)

상위 5개 영향 특성:
  1. V17                  :    -7.2341 (SHAP: +2.3456, 양성 기여)
  2. V14                  :    -8.9876 (SHAP: +1.8765, 양성 기여)
  3. V12                  :    -5.6789 (SHAP: +1.2345, 양성 기여)
  4. V10                  :    -9.0123 (SHAP: +0.9876, 양성 기여)
  5. Amount               :   149.6200 (SHAP: -0.5678, 음성 기여)
```

### Example 2: 특정 인스턴스 분석
```bash
/analyze-shap \
  --model-path "projects/my-project/models/model.pkl" \
  --test-data "projects/my-project/data/test.csv" \
  --target-column "target" \
  --instance-idx 42 \
  --sample-size 500
```

### Example 3: 대용량 데이터
```bash
# 샘플 크기를 작게 설정하여 계산 시간 단축
/analyze-shap \
  --model-path "projects/large-project/models/model.pkl" \
  --test-data "projects/large-project/data/test.csv" \
  --target-column "target" \
  --sample-size 500
```

## SHAP 값 해석

### 기본 개념
- **SHAP 값**: 특성이 예측에 기여하는 정도
- **Base value**: 평균 예측값 (데이터셋 전체)
- **Final prediction**: Base value + 모든 SHAP 값의 합

### 양수 vs 음수
| SHAP 값 | 의미 | 분류 예시 |
|---------|------|---------|
| **양수 (+)** | 예측을 증가시킴 | 양성 클래스 확률 증가 |
| **음수 (-)** | 예측을 감소시킴 | 음성 클래스 확률 증가 |
| **0에 가까움** | 영향 없음 | 예측에 기여하지 않음 |

### 절댓값 크기
- **큰 절댓값**: 예측에 큰 영향
- **작은 절댓값**: 예측에 작은 영향

## Summary Plot 읽는 법

```
Feature Importance (mean |SHAP|)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V17    ●●●●●●●●●●●●●●●●●●●●●●  (많은 점들, 퍼짐)
V14    ●●●●●●●●●●●●●●●●●       (중간 정도 퍼짐)
V12    ●●●●●●●●●●●●            (집중된 분포)
...
       ←─────────────────────→
       음수   0   양수
       (감소)     (증가)
```

**점의 색상**:
- 빨강: 특성 값이 높음
- 파랑: 특성 값이 낮음

**패턴 해석**:
- V17이 높으면(빨강) 양성 예측(오른쪽)
- V17이 낮으면(파랑) 음성 예측(왼쪽)

## Waterfall Plot 읽는 법

```
f(x) = 1.234
        ↑
        │ V17 = -7.23   +2.35  ──────┐
        │ V14 = -8.99   +1.88  ────┐ │
        │ V12 = -5.68   +1.23  ──┐ │ │
        │ Amount = 149   -0.57  ┐ │ │ │
        │                       │ │ │ │
E[f(X)] = 0.001               │ │ │ │
                               └─┴─┴─┘
```

- Base value (E[f(X)]): 평균 예측
- 화살표: 각 특성의 기여도
- 최종 예측 (f(x)): Base + 모든 기여도

## Performance Considerations

### 계산 시간
| Explainer | 속도 | 권장 샘플 크기 |
|-----------|------|---------------|
| **TreeExplainer** | 매우 빠름 | 10,000+ |
| **LinearExplainer** | 빠름 | 5,000+ |
| **KernelExplainer** | 느림 | 500-1,000 |

### 샘플 크기 가이드
- **소형 데이터 (<1k)**: 전체 사용
- **중형 데이터 (1k-10k)**: 1,000-2,000
- **대형 데이터 (>10k)**: 500-1,000 (대표 샘플)

## Related Commands

- `/evaluate-model`: 모델 성능 평가
- `/monitor-model`: 프로덕션 모델 모니터링
- `/profile-data`: 데이터 프로파일링
- `/select-model`: 모델 선택 및 학습

## Agents Used

- `shap-analyst` (필수): SHAP 분석 및 해석 실행

## Troubleshooting

### 문제: SHAP 계산이 너무 느림
- **TreeExplainer**: 빠름, 대부분 1분 이내
- **KernelExplainer**: 느림, 샘플 크기 줄이기
```bash
--sample-size 500
```

### 문제: 메모리 부족
- 샘플 크기 감소
- 배치 처리 사용
```bash
--sample-size 200
```

### 문제: "Explainer not supported for this model type"
- KernelExplainer 사용 (모든 모델 지원)
- 계산 시간이 길 수 있음

### 문제: Force Plot이 생성되지 않음
- JavaScript 초기화 실패
- Waterfall Plot으로 대체 가능

## Notes

⚠️ **주의사항**:
- SHAP 계산은 시간이 소요될 수 있음 (특히 KernelExplainer)
- Tree-based 모델은 TreeExplainer 권장 (빠름)
- 샘플 크기가 클수록 정확하지만 느림

💡 **팁**:
- 먼저 작은 샘플(100-200)로 테스트
- Summary Plot으로 전역 패턴 파악
- Waterfall Plot으로 개별 예측 이해
- Dependence Plot으로 비선형 관계 확인
- 도메인 지식과 SHAP 결과 비교

🎯 **활용 사례**:
- 모델 디버깅 및 검증
- 규제 준수 (설명 가능한 AI)
- 도메인 전문가와 소통
- Feature Engineering 아이디어
- 모델 신뢰도 향상
