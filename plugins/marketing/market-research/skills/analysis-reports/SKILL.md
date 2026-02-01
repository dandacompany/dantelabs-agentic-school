---
name: analysis-reports
description: 마케팅 시장 분석 리포트 제작 도구 - 포괄적인 시장조사 문서 생성
version: 1.0.0
author: Dante Labs
tags:
  - market-research
  - analysis
  - report
  - marketing
---

# Marketing Analysis Report Toolkit

마케팅 시장 분석, 경쟁사 분석, 전략 리포트 등 전문 분석 문서를 제작하는 도구입니다.

## 주요 기능

| 기능 | 설명 | 용도 |
|------|------|------|
| 시장 분석 리포트 | 시장 규모, 성장률, 트렌드 분석 | 투자 의사결정, 전략 수립 |
| 경쟁사 분석 | Porter's 5 Forces, SWOT, 포지셔닝 | 경쟁 전략 |
| 고객 세그먼트 분석 | TAM/SAM/SOM, 세그먼트 매력도 | 타겟팅 전략 |
| 전략 제언 리포트 | 기회 분석, 로드맵, 재무 전망 | 실행 계획 |

## 리포트 구조 (권장 50+ 페이지)

```
1. 표지
2. 목차
3. Executive Summary (2-3p)
4. 시장 정의 및 범위 (4-5p)
5. 시장 규모 및 성장 분석 (6-8p)
6. 산업 동인 및 트렌드 (5-6p)
7. 경쟁 환경 (6-8p)
8. 고객 분석 및 세그먼테이션 (4-5p)
9. 기술 및 혁신 동향 (4-5p)
10. 규제 환경 (3-4p)
11. 리스크 분석 (3-4p)
12. 전략적 기회 및 제언 (4-5p)
13. 실행 로드맵 (3-4p)
14. 투자 논거 및 재무 전망 (3-4p)
15. 부록
```

## Workflow

### 기본 워크플로우

```
[주제 정의] → [데이터 수집] → [시각자료 생성] → [분석 작성] → [리포트 조립]
```

### 1단계: 핵심 시각자료 생성 (6개 필수)

분석 리포트 작성 전, 먼저 핵심 시각자료를 생성합니다:

```bash
# 1. 시장 성장 추이
python scripts/generate_visual.py "시장 성장 막대 그래프 2020-2034, 역사적 데이터 진한 파랑, 전망 데이터 연한 파랑" -o figures/01_market_growth.png

# 2. TAM/SAM/SOM 다이어그램
python scripts/generate_visual.py "TAM SAM SOM 동심원 다이어그램, 각 원에 시장명과 금액 표시" -o figures/02_tam_sam_som.png

# 3. Porter's 5 Forces
python scripts/generate_visual.py "Porter 5 Forces 다이어그램, 중앙에 경쟁 강도, 상하좌우에 위협 요소" -o figures/03_porters_forces.png

# 4. 경쟁 포지셔닝 매트릭스
python scripts/generate_visual.py "2x2 경쟁 포지셔닝 매트릭스, X축 시장 집중도, Y축 솔루션 접근방식" -o figures/04_competitive_positioning.png

# 5. 리스크 히트맵
python scripts/generate_visual.py "리스크 히트맵, X축 영향도, Y축 발생 확률, 색상으로 심각도 표시" -o figures/05_risk_heatmap.png

# 6. 실행 타임라인
python scripts/generate_visual.py "24개월 실행 로드맵 Gantt 차트, 4단계 Phase 표시" -o figures/06_implementation_timeline.png
```

### 2단계: 분석 프레임워크

#### TAM/SAM/SOM 분석

```markdown
## 시장 규모 분석

### Total Addressable Market (TAM)
- 전체 시장: $XXX Billion (2024)
- 예상 성장률: XX.X% CAGR (2024-2034)
- 산출 방법: 탑다운/바텀업 하이브리드

### Serviceable Addressable Market (SAM)
- 접근 가능 시장: $XX Billion
- 지역 제한: [지역]
- 세그먼트 제한: [세그먼트]

### Serviceable Obtainable Market (SOM)
- 현실적 목표: $X Billion
- 시장 점유율 시나리오: X-Y%
```

#### Porter's 5 Forces 분석

```markdown
## 경쟁 환경 분석

### 1. 신규 진입자 위협: [HIGH/MEDIUM/LOW]
- 진입 장벽: [설명]
- 자본 요구 수준: [설명]

### 2. 공급자 교섭력: [HIGH/MEDIUM/LOW]
- 주요 공급자 집중도: [설명]
- 전환 비용: [설명]

### 3. 구매자 교섭력: [HIGH/MEDIUM/LOW]
- 구매자 집중도: [설명]
- 가격 민감도: [설명]

### 4. 대체재 위협: [HIGH/MEDIUM/LOW]
- 대체 솔루션: [설명]
- 전환 비용: [설명]

### 5. 기존 경쟁 강도: [HIGH/MEDIUM/LOW]
- 주요 플레이어 수: [설명]
- 차별화 정도: [설명]
```

#### PESTLE 분석

```markdown
## 외부 환경 분석 (PESTLE)

| 요인 | 주요 동인 | 영향 |
|------|-----------|------|
| **Political** | 정부 정책, 규제 | [설명] |
| **Economic** | 경기 동향, 금리 | [설명] |
| **Social** | 인구통계, 소비 트렌드 | [설명] |
| **Technological** | 기술 혁신, 디지털화 | [설명] |
| **Legal** | 법적 요구사항, 컴플라이언스 | [설명] |
| **Environmental** | 지속가능성, ESG | [설명] |
```

### 3단계: 데이터 테이블

#### 시장 전망 테이블

| 연도 | 시장 규모 (B$) | YoY 성장률 | CAGR |
|------|---------------|-----------|------|
| 2024 | XX.X | - | - |
| 2025 | XX.X | X.X% | - |
| ... | ... | ... | X.X% |
| 2034 | XX.X | X.X% | X.X% |

#### 경쟁사 비교 테이블

| 순위 | 기업명 | 매출 | 시장 점유율 | 성장률 |
|------|--------|------|------------|--------|
| 1 | Company A | $X.XB | XX% | +X% |
| 2 | Company B | $X.XB | XX% | +X% |
| ... | ... | ... | ... | ... |

## 시각자료 가이드

### 필수 시각자료 (6개)

1. **시장 성장 추이 차트** - 막대/선 그래프
2. **TAM/SAM/SOM 다이어그램** - 동심원
3. **Porter's 5 Forces** - 5박스 다이어그램
4. **경쟁 포지셔닝 매트릭스** - 2x2 매트릭스
5. **리스크 히트맵** - 확률 vs 영향 매트릭스
6. **실행 타임라인** - Gantt 차트

### 추가 시각자료 (필요시)

- 지역별 시장 분포 (파이/트리맵)
- 세그먼트 성장률 비교 (가로 막대)
- 기술 로드맵 (타임라인)
- 고객 여정 맵 (플로우차트)
- 시나리오 분석 (그룹 막대)

### 시각자료 생성

`diagram-generator` 스킬과 연동하여 시각자료를 생성합니다:

```bash
# 기본 사용법
python scripts/generate_visual.py "[설명]" -o figures/[filename].png

# 문서 유형 지정 (품질 임계값 조정)
python scripts/generate_visual.py "[설명]" -o figures/[filename].png --doc-type report
```

## 리포트 섹션 작성 가이드

### Executive Summary 작성

Executive Summary는 **마지막에** 작성합니다:

```markdown
## Executive Summary

### 핵심 시장 지표
| 지표 | 값 |
|------|------|
| 현재 시장 규모 | $XX.X Billion (2024) |
| 예상 시장 규모 | $XX.X Billion (2034) |
| CAGR | XX.X% |
| 최대 세그먼트 | [세그먼트명] (XX%) |
| 최고 성장 지역 | [지역명] (+XX%) |

### 투자 논거
- [핵심 기회 1]
- [핵심 기회 2]
- [핵심 기회 3]

### 주요 발견
**시장 동향**
- [발견 1]
- [발견 2]

**경쟁 환경**
- [발견 1]
- [발견 2]

### 전략적 권고사항
| 우선순위 | 권고사항 | 기대 성과 | 시기 |
|---------|----------|----------|------|
| 1 | [권고 1] | [성과] | 즉시 |
| 2 | [권고 2] | [성과] | 단기 |
| 3 | [권고 3] | [성과] | 중기 |
```

### 리스크 분석 작성

```markdown
## 리스크 분석

### 리스크 개요
| 리스크 ID | 리스크명 | 범주 | 확률 | 영향 | 등급 |
|----------|---------|------|------|------|------|
| R1 | [리스크 1] | 시장 | H/M/L | H/M/L | 심각/높음/중간/낮음 |
| R2 | [리스크 2] | 규제 | H/M/L | H/M/L | ... |

### 상세 리스크 분석

#### R1: [리스크명]
- **설명**: [상세 설명]
- **트리거 시나리오**: [발생 조건]
- **잠재적 영향**: [예상 결과]
- **조기 경고 지표**: [모니터링 항목]

### 리스크 대응 전략
| 리스크 | 예방 전략 | 대응 전략 |
|--------|----------|----------|
| R1 | [예방책] | [대응책] |
```

## File Storage

```
{project}/
├── reports/
│   └── market-analysis/        # 최종 리포트
│       ├── [market]-analysis-[date].md
│       └── [market]-analysis-[date].pdf
├── figures/                    # 시각자료
│   ├── 01_market_growth.png
│   ├── 02_tam_sam_som.png
│   └── ...
├── data/                       # 원천 데이터
│   ├── market_data.csv
│   └── competitor_data.csv
└── tmp/
    └── analysis-drafts/        # 초안
```

### 파일 명명 규칙

```
reports/market-analysis/{market}-{type}-{date}.md

예시:
reports/market-analysis/ev-charging-comprehensive-20240115.md
reports/market-analysis/coffee-retail-competitive-20240115.md
```

## 스크립트 및 레퍼런스

### 레퍼런스 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| 리포트 구조 가이드 | `references/report_structure.md` | 섹션별 상세 작성 가이드 |
| 시각화 가이드 | `references/visualization_guide.md` | 시각자료 생성 프롬프트 |
| 데이터 분석 패턴 | `references/data_patterns.md` | 분석 프레임워크 |

### 스크립트

| 스크립트 | 경로 | 설명 |
|---------|------|------|
| generate_visual.py | `scripts/` | 시각자료 생성 (diagram-generator 연동) |

## 연동 스킬

이 스킬은 다음 스킬과 연동됩니다:

- **diagram-generator**: 시각자료 생성
- **pdf**: PDF 리포트 변환
- **docx**: Word 리포트 변환
- **pptx**: 프레젠테이션 변환

## Usage

이 스킬은 `market-analyst`, `competitive-analyst`, `brand-strategist` 에이전트가 시장 분석 및 전략 리포트 작성 시 참조합니다.

### 사용 예시

```
User: "한국 프리미엄 커피 시장 분석 리포트 작성해줘"

1. 시장 정의 및 범위 설정
2. 핵심 시각자료 6개 생성
3. 데이터 수집 및 분석
4. 리포트 섹션별 작성
5. Executive Summary 작성 (마지막)
6. 최종 리포트 조립
```
