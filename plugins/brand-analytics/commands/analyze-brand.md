---
name: analyze-brand
description: 브랜드 소개서를 분석하여 전략 브리프를 생성합니다.
arguments:
  - name: brand-doc
    description: 브랜드 소개서 파일 경로
    required: true
  - name: include-competitive
    description: 경쟁사 분석 포함 여부 (기본값: true)
    required: false
    default: "true"
  - name: output-format
    description: 출력 형식 (markdown, json)
    required: false
    default: "markdown"
---

# /analyze-brand

브랜드 소개서를 기반으로 종합적인 브랜드 분석을 수행합니다.

## Usage

```bash
/analyze-brand --brand-doc "./brand-brief.md"
/analyze-brand --brand-doc "./brand-brief.md" --include-competitive false
/analyze-brand --brand-doc "./brand-brief.md" --output-format json
```

## What This Command Does

1. **브랜드 문서 분석**
   - `brand-strategist` 에이전트를 호출하여 브랜드 핵심 요소 추출
   - 미션, 비전, 가치, USP 식별

2. **경쟁사 분석** (옵션)
   - `competitive-analyst` 에이전트를 호출하여 경쟁 환경 분석
   - 포지션 맵 및 차별화 기회 도출

3. **전략 브리프 생성**
   - Brand Strategy Brief 작성
   - SWOT 분석 포함
   - 다음 단계 권고사항

## Output Structure

```markdown
# Brand Strategy Brief: [브랜드명]

## 1. 브랜드 에센스
> [한 문장 브랜드 정의]

## 2. 핵심 가치
- 가치 1: [설명]
- 가치 2: [설명]
- 가치 3: [설명]

## 3. 포지셔닝 스테이트먼트
For [타겟 고객],
[브랜드명]은 [카테고리]에서
[핵심 차별점]을 통해
[가치 제안]을 제공합니다.

## 4. SWOT 분석
| Strengths | Weaknesses |
|-----------|------------|
| ... | ... |

| Opportunities | Threats |
|---------------|---------|
| ... | ... |

## 5. 경쟁 포지션 (선택적)
[경쟁사 비교 및 포지션 맵]

## 6. 전략적 권고사항
- [ ] 권고 1
- [ ] 권고 2
- [ ] 권고 3

## 7. 다음 단계
- 고객 세그먼테이션: `/create-segments`
- 페르소나 생성: `/build-persona`
```

## Example

```bash
# 단테 커피 브랜드 분석
/analyze-brand --brand-doc "./docs/dante-coffee-brand-brief.md"
```

## Related Commands

- `/create-segments`: 고객 세그먼트 생성
- `/build-persona`: 페르소나 카드 생성
- `/plan-channels`: 채널 전략 수립

## Agents Used

- `brand-strategist` (필수)
- `competitive-analyst` (선택)
