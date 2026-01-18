---
name: brand-positioning
description: 브랜드 포지셔닝 프레임워크 및 전략 수립 가이드
version: 1.0.0
author: Dante Labs
tags:
  - brand
  - positioning
  - strategy
---

# Brand Positioning Framework

브랜드의 시장 내 고유한 위치를 정의하고 차별화 전략을 수립하는 프레임워크입니다.

## Core Frameworks

### 1. Golden Circle (Simon Sinek)

```
WHY (왜) → HOW (어떻게) → WHAT (무엇을)
```

| Level | Question | Example |
|-------|----------|---------|
| WHY | 왜 이 브랜드가 존재하는가? | 커피를 통한 삶의 여유 제공 |
| HOW | 어떻게 그것을 달성하는가? | 싱글오리진 스페셜티 커피 |
| WHAT | 무엇을 제공하는가? | 원두, 드립백, 경험 |

### 2. Positioning Statement Template

```
For [Target Customer]
Who [Customer Need/Want]
[Brand Name] is a [Category]
That [Key Benefit]
Unlike [Competitors]
Because [Reason to Believe]
```

**예시 (Dante Coffee):**
```
For 바쁜 직장인과 프리랜서
Who 일상 속 작은 여유와 품격 있는 커피를 원하는
Dante Coffee는 스페셜티 커피 브랜드로서
편리하면서도 프리미엄한 커피 경험을 제공합니다.
일반 인스턴트 커피와 달리
싱글오리진 원두와 전문 로스팅 기술로 차별화됩니다.
```

### 3. Brand Essence

브랜드의 핵심을 한 단어 또는 한 문장으로 정의합니다.

**구조:**
- **Functional Benefit**: 기능적 혜택
- **Emotional Benefit**: 감성적 혜택
- **Brand Personality**: 브랜드 성격
- **Brand Essence**: 핵심 본질

### 4. Perceptual Mapping

```
                    High Quality
                         ↑
                         |
    Affordable ←---------+---------→ Premium
                         |
                         ↓
                    Mass Market
```

## Analysis Tools

### SWOT Analysis

| Internal | External |
|----------|----------|
| **Strengths** (강점) | **Opportunities** (기회) |
| **Weaknesses** (약점) | **Threats** (위협) |

### 3C Analysis

- **Company**: 자사 분석
- **Customer**: 고객 분석
- **Competitor**: 경쟁사 분석

### USP (Unique Selling Proposition)

1. **Unique**: 경쟁사가 제공하지 않는 것
2. **Selling**: 구매 결정에 영향을 미치는 것
3. **Proposition**: 명확히 전달 가능한 것

## Brand Architecture

### Brand Elements

| Element | Description | Example |
|---------|-------------|---------|
| Brand Name | 브랜드 이름 | Dante Coffee |
| Tagline | 슬로건 | "한 잔의 여유, 단테와 함께" |
| Visual Identity | 로고, 컬러, 폰트 | 따뜻한 갈색 톤 |
| Brand Voice | 커뮤니케이션 스타일 | 따뜻하고 전문적 |

### Tone & Manner

**Voice Attributes:**
- Professional but Warm (전문적이지만 따뜻한)
- Authentic (진정성 있는)
- Inviting (환영하는)
- Passionate (열정적인)

## Implementation Checklist

- [ ] Golden Circle 정의 완료
- [ ] Positioning Statement 작성
- [ ] Brand Essence 한 문장 정의
- [ ] SWOT 분석 완료
- [ ] 경쟁 포지션 맵핑
- [ ] USP 3가지 도출
- [ ] Tone & Manner 가이드 작성

## File Storage

브랜드 분석 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── brand/            # 브랜드 분석 문서 저장 위치
│       ├── brand-strategy-brief.md
│       ├── swot-analysis.md
│       └── competitive-analysis.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/brand/{document-type}-{date}.md

예시:
reports/brand/brand-strategy-brief-20240115.md
reports/brand/swot-analysis-20240115.md
reports/brand/positioning-map-20240115.md
```

## Usage

이 스킬은 `brand-strategist` 에이전트가 브랜드 분석 시 참조합니다.

```
1. 브랜드 문서 수집
2. Golden Circle 프레임워크 적용
3. Positioning Statement 작성
4. SWOT 분석 수행
5. Brand Strategy Brief 산출 → reports/brand/ 저장
```
