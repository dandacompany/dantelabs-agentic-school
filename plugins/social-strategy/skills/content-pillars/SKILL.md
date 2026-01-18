---
name: content-pillars
description: 소셜 미디어 콘텐츠 필러 설계 및 콘텐츠 전략 프레임워크
version: 1.0.0
author: Dante Labs
tags:
  - content
  - social-media
  - pillars
---

# Content Pillars Framework

브랜드의 핵심 메시지를 일관되게 전달하기 위한 콘텐츠 필러 설계 프레임워크입니다.

## Content Pillar 개념

콘텐츠 필러는 브랜드 콘텐츠의 주제 카테고리로, 일관성과 다양성의 균형을 유지합니다.

```
Brand Core Message
        ↓
┌───────┼───────┐
│       │       │
Pillar  Pillar  Pillar
  1       2       3
│       │       │
↓       ↓       ↓
[Contents]
```

## Standard Content Pillars

### 1. Brand Story (브랜드 스토리)
- **목적**: 브랜드 아이덴티티 강화
- **콘텐츠 예시**:
  - 브랜드 탄생 스토리
  - 팀 소개, 비하인드
  - 브랜드 가치 선언
  - 마일스톤 공유
- **비중**: 15-20%

### 2. Product/Service (제품/서비스)
- **목적**: 제품 인지도 및 전환
- **콘텐츠 예시**:
  - 신제품 출시
  - 제품 상세 소개
  - 사용 방법 가이드
  - 프로모션/이벤트
- **비중**: 20-25%

### 3. Education (교육/정보)
- **목적**: 전문성 구축, 가치 제공
- **콘텐츠 예시**:
  - How-to 가이드
  - 팁과 트릭
  - 업계 트렌드
  - Q&A
- **비중**: 25-30%

### 4. Lifestyle (라이프스타일)
- **목적**: 감성적 연결, 공감
- **콘텐츠 예시**:
  - 일상 속 제품 활용
  - 시즌별 콘텐츠
  - 분위기/무드 콘텐츠
  - 영감 공유
- **비중**: 20-25%

### 5. Community (커뮤니티/UGC)
- **목적**: 참여 유도, 신뢰 구축
- **콘텐츠 예시**:
  - 고객 후기 리포스트
  - 사용자 참여 이벤트
  - 질문/설문
  - 댓글 소통
- **비중**: 10-15%

## Coffee Brand Example

### Dante Coffee 콘텐츠 필러

| 필러 | 비중 | 콘텐츠 예시 | 톤 |
|------|------|-----------|-----|
| 브랜드 스토리 | 15% | 단테의 철학, 팀 소개 | 진정성 |
| 제품 소개 | 25% | 원두 리뷰, 드립백 소개 | 전문적 |
| 커피 교육 | 30% | 추출 가이드, 팁 | 친절함 |
| 라이프스타일 | 20% | 아침 루틴, 계절 커피 | 따뜻함 |
| 커뮤니티 | 10% | 고객 후기, 설문 | 소통 |

## Content Format Mix

### Instagram

| 포맷 | 특성 | 적합한 필러 |
|------|------|-----------|
| 피드 | 고품질 이미지 | 제품, 라이프스타일 |
| 릴스 | 15-60초 영상 | 교육, 라이프스타일 |
| 스토리 | 일시적, 친밀 | 커뮤니티, 비하인드 |
| 라이브 | 실시간 소통 | 교육, 커뮤니티 |

### YouTube

| 포맷 | 특성 | 적합한 필러 |
|------|------|-----------|
| 롱폼 | 5-15분 | 교육, 브랜드 스토리 |
| 쇼츠 | 60초 이하 | 팁, 라이프스타일 |

## Content Calendar Template

### 주간 배분 예시

| 요일 | 채널 | 필러 | 포맷 | 아이디어 |
|------|------|------|------|---------|
| 월 | IG 피드 | 라이프스타일 | 이미지 | 새 주의 시작 |
| 화 | IG 릴스 | 교육 | 영상 | 3분 레시피 |
| 수 | IG 스토리 | 커뮤니티 | 설문 | 오늘의 선택 |
| 목 | IG 피드 | 제품 | 캐러셀 | 원두 상세 |
| 금 | IG 릴스 | 라이프스타일 | 영상 | 주말 추천 |
| 토 | YouTube | 교육 | 롱폼 | 추출 가이드 |
| 일 | IG 스토리 | 커뮤니티 | UGC | 고객 리포스트 |

## Content Repurposing

하나의 콘텐츠를 여러 포맷으로 재활용:

```
[원본: 10분 YouTube 영상 - 커피 추출 가이드]
        ↓
├── IG 릴스: 핵심 30초 클립
├── IG 캐러셀: 스텝별 이미지
├── IG 스토리: 비하인드
├── Naver 블로그: 텍스트 가이드
└── KakaoTalk: 요약 카드뉴스
```

## File Storage

콘텐츠 전략 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── strategy/         # 전략 문서 저장 위치
│       ├── content-pillars.md
│       └── content-calendar/
│           ├── weekly-plan.md
│           └── monthly-calendar.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/strategy/{document-type}-{date}.md

예시:
reports/strategy/content-pillars-20240115.md
reports/strategy/content-calendar/january-2024.md
```

## Usage

이 스킬은 `social-strategy-director` 및 `copy-strategist` 에이전트가 콘텐츠 전략 수립 시 참조합니다.
