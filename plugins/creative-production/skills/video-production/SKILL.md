---
name: video-production
description: AI 비디오 생성을 위한 프롬프트 작성 및 제작 가이드
version: 1.0.0
author: Dante Labs
tags:
  - video
  - prompt
  - ai-generation
---

# AI Video Production Guide

AI 비디오 생성 도구를 위한 효과적인 프롬프트 작성 및 제작 가이드입니다.

## Video Prompt Structure

### 기본 구조
```
[장면 설명] + [움직임] + [카메라 동작] + [분위기] + [스타일]
```

### 상세 구조
```
1. Scene (장면): 무엇이 보이는가
2. Action (동작): 무슨 일이 일어나는가
3. Camera (카메라): 카메라가 어떻게 움직이는가
4. Mood (무드): 어떤 분위기인가
5. Style (스타일): 어떤 영상 스타일인가
```

## Scene Description Keywords

### 환경
```
- indoor / outdoor
- home / office / cafe
- kitchen / living room
- minimal background
- natural setting
```

### 시간대
```
- morning light
- golden hour
- sunset
- daytime
- night scene
```

## Action/Motion Keywords

### 제품 동작
```
- rotating slowly
- steam rising
- liquid pouring
- product reveal
- unboxing
```

### 인물 동작
```
- walking
- sitting
- drinking
- working
- smiling
```

### 추상적 동작
```
- floating
- falling
- flowing
- spinning
- transforming
```

## Camera Movement Keywords

### 이동
```
- static shot (고정)
- pan left/right (좌우 이동)
- tilt up/down (상하 이동)
- dolly in/out (전후 이동)
- tracking shot (추적)
```

### 줌
```
- zoom in
- zoom out
- slow zoom
- push in
```

### 특수
```
- handheld
- smooth motion
- cinematic movement
- drone shot
- orbiting
```

## Style Keywords

### 영상 스타일
```
- cinematic
- commercial
- documentary
- lifestyle
- social media
```

### 품질
```
- professional quality
- 4K resolution
- high production value
- smooth motion
- clean footage
```

### 특수 효과
```
- slow motion
- time lapse
- cinemagraph
- loop
- seamless loop
```

## Platform-Specific Guidelines

### Veo 3
```
장점: 최고 품질, 자연스러운 움직임
프롬프트: 상세한 장면 묘사, 복잡한 동작 가능
추천: 광고, 브랜드 영상
```

### Sora 2
```
장점: 창의적 표현, 예술적 스타일
프롬프트: 독특한 시각적 표현 가능
추천: 아트, 창의적 콘텐츠
```

### Kling 1.6
```
장점: 균형 잡힌 품질, 적당한 속도
프롬프트: 명확하고 간결한 설명
추천: 일반 마케팅 영상
```

### Wan 2.1
```
장점: Image-to-Video 강점
프롬프트: 이미지 기반 + 움직임 설명
추천: 제품 애니메이션
```

### Hailuo (Minimax)
```
장점: 빠른 생성, 안정적
프롬프트: 간단한 동작
추천: 빠른 테스트, 간단한 클립
```

## Coffee Brand Video Prompts

### 제품 영상
```
"A cup of specialty coffee on a wooden table,
steam rising gently from the cup,
soft morning light from window,
slow camera zoom in,
warm and cozy atmosphere,
professional product video,
smooth motion, 4K quality"
```

### 추출 과정
```
"Coffee drip bag brewing process,
hot water being poured slowly over drip bag,
coffee dripping into white cup,
overhead shot, close-up detail,
warm natural lighting,
satisfying and calming footage,
slow motion pour"
```

### 라이프스타일
```
"Young professional woman enjoying coffee at home office,
morning sunlight through window,
takes a sip and smiles contentedly,
lifestyle footage, handheld camera,
warm and authentic atmosphere,
casual and relaxed mood"
```

### Shorts/Reels 용
```
"Vertical video format,
quick montage of coffee preparation,
drip bag opening, water pouring, steam rising,
dynamic editing pace,
warm morning vibes,
engaging social media style,
15 seconds total"
```

## Image-to-Video (I2V) Prompts

이미지를 기반으로 움직임 추가:

### Cinemagraph 스타일
```
"Based on the image,
add subtle steam rising from the coffee cup,
gentle movement only in steam,
rest of image stays static,
cinemagraph style,
seamless loop"
```

### 풀 애니메이션
```
"Animate the coffee cup in the image,
camera slowly orbits around the product,
add subtle reflections and highlights,
smooth 360 degree rotation,
professional product video"
```

## Duration Guidelines

| 길이 | 추천 용도 | 프롬프트 복잡도 |
|------|---------|--------------|
| 5초 | 루프, GIF 대체 | 단순 동작 |
| 10초 | 인서트 클립 | 1-2가지 동작 |
| 15초 | Shorts, 광고 | 시작-중간-끝 |
| 30초 | 상세 제품 소개 | 여러 장면 묘사 |

## Prompt Optimization Checklist

- [ ] 장면이 명확히 설명되었는가?
- [ ] 움직임/동작이 지정되었는가?
- [ ] 카메라 동작이 포함되었는가?
- [ ] 분위기/무드가 설명되었는가?
- [ ] 영상 스타일이 지정되었는가?
- [ ] 길이/포맷에 맞는가?
- [ ] 브랜드 가이드라인에 맞는가?

## Post-Production Notes

AI 생성 영상 후처리:

1. **음악 추가**: 별도 편집 필요
2. **자막 추가**: 영상 편집 소프트웨어
3. **컷 편집**: 여러 클립 조합
4. **색보정**: 브랜드 톤 맞춤
5. **로고 추가**: 인트로/아웃트로

## File Storage

생성된 비디오는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── assets/
│   └── videos/           # 최종 비디오 저장 위치
│       ├── products/     # 제품 영상
│       ├── shorts/       # Shorts/Reels 용
│       └── raw/          # 원본 클립
└── tmp/                  # 임시 비디오 (테스트, 초안)
```

### 파일 명명 규칙

```
{project}/assets/videos/{category}/{name}-{duration}-{date}.{ext}

예시:
assets/videos/products/drip-brewing-15s-20240115.mp4
assets/videos/shorts/morning-routine-30s-20240115.mp4
assets/videos/raw/steam-loop-5s-20240115.mp4
```

### 임시 파일

테스트 생성 비디오는 `tmp/` 디렉토리에 저장:

```
tmp/video-draft-001.mp4
tmp/test-prompt-variation.mp4
```

## Usage

이 스킬은 `creative-director` 및 `production-coordinator` 에이전트가 비디오 프롬프트 작성 시 참조합니다.

`kie-video-generator` 스킬을 호출하기 전에 이 가이드를 참고하여 프롬프트를 최적화하세요.
