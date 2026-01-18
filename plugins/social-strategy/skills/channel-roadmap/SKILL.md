---
name: channel-roadmap
description: 소셜 미디어 채널 선정 및 로드맵 수립을 위한 프레임워크
version: 1.0.0
author: Dante Labs
tags:
  - social-media
  - channel
  - strategy
---

# Channel Roadmap Framework

페르소나 기반 최적의 채널 믹스를 설계하고 로드맵을 수립하는 프레임워크입니다.

## Channel Selection Matrix

### 채널 평가 기준

| 기준 | 설명 | 가중치 |
|------|------|--------|
| 타겟 도달률 | 페르소나가 해당 채널을 사용하는 정도 | 30% |
| 콘텐츠 적합도 | 브랜드 콘텐츠와 채널 특성의 적합성 | 25% |
| 경쟁 강도 | 채널 내 경쟁 수준 | 15% |
| 리소스 요구 | 콘텐츠 제작 및 운영 비용 | 15% |
| 성장 잠재력 | 채널의 성장 가능성 | 15% |

### 채널 역할 분류

```
Primary Channel (주력 채널)
├── 주요 타겟 접점
├── 브랜드 인지도 구축
└── 핵심 콘텐츠 허브

Secondary Channel (보조 채널)
├── 특정 세그먼트 타겟
├── 콘텐츠 확장
└── Primary 채널 지원

Support Channel (지원 채널)
├── CRM 및 리텐션
├── 커뮤니티 운영
└── 실시간 소통
```

## Platform Profiles

### Instagram
| 항목 | 내용 |
|------|------|
| 주 사용자 | 18-44세, 여성 비중 높음 |
| 강점 | 비주얼 스토리텔링, 발견 |
| 콘텐츠 | 피드, 릴스, 스토리 |
| 알고리즘 | 참여율, 저장, 공유 |
| 포스팅 빈도 | 피드 주 3-5회, 릴스 주 2-3회 |
| 최적 시간 | 평일 12-13시, 19-21시 |

### YouTube
| 항목 | 내용 |
|------|------|
| 주 사용자 | 전 연령, 정보 탐색 |
| 강점 | 심층 콘텐츠, SEO, 수익화 |
| 콘텐츠 | 롱폼, 쇼츠, 라이브 |
| 알고리즘 | 시청 시간, CTR, 재방문 |
| 포스팅 빈도 | 롱폼 주 1-2회, 쇼츠 주 3-5회 |
| 최적 시간 | 주말 오전, 평일 저녁 |

### TikTok
| 항목 | 내용 |
|------|------|
| 주 사용자 | 16-34세, 엔터테인먼트 |
| 강점 | 바이럴, 트렌드, 도달률 |
| 콘텐츠 | 15-60초 숏폼 |
| 알고리즘 | 시청 완료율, 반복, 공유 |
| 포스팅 빈도 | 매일 1-3회 |
| 최적 시간 | 점심, 저녁 6-9시 |

### Naver Blog
| 항목 | 내용 |
|------|------|
| 주 사용자 | 30-50대, 정보 검색 |
| 강점 | SEO, 신뢰도, 체류 시간 |
| 콘텐츠 | 리뷰, 가이드, 레시피 |
| 알고리즘 | C-rank, 체류 시간 |
| 포스팅 빈도 | 주 2-3회 |
| 최적 시간 | 오전, 점심 시간 |

### KakaoTalk Channel
| 항목 | 내용 |
|------|------|
| 주 사용자 | 전 연령, 모바일 중심 |
| 강점 | CRM, 푸시 메시지, 친밀감 |
| 콘텐츠 | 프로모션, 뉴스레터 |
| 빈도 | 주 1-2회 메시지 |

## Channel Mix Strategy

### 예산별 권장 믹스

**소규모 예산 (월 100만원 이하)**
```
Instagram (60%) + KakaoTalk (40%)
- 1인 운영 가능
- 비주얼 + CRM 집중
```

**중간 예산 (월 100-500만원)**
```
Instagram (40%) + YouTube (30%) + Naver (20%) + KakaoTalk (10%)
- 콘텐츠 다각화
- 2-3인 팀 권장
```

**대규모 예산 (월 500만원 이상)**
```
Full Omni-Channel
- 전문 콘텐츠 팀
- 유료 광고 병행
```

## Roadmap Template

### Phase 1: 기반 구축 (1-2개월)
- Primary 채널 집중
- 브랜드 아이덴티티 확립
- 콘텐츠 템플릿 제작

### Phase 2: 확장 (3-4개월)
- Secondary 채널 추가
- 콘텐츠 재활용 시스템
- 성과 분석 및 최적화

### Phase 3: 성숙 (5-6개월+)
- Support 채널 운영
- 커뮤니티 구축
- 자동화 및 효율화

## File Storage

채널 전략 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── strategy/         # 전략 문서 저장 위치
│       ├── channel-strategy.md
│       ├── channel-roadmap.md
│       └── content-calendar.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/strategy/{document-type}-{date}.md

예시:
reports/strategy/channel-strategy-20240115.md
reports/strategy/channel-roadmap-20240115.md
reports/strategy/content-calendar-january-20240115.md
```

## Usage

이 스킬은 `social-strategy-director` 에이전트가 채널 전략 수립 시 참조합니다.
