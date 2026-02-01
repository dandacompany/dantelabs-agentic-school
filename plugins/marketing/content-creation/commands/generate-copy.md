---
name: generate-copy
description: 채널과 목적에 맞는 마케팅 카피를 생성합니다.
arguments:
  - name: channel
    description: 타겟 채널 (instagram, youtube, naver, kakao, facebook)
    required: true
  - name: purpose
    description: 카피 목적 (awareness, consideration, conversion)
    required: false
    default: "awareness"
  - name: format
    description: 콘텐츠 포맷 (feed, reels, story, shorts, blog)
    required: false
    default: "feed"
  - name: persona
    description: 타겟 페르소나 이름 또는 파일
    required: false
  - name: product
    description: 홍보할 제품/서비스
    required: false
  - name: variations
    description: 생성할 카피 변형 수 (기본값: 3)
    required: false
    default: "3"
---

# /generate-copy

채널, 목적, 포맷에 최적화된 마케팅 카피를 생성합니다.

## Usage

```bash
/generate-copy --channel instagram --format feed --purpose awareness
/generate-copy --channel instagram --format reels --persona "김지현" --product "드립백"
/generate-copy --channel youtube --format shorts --variations 5
```

## What This Command Does

1. **컨텍스트 분석**
   - 채널 특성 파악
   - 페르소나 언어 스타일 확인
   - 제품/서비스 USP 추출

2. **카피 전략 수립**
   - `copy-strategist`가 메시지 프레임 설계
   - 훅/헤드라인 전략 결정

3. **카피 생성**
   - `conversion-copywriter`가 실제 카피 작성
   - 지정된 수의 변형 생성

4. **최적화 검토**
   - 글자 수 제한 확인
   - 해시태그/CTA 포함

## Output Structure

```markdown
# Copy Variations for [채널] - [포맷]

## 카피 목적
- 목적: [awareness/consideration/conversion]
- 타겟: [페르소나명]
- 제품: [제품명]

---

## Option A: [전략 유형]

### 훅 (첫 줄)
> [주목을 끄는 첫 문장]

### 본문
[메인 카피 내용]

### CTA
[행동 유도 문구]

### 해시태그
#해시태그1 #해시태그2 ...

### 메타 정보
- 글자 수: XXX자
- 전략: [AIDA/PAS 등]

---

## Option B: [전략 유형]
...

## Option C: [전략 유형]
...

---

## 권장 옵션
- **A/B 테스트 권장**: Option A vs Option B
- **가장 전환 기대**: Option [X]
- **가장 브랜딩 적합**: Option [Y]

---

## 다음 단계
- 이미지 생성: `/create-image --concept "[카피 기반 이미지 컨셉]"`
- 영상 스크립트: `/write-script --copy "[선택한 카피]"`
```

## Channel-Specific Outputs

### Instagram Feed
```
[훅 - 더보기 전 노출되는 첫 줄]

[본문 - 2,200자 이내]

[CTA]

[해시태그 5-15개]
```

### Instagram Reels
```
[짧은 훅]
[핵심 내용 요약]
#해시태그
```

### YouTube
```
[제목 - 60자 이내]
[설명 - 첫 2줄 + 상세]
```

## Example

```bash
# 단테 커피 인스타그램 피드 카피
/generate-copy --channel instagram --format feed --persona "김지현" --product "이달의 원두"

# 결과 예시:
## Option A: 감성형
> 월요일 아침, 커피 한 잔의 여유가 필요한 순간 ☕

오늘도 바쁜 하루를 시작하기 전,
단 3분만 투자해보세요.

에티오피아 예가체프의 플로럴한 향이
여러분의 아침을 특별하게 만들어드릴 거예요.

👉 이달의 원두 첫 구매 15% 할인 (프로필 링크)

#단테커피 #이달의원두 #에티오피아예가체프 #홈카페 #아침커피 #스페셜티커피
```

## Related Commands

- `/write-script`: 영상 스크립트 작성
- `/create-image`: 카피 기반 이미지 생성
- `/plan-channels`: 채널 전략 (선행)

## Skills Used

- `message-architecture`: 메시지 구조
- `hook-formulas`: 훅 작성 공식

## Agents Used

- `copy-strategist` (전략)
- `conversion-copywriter` (작성)
