---
name: engineer-features
description: 데이터 전처리 및 특성 엔지니어링을 수행하여 모델 학습 준비 완료된 데이터를 생성합니다.
arguments:
  - name: data-path
    description: 원본 데이터 파일 경로
    required: true
  - name: target-column
    description: 타겟 변수 컬럼명 (전처리에서 제외)
    required: false
  - name: scaling-strategy
    description: 스케일링 전략 (robust, standard, minmax)
    required: false
    default: "robust"
  - name: time-features
    description: 시간 특성 추출 (comma-separated: hour,day,cyclical)
    required: false
  - name: output-dir
    description: 전처리 데이터 저장 디렉토리
    required: false
    default: "projects/{project-name}/data/processed"
---

# /engineer-features

데이터 전처리 및 특성 엔지니어링을 수행하여 모델 학습에 적합한 데이터를 생성합니다.

## Usage

```bash
# 기본 사용법 (RobustScaler)
/engineer-features \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv"

# 타겟 컬럼 지정 + 시간 특성 추출
/engineer-features \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical"

# StandardScaler 사용
/engineer-features \
  --data-path "projects/my-analysis/data/raw/data.csv" \
  --scaling-strategy "standard"

# 출력 디렉토리 지정
/engineer-features \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --output-dir "projects/creditcard-fraud-detection/data/processed"
```

## What This Command Does

### 1. 원본 데이터 로드 및 분석
- 파일 로드 및 기본 정보 확인
- 타겟 변수 분리
- 수치형/범주형 변수 식별

### 2. 스케일링 적용
**RobustScaler (기본값, 권장)**:
- 이상치에 강건 (median, IQR 사용)
- 금융 데이터, 이상치 많은 데이터에 적합
```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
```

**StandardScaler**:
- 평균 0, 분산 1로 정규화
- 정규분포 가정, 이상치 민감
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
```

**MinMaxScaler**:
- 0-1 범위로 스케일링
- 이상치에 매우 민감
```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
```

### 3. 시간 특성 추출 (선택)

**Time 컬럼이 있는 경우**:
```python
# Hour 추출 (0-23)
df['Hour'] = (df['Time'] / 3600) % 24

# Day 추출 (0, 1, ...)
df['Day'] = (df['Time'] / 86400).astype(int)

# Cyclical Encoding (주기성 표현)
import numpy as np
df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)
```

**이점**:
- 시간대별 패턴 캡처 (심야 사기 거래 등)
- 주기성 보존 (23시와 0시가 가까움을 모델이 인식)

### 4. 전처리 파이프라인 저장
```python
import joblib

# 파이프라인 저장 (재사용 가능)
joblib.dump(scaler, 'projects/{project-name}/outputs/models/preprocessing_pipeline.pkl')

# 신규 데이터 전처리 시
scaler = joblib.load('projects/{project-name}/outputs/models/preprocessing_pipeline.pkl')
X_new_scaled = scaler.transform(X_new)  # fit 없이 transform만!
```

### 5. 전처리된 데이터 저장
- **CSV 형식**: `{dataset_name}_processed.csv`
- **위치**: `data/processed/`
- **분리 저장**: X (특성), y (타겟)

## Output Structure

### 전처리된 데이터
```
projects/{project-name}/data/processed/
├── creditcard_processed_X.csv  # 특성 데이터
└── creditcard_processed_y.csv  # 타겟 데이터
```

### 전처리 파이프라인
```
projects/{project-name}/outputs/models/
└── preprocessing_pipeline.pkl  # scikit-learn 파이프라인
```

### 변환 로그
```
projects/{project-name}/outputs/reports/
└── creditcard_feature_engineering_log.md
```

**로그 예시**:
```markdown
# 특성 엔지니어링 로그

**생성일**: 2026-01-31 08:30
**원본 데이터**: creditcard.csv (284,807건, 31개 특성)

## 적용된 변환

### 1. 스케일링 (RobustScaler)
- **대상 변수**: Amount
- **변환 후 컬럼**: Amount_scaled
- **원본 컬럼 제거**: ✓
- **이유**: 이상치에 강건, 극단값 존재

### 2. 시간 특성 추출
- **원본**: Time (초 단위 경과 시간)
- **생성된 특성**:
  - Hour (0-23): 시간대 식별
  - Day (0, 1): 날짜 구분
  - Hour_sin, Hour_cos: 주기성 인코딩
- **원본 컬럼 제거**: ✓

### 3. 변수 요약
- **원본 특성**: 31개
- **최종 특성**: 34개 (+3개)
- **제거된 특성**: 2개 (Time, Amount)
- **추가된 특성**: 5개 (Amount_scaled, Hour, Day, Hour_sin, Hour_cos)

### 4. 전처리 파이프라인
- **저장 위치**: projects/{project-name}/outputs/models/preprocessing_pipeline.pkl
- **재사용 방법**:
  ```python
  import joblib
  scaler = joblib.load('projects/{project-name}/outputs/models/preprocessing_pipeline.pkl')
  X_new_scaled = scaler.transform(X_new)
  ```

## 다음 단계
- `/handle-imbalance`: 클래스 불균형 처리 (SMOTE)
- `/train-models`: 모델 학습
```

## Examples

### Example 1: 신용카드 사기 탐지
```bash
/engineer-features \
  --data-path "projects/creditcard-fraud-detection/data/raw/creditcard.csv" \
  --target-column "Class" \
  --time-features "hour,day,cyclical" \
  --scaling-strategy "robust"
```

**결과**:
- Amount → Amount_scaled (RobustScaler)
- Time → Hour, Day, Hour_sin, Hour_cos
- V1-V28: 그대로 유지 (이미 PCA 정규화됨)

### Example 2: 고객 이탈 예측
```bash
/engineer-features \
  --data-path "projects/customer-churn-prediction/data/raw/churn.csv" \
  --target-column "Churn" \
  --scaling-strategy "standard"
```

**결과**:
- tenure, MonthlyCharges → StandardScaler
- gender, Contract → One-hot encoding (자동 감지)

### Example 3: 커스텀 출력 경로
```bash
/engineer-features \
  --data-path "projects/my-experiment/data/raw/data.csv" \
  --output-dir "projects/my-experiment/experiment_1/processed"
```

## Scaling Strategies Comparison

| 전략 | 사용 시기 | 장점 | 단점 |
|------|---------|------|------|
| **RobustScaler** | 이상치 많음 | 이상치 영향 최소 | - |
| **StandardScaler** | 정규분포 | 널리 사용, 표준 | 이상치 민감 |
| **MinMaxScaler** | 0-1 필요 | 직관적 | 이상치 매우 민감 |

**신용카드 사기 탐지**: RobustScaler (Amount에 극단값 존재)

## Time Features Benefits

### 시간대별 패턴 캡처
```python
# 시간대별 사기 비율
fraud_by_hour = df.groupby('Hour')['Class'].mean()
# → 심야(0-6시)에 사기 집중 가능성
```

### Cyclical Encoding 필요성
- 단순 Hour (0-23)만 사용 시:
  - 23시와 0시가 멀리 떨어진 것으로 인식 (차이 23)
  - 실제로는 1시간 차이일 뿐

- Cyclical Encoding 사용 시:
  ```python
  Hour_sin = sin(2π × Hour / 24)
  Hour_cos = cos(2π × Hour / 24)
  # → 23시와 0시가 가까운 것으로 인식
  ```

## Performance Tips

### 대용량 데이터
- 청크 단위 처리: `pd.read_csv(chunksize=10000)`
- Sparse 형식 사용: One-hot encoding 시
- Dask 사용: 메모리 초과 시

### 파이프라인 재사용
```python
# 학습 데이터로 fit
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('scaler', RobustScaler()),
])
pipeline.fit(X_train)

# 테스트 데이터는 transform만
X_test_scaled = pipeline.transform(X_test)

# 프로덕션 배포
joblib.dump(pipeline, 'projects/{project-name}/outputs/models/model.pkl')
```

## Related Commands

- `/profile-data`: 전처리 전 데이터 분석
- `/analyze-profile`: 전처리 전략 수립
- `/handle-imbalance`: 클래스 불균형 처리 (다음 단계)
- `/train-models`: 모델 학습 (전처리 후)

## Agents Used

- `feature-engineer` (필수): 데이터 전처리 및 특성 엔지니어링

## Notes

⚠️ **주의사항**:
- Train/Test 분리 후 전처리 (Data leakage 방지)
- Test 데이터는 transform만 (fit 금지)
- 타겟 변수는 전처리하지 않음

💡 **팁**:
- EDA 레포트(`/analyze-profile`) 먼저 확인하여 전략 수립
- 전처리 파이프라인 저장하여 재사용
- 전처리 후 다시 `/profile-data` 실행하여 검증
