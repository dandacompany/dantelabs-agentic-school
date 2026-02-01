---
name: message-architecture
description: 브랜드 메시지 계층 구조 및 전략 수립 프레임워크
version: 1.0.0
author: Dante Labs
tags:
  - message
  - copywriting
  - strategy
---

# Message Architecture Framework

브랜드 메시지를 체계적으로 구조화하고 일관성 있게 전달하기 위한 프레임워크입니다.

## Message Hierarchy

```
Level 1: Brand Essence (브랜드 에센스)
│        한 단어 또는 한 문장의 브랜드 핵심
│
Level 2: Brand Promise (브랜드 약속)
│        고객에게 하는 핵심 약속
│
Level 3: Key Messages (핵심 메시지)
│        3-5개의 주요 메시지 필러
│
Level 4: Supporting Points (지원 포인트)
│        각 핵심 메시지를 뒷받침하는 근거
│
Level 5: Proof Points (증거 포인트)
         구체적 사실, 데이터, 사례
```

## Message Framework Template

```markdown
## Brand Essence
> [한 단어/문장]

## Brand Promise
> [고객에게 하는 약속]

## Key Messages

### 1. [핵심 메시지 1]
- Supporting Point: [지원 포인트]
- Proof Point: [증거]

### 2. [핵심 메시지 2]
- Supporting Point: [지원 포인트]
- Proof Point: [증거]

### 3. [핵심 메시지 3]
- Supporting Point: [지원 포인트]
- Proof Point: [증거]
```

## Dante Coffee Example

```markdown
## Brand Essence
> 한 잔의 여유

## Brand Promise
> 바쁜 일상 속에서도 간편하게 즐기는 프리미엄 커피 경험

## Key Messages

### 1. "간편함" - 3분이면 충분합니다
- Supporting: 드립백으로 복잡한 도구 없이
- Proof: 1.5분 추출, 세척 필요 없음

### 2. "프리미엄" - 카페 품질, 집에서
- Supporting: 싱글오리진 스페셜티 원두
- Proof: SCA 82점 이상 원두만 사용

### 3. "진정성" - 커피를 사랑하는 사람들이 만듭니다
- Supporting: 전문 로스터의 소량 로스팅
- Proof: 로스팅 후 7일 이내 배송
```

## Channel Message Adaptation

### 채널별 톤 조정

| 채널 | 톤 | 길이 | 스타일 |
|------|-----|------|--------|
| Instagram | 친근, 감성 | 짧음 | 이모지 활용 |
| YouTube | 전문, 교육 | 중간 | 상세 설명 |
| Naver Blog | 정보, 신뢰 | 김 | 상세 리뷰 |
| KakaoTalk | 친밀, 직접 | 매우 짧음 | 혜택 중심 |

### 메시지 변형 예시

**핵심 메시지**: "3분이면 충분합니다"

| 채널 | 변형 |
|------|------|
| Instagram | "바쁜 아침, 딱 3분만 투자하세요 ☕" |
| YouTube | "오늘은 단 3분 만에 완성하는 홈카페 커피를 소개합니다" |
| Naver | "출근 전 3분 루틴으로 카페 부럽지 않은 커피 즐기기" |
| KakaoTalk | "3분 커피, 오늘 첫 주문 15% 할인!" |

## Message by Funnel Stage

### Awareness (인지)
- 목적: 브랜드 인지도 구축
- 메시지 톤: 호기심 유발, 브랜드 스토리
- 예시: "커피 한 잔에 담긴 이야기"

### Consideration (고려)
- 목적: 제품 이해 및 비교
- 메시지 톤: 정보 제공, 차별화
- 예시: "왜 스페셜티 커피인가요?"

### Decision (결정)
- 목적: 구매 결정 유도
- 메시지 톤: 신뢰, 혜택 강조
- 예시: "첫 구매 10% 할인, 무료 배송"

### Retention (유지)
- 목적: 재구매 및 충성도
- 메시지 톤: 감사, 커뮤니티
- 예시: "함께해주셔서 감사합니다"

## Voice & Tone Guidelines

### Brand Voice Attributes

| 속성 | 설명 | Do | Don't |
|------|------|-----|-------|
| 따뜻함 | 친근하고 환영하는 | "함께 즐겨요" | "구매하세요" |
| 전문성 | 커피에 대한 깊은 지식 | "SCA 82점 이상" | "맛있어요" |
| 진정성 | 솔직하고 투명한 | "소량 로스팅" | "최고의 커피" |
| 편안함 | 부담 없고 여유로운 | "천천히 음미해보세요" | "지금 당장!" |

### 이모지 가이드

**사용 권장**
- ☕ 커피
- ✨ 특별함
- 🌿 자연/원두
- 💝 감사/선물
- 👉 CTA

**사용 자제**
- 과도한 이모지 나열
- 브랜드 이미지와 맞지 않는 이모지

## File Storage

메시지 및 카피 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── content/          # 콘텐츠 문서 저장 위치
│       ├── message-framework.md
│       ├── copy-variations/
│       │   ├── instagram-feed.md
│       │   ├── youtube-description.md
│       │   └── blog-posts.md
│       └── scripts/
│           ├── youtube-script-ep01.md
│           └── shorts-script-01.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/content/{type}/{channel}-{name}-{date}.md

예시:
reports/content/copy-variations/instagram-feed-launch-20240115.md
reports/content/scripts/youtube-brewing-tutorial-20240115.md
```

## Usage

이 스킬은 `copy-strategist` 및 `conversion-copywriter` 에이전트가 메시지 전략 수립 시 참조합니다.
