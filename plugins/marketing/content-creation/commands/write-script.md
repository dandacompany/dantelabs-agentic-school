---
name: write-script
description: 영상 콘텐츠를 위한 스크립트를 작성합니다.
arguments:
  - name: format
    description: 영상 포맷 (shorts, reels, tiktok, youtube-long)
    required: true
  - name: duration
    description: 영상 길이 (초 또는 분, 예: 30s, 5m)
    required: false
    default: "30s"
  - name: topic
    description: 영상 주제
    required: true
  - name: style
    description: 영상 스타일 (tutorial, lifestyle, product, story)
    required: false
    default: "tutorial"
  - name: persona
    description: 타겟 페르소나
    required: false
  - name: include-visuals
    description: 비주얼 가이드 포함 여부 (기본값: true)
    required: false
    default: "true"
---

# /write-script

영상 콘텐츠를 위한 상세 스크립트를 작성합니다.

## Usage

```bash
/write-script --format reels --duration 30s --topic "드립백 추출법"
/write-script --format shorts --topic "커피 팁" --style tutorial
/write-script --format youtube-long --duration 10m --topic "원두 선택 가이드" --persona "홈카페 마니아"
```

## What This Command Does

1. **브리프 분석**
   - 포맷별 특성 파악
   - 스타일 및 톤 결정

2. **구조 설계**
   - `script-writer`가 타임라인 구성
   - 훅 → 본문 → CTA 배치

3. **스크립트 작성**
   - 나레이션/대사
   - 장면 설명
   - 자막/텍스트

4. **비주얼 가이드** (옵션)
   - 촬영 체크리스트
   - 편집 참고사항

## Output Structure

```markdown
# Script: [영상 제목]

## 영상 정보
| 항목 | 내용 |
|------|------|
| 포맷 | [reels/shorts/youtube] |
| 길이 | [XX초/분] |
| 스타일 | [tutorial/lifestyle/product] |
| 타겟 | [페르소나명] |

---

## 스크립트

### [0:00-0:03] HOOK

**화면**
[화면 설명]

**나레이션/자막**
> "[나레이션]"
> 자막: [자막 텍스트]

**비고**
- [촬영/편집 참고사항]

---

### [0:03-0:10] INTRO
...

### [0:10-0:25] MAIN CONTENT
...

### [0:25-0:30] CTA
...

---

## 비주얼 가이드

### 촬영 체크리스트
- [ ] [필요 소품 1]
- [ ] [필요 소품 2]
- [ ] [장소/배경]
- [ ] [조명]

### 편집 참고
- 배경음악: [분위기]
- 자막 스타일: [폰트/위치]
- 컬러 그레이딩: [톤]
- 전환 효과: [컷/디졸브 등]

### 썸네일 아이디어
- 텍스트: "[썸네일 텍스트]"
- 이미지: [썸네일 이미지 설명]

---

## 제작 예상 시간
- 촬영: [X시간]
- 편집: [X시간]

---

## 다음 단계
- 이미지 생성: `/create-image --type thumbnail --concept "[썸네일 컨셉]"`
- 비디오 생성: `/create-video --script "[이 스크립트]"`
```

## Format-Specific Templates

### Shorts/Reels (15-60초)
```
[0-3초] HOOK - 즉각 주목
[3-7초] CONTEXT - 문제/상황 제시
[7-25초] CONTENT - 핵심 내용
[25-30초] CTA - 행동 유도
```

### TikTok (15-60초)
```
[0-2초] HOOK - 강렬한 시작
[2-5초] PROMISE - 기대 설정
[5-50초] DELIVERY - 가치 전달
[50-60초] CTA - 팔로우/좋아요
```

### YouTube 롱폼 (5-15분)
```
[0-30초] HOOK + 약속
[30초-1분] 인트로
[1-2분] 목차 제시
[2-X분] 본론 (파트별)
[마지막] 요약 + CTA + 다음 영상 예고
```

## Example

```bash
/write-script --format reels --duration 30s --topic "3분 드립백 루틴" --style lifestyle

# 결과:
# Script: 3분 드립백 루틴

## [0:00-0:03] HOOK
**화면**: 커피잔 클로즈업, 모락모락 김
**자막**: "아직도 인스턴트?"
**효과음**: 커피 따르는 소리

## [0:03-0:07] PROBLEM
**화면**: 바쁜 아침 출근 준비 (빠른 컷)
**나레이션**: "아침마다 카페 줄 서기 지치셨죠"

## [0:07-0:22] SOLUTION
**화면**: 드립백 추출 과정 (슬로우모션)
1. 드립백 개봉 [0:07-0:10]
2. 컵에 거치 [0:10-0:13]
3. 물 붓기 [0:13-0:18]
4. 완성 [0:18-0:22]

**나레이션**: "단테 드립백이면 딱 3분"
**자막**: "1. 개봉 → 2. 거치 → 3. 물붓기"

## [0:22-0:30] CTA
**화면**: 커피 마시며 만족 → 제품 로고
**자막**: "첫 구매 10% 할인 👉 프로필 링크"
**나레이션**: "집에서 즐기는 스페셜티, 지금 시작하세요"
```

## Related Commands

- `/generate-copy`: 카피 생성 (연계)
- `/create-image`: 썸네일 생성
- `/create-video`: AI 비디오 생성

## Agents Used

- `script-writer` (필수)
- `copy-strategist` (메시지 전략)
