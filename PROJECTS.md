# 프로젝트 구조 가이드

## 📁 프로젝트 폴더 구조

모든 데이터 사이언스 분석 프로젝트는 `projects/` 폴더 하위에 주제별로 구성됩니다.

```
dantelabs-agentic-school/
├── plugins/                    # 재사용 가능한 플러그인 (카테고리별 구성)
│   ├── common/                 # 공통 유틸리티
│   ├── marketing/              # 마케팅 플러그인 (8개)
│   └── data-science/           # 데이터 사이언스 플러그인 (9개)
│       ├── data-profiling/
│       ├── feature-engineering/
│       ├── imbalance-handling/
│       ├── model-selection/
│       ├── hyperparameter-tuning/
│       ├── model-evaluation/
│       ├── shap-analysis/
│       ├── model-monitoring/
│       └── model-deployment/
│
├── projects/                   # 분석 프로젝트들 (주제별)
│   ├── creditcard-fraud-detection/
│   ├── customer-churn-prediction/
│   └── house-price-prediction/
│
├── samples/                    # 샘플 및 튜토리얼
│   └── datascience/
│
└── scripts/                    # 유틸리티 스크립트
    └── init_project.py         # 프로젝트 초기화
```

---

## 🏗️ 프로젝트 구조

각 프로젝트는 다음과 같은 표준 구조를 따릅니다:

```
projects/{project-name}/
├── data/
│   ├── raw/              # 원본 데이터 (읽기 전용, 수정 금지)
│   ├── processed/        # 전처리 완료 데이터 (모델 학습용)
│   └── interim/          # 중간 처리 데이터
│
├── outputs/
│   ├── models/           # 학습된 모델 및 파이프라인
│   │   ├── *.pkl         # Joblib 직렬화 모델
│   │   └── preprocessing_pipeline.pkl
│   │
│   ├── reports/          # 분석 리포트
│   │   ├── *_profile_report.html
│   │   ├── *_eda_report.md
│   │   └── *_evaluation_report.pdf
│   │
│   └── figures/          # 시각화 결과
│       ├── confusion_matrix.png
│       ├── pr_curve.png
│       └── shap_summary.png
│
├── notebooks/            # Jupyter 노트북 (탐색, 실험용)
│
├── .gitignore            # Git 제외 설정
└── README.md             # 프로젝트 문서
```

---

## 🚀 새 프로젝트 시작하기

### 1. 프로젝트 초기화

```bash
python scripts/init_project.py --name my-analysis-project
```

**생성되는 파일**:
- 표준 폴더 구조
- `.gitignore` (데이터/모델 제외)
- `README.md` (템플릿)

### 2. 데이터 준비

```bash
# 원본 데이터를 data/raw/에 복사
cp /path/to/your/data.csv projects/my-analysis-project/data/raw/
```

### 3. 분석 파이프라인 실행

#### Step 1: 프로파일링
```bash
python plugins/data-science/data-profiling/skills/profiling/scripts/generate_profile.py \
  --data-path "projects/my-analysis-project/data/raw/data.csv" \
  --target-column "target" \
  --output-dir "projects/my-analysis-project/outputs/reports"
```

#### Step 2: EDA 분석
```bash
python plugins/data-science/data-profiling/skills/profiling/scripts/analyze_eda.py \
  --data-path "projects/my-analysis-project/data/raw/data.csv" \
  --target-column "target" \
  --output-dir "projects/my-analysis-project/outputs/reports"
```

#### Step 3: 특성 엔지니어링
```bash
python plugins/data-science/feature-engineering/skills/feature-engineering/scripts/transform_features.py \
  --data-path "projects/my-analysis-project/data/raw/data.csv" \
  --target-column "target" \
  --output-dir "projects/my-analysis-project/data/processed"
```

#### Step 4: 불균형 처리
```bash
python plugins/data-science/imbalance-handling/skills/imbalance-handling/scripts/balance_data.py \
  --X-path "projects/my-analysis-project/data/processed/data_processed_X.csv" \
  --y-path "projects/my-analysis-project/data/processed/data_processed_y.csv" \
  --method smote \
  --output-dir "projects/my-analysis-project/data/processed"
```

#### Step 5: 모델 학습
```bash
python plugins/data-science/model-selection/skills/model-selection/scripts/train_model.py \
  --X-train-path "projects/my-analysis-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-analysis-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-analysis-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-analysis-project/data/processed/y_test.csv" \
  --algorithm xgboost \
  --output-dir "projects/my-analysis-project/outputs/models"
```

---

## 📝 프로젝트별 관리

### Git 관리

각 프로젝트의 `.gitignore`:
```gitignore
# 데이터 파일 (커밋 제외)
data/raw/*.csv
data/processed/*.csv

# 모델 파일 (커밋 제외)
outputs/models/*.pkl

# 대용량 리포트 (커밋 제외)
outputs/reports/*.html
```

**커밋 대상**:
- ✅ `README.md` (프로젝트 문서)
- ✅ `notebooks/*.ipynb` (분석 노트북)
- ✅ `outputs/reports/*.md` (Markdown 레포트)

**제외 대상**:
- ❌ 데이터 파일 (`data/`)
- ❌ 모델 파일 (`outputs/models/*.pkl`)
- ❌ 대용량 HTML 리포트

### 프로젝트 아카이빙

완료된 프로젝트는 압축하여 보관:
```bash
cd projects
tar -czf creditcard-fraud-detection.tar.gz creditcard-fraud-detection/
```

---

## 🎯 예시 프로젝트

### creditcard-fraud-detection
```bash
projects/creditcard-fraud-detection/
├── data/raw/creditcard.csv              # Kaggle 원본
├── data/processed/
│   ├── creditcard_processed_X.csv       # 33개 특성 (시간 특성 추가)
│   ├── X_train_balanced.csv             # SMOTE 적용
│   └── X_test.csv
├── outputs/
│   ├── models/
│   │   ├── xgboost_model.pkl            # ROC-AUC: 0.9760
│   │   └── preprocessing_pipeline.pkl
│   └── reports/
│       ├── creditcard_profile_report.html
│       └── creditcard_eda_report.md
└── README.md
```

---

## 💡 Best Practices

### 1. 명명 규칙
- 프로젝트명: 소문자 + 하이픈 (예: `house-price-prediction`)
- 데이터 파일: 설명적 이름 (예: `creditcard.csv`, `customer_churn.csv`)

### 2. 폴더 용도 준수
- `data/raw/`: 원본 데이터만 (절대 수정 금지)
- `data/interim/`: 중간 처리 결과 (디버깅용)
- `data/processed/`: 최종 전처리 데이터 (모델 학습용)

### 3. 재현 가능성
- Random seed 고정 (42)
- 전처리 파이프라인 저장
- 환경 정보 기록 (requirements.txt)

### 4. 문서화
- README.md에 분석 목적, 주요 결과, 다음 단계 기록
- 각 단계별 명령어 기록
- 성능 지표 기록

---

**생성일**: 2026-01-31
**업데이트**: 프로젝트별 폴더 구조 표준화
