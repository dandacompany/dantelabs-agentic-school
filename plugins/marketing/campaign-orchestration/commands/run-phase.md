---
name: run-phase
description: 캠페인 파이프라인의 특정 단계만 실행합니다.
arguments:
  - name: phase
    description: 실행할 단계 번호 또는 이름 (1-6, brand, segment, persona, channel, content, creative)
    required: true
  - name: input
    description: 이전 단계 산출물 또는 입력 파일 경로
    required: false
  - name: options
    description: 단계별 추가 옵션 (JSON 형식)
    required: false
---

# /run-phase

캠페인 파이프라인의 특정 단계만 독립적으로 실행합니다.

## Usage

```bash
/run-phase --phase 1 --input "./brand-brief.md"
/run-phase --phase brand --input "./brand-doc.md"
/run-phase --phase 3 --input "./segments.md" --options '{"segment": "워라밸 직장인"}'
/run-phase --phase content --input "./persona.md" --options '{"channel": "instagram"}'
```

## Available Phases

| # | Name | Plugin | Description |
|---|------|--------|-------------|
| 1 | brand | brand-analytics | 브랜드 분석 |
| 2 | segment | customer-segmentation | 고객 세그먼테이션 |
| 3 | persona | persona-builder | 페르소나 생성 |
| 4 | channel | social-strategy | 채널 전략 |
| 5 | content | content-creation | 콘텐츠 제작 |
| 6 | creative | creative-production | 크리에이티브 제작 |

## Phase Details

### Phase 1: Brand Analysis
```bash
/run-phase --phase 1 --input "./brand-brief.md"

# 옵션:
# --options '{"include-competitive": true}'
```

**입력**: 브랜드 소개서
**출력**: Brand Strategy Brief, SWOT

---

### Phase 2: Segmentation
```bash
/run-phase --phase 2 --input "./brand-strategy-brief.md"

# 옵션:
# --options '{"segment-count": 4}'
```

**입력**: Brand Strategy Brief
**출력**: Segment Profiles

---

### Phase 3: Persona
```bash
/run-phase --phase 3 --input "./segments.md"

# 옵션:
# --options '{"segment": "워라밸 직장인"}'
```

**입력**: Segment Profiles
**출력**: Persona Card, Empathy Map

---

### Phase 4: Channel Strategy
```bash
/run-phase --phase 4 --input "./persona.md"

# 옵션:
# --options '{"channels": ["instagram", "youtube"]}'
```

**입력**: Persona Card
**출력**: Channel Plan, Content Calendar

---

### Phase 5: Content Creation
```bash
/run-phase --phase 5 --input "./channel-plan.md"

# 옵션:
# --options '{"channel": "instagram", "format": "feed", "variations": 3}'
```

**입력**: Channel Plan + Persona
**출력**: Copy Variations, Scripts

---

### Phase 6: Creative Production
```bash
/run-phase --phase 6 --input "./content-output/"

# 옵션:
# --options '{"type": "image", "model": "flux-pro"}'
# --options '{"type": "video", "model": "kling", "duration": "15s"}'
```

**입력**: Copy, Scripts
**출력**: Images, Videos

## Phase Dependencies

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
```

단계를 건너뛰는 경우, 필요한 입력 데이터를 직접 제공해야 합니다.

## Output Structure

```
[current-dir]/
└── phase-[N]-output/
    └── [산출물 파일들]
```

## Example Scenarios

### 시나리오 1: 기존 브랜드 분석 결과로 세그먼트만 재생성
```bash
/run-phase --phase 2 --input "./existing-brand-brief.md" --options '{"segment-count": 5}'
```

### 시나리오 2: 새로운 페르소나로 채널 전략만 수립
```bash
/run-phase --phase 4 --input "./new-persona.md" --options '{"channels": ["tiktok", "youtube"]}'
```

### 시나리오 3: 특정 채널용 카피만 추가 생성
```bash
/run-phase --phase 5 --input "./channel-plan.md" --options '{"channel": "tiktok", "format": "shorts"}'
```

### 시나리오 4: 이미지만 추가 생성
```bash
/run-phase --phase 6 --input "./copy-output/" --options '{"type": "image", "concept": "라이프스타일", "count": 3}'
```

## Related Commands

- `/run-full-pipeline`: 전체 파이프라인 실행
- Individual phase commands:
  - `/analyze-brand`
  - `/create-segments`
  - `/build-persona`
  - `/plan-channels`
  - `/generate-copy`, `/write-script`
  - `/create-image`, `/create-video`

## Agents Used (Phase별)

| Phase | Primary Agent | Support Agents |
|-------|--------------|----------------|
| 1 | brand-strategist | competitive-analyst |
| 2 | segmentation-architect | data-analyst |
| 3 | persona-architect | customer-insights-partner |
| 4 | social-strategy-director | channel-analyst |
| 5 | copy-strategist | conversion-copywriter, script-writer |
| 6 | creative-director | production-coordinator |
