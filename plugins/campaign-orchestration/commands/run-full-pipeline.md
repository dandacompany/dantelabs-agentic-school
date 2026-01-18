---
name: run-full-pipeline
description: 브랜드 문서부터 크리에이티브 제작까지 전체 마케팅 파이프라인을 실행합니다.
arguments:
  - name: brand-doc
    description: 브랜드 소개서 파일 경로
    required: true
  - name: target-segment
    description: 집중할 타겟 세그먼트 (선택, 자동 선정)
    required: false
  - name: channels
    description: 타겟 채널 (기본값: instagram,youtube)
    required: false
    default: "instagram,youtube"
  - name: skip-phases
    description: 건너뛸 단계 (콤마 구분)
    required: false
  - name: output-dir
    description: 결과물 저장 디렉토리
    required: false
    default: "./campaign-output"
---

# /run-full-pipeline

브랜드 분석부터 크리에이티브 제작까지 전체 마케팅 파이프라인을 순차적으로 실행합니다.

## Usage

```bash
/run-full-pipeline --brand-doc "./brand-brief.md"
/run-full-pipeline --brand-doc "./brand.md" --target-segment "워라밸 직장인"
/run-full-pipeline --brand-doc "./brand.md" --channels "instagram,tiktok" --skip-phases "competitive"
```

## What This Command Does

전체 6단계 파이프라인을 순차적으로 실행합니다:

### Phase 1: Brand Analysis
```
/analyze-brand --brand-doc "[brand-doc]"
→ Brand Strategy Brief
→ SWOT Analysis
→ Competitive Analysis (optional)
```

### Phase 2: Customer Segmentation
```
/create-segments --brand-doc "[Phase 1 output]"
→ 3-5 Segment Profiles
→ Segment Prioritization
```

### Phase 3: Persona Building
```
/build-persona --segment "[selected segment]"
→ Detailed Persona Card
→ Empathy Map
→ Customer Journey
```

### Phase 4: Channel Strategy
```
/plan-channels --persona "[Phase 3 output]"
→ Channel Plan
→ Content Calendar
→ KPI Framework
```

### Phase 5: Content Creation
```
/generate-copy --channel "[channels]" --persona "[persona]"
/write-script --format reels --topic "[topic]"
→ Marketing Copy (3+ variations)
→ Video Scripts
```

### Phase 6: Creative Production
```
/create-image --concept "[from copy]"
/create-video --script "[from script]"
→ Marketing Images
→ Marketing Videos
```

## Output Structure

```
[output-dir]/
├── campaign-summary.md           # 전체 캠페인 요약
├── 01-brand-analysis/
│   ├── brand-strategy-brief.md
│   └── competitive-analysis.md
├── 02-segmentation/
│   └── segment-profiles.md
├── 03-persona/
│   ├── persona-card.md
│   └── empathy-map.md
├── 04-channel-strategy/
│   ├── channel-plan.md
│   └── content-calendar.md
├── 05-content/
│   ├── instagram-copy.md
│   ├── youtube-copy.md
│   └── video-scripts.md
└── 06-creative/
    ├── images/
    │   └── [generated images]
    └── videos/
        └── [generated videos]
```

## Pipeline Progress

실행 중 진행 상황이 표시됩니다:

```markdown
## Campaign Pipeline Progress

| # | Phase | Status | Time | Output |
|---|-------|--------|------|--------|
| 1 | Brand Analysis | ✅ Complete | 2m | brand-brief.md |
| 2 | Segmentation | ✅ Complete | 3m | 4 segments |
| 3 | Persona | ✅ Complete | 2m | 김지현 |
| 4 | Channel Strategy | 🔄 Running | - | - |
| 5 | Content Creation | ⏳ Pending | - | - |
| 6 | Creative Production | ⏳ Pending | - | - |

**Current**: Phase 4 - Channel Strategy
**Elapsed**: 7 minutes
**Estimated Remaining**: ~10 minutes
```

## Campaign Summary Output

```markdown
# Campaign Summary: [브랜드명]

## 캠페인 개요
- 시작: [시작 시간]
- 완료: [완료 시간]
- 총 소요 시간: [시간]

## 핵심 결과

### 브랜드 에센스
> "[한 문장 정의]"

### 타겟 페르소나
- 이름: [페르소나명]
- 특성: [핵심 특성]

### 채널 전략
- Primary: [채널]
- Secondary: [채널]

### 핵심 메시지
> "[메인 카피]"

## 생성된 에셋

### 이미지
- 제품 이미지: X개
- 라이프스타일: X개

### 비디오
- Shorts/Reels: X개
- 롱폼 스크립트: X개

### 카피
- Instagram: X개 변형
- YouTube: X개 변형

## 다음 단계 권고
1. [ ] 이미지 A/B 테스트
2. [ ] 첫 주 콘텐츠 발행
3. [ ] 성과 측정 (2주 후)

## 전체 산출물 목록
- [링크/경로 목록]
```

## Example

```bash
# 단테 커피 전체 캠페인 실행
/run-full-pipeline --brand-doc "./docs/dante-coffee-brand-brief.md" \
  --channels "instagram,youtube" \
  --output-dir "./dante-campaign-2024"

# 결과:
# Phase 1: Brand Strategy Brief 생성
# Phase 2: 4개 세그먼트 정의 (워라밸 직장인, 트렌드세터, 프리미엄 애호가, 홈카페 마니아)
# Phase 3: 워라밸 직장인 → 페르소나 "김지현" 생성
# Phase 4: Instagram 중심 채널 전략 수립
# Phase 5: Instagram 피드 카피 3개, Reels 스크립트 2개 생성
# Phase 6: 제품 이미지 2개, 15초 비디오 1개 생성
#
# 전체 소요 시간: 약 15분
# 산출물: ./dante-campaign-2024/
```

## Related Commands

- `/run-phase`: 특정 단계만 실행
- `/campaign-status`: 진행 상황 확인

## Agents Used

전체 파이프라인에서 사용되는 에이전트:

1. `campaign-director`: 전체 총괄
2. `workflow-coordinator`: 실행 조율
3. `brand-strategist`: 브랜드 분석
4. `competitive-analyst`: 경쟁사 분석
5. `segmentation-architect`: 세그먼트 설계
6. `persona-architect`: 페르소나 생성
7. `social-strategy-director`: 채널 전략
8. `copy-strategist`: 메시지 전략
9. `conversion-copywriter`: 카피 작성
10. `script-writer`: 스크립트 작성
11. `creative-director`: 크리에이티브 총괄
12. `production-coordinator`: 제작 조율

## External Skills Used

- `kie-image-generator`: AI 이미지 생성
- `kie-video-generator`: AI 비디오 생성
