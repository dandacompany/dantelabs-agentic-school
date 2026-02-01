---
name: competitive-landscape
description: Porter's 5 Forces 및 경쟁사 포지셔닝 분석으로 경쟁 환경을 분석합니다.
arguments:
  - name: market
    description: 분석할 시장/산업명
    required: true
  - name: competitors
    description: 주요 경쟁사 목록 (쉼표로 구분)
    required: false
  - name: include-positioning
    description: 포지셔닝 맵 포함 여부 (기본값: true)
    required: false
    default: "true"
  - name: output-format
    description: 출력 형식 (markdown, json)
    required: false
    default: "markdown"
---

# /competitive-landscape

Porter's Five Forces와 경쟁사 포지셔닝 분석으로 산업 수준의 경쟁 환경을 분석합니다.

## Usage

```bash
/competitive-landscape --market "한국 커피 시장"
/competitive-landscape --market "Korean coffee retail" --competitors "스타벅스,이디야,투썸"
/competitive-landscape --market "SaaS 시장" --include-positioning true
```

## What This Command Does

1. **Porter's Five Forces 분석**
   - `competitive-intelligence` 에이전트를 호출
   - 5가지 경쟁 요인별 위협 수준 평가
   - 산업 매력도 종합 판단

2. **경쟁사 포지셔닝 분석** (옵션)
   - 주요 경쟁사 식별 및 분류
   - 가격-품질 매트릭스 작성
   - 시장 점유율 분석

3. **전략적 기회 도출**
   - 빈 공간(White Space) 식별
   - 차별화 기회 영역 도출
   - 진입 장벽 분석

## Output Structure

```markdown
# 경쟁 환경 분석: [산업명]

## Executive Summary
> [핵심 발견 사항]

## 1. Porter's Five Forces 분석

### 1.1 산업 내 경쟁 (Industry Rivalry): [HIGH/MEDIUM/LOW]
- 현황: [분석]
- 주요 경쟁사: [리스트]
- 경쟁 요인: [요인들]

### 1.2 신규 진입자 위협: [HIGH/MEDIUM/LOW]
- 진입 장벽: [분석]
- 필요 자본: [수준]
- 규제 환경: [분석]

### 1.3 대체재 위협: [HIGH/MEDIUM/LOW]
- 대체재 유형: [리스트]
- 가격/성능 비교: [분석]

### 1.4 공급자 교섭력: [HIGH/MEDIUM/LOW]
- 공급자 집중도: [분석]
- 전환 비용: [분석]

### 1.5 구매자 교섭력: [HIGH/MEDIUM/LOW]
- 구매자 특성: [분석]
- 가격 민감도: [분석]

## 2. 경쟁사 포지셔닝

| 경쟁사 | 포지션 | 가격대 | 주요 강점 | 시장 점유율 |
|--------|--------|--------|----------|------------|
| A사 | ... | ... | ... | ...% |
| B사 | ... | ... | ... | ...% |

### 포지셔닝 맵
```
       High
  가격  │    ● Premium Leaders
       │
       │    ★ Target Position
       │
  Low   │ ● Low-cost Players
       └──────────────────
          Low   품질/가치   High
```

## 3. 전략적 기회

### 빈 공간 (White Space)
- [기회 영역 1]
- [기회 영역 2]

### 차별화 기회
- [차별화 포인트 1]
- [차별화 포인트 2]

## 4. 핵심 시사점
- [시사점 1]
- [시사점 2]
- [시사점 3]

## 5. 다음 단계
- 브랜드 분석: `/analyze-brand`
- 고객 세그먼테이션: `/create-segments`
```

## Example

```bash
# 한국 커피 시장 경쟁 환경 분석
/competitive-landscape --market "한국 프리미엄 커피 시장"

# 특정 경쟁사 포함 분석
/competitive-landscape --market "한국 커피 시장" --competitors "스타벅스,이디야,투썸플레이스,블루보틀"
```

## Related Commands

- `/analyze-market`: 시장 규모 및 성장률 분석
- `/analyze-brand`: 브랜드 분석 및 전략 브리프 생성
- `/create-segments`: 고객 세그먼트 생성

## Agents Used

- `competitive-intelligence` (필수)

## Related Skills

- `analysis-reports`: 분석 리포트 템플릿
- `diagram-generator`: Porter's 5 Forces 다이어그램, 포지셔닝 맵 생성
