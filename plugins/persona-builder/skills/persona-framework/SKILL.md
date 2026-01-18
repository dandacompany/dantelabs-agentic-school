---
name: persona-framework
description: 고객 페르소나 작성을 위한 프레임워크 및 템플릿 가이드
version: 1.0.0
author: Dante Labs
tags:
  - persona
  - customer
  - empathy-map
---

# Persona Framework

마케팅 전략에 생명을 불어넣는 생생한 고객 페르소나를 작성하기 위한 프레임워크입니다.

## Persona Components

### 1. 기본 정보 (Demographics)

```markdown
## 기본 정보
| 항목 | 내용 |
|------|------|
| 이름 | [가상의 한국 이름] |
| 나이 | [세] |
| 성별 | |
| 직업 | |
| 소득 | [월/연] |
| 거주지 | [도시/지역] |
| 가족 구성 | |
| 교육 | |
```

### 2. 심리 프로필 (Psychographics)

```markdown
## 성격 및 가치관
- **성격 유형**: [MBTI 또는 서술]
- **핵심 가치**:
- **라이프스타일**:
- **관심사**:
- **목표/포부**:
```

### 3. 행동 패턴 (Behavioral)

```markdown
## 행동 패턴
- **구매 습관**:
- **정보 탐색**:
- **미디어 소비**:
- **브랜드 충성도**:
- **의사결정 스타일**:
```

## Empathy Map Framework

공감 맵은 고객을 깊이 이해하기 위한 시각화 도구입니다.

```
         ┌─────────────────────────────────┐
         │            THINKS               │
         │   (생각하지만 말하지 않는 것)      │
         ├─────────────────────────────────┤
┌────────┤            SEES                 ├────────┐
│ HEARS  │   (환경, 친구, 시장에서 보는 것)  │  SAYS  │
│        │                                 │        │
│ (친구, │                                 │(말하는 │
│ 미디어 │                                 │ 것,    │
│ 등에서 │         [페르소나]               │ 태도)  │
│ 듣는것)│                                 │        │
└────────┤            DOES                 ├────────┘
         │   (실제 행동, 습관)              │
         ├─────────────────────────────────┤
         │            FEELS                │
         │   (감정, 두려움, 기대)           │
         └─────────────────────────────────┘
```

### 2x2 Matrix Version

| Says (말) | Thinks (생각) |
|-----------|--------------|
| 공개적으로 말하는 것, 표현하는 태도 | 내면의 생각, 걱정, 희망 |

| Does (행동) | Feels (감정) |
|------------|-------------|
| 실제 행동, 일상 습관 | 감정 상태, 불안, 기대 |

## Jobs-to-be-Done (JTBD)

고객이 "고용"하는 제품/서비스의 목적을 이해합니다.

```
When I [상황/컨텍스트],
I want to [동기/목표],
So I can [기대 결과/혜택].
```

**예시 (커피):**
```
When I 아침에 출근 준비를 하면서,
I want to 빠르게 맛있는 커피를 마시고 싶어서,
So I can 상쾌하게 하루를 시작할 수 있다.
```

## Customer Journey Map

페르소나의 브랜드 경험 여정을 시각화합니다.

| 단계 | 인지 | 고려 | 결정 | 구매 | 사용 | 재구매 |
|------|------|------|------|------|------|--------|
| 행동 | | | | | | |
| 터치포인트 | | | | | | |
| 감정 | | | | | | |
| 페인포인트 | | | | | | |
| 기회 | | | | | | |

## Persona Naming Convention

효과적인 페르소나 이름 짓기:

- **한국 이름 사용**: 친숙함 부여
- **세그먼트 특성 반영**: "워라밸 지현", "트렌디 수진"
- **기억하기 쉬운 이름**: 짧고 발음하기 쉬운 이름

## AI Image Prompt Template

페르소나 시각화를 위한 이미지 프롬프트:

```
Professional lifestyle photo of a [age]-year-old Korean [gender],
[occupation], [personality trait] expression,
wearing [clothing style that reflects persona],
in [setting that matches lifestyle],
[activity related to product/service],
warm natural lighting, high quality portrait photography
```

**예시:**
```
Professional lifestyle photo of a 32-year-old Korean woman,
marketing professional, confident and warm expression,
wearing smart casual blazer with white t-shirt,
in a modern minimalist home office with plants,
holding a cup of coffee while looking at laptop,
warm morning natural lighting, high quality portrait photography
```

## Validation Checklist

- [ ] 세그먼트 특성이 반영되었는가?
- [ ] 구체적이고 현실적인가?
- [ ] 팀원들이 공감할 수 있는가?
- [ ] 마케팅 의사결정에 활용 가능한가?
- [ ] 니즈와 페인포인트가 명확한가?
- [ ] 브랜드 접점이 정의되었는가?

## File Storage

페르소나 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── persona/          # 페르소나 문서 저장 위치
│       ├── persona-jihyun.md
│       ├── persona-sujin.md
│       ├── empathy-maps/
│       │   └── jihyun-empathy-map.md
│       └── customer-journeys/
│           └── jihyun-journey.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/persona/{type}-{name}-{date}.md

예시:
reports/persona/persona-jihyun-20240115.md
reports/persona/empathy-maps/jihyun-empathy-map-20240115.md
reports/persona/customer-journeys/jihyun-journey-20240115.md
```

## Usage

이 스킬은 `persona-architect` 에이전트가 페르소나 카드 작성 시 참조합니다.
