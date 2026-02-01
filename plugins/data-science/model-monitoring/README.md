## Model Monitoring Plugin

프로덕션 환경에서 모델 성능을 모니터링하고 데이터 드리프트를 탐지하는 플러그인입니다.

## 📋 개요

이 플러그인은 프로덕션 모델의 지속적인 품질 관리를 위한 도구로, 다음을 제공합니다:

### 주요 기능
- ✅ **데이터 드리프트 탐지** (PSI, KS Test)
- ✅ **예측 분포 모니터링**
- ✅ **성능 추적** (분류/회귀)
- ✅ **자동 알림 시스템** (JSON)
- ✅ **시각화 리포트** (PNG, Markdown)
- ✅ **Evidently 통합**

### 왜 모델 모니터링이 필요한가?
프로덕션 환경에서 모델은 다음 이유로 성능이 저하될 수 있습니다:
- **데이터 드리프트**: 입력 데이터 분포 변화
- **컨셉 드리프트**: 타겟과 특성의 관계 변화
- **계절성**: 시간에 따른 패턴 변화
- **데이터 품질 저하**: 결측치, 이상치 증가

## 🚀 빠른 시작

### 1. 의존성 설치

**uv 사용 (권장)**:
```bash
cd plugins/model-monitoring/skills/monitoring
uv pip install -r requirements.txt
```

**pip 사용**:
```bash
pip install -r requirements.txt
```

### 2. 모델 모니터링 실행

```bash
# Claude Code에서 실행
/monitor-model \
  --model-path "projects/creditcard-fraud-detection/models/xgboost_model.pkl" \
  --reference-data "projects/creditcard-fraud-detection/data/processed/train.csv" \
  --current-data "projects/creditcard-fraud-detection/data/production/prod_2024_01.csv" \
  --target-column "Class"
```

**출력**: `projects/creditcard-fraud-detection/outputs/monitoring/` 폴더에 모든 리포트 및 알림 저장

## 📁 플러그인 구조

```
plugins/model-monitoring/
├── plugin.json
├── README.md
├── agents/
│   └── model-monitor.md
├── commands/
│   └── monitor-model.md
└── skills/
    └── monitoring/
        ├── requirements.txt
        └── scripts/
            └── monitor_performance.py
```

## 🎯 주요 기능

### 1. 데이터 드리프트 탐지

#### PSI (Population Stability Index)
- 학습 데이터 vs 프로덕션 데이터 분포 비교
- 특성별 PSI 계산
- 임계값 기반 드리프트 판정 (기본값: 0.1)

#### KS Test (Kolmogorov-Smirnov)
- 두 분포의 통계적 차이 검정
- p-value < 0.05 시 드리프트 판정

### 2. 예측 분포 모니터링
- 참조 데이터 vs 현재 데이터 예측 분포 비교
- 히스토그램 시각화
- KS 통계량으로 차이 정량화

### 3. 성능 추적
**분류**:
- Accuracy, Precision, Recall, F1-Score

**회귀**:
- MAE, MSE, RMSE, R²

### 4. 알림 시스템
다음 경우 자동 알림:
- 데이터 드리프트 발생
- 성능 저하 (F1 < 0.7 또는 R² < 0.7)
- JSON 형식으로 저장 → 대시보드 연동 가능

### 5. 모니터링 리포트
- Markdown 형식
- 알림 요약
- 성능 메트릭
- 드리프트 상세 정보
- 시각화 파일 목록

## 📊 사용 예시

### Example 1: 정기 모니터링
```bash
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod_2024_01.csv" \
  --target-column "target"
```

### Example 2: 타겟 없이 드리프트만 확인
```bash
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod_unlabeled.csv"
```

### Example 3: 드리프트 임계값 조정
```bash
/monitor-model \
  --model-path "projects/my-project/models/model.pkl" \
  --reference-data "projects/my-project/data/train.csv" \
  --current-data "projects/my-project/data/prod.csv" \
  --target-column "target" \
  --alert-threshold 0.15
```

## 🔧 파라미터

### 필수 파라미터
- `--model-path`: 학습된 모델 파일 경로
- `--reference-data`: 참조 데이터 (학습 데이터)
- `--current-data`: 현재 데이터 (프로덕션 데이터)

### 선택 파라미터
- `--target-column`: 타겟 컬럼명
- `--task-type`: 태스크 타입 (classification/regression/auto)
- `--alert-threshold`: 드리프트 알림 임계값 (기본값: 0.1)
- `--output-dir`: 출력 디렉토리

## 📤 출력

### 시각화
- `drift_summary.png`: PSI & KS 통계량
- `prediction_distribution.png`: 예측 분포 비교

### 데이터
- `drift_report.csv`: 특성별 드리프트 상세
- `alerts.json`: 알림 목록 (JSON)

### 리포트
- `{model_name}_monitoring_report.md`: 종합 리포트

## 🔍 PSI 해석

| PSI 값 | 의미 | 조치 |
|--------|------|------|
| 0.0 - 0.1 | 변화 없음 | 정상 운영 |
| 0.1 - 0.2 | 약간의 변화 | 모니터링 강화 |
| 0.2+ | 큰 변화 | 재학습 고려 |

## 🐛 트러블슈팅

### 문제: 모든 특성에서 드리프트 발생
- 임계값이 너무 낮음
- **해결**: `--alert-threshold 0.15`

### 문제: 성능 추적 건너뜀
- 타겟 컬럼이 없음
- **해결**: `--target-column` 지정

### 문제: 일부 컬럼 누락 경고
- 프로덕션 데이터에 일부 특성 없음
- **해결**: 전처리 파이프라인 동기화

## 📚 관련 문서

- [Evidently AI](https://www.evidentlyai.com/)
- [PSI 설명](https://mwburke.github.io/data%20science/2018/04/29/population-stability-index.html)

## 🔗 관련 플러그인

- `model-evaluation`: 모델 성능 평가
- `model-deployment`: 모델 배포
- `shap-analysis`: 드리프트 원인 분석

## 💡 모범 사례

### 모니터링 주기
- **실시간**: 중요 서비스 (금융, 의료)
- **일일**: 대부분의 프로덕션 모델
- **주간**: 낮은 트래픽 모델

### 재학습 기준
1. PSI > 0.2 (여러 특성)
2. 성능 10% 이상 하락
3. 예측 분포 KS p < 0.01
4. 비즈니스 요구 변화

### 알림 통합
```python
# alerts.json을 Slack/Email로 전송
import json
alerts = json.load(open('alerts.json'))
if alerts:
    send_to_slack(alerts)
```

## 📝 라이선스

MIT License

## 👤 작성자

- **Dante Labs**
- Email: datapod.k@gmail.com
- 버전: 1.0.0
