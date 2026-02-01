---
name: profiling
description: 데이터 프로파일링 및 자동화된 EDA를 위한 유틸리티 스크립트
version: 1.0.0
tags: [data-science, eda, profiling, statistics]
---

# Profiling Skill

데이터셋의 품질과 특성을 자동으로 분석하여 종합 리포트를 생성하는 스킬입니다.

## 개요

이 스킬은 **ydata-profiling** (구 pandas-profiling)을 사용하여 다음을 수행합니다:

1. ✅ 데이터 품질 검증 (결측치, 중복, 이상치)
2. ✅ 통계적 분석 (분포, 상관관계, 왜도/첨도)
3. ✅ 자동 시각화 (히스토그램, 상관관계 히트맵 등)
4. ✅ HTML 리포트 생성 및 **브라우저 자동 오픈**
5. ✅ 주요 발견사항 요약

## 설치

### uv 패키지 매니저 (권장 - 10-100배 빠름)

```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 macOS
brew install uv

# 의존성 설치
cd plugins/data-profiling/skills/profiling
uv pip install -r requirements.txt
```

### pip 사용 (기존 방식)

```bash
cd plugins/data-profiling/skills/profiling
pip install -r requirements.txt
```

### 설치 확인

```bash
python3 -c "import ydata_profiling; print(f'✓ ydata-profiling {ydata_profiling.__version__}')"
```

## 사용법

### Python 스크립트 직접 실행

```bash
cd plugins/data-profiling/skills/profiling/scripts

# 기본 사용법
python generate_profile.py \
  --data-path "path/to/data.csv" \
  --output-dir "outputs/reports"

# 타겟 컬럼 지정
python generate_profile.py \
  --data-path "samples/datascience/data/raw/creditcard.csv" \
  --target-column "Class" \
  --mode explorative

# 대용량 데이터 샘플링
python generate_profile.py \
  --data-path "large_data.csv" \
  --sample-size 50000 \
  --mode minimal
```

### Claude Code 커맨드로 실행

```bash
/profile-data --data-path "./data/raw/creditcard.csv" --target-column "Class"
```

## 스크립트 파일

### `generate_profile.py`

**주요 기능**:
- 다양한 파일 형식 지원 (CSV, Excel, Parquet, JSON 등)
- 자동 샘플링 (대용량 데이터)
- ydata-profiling을 통한 종합 분석
- HTML 리포트 생성
- **운영체제별 브라우저 자동 실행** (macOS, Linux, Windows)
- 콘솔 요약 출력

**의존성**:
```bash
# uv 사용 (권장)
cd plugins/data-profiling/skills/profiling
uv pip install -r requirements.txt

# 또는 pip 사용
pip install -r requirements.txt
```

**포함 패키지**:
- `pandas` - 데이터 처리
- `ydata-profiling` - 자동화된 EDA

**주요 파라미터**:
| 파라미터 | 설명 | 기본값 |
|---------|------|--------|
| `--data-path` | 데이터 파일 경로 | (필수) |
| `--target-column` | 타겟 변수 컬럼명 | None |
| `--sample-size` | 샘플링 크기 | None (전체) |
| `--mode` | 프로파일링 모드 | explorative |
| `--output-dir` | 리포트 저장 디렉토리 | outputs/reports |
| `--no-browser` | 브라우저 자동 오픈 비활성화 | False |

## 프로파일링 모드

### 1. minimal
- **실행 시간**: ~1분
- **포함 내용**: 기본 통계, 결측치, 데이터 타입
- **권장 상황**: 빠른 데이터 확인

### 2. default (기본)
- **실행 시간**: ~3분
- **포함 내용**: 분포, 상관관계, 기본 시각화
- **권장 상황**: 일반적인 EDA

### 3. explorative (고급)
- **실행 시간**: ~5-10분
- **포함 내용**: 모든 분석 + 상호작용 분석
- **권장 상황**: 심도있는 탐색

## HTML 리포트 구조

생성된 리포트는 다음 섹션을 포함합니다:

### 1. Overview (개요)
- Dataset info (행/열 개수, 메모리 사용량)
- Variable types (수치형, 범주형, 날짜형 등)
- Warnings (경고 개수)

### 2. Variables (변수별 분석)
각 변수마다:
- **통계량**: Mean, Median, Min, Max, Std, Skewness, Kurtosis
- **분포 시각화**: Histogram, KDE plot
- **결측치**: Missing count & percentage
- **고유값**: Distinct count, Most common values
- **극단값**: Minimum/Maximum values

### 3. Interactions (상호작용)
- Scatter plot matrix (변수 간 산점도)
- Pairwise relationships

### 4. Correlations (상관관계)
- Pearson correlation matrix
- Spearman correlation matrix
- Heatmap 시각화

### 5. Missing Values (결측치)
- Missing value matrix
- Missing value heatmap
- Nullity correlation

### 6. Sample (샘플 데이터)
- First 10 rows
- Last 10 rows
- Random sample

### 7. Alerts (경고)
자동 탐지되는 이슈:
- ⚠️ High correlation (> 0.9)
- ⚠️ High missing rate (> 50%)
- ⚠️ Constant/Quasi-constant features
- ⚠️ High cardinality (범주형 변수)
- ⚠️ Imbalanced classes
- ⚠️ Outliers

## 예시: 신용카드 사기 탐지 데이터

```bash
python generate_profile.py \
  --data-path "samples/datascience/data/raw/creditcard.csv" \
  --target-column "Class" \
  --mode explorative \
  --output-dir "outputs/reports"
```

**예상 출력**:
```
═══════════════════════════════════════════════════════════
데이터 프로파일링 시작
═══════════════════════════════════════════════════════════

✓ 데이터 로드 완료: 284,807건, 31개 컬럼
✓ 메모리 사용량: 67.4 MB

─────────────────────────────────────────────────────────
기본 정보
─────────────────────────────────────────────────────────

전체 거래 건수: 284,807건
특성 개수: 31개
결측치: 0개

클래스 분포:
  정상 거래 (Class 0): 284,315건 (99.83%)
  사기 거래 (Class 1): 492건 (0.17%)
  불균형 비율: 1:578

─────────────────────────────────────────────────────────
프로파일링 리포트 생성 중...
─────────────────────────────────────────────────────────
⏳ 약 5분 소요될 수 있습니다...

✓ 완료!
📊 리포트 저장 위치: outputs/reports/creditcard_profile_report.html

🌐 브라우저에서 리포트가 자동으로 열렸습니다.

⚠️  주요 발견사항:
   - 클래스 불균형: 1:578 (사기: 0.17%)
   - Amount 변수에서 이상치 탐지
   - Time 변수는 초 단위 경과 시간

💡 권고사항:
   1. 클래스 불균형 처리 필요 (SMOTE, Undersampling)
   2. Amount 변수 스케일링 권장 (StandardScaler, RobustScaler)
   3. Time 변수에서 시간대 특성 추출 고려
   4. V1-V28은 PCA 변환된 특성 (직접 해석 어려움)

다음 단계:
   /engineer-features: 특성 엔지니어링
   /handle-imbalance: 클래스 불균형 처리
```

## 브라우저 자동 오픈 기능

스크립트는 운영체제를 자동 감지하여 적절한 명령어로 브라우저를 엽니다:

```python
import platform
import subprocess

def open_in_browser(filepath):
    """운영체제에 맞게 브라우저에서 HTML 파일 열기"""
    system = platform.system()

    if system == 'Darwin':  # macOS
        subprocess.run(['open', filepath])
    elif system == 'Linux':
        subprocess.run(['xdg-open', filepath])
    elif system == 'Windows':
        subprocess.run(['start', filepath], shell=True)
```

**비활성화 옵션**:
```bash
# 브라우저 자동 오픈 안 함
python generate_profile.py \
  --data-path "data.csv" \
  --no-browser
```

## 성능 최적화

### 대용량 데이터 (100만 건 이상)
1. **샘플링 사용**:
   ```bash
   --sample-size 50000
   ```

2. **Minimal 모드**:
   ```bash
   --mode minimal
   ```

3. **결합**:
   ```bash
   python generate_profile.py \
     --data-path "big_data.csv" \
     --sample-size 100000 \
     --mode minimal
   ```

### 메모리 사용량 줄이기
- 불필요한 컬럼 제거 후 분석
- Explorative 모드 대신 Default 모드 사용
- 샘플 크기 10,000~50,000으로 제한

## 출력 파일 관리

### 파일명 규칙
```
{dataset_name}_profile_report.html
```

예시:
- `creditcard_profile_report.html`
- `customer_churn_profile_report.html`

### Git 관리
HTML 리포트는 용량이 크므로 `.gitignore`에 추가:
```gitignore
outputs/reports/*.html
```

## 참고 문서

- [ydata-profiling 공식 문서](https://docs.profiling.ydata.ai/)
- [pandas-profiling (구버전) GitHub](https://github.com/ydataai/ydata-profiling)

## 라이선스

MIT License
