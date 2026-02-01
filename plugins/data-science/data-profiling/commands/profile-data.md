---
name: profile-data
description: 데이터셋의 품질과 특성을 분석하여 자동화된 EDA 리포트를 생성합니다.
arguments:
  - name: data-path
    description: 분석할 데이터 파일 경로 (CSV, Excel, Parquet 등)
    required: true
  - name: target-column
    description: 타겟 변수 컬럼명 (분류/회귀 문제인 경우)
    required: false
  - name: sample-size
    description: 샘플링 크기 (대용량 데이터인 경우, 예: 50000)
    required: false
  - name: mode
    description: 프로파일링 모드 (minimal, default, explorative)
    required: false
    default: "explorative"
  - name: output-dir
    description: 리포트 저장 디렉토리
    required: false
    default: "projects/{project-name}/outputs/reports"
---

# /profile-data

데이터셋을 자동으로 분석하여 종합적인 EDA 리포트를 생성하고 브라우저에서 엽니다.

## Usage

```bash
# 기본 사용법
/profile-data --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv"

# 타겟 컬럼 지정
/profile-data \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"

# 대용량 데이터 샘플링
/profile-data \
  --data-path "projects/large-data-analysis/data/raw/large_data.csv" \
  --sample-size 50000

# Minimal 모드 (빠른 분석)
/profile-data \
  --data-path "projects/my-analysis/data/raw/data.csv" \
  --mode minimal

# 출력 디렉토리 지정
/profile-data \
  --data-path "projects/my-analysis/data/raw/data.csv" \
  --output-dir "projects/my-analysis/outputs/reports"
```

## What This Command Does

### 1. 데이터 로드 및 검증
- 파일 존재 여부 확인
- 데이터 타입 자동 감지 (CSV, Excel, Parquet, JSON 등)
- 기본 정보 출력 (행/열 개수, 메모리 사용량)

### 2. 자동화된 프로파일링
- **ydata-profiling**을 사용한 종합 분석:
  - 각 변수별 상세 통계
  - 분포 시각화 (히스토그램, KDE)
  - 결측치 패턴 분석
  - 상관관계 매트릭스
  - 중복 데이터 탐지
  - 데이터 품질 경고 (Alerts)

### 3. 커스텀 분석 (타겟 컬럼이 지정된 경우)
- 클래스 분포 분석
- 클래스 불균형 계산
- 타겟 변수와 특성 간 관계 분석

### 4. HTML 리포트 생성 및 자동 오픈
- 인터랙티브 HTML 리포트 생성
- 브라우저 자동 실행
- 리포트 경로 출력

### 5. 주요 발견사항 요약
- Markdown 형식 요약 생성
- 데이터 품질 이슈 하이라이트
- 다음 단계 권고사항 제시

## Output Structure

### HTML 리포트
```
projects/{project-name}/outputs/reports/
└── {dataset_name}_profile_report.html
```

**리포트 섹션**:
1. **Overview**: 데이터셋 개요 및 기본 통계
2. **Variables**: 변수별 상세 분석
   - Type, Distinct count, Missing values
   - Histogram, Common values, Extreme values
3. **Interactions**: 변수 간 산점도 매트릭스
4. **Correlations**: 상관관계 히트맵
5. **Missing values**: 결측치 패턴 시각화
6. **Sample**: 데이터 샘플 (처음/마지막 10행)
7. **Alerts**: 데이터 품질 경고
   - 높은 상관관계
   - 높은 결측치 비율
   - 불균형 클래스
   - 이상치 탐지

### 콘솔 출력 (요약)
```markdown
═══════════════════════════════════════════════════════════
데이터 프로파일링 완료
═══════════════════════════════════════════════════════════

📊 데이터셋: creditcard.csv
   행 수: 284,807
   열 수: 31
   메모리: 67.4 MB

⚠️  주요 발견사항:
   - 클래스 불균형: 1:578 (사기: 0.17%)
   - 결측치: 없음
   - 높은 상관관계: 없음
   - 이상치: Amount 변수에서 탐지

💡 권고사항:
   1. 클래스 불균형 처리 필요 → /handle-imbalance
   2. Amount 변수 스케일링 권장 → /engineer-features
   3. 시간 변수(Time) 특성 추출 고려

📁 리포트 저장: projects/creditcard-fraud-detection/outputs/reports/creditcard_profile_report.html
🌐 브라우저에서 리포트가 자동으로 열렸습니다.
```

## Examples

### Example 1: 신용카드 사기 탐지
```bash
/profile-data \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class"
```

**예상 결과**:
- 클래스 불균형 탐지 (0.17% 사기)
- PCA 변환된 특성(V1-V28) 분포 분석
- Amount 변수 이상치 탐지

### Example 2: 대용량 데이터 (샘플링)
```bash
/profile-data \
  --data-path "projects/large-data-analysis/data/raw/large_dataset.csv" \
  --sample-size 100000 \
  --mode minimal
```

**이점**:
- 메모리 효율적 분석
- 빠른 실행 시간 (1-2분)

### Example 3: 타임시리즈 데이터
```bash
/profile-data \
  --data-path "projects/stock-analysis/data/raw/stock_prices.csv" \
  --target-column "Close"
```

## Profiling Modes

| Mode | 실행 시간 | 세부 수준 | 권장 상황 |
|------|---------|---------|---------|
| **minimal** | 빠름 (~1분) | 기본 통계만 | 빠른 데이터 확인 |
| **default** | 보통 (~3분) | 표준 분석 | 일반적인 EDA |
| **explorative** | 느림 (~5-10분) | 모든 분석 포함 | 심도있는 분석 |

## File Format Support

| 형식 | 확장자 | 지원 여부 |
|------|--------|---------|
| CSV | `.csv` | ✅ |
| Excel | `.xlsx`, `.xls` | ✅ |
| Parquet | `.parquet` | ✅ |
| JSON | `.json` | ✅ |
| Feather | `.feather` | ✅ |
| HDF5 | `.h5`, `.hdf5` | ✅ |

## Performance Tips

### 대용량 데이터 (100만 건 이상)
```bash
# 샘플링 + minimal 모드
/profile-data \
  --data-path "projects/big-data-analysis/data/raw/big_data.csv" \
  --sample-size 50000 \
  --mode minimal
```

### 메모리 부족 시
1. 샘플 크기 줄이기 (`--sample-size 10000`)
2. minimal 모드 사용
3. 불필요한 컬럼 제거 후 분석

## Related Commands

- `/engineer-features`: 특성 엔지니어링 및 변환
- `/handle-imbalance`: 클래스 불균형 처리
- `/train-models`: 모델 학습
- `/generate-report`: 종합 분석 리포트 생성

## Agents Used

- `data-profiler` (필수): 자동화된 EDA 실행

## Troubleshooting

### 문제: "ydata-profiling not found"
```bash
pip install ydata-profiling
```

### 문제: 메모리 부족 에러
```bash
# 샘플 크기 줄이기
/profile-data \
  --data-path "projects/my-project/data/raw/data.csv" \
  --sample-size 10000
```

### 문제: 브라우저가 자동으로 열리지 않음
- 수동으로 열기: `open projects/{project-name}/outputs/reports/{filename}.html`
- macOS: `open` 명령어
- Linux: `xdg-open` 명령어
- Windows: `start` 명령어

## Notes

⚠️ **주의사항**:
- 대용량 데이터(100만 건 이상)는 샘플링 권장
- 민감 정보가 포함된 데이터는 익명화 후 분석
- 생성된 HTML 리포트는 Git에 커밋하지 않음 (.gitignore 설정)

💡 **팁**:
- 프로파일링은 데이터 사이언스 파이프라인의 첫 단계
- 리포트의 "Alerts" 섹션을 우선 확인
- 상관관계 > 0.9인 변수는 하나 제거 고려
