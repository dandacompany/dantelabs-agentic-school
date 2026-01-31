---
name: balance-data
description: 클래스 불균형 문제를 해결하기 위해 오버샘플링, 언더샘플링, 하이브리드 기법을 적용합니다.
arguments:
  - name: X-path
    description: 특성 데이터 파일 경로 (전처리 완료된 X)
    required: true
  - name: y-path
    description: 타겟 데이터 파일 경로 (전처리 완료된 y)
    required: true
  - name: method
    description: 리샘플링 방법 (smote, adasyn, borderline, undersample, smote-tomek)
    required: false
    default: "smote"
  - name: ratio
    description: 소수 클래스 비율 (0.1 = 1:10, 1.0 = 1:1)
    required: false
    default: "0.1"
  - name: test-size
    description: 테스트 데이터 비율 (0.0-1.0)
    required: false
    default: "0.2"
  - name: output-dir
    description: 리샘플링된 데이터 저장 디렉토리
    required: false
    default: "projects/{project-name}/data/processed"
---

# /balance-data

클래스 불균형 데이터셋을 다양한 리샘플링 기법으로 균형 있게 조정합니다.

## Usage

```bash
# SMOTE 사용 (기본값)
/balance-data \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv"

# 타겟 비율 지정 (1:10)
/balance-data \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1

# ADASYN 사용
/balance-data \
  --X-path "projects/my-project/data/processed/data_processed_X.csv" \
  --y-path "projects/my-project/data/processed/data_processed_y.csv" \
  --method adasyn

# 출력 디렉토리 지정
/balance-data \
  --X-path "projects/my-project/data/processed/data_processed_X.csv" \
  --y-path "projects/my-project/data/processed/data_processed_y.csv" \
  --output-dir "projects/my-project/data/balanced"
```

## What This Command Does

### 1. 데이터 로드 및 검증
- 전처리된 특성(X)과 타겟(y) 데이터 로드
- 데이터 shape 및 클래스 분포 확인
- 불균형 비율 계산

### 2. Train/Test 분리 (Data Leakage 방지)
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**중요**: 리샘플링은 **Train 데이터에만** 적용!

### 3. 리샘플링 적용

#### SMOTE (Synthetic Minority Over-sampling Technique)
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

**특징**:
- 소수 클래스의 합성 샘플 생성
- k-NN 기반 보간
- 가장 널리 사용됨

**적용 시기**: 대부분의 경우 (기본 추천)

#### ADASYN (Adaptive Synthetic Sampling)
```python
from imblearn.over_sampling import ADASYN

adasyn = ADASYN(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = adasyn.fit_resample(X_train, y_train)
```

**특징**:
- 학습하기 어려운 샘플에 더 많은 가중치
- SMOTE보다 정교한 샘플 생성

**적용 시기**: SMOTE보다 향상된 성능 필요 시

#### BorderlineSMOTE
```python
from imblearn.over_sampling import BorderlineSMOTE

borderline = BorderlineSMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = borderline.fit_resample(X_train, y_train)
```

**특징**:
- 경계선 근처 샘플만 오버샘플링
- 노이즈 감소

**적용 시기**: 클래스 경계가 불분명한 경우

#### Random Under-sampling
```python
from imblearn.under_sampling import RandomUnderSampler

undersampler = RandomUnderSampler(sampling_strategy=0.5, random_state=42)
X_resampled, y_resampled = undersampler.fit_resample(X_train, y_train)
```

**특징**:
- 다수 클래스 샘플 제거
- 빠른 학습 시간

**적용 시기**: 데이터가 충분히 많은 경우 (100만 건 이상)

#### SMOTE-Tomek (Hybrid)
```python
from imblearn.combine import SMOTETomek

smote_tomek = SMOTETomek(random_state=42)
X_resampled, y_resampled = smote_tomek.fit_resample(X_train, y_train)
```

**특징**:
- SMOTE + Tomek Links
- 오버샘플링 후 경계선 정리

**적용 시기**: 노이즈가 많은 데이터

### 4. 균형 데이터 저장

저장 파일:
- `X_train_balanced.csv`: 리샘플링된 Train 특성
- `y_train_balanced.csv`: 리샘플링된 Train 타겟
- `X_test.csv`: 원본 Test 특성 (리샘플링 X)
- `y_test.csv`: 원본 Test 타겟 (리샘플링 X)

## Output Structure

```
projects/{project-name}/data/processed/
├── X_train_balanced.csv    # 리샘플링된 Train 특성
├── y_train_balanced.csv    # 리샘플링된 Train 타겟
├── X_test.csv              # 원본 Test 특성
└── y_test.csv              # 원본 Test 타겟
```

## Resampling Methods Comparison

| 방법 | 유형 | 속도 | 성능 | 사용 시기 |
|------|------|------|------|---------|
| **SMOTE** | Over-sampling | 보통 | 우수 | 기본 추천 |
| **ADASYN** | Over-sampling | 느림 | 매우 우수 | 정교한 샘플링 필요 |
| **BorderlineSMOTE** | Over-sampling | 보통 | 우수 | 경계 불분명 |
| **RandomUnderSampler** | Under-sampling | 빠름 | 보통 | 대용량 데이터 |
| **SMOTE-Tomek** | Hybrid | 느림 | 매우 우수 | 노이즈 많음 |

## Sampling Ratio Guide

| 원본 비율 | 권장 ratio | 최종 비율 | 설명 |
|----------|-----------|----------|------|
| 1:500 | 0.1 | 1:10 | 극심한 불균형 → 보수적 |
| 1:100 | 0.2 | 1:5 | 심한 불균형 |
| 1:50 | 0.5 | 1:2 | 중간 불균형 |
| 1:10 | 1.0 | 1:1 | 가벼운 불균형 → 완전 균형 |

**주의**: ratio를 너무 높이면 과적합 위험!

## Examples

### Example 1: 신용카드 사기 탐지 (1:578)
```bash
/balance-data \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1
```

**결과**:
- 원본 Train: 227,451 (정상) vs 394 (사기) = 1:577
- 리샘플링 후: 227,451 vs 22,745 = 1:10

### Example 2: 고객 이탈 예측 (1:5)
```bash
/balance-data \
  --X-path "projects/customer-churn/data/processed/churn_processed_X.csv" \
  --y-path "projects/customer-churn/data/processed/churn_processed_y.csv" \
  --method smote \
  --ratio 1.0
```

**결과**: 완전 균형 (1:1)

### Example 3: ADASYN으로 더 정교한 샘플링
```bash
/balance-data \
  --X-path "projects/my-project/data/processed/X.csv" \
  --y-path "projects/my-project/data/processed/y.csv" \
  --method adasyn \
  --ratio 0.2
```

## Performance Tips

### 메모리 효율화
- 대용량 데이터는 ratio를 낮게 (0.05-0.1)
- SMOTE보다 RandomUnderSampler 고려

### 과적합 방지
- ratio를 1.0 미만으로 유지
- SMOTE-Tomek로 노이즈 제거
- Cross-validation으로 검증

### 최적 ratio 찾기
```python
# Optuna로 자동 튜닝
import optuna

def objective(trial):
    ratio = trial.suggest_float('ratio', 0.05, 0.5)
    # ... 리샘플링 및 모델 학습
    return f1_score
```

## Troubleshooting

### 문제: "ValueError: The least populated class has only 1 member"
- 클래스 샘플이 너무 적음
- 데이터 수집 추가 필요

### 문제: 리샘플링 후 성능 오히려 하락
- ratio를 낮춰보기 (1.0 → 0.1)
- SMOTE 대신 Class weights 사용
```python
model = XGBClassifier(scale_pos_weight=578)
```

### 문제: 메모리 부족
- ratio를 낮춤 (0.05)
- RandomUnderSampler 사용
- 청크 단위 처리

## Related Commands

- `/profile-data`: 클래스 분포 확인
- `/engineer-features`: 전처리 (리샘플링 전 필수)
- `/train-models`: 모델 학습 (리샘플링 후)

## Agents Used

- `imbalance-handler` (필수): 클래스 불균형 처리

## Notes

⚠️ **주의사항**:
- **Train 데이터만** 리샘플링 (Test는 원본 유지)
- Train/Test 분리 **후** 리샘플링 (Data leakage 방지)
- ratio를 너무 높이면 과적합 위험

💡 **팁**:
- 기본값(SMOTE, ratio=0.1)으로 시작
- F1-Score 모니터링하며 ratio 조정
- SMOTE가 안 되면 ADASYN 시도
- 대용량 데이터는 언더샘플링 고려

## Best Practices

### 1. 리샘플링 전 확인사항
- [ ] 데이터 전처리 완료 (`/engineer-features`)
- [ ] 클래스 분포 확인 (`/profile-data`)
- [ ] 불균형 비율 확인 (1:10 미만이면 리샘플링 필요)

### 2. 리샘플링 후 확인사항
- [ ] Train/Test 분포 확인
- [ ] 생성된 샘플 수 확인
- [ ] 파일 크기 확인 (메모리)

### 3. 모델 학습 시
- [ ] Stratified K-Fold CV 사용
- [ ] F1-Score, PR-AUC로 평가 (Accuracy 금지)
- [ ] Class weights와 병행 고려
