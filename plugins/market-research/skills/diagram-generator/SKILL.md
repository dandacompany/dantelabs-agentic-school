---
name: diagram-generator
description: AI 기반 비즈니스 다이어그램 및 차트 생성 도구
version: 1.0.0
author: Dante Labs
tags:
  - diagram
  - chart
  - visualization
  - ai-generation
---

# Business Diagram Generator

AI 이미지 생성 모델을 활용하여 비즈니스 다이어그램, 차트, 분석 시각자료를 생성하는 도구입니다.

## 주요 기능

| 기능 | 설명 | 용도 |
|------|------|------|
| 전략 다이어그램 | Porter's 5 Forces, SWOT, BCG 매트릭스 | 전략 분석 |
| 시장 차트 | 성장 추이, 세그먼트 분포, 지역 분석 | 시장 분석 |
| 프로세스 플로우 | 워크플로우, 고객 여정, 밸류 체인 | 프로세스 문서화 |
| 비교 매트릭스 | 포지셔닝 맵, 경쟁 비교, 리스크 히트맵 | 비교 분석 |

## Workflow

### 기본 생성 프로세스

```
[프롬프트 작성] → [이미지 생성] → [품질 평가] → [반복 개선] → [최종 저장]
```

### 1단계: 프롬프트 작성

효과적인 다이어그램 생성을 위한 프롬프트 구조:

```
[다이어그램 유형]: [구체적 설명]
- 레이아웃: [배치 설명]
- 색상: [컬러 스키마]
- 레이블: [텍스트 요구사항]
- 스타일: [비즈니스/컨설팅/인포그래픽]
```

### 2단계: 생성 명령어

```bash
# 기본 사용법
python scripts/generate_visual.py "프롬프트" -o output.png

# 문서 유형 지정 (품질 임계값 자동 설정)
python scripts/generate_visual.py "프롬프트" -o output.png --doc-type report

# 커스텀 품질 임계값
python scripts/generate_visual.py "프롬프트" -o output.png --threshold 7.5

# 최대 반복 횟수 지정
python scripts/generate_visual.py "프롬프트" -o output.png --max-iterations 5
```

### 3단계: 품질 검증

생성된 이미지는 자동으로 품질 평가됩니다:

| 문서 유형 | 품질 임계값 | 설명 |
|----------|------------|------|
| journal | 8.5/10 | 학술 저널 수준 |
| report | 7.5/10 | 비즈니스 리포트 |
| presentation | 6.5/10 | 프레젠테이션 |

## 다이어그램 유형별 프롬프트 예시

### 1. Porter's Five Forces

```bash
python scripts/generate_visual.py "Porter 5 Forces 분석 다이어그램:
- 중앙에 Industry Rivalry (산업 내 경쟁) 박스
- 상단: Threat of New Entrants, 하단: Threat of Substitutes
- 좌측: Supplier Power, 우측: Buyer Power
- 각 박스에 HIGH/MEDIUM/LOW 표시
- 화살표로 관계 표시
- 깔끔한 컨설팅 스타일, 비즈니스 컬러" -o figures/porters_forces.png --doc-type report
```

### 2. TAM/SAM/SOM

```bash
python scripts/generate_visual.py "TAM SAM SOM 동심원 다이어그램:
- 가장 큰 원: TAM (Total Addressable Market) - 연한 파랑
- 중간 원: SAM (Serviceable Addressable Market) - 중간 파랑
- 작은 원: SOM (Serviceable Obtainable Market) - 진한 파랑
- 각 원에 시장명과 금액 표시
- 우측에 범례
- 깔끔한 비즈니스 스타일" -o figures/tam_sam_som.png --doc-type report
```

### 3. 경쟁 포지셔닝 매트릭스

```bash
python scripts/generate_visual.py "2x2 경쟁 포지셔닝 매트릭스:
- X축: Market Focus (Niche ↔ Mass)
- Y축: Approach (Traditional ↔ Innovative)
- 4개 사분면 레이블: Leaders, Challengers, Niche Players, Visionaries
- 기업 위치는 원형 마커로 표시
- 마커 크기 = 시장 점유율
- 깔끔한 컨설팅 스타일" -o figures/competitive_positioning.png --doc-type report
```

### 4. 리스크 히트맵

```bash
python scripts/generate_visual.py "리스크 히트맵 매트릭스:
- X축: Impact (Low, Medium, High)
- Y축: Probability (Low, Medium, High)
- 색상: 초록(낮음) → 노랑(중간) → 빨강(높음)
- 각 셀에 리스크 ID 배치
- 우측에 범례
- 비즈니스 스타일" -o figures/risk_heatmap.png --doc-type report
```

### 5. 시장 성장 차트

```bash
python scripts/generate_visual.py "시장 성장 막대 그래프:
- X축: 연도 (2020-2034)
- Y축: 시장 규모 (Billion USD)
- 역사적 데이터: 진한 파랑, 전망: 연한 파랑
- 각 막대에 수치 레이블
- CAGR 주석
- 깔끔한 비즈니스 차트 스타일" -o figures/market_growth.png --doc-type report
```

### 6. Gantt 타임라인

```bash
python scripts/generate_visual.py "24개월 실행 로드맵 Gantt 차트:
- 4단계: Foundation, Growth, Expansion, Optimization
- 각 Phase에 3-4개 마일스톤
- Phase별 색상 구분
- 주요 마일스톤에 다이아몬드 마커
- 프로젝트 관리 스타일" -o figures/timeline.png --doc-type report
```

## 스타일 가이드

### 비즈니스 컬러 팔레트

```
Primary:    #1a365d (Navy)
Secondary:  #2b6cb0 (Blue)
Accent:     #ed8936 (Orange)
Success:    #38a169 (Green)
Warning:    #d69e2e (Yellow)
Danger:     #e53e3e (Red)
```

### 스타일 키워드

| 용도 | 추천 키워드 |
|------|------------|
| 전략 문서 | `consulting style`, `McKinsey`, `strategic diagram` |
| 데이터 시각화 | `clean chart`, `data visualization`, `infographic` |
| 비즈니스 리포트 | `professional`, `corporate`, `business style` |
| 프레젠테이션 | `slide-ready`, `executive`, `presentation` |

### 피해야 할 키워드

- 지나치게 장식적인 표현 (`ornate`, `decorative`)
- 비현실적 스타일 (`fantasy`, `artistic`)
- 저해상도 암시 (`sketch`, `rough`)

## 품질 체크리스트

- [ ] 텍스트가 명확하게 읽히는가?
- [ ] 색상 대비가 충분한가?
- [ ] 모든 데이터 포인트에 레이블이 있는가?
- [ ] 범례가 필요한 경우 포함되었는가?
- [ ] 해상도가 인쇄 품질인가?
- [ ] 비즈니스 문서에 적합한 스타일인가?

## File Storage

```
{project}/
├── figures/                    # 생성된 시각자료
│   ├── 01_market_growth.png
│   ├── 02_tam_sam_som.png
│   ├── 03_porters_forces.png
│   └── ...
└── tmp/
    └── diagram-drafts/         # 초안 및 반복 버전
```

### 파일 명명 규칙

```
figures/{순번}_{다이어그램유형}.png

예시:
figures/01_market_growth.png
figures/02_tam_sam_som.png
figures/03_porters_forces.png
figures/04_competitive_positioning.png
figures/05_risk_heatmap.png
figures/06_implementation_timeline.png
```

## 스크립트

| 스크립트 | 경로 | 설명 |
|---------|------|------|
| generate_visual.py | `scripts/` | 다이어그램 생성 (AI 모델 연동) |

## 기술 스택

- **이미지 생성**: OpenRouter API (Nano Banana Pro)
- **품질 평가**: Gemini 모델
- **출력 형식**: PNG (300 DPI)

## 연동 스킬

이 스킬은 다음 스킬에서 호출됩니다:

- **analysis-reports**: 마케팅 분석 리포트의 시각자료 생성
- **brand-analytics**: 브랜드 분석 다이어그램
- **competitive-analyst**: 경쟁 분석 차트

## Usage

```python
# 분석 리포트에서 사용 예시
# 1. 시장 성장 차트 생성
python scripts/generate_visual.py "시장 성장 막대 그래프 2020-2034..." -o figures/01_market_growth.png --doc-type report

# 2. 결과 확인 및 리포트에 삽입
# 리포트 마크다운에서:
# ![시장 성장 추이](figures/01_market_growth.png)
```
