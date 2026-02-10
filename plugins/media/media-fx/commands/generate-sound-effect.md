---
name: generate-sound-effect
description: 텍스트 설명으로 사운드 이펙트 생성
arguments:
  - name: description
    required: true
    description: 생성할 사운드의 텍스트 설명
  - name: duration
    required: false
    description: 사운드 길이 (초, 0.5~30.0, 기본값: 5.0)
  - name: output
    required: false
    description: 출력 파일 경로 (기본값: sound_effect.mp3)
  - name: influence
    required: false
    description: 프롬프트 영향력 (0.0~1.0, 기본값: 0.3)
  - name: loop
    required: false
    description: 루프 사운드 생성 여부 (true/false, 기본값: false)
  - name: model
    required: false
    description: 사용할 모델 (기본값: eleven_text_to_sound_v2)
---

# Generate Sound Effect Command

텍스트 설명으로 고품질 사운드 이펙트를 생성하는 명령어입니다.

## 사용 방법

```bash
/generate-sound-effect --description "경쾌한 종소리와 박수 소리"
```

## 상세 옵션

```bash
/generate-sound-effect \
  --description "빗소리와 천둥소리" \
  --duration 10.0 \
  --output rain_thunder.mp3 \
  --influence 0.3 \
  --loop false \
  --model eleven_text_to_sound_v2
```

## 실행 단계

1. **인증 확인**: `~/.claude/auth/elevenlabs.env`에서 API 키 로드
2. **설명 검증**: 텍스트 설명이 명확하고 구체적인지 확인
3. **파라미터 검증**: duration이 0.5~30.0 범위 내인지 확인
4. **API 호출**: ElevenLabs Sound Generation API로 POST 요청
5. **파일 저장**: 생성된 사운드를 지정된 경로에 저장
6. **결과 출력**: 파일 경로, 크기, 길이 출력

## API 요청 예시

```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "빗소리와 천둥소리",
    "duration_seconds": 10.0,
    "prompt_influence": 0.3,
    "model_id": "eleven_text_to_sound_v2",
    "loop": false
  }' \
  --output rain_thunder.mp3
```

## 사용 예시

### 게임 효과음

```bash
# 총소리
/generate-sound-effect --description "권총 발사음과 탄피 떨어지는 소리" --duration 2.0

# 폭발음
/generate-sound-effect --description "큰 폭발음과 잔해 떨어지는 소리" --duration 3.0

# 발자국
/generate-sound-effect --description "자갈길 위의 발자국 소리" --duration 5.0 --loop true
```

### 영화 사운드

```bash
# 액션 신
/generate-sound-effect --description "자동차 추격전, 타이어 끽끽 소리" --duration 8.0

# 호러 신
/generate-sound-effect --description "삐걱거리는 문소리와 바람 소리" --duration 6.0

# 드라마 신
/generate-sound-effect --description "카페 배경음, 사람들 대화와 커피 머신 소리" --duration 30.0
```

### 환경음 (Ambient)

```bash
# 자연
/generate-sound-effect --description "숲속 새소리와 바람 소리" --duration 30.0 --loop true

# 도시
/generate-sound-effect --description "도심 교통 소음과 사람들 소리" --duration 30.0 --loop true

# 실내
/generate-sound-effect --description "사무실 키보드 소리와 프린터 소리" --duration 20.0
```

### Foley 사운드

```bash
# 문
/generate-sound-effect --description "나무 문 여닫는 소리" --duration 2.0

# 의류
/generate-sound-effect --description "옷 바스락거리는 소리" --duration 3.0

# 음식
/generate-sound-effect --description "바삭한 과자 씹는 소리" --duration 4.0
```

## 파라미터 가이드

### Duration (길이)
- **0.5~2.0초**: 짧은 효과음 (버튼 클릭, 알림)
- **2.0~5.0초**: 일반 효과음 (총소리, 문 여닫음)
- **5.0~15.0초**: 긴 효과음 (환경음, 액션 신)
- **15.0~30.0초**: 배경음 (앰비언트, 루프)

### Prompt Influence (프롬프트 영향력)
- **0.0~0.2**: 창의적이고 다양한 해석
- **0.3~0.5**: 균형잡힌 결과
- **0.6~1.0**: 설명에 매우 충실

### Loop (루프)
- **false**: 일반 사운드 (시작과 끝이 명확)
- **true**: 매끄럽게 반복되는 사운드 (배경음에 적합)

## 효과적인 설명 작성 팁

### 1. 구체적으로 작성
❌ "폭발 소리"
✅ "큰 폭발음과 잔해 떨어지는 소리, 여운이 남는 느낌"

### 2. 여러 요소 결합
❌ "비 소리"
✅ "빗소리와 천둥소리, 빗방울이 유리창에 떨어지는 소리"

### 3. 감정과 분위기 추가
❌ "발자국"
✅ "조용한 밤, 긴장감 있는 느린 발자국 소리"

### 4. 시간적 흐름 묘사
❌ "문 소리"
✅ "삐걱거리며 천천히 열리는 오래된 나무 문, 그리고 '쾅' 하고 닫히는 소리"

## 출력 포맷

- **기본 포맷**: MP3 (고품질, 압축)
- **WAV 다운로드**: 48kHz 샘플레이트 (영화/TV/게임 표준)
- 루프 사운드는 WAV로 다운로드 불가

## 제약 사항

- 최소 길이: 0.5초
- 최대 길이: 30.0초
- 루프 기능: `eleven_text_to_sound_v2` 모델만 지원
- 동시 생성 제한: API 플랜에 따라 다름

## 비용 정보

Sound Effects는 **생성당 과금**됩니다 (문자 수 기반 TTS와 다름).

- Free Tier: 매월 제한된 생성 횟수
- Creator Tier: 더 많은 생성 횟수
- Pro/Business: 무제한 생성

자세한 내용은 [ElevenLabs Pricing](https://elevenlabs.io/pricing) 참조

## 에러 핸들링

- **401 Unauthorized**: API 키 확인
- **422 Unprocessable**: 잘못된 duration 또는 파라미터
- **429 Too Many Requests**: 생성 제한 초과, 플랜 업그레이드 권장
- **500 Internal Server Error**: 재시도 권장

## 품질 최적화 팁

1. **명확한 설명**: 원하는 사운드를 구체적으로 묘사
2. **적절한 길이**: 용도에 맞는 duration 설정
3. **프롬프트 영향력**: 0.3~0.5 범위에서 실험
4. **루프 활용**: 배경음은 loop=true로 설정
5. **반복 생성**: 만족스러운 결과가 나올 때까지 재시도

## 참고 자료

- [Sound Effects API 문서](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert)
- [Sound Effects 가이드](https://elevenlabs.io/docs/overview/capabilities/sound-effects)
- [Sound Effects Quickstart](https://elevenlabs.io/docs/developers/guides/cookbooks/sound-effects)
- [샘플 갤러리](https://elevenlabs.io/sound-effects)
