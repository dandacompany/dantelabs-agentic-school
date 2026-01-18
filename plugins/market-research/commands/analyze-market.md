---
name: analyze-market
description: 시장 규모, 성장률, 트렌드를 종합 분석하여 시장 분석 리포트를 생성합니다.
arguments:
  - name: industry
    description: 분석할 산업/시장명
    required: true
  - name: scope
    description: 분석 범위 (예: 2024-2030, Korea, Global)
    required: false
    default: "2024-2030"
  - name: include-pestle
    description: PESTLE 분석 포함 여부 (기본값: true)
    required: false
    default: "true"
  - name: output-format
    description: 출력 형식 (markdown, json)
    required: false
    default: "markdown"
---

# /analyze-market

시장 규모, 성장률, 트렌드를 종합 분석하여 전략적 시장 인사이트를 제공합니다.

## Usage

```bash
/analyze-market --industry "한국 프리미엄 커피 시장"
/analyze-market --industry "Korean specialty coffee" --scope "2024-2034"
/analyze-market --industry "SaaS 시장" --include-pestle true --output-format json
```

## What This Command Does

1. **시장 규모 추정**
   - `market-analyst` 에이전트를 호출하여 시장 규모 분석
   - TAM/SAM/SOM 모델링 수행
   - 성장률(CAGR) 산출

2. **트렌드 분석**
   - 시장 동인 및 저해 요인 파악
   - 주요 세그먼트별 분석
   - 지역별 시장 현황

3. **PESTLE 환경 분석** (옵션)
   - Political, Economic, Social 요인 분석
   - Technological, Legal, Environmental 요인 분석
   - 각 요인별 영향도 평가

4. **전략적 시사점 도출**
   - 시장 기회 영역 식별
   - 진입 전략 권고
   - 리스크 요인 정리

## Output Structure

```markdown
# 시장 분석 리포트: [산업명]

## Executive Summary
> [핵심 발견 사항 요약]

## 1. 시장 정의
- 산업 범위: [정의]
- 주요 세그먼트: [분류]
- 분석 기간: [기간]

## 2. 시장 규모
| 연도 | 시장 규모 | 성장률 |
|------|----------|--------|
| 2024 | X조원 | - |
| 2025 | Y조원 | Z% |
| ... | ... | ... |

### TAM/SAM/SOM
- TAM: [금액] - [설명]
- SAM: [금액] - [설명]
- SOM: [금액] - [설명]

## 3. 성장 동인
1. [동인 1]: [설명]
2. [동인 2]: [설명]
3. [동인 3]: [설명]

## 4. 시장 트렌드 (PESTLE)
| 요인 | 트렌드 | 영향도 | 시사점 |
|------|--------|--------|--------|
| Political | ... | High/Medium/Low | ... |
| Economic | ... | ... | ... |
| ... | ... | ... | ... |

## 5. 핵심 인사이트
- [인사이트 1]
- [인사이트 2]
- [인사이트 3]

## 6. 전략적 시사점
- [시사점 및 권고]

## 7. 다음 단계
- 경쟁 환경 분석: `/competitive-landscape`
- 브랜드 분석: `/analyze-brand`
```

## Example

```bash
# 단테 커피 시장 분석
/analyze-market --industry "한국 프리미엄 커피 시장" --scope "2024-2034"

# 글로벌 SaaS 시장 분석
/analyze-market --industry "Global Enterprise SaaS" --include-pestle true
```

## Related Commands

- `/competitive-landscape`: 경쟁 환경 및 산업 구조 분석
- `/analyze-brand`: 브랜드 분석 및 전략 브리프 생성
- `/create-segments`: 고객 세그먼트 생성

## Agents Used

- `market-analyst` (필수)

## Related Skills

- `analysis-reports`: 분석 리포트 템플릿
- `diagram-generator`: 차트 및 시각화 생성
