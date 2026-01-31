# Creditcard Fraud Detection

**생성일**: 2026-01-31

## 📋 프로젝트 개요

[프로젝트 설명을 여기에 작성하세요]

## 📁 폴더 구조

```
creditcard-fraud-detection/
├── data/
│   ├── raw/              # 원본 데이터 (읽기 전용)
│   ├── processed/        # 전처리 완료 데이터
│   └── interim/          # 중간 처리 데이터
├── outputs/
│   ├── models/           # 학습된 모델 및 파이프라인
│   ├── reports/          # 분석 리포트 (HTML, Markdown, PDF)
│   └── figures/          # 시각화 결과
├── notebooks/            # Jupyter 노트북
└── README.md             # 이 파일
```

## 🚀 사용법

### 1. 원본 데이터 준비
원본 데이터를 `data/raw/` 폴더에 저장하세요.

### 2. 데이터 프로파일링
```bash
python plugins/data-profiling/skills/profiling/scripts/generate_profile.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/your_data.csv" \
  --target-column "target" \
  --output-dir "projects/creditcard-fraud-detection/outputs/reports"
```

### 3. EDA 분석
```bash
python plugins/data-profiling/skills/profiling/scripts/analyze_eda.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/your_data.csv" \
  --target-column "target" \
  --output-dir "projects/creditcard-fraud-detection/outputs/reports"
```

### 4. 특성 엔지니어링
```bash
python plugins/feature-engineering/skills/feature-engineering/scripts/transform_features.py \
  --data-path "projects/creditcard-fraud-detection/data/raw/your_data.csv" \
  --target-column "target" \
  --time-features "hour,day,cyclical" \
  --output-dir "projects/creditcard-fraud-detection/data/processed"
```

### 5. 불균형 처리
```bash
python plugins/imbalance-handling/skills/imbalance-handling/scripts/balance_data.py \
  --X-path "projects/creditcard-fraud-detection/data/processed/your_data_processed_X.csv" \
  --y-path "projects/creditcard-fraud-detection/data/processed/your_data_processed_y.csv" \
  --method smote \
  --ratio 0.1 \
  --output-dir "projects/creditcard-fraud-detection/data/processed"
```

### 6. 모델 학습
```bash
python plugins/model-selection/skills/model-selection/scripts/train_model.py \
  --X-train-path "projects/creditcard-fraud-detection/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/creditcard-fraud-detection/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/creditcard-fraud-detection/data/processed/X_test.csv" \
  --y-test-path "projects/creditcard-fraud-detection/data/processed/y_test.csv" \
  --algorithm xgboost \
  --output-dir "projects/creditcard-fraud-detection/outputs/models"
```

## 📊 결과

### 데이터
- 원본: `data/raw/your_data.csv`
- 전처리: `data/processed/your_data_processed_X.csv`

### 모델
- 학습된 모델: `outputs/models/xgboost_model.pkl`
- 전처리 파이프라인: `outputs/models/preprocessing_pipeline.pkl`

### 리포트
- 프로파일링: `outputs/reports/your_data_profile_report.html`
- EDA 분석: `outputs/reports/your_data_eda_report.md`
- 특성 엔지니어링 로그: `outputs/reports/your_data_feature_engineering_log.md`

## 📝 노트

[여기에 프로젝트 진행 중 메모를 작성하세요]

---

**생성 도구**: DanteLabs Agentic School - Data Science Plugins
