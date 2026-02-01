---
name: image-prompt-guide
description: AI 이미지 생성을 위한 프롬프트 작성 가이드 및 최적화 기법
version: 1.0.0
author: Dante Labs
tags:
  - image
  - prompt
  - ai-generation
---

# AI Image Prompt Guide

AI 이미지 생성 도구를 위한 효과적인 프롬프트 작성 가이드입니다.

## Prompt Structure

### 기본 구조
```
[주제/대상] + [스타일] + [무드/분위기] + [조명] + [구도] + [품질 키워드]
```

### 상세 구조
```
1. Subject (주제): 무엇을 생성할 것인가
2. Style (스타일): 어떤 스타일로 생성할 것인가
3. Mood (무드): 어떤 분위기를 원하는가
4. Lighting (조명): 어떤 조명 조건인가
5. Composition (구도): 어떤 앵글/프레이밍인가
6. Quality (품질): 품질 관련 키워드
```

## Subject Keywords

### 제품
```
- product photography
- commercial photography
- packshot
- product on white background
- product in context
- flatlay
```

### 인물
```
- portrait
- lifestyle photography
- candid photo
- natural pose
- professional headshot
```

### 음식/음료
```
- food photography
- beverage photography
- coffee photography
- overhead shot
- close-up detail
```

## Style Keywords

### 사진 스타일
```
- professional photography
- editorial photography
- lifestyle photography
- documentary style
- candid photography
```

### 아트 스타일
```
- digital art
- illustration
- minimalist design
- modern aesthetic
- clean and simple
```

### 특정 스타일
```
- minimal
- vintage
- modern
- rustic
- scandinavian
```

## Mood/Atmosphere Keywords

### 따뜻한 무드
```
- warm and cozy
- inviting atmosphere
- comfortable
- homey
- welcoming
```

### 프리미엄 무드
```
- luxurious
- elegant
- sophisticated
- premium quality
- high-end
```

### 자연스러운 무드
```
- natural
- organic
- authentic
- effortless
- relaxed
```

## Lighting Keywords

### 자연광
```
- natural lighting
- soft natural light
- morning sunlight
- golden hour
- window light
- diffused daylight
```

### 스튜디오 조명
```
- studio lighting
- soft box lighting
- rim lighting
- dramatic lighting
- even lighting
```

### 특수 조명
```
- backlit
- side lighting
- warm tones
- cool tones
- soft shadows
```

## Composition Keywords

### 앵글
```
- eye level
- overhead shot
- 45-degree angle
- low angle
- bird's eye view
```

### 프레이밍
```
- close-up
- extreme close-up
- medium shot
- wide shot
- rule of thirds
```

### 포커스
```
- shallow depth of field
- bokeh background
- sharp focus on subject
- soft focus
- tilt-shift effect
```

## Quality Keywords

```
- high quality
- high resolution
- 8k
- ultra detailed
- sharp
- professional
- photorealistic
```

## Platform-Specific Tips

### Flux Pro/Dev
- 상세한 묘사가 효과적
- 스타일 키워드 강조
- 품질 키워드 포함

### GPT-4O Image
- 자연스러운 문장 형태
- 인물 묘사에 강점
- 맥락 설명 포함

### Ideogram
- 텍스트 포함 이미지에 강점
- 그래픽 디자인 스타일
- 명확한 레이아웃 설명

### Imagen
- 사실적 묘사
- 디테일한 환경 설명
- 자연스러운 조명

## Coffee Brand Prompt Examples

### 제품 사진
```
"A drip bag coffee package on a minimal white marble table,
soft morning natural light from side window,
warm brown and cream tones,
professional product photography,
shallow depth of field,
clean and minimal composition,
high quality, 8k resolution"
```

### 라이프스타일
```
"A 30-year-old Korean woman enjoying coffee in a cozy home office,
wearing casual clothes, warm smile,
morning sunlight through window,
lifestyle photography,
natural and candid pose,
warm and inviting atmosphere,
high quality portrait photography"
```

### 브랜드 무드
```
"Steam rising from a cup of specialty coffee,
close-up shot, shallow depth of field,
warm morning light,
cozy cafe atmosphere,
minimalist aesthetic,
professional food photography,
warm brown tones, cream accents"
```

### 썸네일
```
"YouTube thumbnail design,
coffee cup and coffee beans arrangement,
bold text space on right side,
warm brown color scheme,
eye-catching composition,
professional graphic design,
clean and modern style"
```

## Negative Prompts (피해야 할 것)

일부 모델에서 지원:

```
"low quality, blurry, distorted, ugly,
bad proportions, watermark, text,
oversaturated, underexposed,
artificial looking, plastic texture"
```

## Prompt Optimization Checklist

- [ ] 주제가 명확한가?
- [ ] 스타일이 지정되었는가?
- [ ] 무드/분위기가 설명되었는가?
- [ ] 조명 조건이 포함되었는가?
- [ ] 구도/앵글이 설명되었는가?
- [ ] 품질 키워드가 포함되었는가?
- [ ] 브랜드 가이드라인에 맞는가?

## File Storage

생성된 이미지는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── assets/
│   └── images/           # 최종 이미지 저장 위치
│       ├── products/     # 제품 이미지
│       ├── lifestyle/    # 라이프스타일 이미지
│       └── thumbnails/   # 썸네일 이미지
└── tmp/                  # 임시 이미지 (테스트, 초안)
```

### 파일 명명 규칙

```
{project}/assets/images/{category}/{name}-{date}.{ext}

예시:
assets/images/products/drip-bag-hero-20240115.png
assets/images/lifestyle/morning-coffee-20240115.png
assets/images/thumbnails/youtube-ep01-20240115.png
```

### 임시 파일

테스트 생성 이미지는 `tmp/` 디렉토리에 저장:

```
tmp/image-draft-001.png
tmp/test-prompt-variation.png
```

## Usage

이 스킬은 `creative-director` 및 `production-coordinator` 에이전트가 이미지 프롬프트 작성 시 참조합니다.

`kie-image-generator` 스킬을 호출하기 전에 이 가이드를 참고하여 프롬프트를 최적화하세요.
