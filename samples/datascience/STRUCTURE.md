# 프로젝트 구조

```
samples/datascience/
├── README.md                    # 프로젝트 개요 및 학습 가이드
├── STRUCTURE.md                 # 이 파일 (폴더 구조 설명)
├── .gitignore                   # Git 제외 파일 설정
│
├── data/                        # 데이터 저장소
│   ├── raw/                     # 원본 데이터 (읽기 전용)
│   │   └── creditcard.csv       # Kaggle 다운로드 원본 (284,807건)
│   ├── interim/                 # 중간 처리 데이터
│   └── processed/               # 최종 전처리 완료 데이터
│
├── notebooks/                   # Jupyter 노트북
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_imbalance_handling.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation_and_interpretation.ipynb
│
├── scripts/                     # 재사용 가능한 Python 스크립트
│   ├── 01_data_profiling.py     # 자동화된 EDA 리포트 생성
│   ├── 02_preprocessing.py      # 전처리 파이프라인
│   ├── 03_train_models.py       # 모델 학습 스크립트
│   ├── 04_evaluate_models.py    # 모델 평가 스크립트
│   └── utils.py                 # 공통 유틸리티 함수
│
└── outputs/                     # 산출물 저장소
    ├── models/                  # 학습된 모델 파일
    │   ├── *.pkl                # scikit-learn 모델
    │   ├── *.joblib             # joblib 직렬화
    │   └── model_registry.json  # 모델 메타데이터
    │
    ├── reports/                 # 분석 리포트
    │   ├── data_profile_report.html
    │   ├── evaluation_report.pdf
    │   └── model_comparison.xlsx
    │
    └── figures/                 # 시각화 결과
        ├── class_distribution.png
        ├── correlation_heatmap.png
        ├── confusion_matrix.png
        ├── pr_curve.png
        └── shap_summary.png
```

---

## 폴더 역할

### `data/`
- **raw/**: 원본 데이터. 절대 수정하지 않음 (immutable)
- **interim/**: 중간 단계 데이터 (예: 이상치 제거 후, 리샘플링 전)
- **processed/**: 모델 학습에 바로 사용 가능한 최종 데이터

### `notebooks/`
- 탐색적 분석, 실험, 프로토타이핑용
- 각 노트북은 하나의 단계에 집중
- 재현 가능하도록 셀 실행 순서 유지

### `scripts/`
- 프로덕션 수준의 재사용 가능한 코드
- 노트북에서 검증된 로직을 스크립트화
- CLI로 실행 가능 (`python scripts/01_data_profiling.py`)

### `outputs/`
- 학습 결과물 저장 (Git에는 커밋하지 않음)
- 모델 버전 관리
- 리포트 자동 생성

---

## 데이터 흐름

```
data/raw/creditcard.csv
    ↓ [01_data_profiling.py]
outputs/reports/data_profile_report.html
    ↓ [02_preprocessing.py]
data/processed/X_train.csv, y_train.csv
    ↓ [03_train_models.py]
outputs/models/random_forest_v1.pkl
    ↓ [04_evaluate_models.py]
outputs/reports/evaluation_report.pdf
```

---

## 명명 규칙

### 스크립트 파일
- `01_`, `02_`, ... : 실행 순서
- 동사로 시작 (`train`, `evaluate`, `preprocess`)
- 소문자 + 언더스코어

### 노트북 파일
- 단계별 번호 + 설명적 제목
- 예: `01_exploratory_data_analysis.ipynb`

### 모델 파일
- `{모델명}_{버전}_{날짜}.pkl`
- 예: `random_forest_v1_20260131.pkl`

### 리포트 파일
- 설명적 이름 사용
- 예: `evaluation_report_20260131.pdf`

---

## Git 관리

### 커밋 대상
✅ 코드 (`.py`, `.ipynb`)
✅ 문서 (`.md`)
✅ 설정 파일 (`.gitignore`)

### 제외 대상
❌ 데이터 파일 (`data/`)
❌ 모델 파일 (`outputs/models/`)
❌ 대용량 리포트 (`outputs/reports/*.html`)

---

**생성일**: 2026-01-31
