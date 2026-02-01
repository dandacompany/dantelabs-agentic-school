---
name: activation-map
description: 세그먼트를 실제 마케팅 액션으로 연결하는 활성화 맵 프레임워크
version: 1.0.0
author: Dante Labs
tags:
  - segmentation
  - activation
  - gtm
---

# Segment Activation Map

세그먼트 인사이트를 구체적인 GTM 액션으로 변환하는 프레임워크입니다.

## Activation Framework

### 1. Segment → Insight → Action 흐름

```
[세그먼트 정의] → [핵심 인사이트] → [마케팅 액션]
        ↓              ↓                ↓
    WHO           WHY/WHAT          HOW/WHERE
```

### 2. Activation Matrix

| 세그먼트 | 핵심 인사이트 | 채널 | 메시지 | 오퍼 | KPI |
|---------|-------------|------|--------|-----|-----|
| A | | | | | |
| B | | | | | |
| C | | | | | |

## Activation Levers

### 채널 전략 (Channel)
- **Paid**: 광고, 스폰서십
- **Owned**: 웹사이트, 앱, 뉴스레터
- **Earned**: PR, 입소문, 리뷰

### 메시지 전략 (Message)
- 핵심 메시지: 세그먼트 니즈 기반
- 톤앤매너: 세그먼트 특성 맞춤
- CTA: 행동 유도 문구

### 오퍼 전략 (Offer)
- 제품/서비스: 세그먼트 선호도
- 가격/프로모션: 가격 민감도
- 번들링: 크로스셀 기회

## Segment-Specific Playbook

### Template

```markdown
## 세그먼트: [이름]

### 활성화 전략 요약
| 항목 | 내용 |
|------|------|
| 목표 | |
| 핵심 메시지 | |
| 주요 채널 | |
| 오퍼 | |
| 성공 지표 | |

### 채널 믹스
- Primary:
- Secondary:
- Support:

### 콘텐츠 유형
- Awareness:
- Consideration:
- Conversion:
- Retention:

### 캠페인 아이디어
1.
2.
3.

### 측정 계획
| 단계 | 지표 | 목표 |
|------|------|------|
| 인지 | | |
| 고려 | | |
| 전환 | | |
| 유지 | | |
```

## Example: Coffee Brand Activation

### 세그먼트: 워라밸 직장인

| 항목 | 내용 |
|------|------|
| 목표 | 일상 속 간편 프리미엄 커피 경험 제공 |
| 핵심 메시지 | "바쁜 하루, 단 3분의 여유" |
| 주요 채널 | 인스타그램, 네이버 스마트스토어 |
| 오퍼 | 드립백 정기 구독 10% 할인 |
| 성공 지표 | 신규 구독자 월 500명 |

### 채널 믹스
- **Primary**: 인스타그램 피드/릴스
- **Secondary**: 네이버 블로그, 카카오톡
- **Support**: 이메일 뉴스레터

### 콘텐츠 유형
- **Awareness**: "출근 전 3분 루틴" 릴스
- **Consideration**: 드립백 vs 캡슐 비교 콘텐츠
- **Conversion**: 첫 구독 혜택 랜딩페이지
- **Retention**: 월간 커피 추천 이메일

## Prioritization Framework

### ICE Score
- **Impact**: 비즈니스 영향도 (1-10)
- **Confidence**: 성공 확신도 (1-10)
- **Ease**: 실행 용이성 (1-10)

```
ICE Score = (Impact + Confidence + Ease) / 3
```

### 우선순위 매트릭스

```
        High Impact
             ↑
    Quick    |    Major
    Wins     |    Projects
    ─────────┼─────────→ High Effort
    Fill-ins |    Money
             |    Pits
```

## File Storage

활성화 맵 및 플레이북 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── strategy/         # 전략 문서 저장 위치
│       ├── activation-map.md
│       └── segment-playbooks/
│           ├── worklife-balance-playbook.md
│           └── trendsetter-playbook.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/strategy/{document-type}-{date}.md

예시:
reports/strategy/activation-map-20240115.md
reports/strategy/segment-playbooks/worklife-balance-20240115.md
```

## Usage

이 스킬은 세그먼트를 정의한 후 구체적인 마케팅 액션 플랜을 수립할 때 참조합니다.

```
1. 세그먼트 정의 완료 (/create-segments)
2. 활성화 맵 작성 → reports/strategy/ 저장
3. 채널 및 메시지 전략 수립 (/plan-channels)
4. 콘텐츠 제작 (/generate-copy, /create-image)
```
