# Feature Engineering Plugin

데이터 전처리 및 특성 엔지니어링을 수행하여 모델 학습에 적합한 데이터를 생성하는 플러그인입니다.

## 📋 개요

이 플러그인은 원본 데이터를 모델 학습에 최적화된 형태로 변환합니다:

- ✅ **스케일링**: RobustScaler, StandardScaler, MinMaxScaler
- ✅ **시간 특성 추출**: Hour, Day, Cyclical encoding
- ✅ **범주형 인코딩**: One-hot, Label, Target encoding (예정)
- ✅ **결측치/이상치 처리** (예정)
- ✅ **파생 변수 생성** (예정)
- ✅ **전처리 파이프라인 저장**: 재사용 가능

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
cd plugins/feature-engineering/skills/feature-engineering
uv pip install --system -r requirements.txt
```

### 2. 특성 엔지니어링 실행

```bash
python scripts/transform_features.py \
  --data-path "../../../../projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical" \
  --scaling-strategy "robust"
```

## 📁 플러그인 구조

```
plugins/feature-engineering/
├── plugin.json
├── README.md
├── agents/
│   └── feature-engineer.md
├── commands/
│   └── engineer-features.md
└── skills/
    └── feature-engineering/
        ├── requirements.txt
        └── scripts/
            └── transform_features.py
```

## 🎯 주요 기능

### 1. 스케일링
- **RobustScaler** (권장): 이상치에 강건
- **StandardScaler**: 평균 0, 분산 1
- **MinMaxScaler**: 0-1 범위

### 2. 시간 특성 추출
- Hour (0-23)
- Day (0, 1, ...)
- Cyclical encoding (sin, cos)

### 3. 전처리 파이프라인
- joblib로 저장
- 신규 데이터 전처리 시 재사용

## 📊 출력

### 전처리된 데이터
```
projects/{project-name}/data/processed/
├── {dataset}_processed_X.csv  # 특성
└── {dataset}_processed_y.csv  # 타겟
```

### 전처리 파이프라인
```
projects/{project-name}/outputs/models/
└── {dataset}_preprocessing_pipeline.pkl
```

### 변환 로그
```
projects/{project-name}/outputs/reports/
└── {dataset}_feature_engineering_log.md
```

## 🔧 사용 예시

### 신용카드 사기 탐지
```bash
python transform_features.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical"
```

**결과**:
- Amount → Amount_scaled (RobustScaler)
- Time → Hour, Day, Hour_sin, Hour_cos
- V1-V28 유지 (이미 정규화됨)

## 🔗 관련 플러그인

- `data-profiling`: 전처리 전 데이터 분석
- `imbalance-handling`: 클래스 불균형 처리 (다음 단계)
- `model-selection`: 모델 학습 (전처리 후)

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0
