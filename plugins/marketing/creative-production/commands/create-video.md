---
name: create-video
description: AI 비디오 생성 도구를 사용하여 마케팅 비디오를 생성합니다.
arguments:
  - name: concept
    description: 비디오 컨셉 또는 설명
    required: true
  - name: type
    description: 비디오 유형 (product, lifestyle, ad, shorts)
    required: false
    default: "shorts"
  - name: model
    description: AI 모델 (veo3, sora2, kling, wan, hailuo)
    required: false
    default: "kling"
  - name: duration
    description: 비디오 길이 (5s, 10s, 15s, 30s)
    required: false
    default: "10s"
  - name: script
    description: 스크립트 파일 경로 또는 내용
    required: false
  - name: source-image
    description: Image-to-Video를 위한 소스 이미지 URL/경로
    required: false
---

# /create-video

AI 비디오 생성 도구(kie-video-generator)를 사용하여 마케팅 비디오를 생성합니다.

## Usage

```bash
/create-video --concept "커피 추출 과정" --type product --duration 10s
/create-video --concept "아침 루틴" --type lifestyle --model veo3
/create-video --concept "제품 소개" --source-image "./product.jpg" --model wan
```

## What This Command Does

1. **컨셉 분석**
   - `creative-director`가 비주얼 방향 설정
   - 스크립트가 있으면 비주얼 가이드 추출

2. **프롬프트 생성**
   - `video-production` 스킬 참조
   - 최적화된 비디오 프롬프트 작성

3. **비디오 생성**
   - `kie-video-generator` 스킬 호출
   - Text-to-Video 또는 Image-to-Video

4. **결과 전달**
   - 생성된 비디오 URL/파일
   - 사용된 프롬프트 기록

## Model Selection Guide

| 모델 | 강점 | 추천 용도 | 속도 |
|------|------|----------|------|
| veo3 | 최고 품질 | 광고, 브랜드 | 느림 |
| sora2 | 창의적 스타일 | 아트, 독특한 영상 | 느림 |
| kling | 균형 잡힌 품질 | 일반 용도 | 중간 |
| wan | Image-to-Video 강점 | 제품 애니메이션 | 중간 |
| hailuo | 안정적, 빠름 | 빠른 테스트 | 빠름 |

## Duration Options

| 길이 | 용도 |
|------|------|
| 5s | 루프 영상, GIF 대체 |
| 10s | 짧은 클립, 인서트 |
| 15s | 짧은 광고, Shorts |
| 30s | 상세 제품 소개 |

## Video Types

### Product (제품)
- 제품 회전, 클로즈업
- 기능 시연
- 사용 과정

### Lifestyle (라이프스타일)
- 일상 장면
- 제품 사용 상황
- 감성적 무드

### Ad (광고)
- 임팩트 있는 시작
- 명확한 메시지
- CTA 포함

### Shorts (숏폼)
- 세로 화면 최적화
- 빠른 전개
- 훅 + 핵심 + CTA

## Output Structure

```markdown
# Generated Video

## 요청 정보
| 항목 | 내용 |
|------|------|
| 컨셉 | [입력한 컨셉] |
| 유형 | [product/lifestyle/ad/shorts] |
| 모델 | [사용된 모델] |
| 길이 | [초] |

## 생성된 프롬프트
> [최적화된 프롬프트 전문]

## 결과
- **비디오 URL**: [URL]
- **로컬 저장 경로**: [있을 경우]
- **생성 시간**: [시간]
- **해상도**: [해상도]

## 사용 가이드
- Reels/Shorts: 바로 업로드 가능
- 긴 영상 편집: 인서트 클립으로 활용
- 음악 추가: 별도 편집 필요

## 다음 단계
- 변형 생성: `/create-video --concept "[컨셉]" --model different`
- 음악 추가: 편집 소프트웨어 사용
- 자막 추가: 영상 편집 후 업로드
```

## Prompt Templates

### Product Video
```
[제품] on [배경],
[카메라 무브먼트: slowly rotating, zoom in],
[조명: soft studio lighting],
professional product video,
smooth motion, high quality
```

### Lifestyle Video
```
[인물 설명] [행동],
[장소/환경],
[카메라: handheld, cinematic],
natural lighting,
warm and cozy atmosphere,
lifestyle footage
```

### Shorts/Reels
```
Vertical video format,
[주요 액션],
[빠른 전개 설명],
engaging and dynamic,
social media style,
attention-grabbing
```

## Image-to-Video (I2V)

이미지를 기반으로 움직임을 추가:

```bash
/create-video --source-image "./coffee-cup.jpg" --concept "김이 모락모락 피어오르는 커피" --model wan
```

**I2V 프롬프트**:
```
[이미지 기반] - [추가할 움직임]
Steam rising from the coffee cup,
subtle camera movement,
warm morning atmosphere,
cinemagraph style
```

## Example

```bash
/create-video --concept "드립백 커피 추출 과정" --type product --model kling --duration 15s

# 생성된 프롬프트:
> "Drip bag coffee brewing process,
> hot water being poured slowly,
> steam rising, coffee dripping,
> close-up product shot,
> warm morning light,
> smooth camera movement,
> professional product video"

# 결과:
# 비디오 URL: https://...
# 길이: 15초
# 해상도: 1080x1920 (Shorts용)
```

## Integration

```
/create-video
    ↓
creative-director (방향 설정)
    ↓
video-production (프롬프트 최적화)
    ↓
kie-video-generator (실제 생성)
    ↓
결과 반환
```

## Related Commands

- `/create-image`: 이미지 생성 (I2V 소스로 활용)
- `/write-script`: 스크립트 작성
- `/generate-copy`: 영상용 카피

## External Skill Used

- `kie-video-generator`: 실제 비디오 생성 수행
