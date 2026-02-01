---
name: create-segments
description: 브랜드 정보를 기반으로 고객 세그먼트를 생성합니다.
arguments:
  - name: brand-doc
    description: 브랜드 소개서 또는 분석 결과 파일 경로
    required: true
  - name: segment-count
    description: 생성할 세그먼트 수 (기본값: 4)
    required: false
    default: "4"
  - name: focus
    description: 세그먼트 기준 우선순위 (demographic, behavioral, psychographic)
    required: false
    default: "balanced"
---

# /create-segments

브랜드 특성과 시장 정보를 바탕으로 의미 있는 고객 세그먼트를 생성합니다.

## Usage

```bash
/create-segments --brand-doc "./brand-strategy-brief.md"
/create-segments --brand-doc "./brand-brief.md" --segment-count 3
/create-segments --brand-doc "./brand-brief.md" --focus behavioral
```

## What This Command Does

1. **브랜드 정보 분석**
   - 타겟 시장 및 고객 힌트 추출
   - 제품/서비스 특성 파악

2. **세그먼트 가설 수립**
   - `segmentation-architect` 에이전트가 세그먼트 설계
   - 인구통계, 심리적, 행동적 기준 적용

3. **세그먼트 프로필 생성**
   - 각 세그먼트별 상세 프로필 작성
   - 니즈, 페인포인트, 행동 특성 정의

4. **우선순위 및 권고사항**
   - 타겟 세그먼트 우선순위 제안
   - 세그먼트별 접근 전략

## Output Structure

```markdown
# Customer Segmentation: [브랜드명]

## 세그먼테이션 개요
- 세그먼트 수: X개
- 세그먼트 기준: [기준 설명]

---

## 세그먼트 1: [세그먼트명]

### 프로필 요약
| 항목 | 내용 |
|------|------|
| 연령대 | |
| 직업 | |
| 라이프스타일 | |

### 특성
- **인구통계**:
- **심리적 특성**:
- **행동 패턴**:

### 니즈 & 페인포인트
- 니즈:
- 페인포인트:

### 브랜드 적합도: ★★★★☆
- 이유:

---

## 세그먼트 2: [세그먼트명]
...

---

## 세그먼트 우선순위

| 순위 | 세그먼트 | 적합도 | 권장 사유 |
|------|---------|--------|---------|
| 1 | | ★★★★★ | |
| 2 | | ★★★★☆ | |

## 다음 단계
- 페르소나 생성: `/build-persona --segment "[세그먼트명]"`
```

## Example

```bash
# 단테 커피 세그먼트 생성
/create-segments --brand-doc "./docs/dante-coffee-brand-brief.md" --segment-count 4

# 결과 예시:
# 1. 워라밸 직장인 (30대, 균형 추구)
# 2. 트렌드세터 (2030, 경험 중시)
# 3. 프리미엄 애호가 (40대+, 품질 추구)
# 4. 홈카페 마니아 (전 연령, DIY 선호)
```

## Related Commands

- `/analyze-brand`: 브랜드 분석 (선행 단계)
- `/build-persona`: 페르소나 생성 (후속 단계)

## Skills Used

- `segmentation-framework`: 세그먼테이션 프레임워크
- `activation-map`: 세그먼트 활성화 맵

## Agents Used

- `segmentation-architect` (필수)
- `data-analyst` (데이터 있을 경우)
