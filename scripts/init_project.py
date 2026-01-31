#!/usr/bin/env python3
"""
데이터 사이언스 프로젝트 초기화 스크립트

사용법:
    python scripts/init_project.py --name creditcard-fraud-detection

생성되는 구조:
    projects/{project-name}/
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── interim/
    ├── outputs/
    │   ├── models/
    │   ├── reports/
    │   └── figures/
    ├── notebooks/
    └── README.md
"""

import argparse
from datetime import datetime
from pathlib import Path


def create_project_structure(project_name):
    """프로젝트 폴더 구조 생성"""

    # 프로젝트 루트 경로
    project_root = Path('projects') / project_name

    if project_root.exists():
        print(f"⚠️  프로젝트 '{project_name}'이 이미 존재합니다: {project_root}")
        return None

    # 폴더 구조 생성
    folders = [
        project_root / 'data' / 'raw',
        project_root / 'data' / 'processed',
        project_root / 'data' / 'interim',
        project_root / 'outputs' / 'models',
        project_root / 'outputs' / 'reports',
        project_root / 'outputs' / 'figures',
        project_root / 'notebooks',
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    # .gitignore 생성
    gitignore_content = """# Data files
data/raw/*.csv
data/raw/*.xlsx
data/raw/*.parquet
data/processed/*.csv
data/interim/*.csv
*.zip

# Model files
outputs/models/*.pkl
outputs/models/*.joblib
outputs/models/*.h5

# Large reports
outputs/reports/*.html

# Jupyter Notebook checkpoints
.ipynb_checkpoints/
**/.ipynb_checkpoints/

# Python
__pycache__/
*.py[cod]

# OS
.DS_Store
"""

    (project_root / '.gitignore').write_text(gitignore_content)

    # README.md 생성
    readme_content = f"""# {project_name.replace('-', ' ').title()}

**생성일**: {datetime.now().strftime('%Y-%m-%d')}

## 📋 프로젝트 개요

[프로젝트 설명을 여기에 작성하세요]

## 📁 폴더 구조

```
{project_name}/
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
python plugins/data-profiling/skills/profiling/scripts/generate_profile.py \\
  --data-path "projects/{project_name}/data/raw/your_data.csv" \\
  --target-column "target" \\
  --output-dir "projects/{project_name}/outputs/reports"
```

### 3. EDA 분석
```bash
python plugins/data-profiling/skills/profiling/scripts/analyze_eda.py \\
  --data-path "projects/{project_name}/data/raw/your_data.csv" \\
  --target-column "target" \\
  --output-dir "projects/{project_name}/outputs/reports"
```

### 4. 특성 엔지니어링
```bash
python plugins/feature-engineering/skills/feature-engineering/scripts/transform_features.py \\
  --data-path "projects/{project_name}/data/raw/your_data.csv" \\
  --target-column "target" \\
  --time-features "hour,day,cyclical" \\
  --output-dir "projects/{project_name}/data/processed"
```

### 5. 불균형 처리
```bash
python plugins/imbalance-handling/skills/imbalance-handling/scripts/balance_data.py \\
  --X-path "projects/{project_name}/data/processed/your_data_processed_X.csv" \\
  --y-path "projects/{project_name}/data/processed/your_data_processed_y.csv" \\
  --method smote \\
  --ratio 0.1 \\
  --output-dir "projects/{project_name}/data/processed"
```

### 6. 모델 학습
```bash
python plugins/model-selection/skills/model-selection/scripts/train_model.py \\
  --X-train-path "projects/{project_name}/data/processed/X_train_balanced.csv" \\
  --y-train-path "projects/{project_name}/data/processed/y_train_balanced.csv" \\
  --X-test-path "projects/{project_name}/data/processed/X_test.csv" \\
  --y-test-path "projects/{project_name}/data/processed/y_test.csv" \\
  --algorithm xgboost \\
  --output-dir "projects/{project_name}/outputs/models"
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
"""

    (project_root / 'README.md').write_text(readme_content)

    return project_root


def main():
    parser = argparse.ArgumentParser(description='데이터 사이언스 프로젝트 초기화')
    parser.add_argument('--name', type=str, required=True, help='프로젝트 이름 (예: creditcard-fraud-detection)')

    args = parser.parse_args()

    print("=" * 60)
    print("프로젝트 초기화")
    print("=" * 60)

    project_root = create_project_structure(args.name)

    if project_root:
        print(f"\n✅ 프로젝트 생성 완료: {project_root}")
        print(f"\n📁 생성된 폴더:")
        for folder in sorted(project_root.rglob('*')):
            if folder.is_dir():
                print(f"   {folder.relative_to('projects')}/")

        print(f"\n📄 생성된 파일:")
        print(f"   {args.name}/.gitignore")
        print(f"   {args.name}/README.md")

        print(f"\n🚀 다음 단계:")
        print(f"   1. 원본 데이터를 projects/{args.name}/data/raw/ 에 저장")
        print(f"   2. 데이터 프로파일링 실행")
        print(f"   3. projects/{args.name}/README.md 참고\n")


if __name__ == "__main__":
    main()
