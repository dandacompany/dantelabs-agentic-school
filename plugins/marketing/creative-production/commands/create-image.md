---
name: create-image
description: AI 이미지 생성 도구를 사용하여 마케팅 이미지를 생성합니다.
arguments:
  - name: concept
    description: 이미지 컨셉 또는 설명
    required: true
  - name: type
    description: 이미지 유형 (product, lifestyle, brand, thumbnail)
    required: false
    default: "product"
  - name: model
    description: AI 모델 (flux-pro, gpt-4o, ideogram, imagen)
    required: false
    default: "flux-pro"
  - name: size
    description: 이미지 크기 (1:1, 4:5, 9:16, 16:9)
    required: false
    default: "1:1"
  - name: style
    description: 스타일 키워드 (예: minimal, warm, professional)
    required: false
---

# /create-image

AI 이미지 생성 도구(kie-image-generator)를 사용하여 마케팅 이미지를 생성합니다.

## Usage

```bash
/create-image --concept "커피 제품 사진" --type product
/create-image --concept "아침 홈카페 라이프스타일" --type lifestyle --size 4:5
/create-image --concept "유튜브 썸네일" --type thumbnail --model gpt-4o
```

## What This Command Does

1. **컨셉 분석**
   - `creative-director`가 비주얼 방향 설정
   - 브랜드 가이드라인 적용

2. **프롬프트 생성**
   - `image-prompt-guide` 스킬 참조
   - 최적화된 프롬프트 작성

3. **이미지 생성**
   - `kie-image-generator` 스킬 호출
   - 선택된 모델로 이미지 생성

4. **결과 전달**
   - 생성된 이미지 URL/파일
   - 사용된 프롬프트 기록

## Model Selection Guide

| 모델 | 강점 | 추천 용도 |
|------|------|----------|
| flux-pro | 고품질, 디테일 | 제품 사진, 광고 |
| gpt-4o | 자연스러운 인물 | 라이프스타일, 인물 |
| ideogram | 아트/그래픽 | 일러스트, 아트워크 |
| imagen | 사실적 | 사진급 퀄리티 |
| flux-schnell | 빠른 생성 | 테스트, 아이디어 |

## Size Guide

| 비율 | 픽셀 | 용도 |
|------|------|------|
| 1:1 | 1024x1024 | Instagram 피드 |
| 4:5 | 1024x1280 | Instagram 세로 |
| 9:16 | 1024x1820 | Stories, Reels |
| 16:9 | 1820x1024 | YouTube, 가로 |

## Output Structure

```markdown
# Generated Image

## 요청 정보
| 항목 | 내용 |
|------|------|
| 컨셉 | [입력한 컨셉] |
| 유형 | [product/lifestyle/brand] |
| 모델 | [사용된 모델] |
| 크기 | [비율] |

## 생성된 프롬프트
> [최적화된 프롬프트 전문]

## 결과
- **이미지 URL**: [URL]
- **로컬 저장 경로**: [있을 경우]
- **생성 시간**: [시간]

## 사용 가이드
- Instagram 피드: 바로 사용 가능
- 스토리: 텍스트 추가 권장
- 광고: A/B 테스트 변형 생성 권장

## 다음 단계
- 변형 생성: `/create-image --concept "[컨셉]" --style different`
- 비디오화: `/create-video --image "[이미지URL]"`
- 카피 추가: `/generate-copy --for-image "[이미지URL]"`
```

## Prompt Templates by Type

### Product (제품)
```
[제품 설명] on [배경 설명],
[조명 설명],
professional product photography,
high quality, sharp focus,
[무드 키워드]
```

### Lifestyle (라이프스타일)
```
[인물 설명] [행동],
[장소/환경],
[조명 설명],
lifestyle photography,
warm and inviting atmosphere,
candid natural pose
```

### Thumbnail (썸네일)
```
YouTube thumbnail style,
[주요 요소],
bold text space on [위치],
[색상] color scheme,
attention-grabbing composition,
professional graphic design
```

## Example

```bash
/create-image --concept "미니멀 테이블 위 드립백 커피" --type product --model flux-pro

# 생성된 프롬프트:
> "A drip bag coffee on a minimal white wooden table,
> soft morning natural light from window,
> professional product photography,
> warm brown tones, cozy atmosphere,
> shallow depth of field,
> high quality, 8k resolution"

# 결과:
# 이미지 URL: https://...
```

## Integration

이 커맨드는 내부적으로 `kie-image-generator` 스킬을 호출합니다.

```
/create-image
    ↓
creative-director (방향 설정)
    ↓
image-prompt-guide (프롬프트 최적화)
    ↓
kie-image-generator (실제 생성)
    ↓
결과 반환
```

## Related Commands

- `/create-video`: 비디오 생성
- `/generate-copy`: 이미지용 카피 생성

## External Skill Used

- `kie-image-generator`: 실제 이미지 생성 수행
