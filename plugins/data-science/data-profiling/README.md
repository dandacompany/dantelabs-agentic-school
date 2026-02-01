# Data Profiling Plugin

데이터 품질 검증 및 자동화된 탐색적 데이터 분석(EDA)을 수행하는 플러그인입니다.

## 📋 개요

이 플러그인은 데이터 사이언스 파이프라인의 첫 단계로, 데이터셋을 자동으로 분석하여 다음을 제공합니다:

### 1️⃣ 프로파일링 (Profiling)
- ✅ 데이터 품질 검증 (결측치, 중복, 이상치)
- ✅ 통계적 분석 (분포, 상관관계, 왜도/첨도)
- ✅ 자동 시각화 (히스토그램, 상관관계 히트맵 등)
- ✅ **HTML 리포트 생성 및 브라우저 자동 오픈**

### 2️⃣ EDA 분석 (Analysis) ⭐ NEW
- ✅ 프로파일링 리포트 심층 분석
- ✅ 데이터 전처리 지침 (우선순위별, 코드 포함)
- ✅ 추가 분석 권고사항 (Feature importance, SHAP 등)
- ✅ 모델링 전략 (알고리즘, 평가지표, 하이퍼파라미터)
- ✅ **A4 한 장 분량 Markdown 레포트** (PDF 변환 가능)

## 🚀 빠른 시작

### 1. 의존성 설치

**uv 사용 (권장 - 10-100배 빠름)**:
```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 macOS
brew install uv

# 패키지 설치
cd plugins/data-profiling/skills/profiling
uv pip install -r requirements.txt
```

**pip 사용 (기존 방식)**:
```bash
cd plugins/data-profiling/skills/profiling
pip install -r requirements.txt
```

### 2. 데이터 프로파일링

```bash
# Claude Code에서 실행
/profile-data \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# 또는 Python 스크립트 직접 실행
cd plugins/data-profiling/skills/profiling/scripts
python generate_profile.py \
  --data-path "../../../../../projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --mode explorative
```

**출력**: `projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html` (브라우저 자동 오픈)

### 3. EDA 분석 레포트 생성 ⭐ NEW

```bash
# Claude Code에서 실행
/analyze-profile \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# 또는 Python 스크립트 직접 실행
python analyze_eda.py \
  --data-path "../../../../../projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --output-format markdown
```

**출력**: `projects/creditcard-fraud-detection/outputs/reports/creditcard_eda_report.md` (A4 한 장 분량)

## 📁 플러그인 구조

```
plugins/data-profiling/
├── plugin.json                  # 플러그인 메타데이터
├── README.md                    # 플러그인 문서
├── agents/
│   ├── data-profiler.md         # 프로파일링 에이전트
│   └── eda-analyst.md          # ⭐ EDA 분석 에이전트 (NEW)
├── commands/
│   ├── profile-data.md          # 프로파일링 커맨드
│   └── analyze-profile.md      # ⭐ EDA 분석 커맨드 (NEW)
└── skills/
    └── profiling/
        ├── SKILL.md             # 스킬 문서
        ├── requirements.txt     # Python 패키지 의존성
        └── scripts/
            ├── generate_profile.py  # 프로파일링 스크립트
            └── analyze_eda.py      # ⭐ EDA 분석 스크립트 (NEW)
```

## 🎯 주요 기능

### 1. 자동화된 EDA
- ydata-profiling을 사용한 종합 분석
- 30+ 통계 지표 자동 계산
- 인터랙티브 시각화

### 2. 브라우저 자동 오픈
- HTML 리포트 생성 후 자동으로 브라우저에서 오픈
- macOS, Linux, Windows 모두 지원

### 3. 커스텀 분석
- 클래스 불균형 탐지
- 스케일 차이 경고
- 높은 상관관계 감지

### 4. 성능 최적화
- 대용량 데이터 샘플링 지원
- 3가지 프로파일링 모드 (minimal, default, explorative)

## 📊 사용 예시

### Example 1: 기본 프로파일링
```bash
/profile-data --data-path "projects/my-analysis/data/raw/data.csv"
```

### Example 2: 타겟 컬럼 지정 (분류 문제)
```bash
/profile-data \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"
```

### Example 3: 대용량 데이터 샘플링
```bash
/profile-data \
  --data-path "projects/big-data-analysis/data/raw/large_data.csv" \
  --sample-size 50000 \
  --mode minimal
```

### Example 4: 브라우저 자동 오픈 비활성화
```bash
python generate_profile.py \
  --data-path "projects/my-analysis/data/raw/data.csv" \
  --no-browser
```

## 📈 프로파일링 모드

| 모드 | 실행 시간 | 세부 수준 | 권장 상황 |
|------|---------|---------|---------|
| **minimal** | ~1분 | 기본 통계만 | 빠른 데이터 확인 |
| **default** | ~3분 | 표준 분석 | 일반적인 EDA |
| **explorative** | ~5-10분 | 모든 분석 포함 | 심도있는 분석 |

## 🔧 파라미터

### 필수 파라미터
- `--data-path`: 분석할 데이터 파일 경로

### 선택 파라미터
- `--target-column`: 타겟 변수 컬럼명 (분류/회귀 문제)
- `--sample-size`: 샘플링 크기 (대용량 데이터)
- `--mode`: 프로파일링 모드 (minimal/default/explorative)
- `--output-dir`: 리포트 저장 디렉토리 (기본값: outputs/reports)
- `--no-browser`: 브라우저 자동 오픈 비활성화

## 📤 출력

### HTML 리포트
- **위치**: `projects/{project-name}/outputs/reports/{dataset_name}_profile_report.html`
- **포함 내용**:
  - Overview (데이터셋 개요)
  - Variables (변수별 상세 분석)
  - Interactions (변수 간 상호작용)
  - Correlations (상관관계 매트릭스)
  - Missing values (결측치 패턴)
  - Alerts (데이터 품질 경고)

### 콘솔 출력
- 기본 정보 (행/열 개수, 메모리)
- 클래스 분포 (타겟 컬럼이 있는 경우)
- 주요 발견사항
- 권고사항
- 다음 단계 안내

## 🎨 출력 예시

```
═══════════════════════════════════════════════════════════
데이터 프로파일링 시작
═══════════════════════════════════════════════════════════

✓ 데이터 로드 완료: 284,807건, 31개 컬럼
✓ 메모리 사용량: 67.4 MB

─────────────────────────────────────────────────────────
기본 정보
─────────────────────────────────────────────────────────

전체 행 수: 284,807건
전체 열 수: 31개
메모리 사용량: 67.4 MB
결측치: 0개

타겟 컬럼: Class
클래스 분포:
  클래스 0: 284,315건 (99.83%)
  클래스 1: 492건 (0.17%)
  불균형 비율: 1:578

─────────────────────────────────────────────────────────
프로파일링 리포트 생성 중...
─────────────────────────────────────────────────────────
모드: explorative
⏳ 수 분 소요될 수 있습니다...

✓ 완료!
📊 리포트 저장 위치: projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html

🌐 브라우저에서 리포트를 여는 중...
✓ 브라우저에서 리포트가 열렸습니다.

─────────────────────────────────────────────────────────
⚠️  주요 발견사항 및 권고사항
─────────────────────────────────────────────────────────

⚠️  클래스 불균형: 1:578
   권고: /handle-imbalance로 불균형 처리 (SMOTE, Undersampling)

⚠️  변수 간 스케일 차이가 큽니다 (최대/최소 = 1000배)
   권고: /engineer-features로 스케일링 (StandardScaler, MinMaxScaler)

💡 다음 단계:
   /engineer-features: 특성 엔지니어링 및 전처리
   /handle-imbalance: 클래스 불균형 처리
   /train-models: 모델 학습

═══════════════════════════════════════════════════════════
프로파일링 완료
═══════════════════════════════════════════════════════════
```

## 🔍 지원 파일 형식

| 형식 | 확장자 | 지원 여부 |
|------|--------|---------|
| CSV | `.csv` | ✅ |
| Excel | `.xlsx`, `.xls` | ✅ |
| Parquet | `.parquet` | ✅ |
| JSON | `.json` | ✅ |
| Feather | `.feather` | ✅ |
| HDF5 | `.h5`, `.hdf5` | ✅ |

## 🐛 트러블슈팅

### 문제: "ModuleNotFoundError: No module named 'ydata_profiling'"
```bash
pip install ydata-profiling
```

### 문제: 메모리 부족 에러
```bash
# 샘플 크기 줄이기
/profile-data \
  --data-path "projects/my-analysis/data/raw/data.csv" \
  --sample-size 10000
```

### 문제: 브라우저가 자동으로 열리지 않음
- macOS: `open projects/{project-name}/outputs/reports/report.html`
- Linux: `xdg-open projects/{project-name}/outputs/reports/report.html`
- Windows: `start projects/{project-name}/outputs/reports/report.html`

## 📚 관련 문서

- [ydata-profiling 공식 문서](https://docs.profiling.ydata.ai/)
- [Agent 정의](./agents/data-profiler.md)
- [Command 문서](./commands/profile-data.md)
- [Skill 문서](./skills/profiling/SKILL.md)

## 🔗 관련 플러그인

- `feature-engineering`: 특성 생성 및 변환
- `imbalance-handling`: 클래스 불균형 처리
- `model-selection`: 모델 학습 및 선택

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0
