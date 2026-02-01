# Imbalance Handling Plugin

클래스 불균형 문제를 해결하기 위한 다양한 리샘플링 기법을 제공하는 플러그인입니다.

## 📋 개요

이 플러그인은 불균형 데이터셋을 균형 있게 조정하여 모델 성능을 향상시킵니다:

- ✅ **오버샘플링**: SMOTE, ADASYN, BorderlineSMOTE
- ✅ **언더샘플링**: RandomUnderSampler
- ✅ **하이브리드**: SMOTE-Tomek
- ✅ **자동 Train/Test 분리**: Data leakage 방지
- ✅ **유연한 샘플링 비율**: 0.05 ~ 1.0

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd plugins/imbalance-handling/skills/imbalance-handling
uv pip install --system -r requirements.txt
```

### 2. 클래스 불균형 처리

```bash
# SMOTE 사용 (기본값, 권장)
python scripts/balance_data.py \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1
```

## 📁 플러그인 구조

```
plugins/imbalance-handling/
├── plugin.json
├── README.md
├── agents/
│   └── imbalance-handler.md
├── commands/
│   └── balance-data.md
└── skills/
    └── imbalance-handling/
        ├── requirements.txt
        └── scripts/
            └── balance_data.py
```

## 🎯 주요 기능

### 1. 오버샘플링 (Over-sampling)
소수 클래스의 합성 샘플 생성

**SMOTE** (Synthetic Minority Over-sampling Technique)
- k-NN 기반 보간
- 가장 널리 사용됨
- 대부분의 경우 우수한 성능

**ADASYN** (Adaptive Synthetic Sampling)
- 학습하기 어려운 샘플에 더 많은 가중치
- SMOTE보다 정교한 샘플 생성

**BorderlineSMOTE**
- 경계선 근처 샘플만 오버샘플링
- 노이즈 감소

### 2. 언더샘플링 (Under-sampling)
다수 클래스 샘플 제거

**RandomUnderSampler**
- 무작위로 다수 클래스 샘플 제거
- 빠른 학습 시간
- 대용량 데이터에 적합

### 3. 하이브리드 (Hybrid)
오버샘플링 + 언더샘플링

**SMOTE-Tomek**
- SMOTE 후 Tomek Links로 경계선 정리
- 노이즈가 많은 데이터에 효과적

## 📊 출력

### 리샘플링된 데이터
```
projects/{project-name}/data/processed/
├── X_train_balanced.csv    # 리샘플링된 Train 특성
├── y_train_balanced.csv    # 리샘플링된 Train 타겟
├── X_test.csv              # 원본 Test 특성 (리샘플링 X)
└── y_test.csv              # 원본 Test 타겟 (리샘플링 X)
```

### 콘솔 출력
```
============================================================
클래스 불균형 처리 시작
============================================================

데이터 로드 중...
✓ X: 284,807건 × 33개 특성
✓ y: 284,807건

Train/Test 분리 (test_size=0.2)...
✓ Train: 227,845건, Test: 56,962건

리샘플링 적용 중 (방법: smote, 비율: 0.1)...
  원본 분포: {0: 227,451, 1: 394}
  변환 후 분포: {0: 227,451, 1: 22,745}
  생성된 샘플: 22,351건

✓ 저장 완료:
   projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv
   projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv
   projects/creditcard-fraud-detection/data/processed/X_test.csv
   projects/creditcard-fraud-detection/data/processed/y_test.csv

============================================================
클래스 불균형 처리 완료
============================================================

다음 단계:
   /train-models --algorithms xgboost,lightgbm
```

## 🔧 사용 예시

### Example 1: 신용카드 사기 탐지 (1:578 → 1:10)
```bash
python balance_data.py \
  --X-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/creditcard_processed_y.csv" \
  --method smote \
  --ratio 0.1
```

**결과**:
- 원본: 284,315 (정상) vs 492 (사기) = 1:578
- 리샘플링 후: 227,451 vs 22,745 = 1:10

### Example 2: ADASYN으로 정교한 샘플링
```bash
python balance_data.py \
  --X-path "projects/my-project/data/processed/X.csv" \
  --y-path "projects/my-project/data/processed/y.csv" \
  --method adasyn \
  --ratio 0.2
```

### Example 3: 대용량 데이터 - 언더샘플링
```bash
python balance_data.py \
  --X-path "projects/big-data/data/processed/X.csv" \
  --y-path "projects/big-data/data/processed/y.csv" \
  --method undersample \
  --ratio 0.5
```

## 📈 리샘플링 방법 비교

| 방법 | 유형 | 속도 | 성능 | 사용 시기 |
|------|------|------|------|---------|
| **SMOTE** | Over-sampling | 보통 | 우수 | 기본 추천 (대부분의 경우) |
| **ADASYN** | Over-sampling | 느림 | 매우 우수 | 정교한 샘플링 필요 시 |
| **BorderlineSMOTE** | Over-sampling | 보통 | 우수 | 클래스 경계 불분명 시 |
| **RandomUnderSampler** | Under-sampling | 빠름 | 보통 | 대용량 데이터 (100만 건+) |
| **SMOTE-Tomek** | Hybrid | 느림 | 매우 우수 | 노이즈 많은 데이터 |

## 📊 샘플링 비율 가이드

| 원본 불균형 비율 | 권장 ratio | 최종 비율 | 설명 |
|----------------|-----------|----------|------|
| 1:500+ | 0.05-0.1 | 1:20 ~ 1:10 | 극심한 불균형 → 보수적 |
| 1:100 | 0.1-0.2 | 1:10 ~ 1:5 | 심한 불균형 |
| 1:50 | 0.2-0.5 | 1:5 ~ 1:2 | 중간 불균형 |
| 1:10 | 0.5-1.0 | 1:2 ~ 1:1 | 가벼운 불균형 |

⚠️ **주의**: ratio를 1.0에 가깝게 설정하면 과적합 위험!

## 🐛 트러블슈팅

### 문제: 리샘플링 후 성능 오히려 하락
**해결**:
- ratio를 낮춤 (1.0 → 0.1)
- SMOTE 대신 Class weights 사용
```python
model = XGBClassifier(scale_pos_weight=578)
```

### 문제: 메모리 부족
**해결**:
- ratio를 낮춤 (0.1 → 0.05)
- RandomUnderSampler 사용
- 청크 단위 처리

### 문제: "ValueError: The least populated class has only 1 member"
**해결**:
- 클래스 샘플 수가 너무 적음
- 데이터 수집 추가 필요

## 🔗 관련 플러그인

- `data-profiling`: 클래스 분포 확인
- `feature-engineering`: 전처리 (리샘플링 전 필수)
- `model-selection`: 모델 학습 (리샘플링 후)

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0

## 💡 Best Practices

### 리샘플링 전
- [ ] 데이터 전처리 완료 (`/engineer-features`)
- [ ] 클래스 분포 확인 (`/profile-data`)
- [ ] 불균형 비율 계산 (1:10 미만이면 리샘플링 필요)

### 리샘플링 시
- [ ] **Train 데이터만** 리샘플링 (Test는 원본 유지)
- [ ] Train/Test 분리 **후** 리샘플링 (Data leakage 방지)
- [ ] ratio는 0.1부터 시작하여 조정

### 리샘플링 후
- [ ] Train/Test 클래스 분포 확인
- [ ] 파일 크기 확인 (메모리 고려)
- [ ] F1-Score로 성능 평가 (Accuracy 금지)
