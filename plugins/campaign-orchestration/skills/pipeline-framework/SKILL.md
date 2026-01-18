---
name: pipeline-framework
description: 마케팅 캠페인 파이프라인 설계 및 실행 프레임워크
version: 1.0.0
author: Dante Labs
tags:
  - campaign
  - pipeline
  - orchestration
---

# Marketing Campaign Pipeline Framework

브랜드 분석부터 크리에이티브 제작까지 체계적인 마케팅 캠페인을 실행하기 위한 프레임워크입니다.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  AGENTIC MARKETING PIPELINE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [INPUT]                                                    │
│  └── Brand Document                                         │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PHASE 1: DISCOVERY                                   │   │
│  │ ├── Brand Analysis                                   │   │
│  │ └── Competitive Analysis                             │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PHASE 2: TARGETING                                   │   │
│  │ ├── Customer Segmentation                            │   │
│  │ └── Persona Development                              │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PHASE 3: PLANNING                                    │   │
│  │ ├── Channel Strategy                                 │   │
│  │ └── Content Planning                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↓                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PHASE 4: CREATION                                    │   │
│  │ ├── Copy & Script Writing                            │   │
│  │ └── Creative Production                              │   │
│  └─────────────────────────────────────────────────────┘   │
│              ↓                                              │
│  [OUTPUT]                                                   │
│  └── Complete Campaign Assets                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Phase Details

### Phase 1: Discovery (발견)

**목적**: 브랜드와 시장 이해

| 단계 | 활동 | 산출물 |
|------|------|--------|
| 1.1 | 브랜드 분석 | Brand Strategy Brief |
| 1.2 | 경쟁사 분석 | Competitive Analysis |
| 1.3 | SWOT 분석 | SWOT Matrix |

**소요 시간**: ~10분

### Phase 2: Targeting (타겟팅)

**목적**: 타겟 고객 정의

| 단계 | 활동 | 산출물 |
|------|------|--------|
| 2.1 | 세그먼트 설계 | Segment Profiles |
| 2.2 | 페르소나 개발 | Persona Cards |
| 2.3 | 공감 맵 작성 | Empathy Maps |

**소요 시간**: ~10분

### Phase 3: Planning (계획)

**목적**: 채널 및 콘텐츠 전략 수립

| 단계 | 활동 | 산출물 |
|------|------|--------|
| 3.1 | 채널 선정 | Channel Mix |
| 3.2 | 콘텐츠 필러 정의 | Content Pillars |
| 3.3 | 콘텐츠 캘린더 | Content Calendar |

**소요 시간**: ~10분

### Phase 4: Creation (제작)

**목적**: 실제 콘텐츠 자산 생성

| 단계 | 활동 | 산출물 |
|------|------|--------|
| 4.1 | 카피 작성 | Marketing Copy |
| 4.2 | 스크립트 작성 | Video Scripts |
| 4.3 | 이미지 생성 | Visual Assets |
| 4.4 | 비디오 생성 | Video Assets |

**소요 시간**: ~15분

## Data Flow

```
Brand Doc
    ↓
Brand Brief ─────────────────────┐
    ↓                            │
Segments ────────────────────────┤
    ↓                            │
Persona ─────────────────────────┤
    ↓                            │
Channel Plan ────────────────────┤
    ↓                            │
Copy/Scripts ────────────────────┤
    ↓                            │
Images/Videos ───────────────────┘
    ↓
Campaign Package (All Assets)
```

## Agent Mapping

| Phase | Primary Agents | Support Agents |
|-------|---------------|----------------|
| 1 | brand-strategist | competitive-analyst |
| 2 | segmentation-architect, persona-architect | data-analyst, customer-insights-partner |
| 3 | social-strategy-director | channel-analyst |
| 4 | copy-strategist, script-writer, creative-director | conversion-copywriter, production-coordinator |

## Execution Modes

### 1. Full Pipeline Mode
모든 단계를 순차적으로 자동 실행

```bash
/run-full-pipeline --brand-doc "./brand.md"
```

### 2. Step-by-Step Mode
각 단계 완료 후 검토/승인

```bash
/run-phase --phase 1 --input "./brand.md"
# 검토 후
/run-phase --phase 2 --input "./phase1-output/"
# ...
```

### 3. Selective Mode
필요한 단계만 선택 실행

```bash
/run-full-pipeline --skip-phases "competitive,persona"
```

### 4. Iterative Mode
특정 단계 반복 개선

```bash
/run-phase --phase 5 --options '{"variations": 5}'
```

## Quality Checkpoints

### Phase 1 완료 체크
- [ ] 브랜드 에센스가 명확한가?
- [ ] USP가 도출되었는가?
- [ ] SWOT이 완성되었는가?

### Phase 2 완료 체크
- [ ] 세그먼트가 명확히 구분되는가?
- [ ] 페르소나가 구체적인가?
- [ ] 타겟이 브랜드와 적합한가?

### Phase 3 완료 체크
- [ ] 채널 선택이 페르소나에 맞는가?
- [ ] 콘텐츠 필러가 정의되었는가?
- [ ] 캘린더가 실행 가능한가?

### Phase 4 완료 체크
- [ ] 카피가 메시지 전략에 맞는가?
- [ ] 이미지가 브랜드 가이드에 맞는가?
- [ ] 비디오가 채널 포맷에 맞는가?

## Error Handling

### 단계 실패 시
1. 오류 로그 기록
2. 재시도 (최대 3회)
3. 실패 시 Campaign Director에 보고
4. 수동 개입 또는 대체 전략

### 의존성 누락 시
1. 필요 입력 데이터 요청
2. 이전 단계 재실행 제안
3. 수동 입력 옵션 제공

## Metrics & Tracking

### 실행 메트릭
- 각 단계 소요 시간
- 재시도 횟수
- 생성된 자산 수

### 품질 메트릭
- 브랜드 일관성 점수
- 메시지 정합성
- 에이전트 신뢰도

## File Storage

파이프라인 실행 시 모든 산출물은 아래 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── assets/               # 정적 에셋 (이미지, 비디오)
│   ├── images/           # AI 생성 이미지
│   │   ├── products/     # 제품 이미지
│   │   ├── lifestyle/    # 라이프스타일 이미지
│   │   └── thumbnails/   # 썸네일
│   └── videos/           # AI 생성 비디오
│       ├── products/     # 제품 영상
│       ├── shorts/       # Shorts/Reels
│       └── raw/          # 원본 클립
│
├── reports/              # 마케팅 문서
│   ├── brand/            # 브랜드 분석 (Phase 1)
│   │   ├── brand-strategy-brief.md
│   │   └── swot-analysis.md
│   ├── persona/          # 페르소나 (Phase 2-3)
│   │   ├── segment-profiles.md
│   │   └── persona-cards/
│   ├── strategy/         # 전략 문서 (Phase 3-4)
│   │   ├── channel-strategy.md
│   │   └── content-calendar.md
│   └── content/          # 콘텐츠 (Phase 5)
│       ├── copy-variations/
│       └── scripts/
│
├── scripts/              # 실행 스크립트
│   └── automation/       # 자동화 스크립트
│
└── tmp/                  # 임시 파일
    ├── drafts/           # 초안
    └── test/             # 테스트 생성물
```

### Phase별 저장 위치

| Phase | 산출물 | 저장 위치 |
|-------|--------|----------|
| 1 | Brand Strategy Brief | `reports/brand/` |
| 2 | Segment Profiles | `reports/persona/` |
| 3 | Persona Cards | `reports/persona/` |
| 4 | Channel Strategy | `reports/strategy/` |
| 5 | Copy, Scripts | `reports/content/` |
| 6 | Images, Videos | `assets/images/`, `assets/videos/` |

### 디렉토리 초기화

파이프라인 실행 전 디렉토리 구조 생성:

```bash
mkdir -p assets/images/{products,lifestyle,thumbnails}
mkdir -p assets/videos/{products,shorts,raw}
mkdir -p reports/{brand,persona,strategy,content}
mkdir -p reports/content/{copy-variations,scripts}
mkdir -p scripts/automation
mkdir -p tmp/{drafts,test}
```

## Usage

이 스킬은 `campaign-director` 및 `workflow-coordinator` 에이전트가 캠페인 파이프라인 설계 및 실행 시 참조합니다.
