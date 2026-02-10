---
name: generate-speech
description: ElevenLabs API를 사용하여 텍스트를 자연스러운 음성으로 변환
arguments:
  - name: text
    required: true
    description: 음성으로 변환할 텍스트
  - name: voice-id
    required: false
    description: 사용할 음성 ID (기본값: Rachel - 21m00Tcm4TlvDq8ikWAM)
  - name: output
    required: false
    description: 출력 파일 경로 (기본값: speech.mp3)
  - name: model
    required: false
    description: 사용할 모델 (기본값: eleven_multilingual_v2)
  - name: language
    required: false
    description: 언어 코드 (예: ko, en, ja)
  - name: stability
    required: false
    description: 감정 범위 (0.0~1.0, 기본값: 0.5)
  - name: similarity
    required: false
    description: 음성 유사도 (0.0~1.0, 기본값: 0.75)
  - name: style
    required: false
    description: 스타일 강조 (0.0~1.0, 기본값: 0.0)
  - name: speed
    required: false
    description: 재생 속도 (0.5~2.0, 기본값: 1.0)
---

# Generate Speech Command

텍스트를 고품질 AI 음성으로 변환하는 명령어입니다.

## 사용 방법

```bash
/generate-speech --text "안녕하세요, ElevenLabs 음성입니다."
```

## 상세 옵션

```bash
/generate-speech \
  --text "한국어 음성 테스트입니다." \
  --voice-id 21m00Tcm4TlvDq8ikWAM \
  --output korean_speech.mp3 \
  --model eleven_multilingual_v2 \
  --language ko \
  --stability 0.5 \
  --similarity 0.75 \
  --style 0.0 \
  --speed 1.0
```

## 실행 단계

1. **인증 확인**: `~/.claude/auth/elevenlabs.env`에서 API 키 로드
2. **텍스트 검증**: 입력 텍스트가 비어있지 않은지 확인
3. **API 호출**: ElevenLabs TTS API로 POST 요청
4. **파일 저장**: 응답받은 오디오를 지정된 경로에 저장
5. **결과 출력**: 생성된 파일 경로와 크기 출력

## API 요청 예시

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "안녕하세요, ElevenLabs 음성입니다.",
    "model_id": "eleven_multilingual_v2",
    "language_code": "ko",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "speed": 1.0,
      "use_speaker_boost": true
    }
  }' \
  --output speech.mp3
```

## 인기 음성 ID

| 음성 이름 | Voice ID | 설명 |
|---------|----------|------|
| Rachel | 21m00Tcm4TlvDq8ikWAM | 미국 영어, 여성, 내레이션 |
| Adam | pNInz6obpgDQGcFmaJgB | 미국 영어, 남성, 내레이션 |
| Domi | AZnzlk1XvdvUeBnXmlld | 미국 영어, 여성, 활기찬 |
| Bella | EXAVITQu4vr4xnSDxMaL | 미국 영어, 여성, 부드러운 |
| Antoni | ErXwobaYiN019PkySvjV | 미국 영어, 남성, 따뜻한 |
| Elli | MF3mGyEYCl7XYWbV9V6O | 미국 영어, 여성, 감정적 |

## 음성 설정 가이드

### Stability (안정성)
- **0.0~0.3**: 매우 표현적, 감정 변화 큼
- **0.4~0.6**: 균형잡힌, 일반적 사용
- **0.7~1.0**: 안정적, 일관된 톤

### Similarity Boost (유사도)
- **0.0~0.5**: 창의적 변형 많음
- **0.6~0.8**: 균형잡힌 유사도
- **0.9~1.0**: 원본 음성에 매우 가까움

### Style (스타일)
- **0.0**: 자연스러운 톤
- **0.5**: 적당한 강조
- **1.0**: 매우 과장된 표현

### Speed (속도)
- **0.5**: 매우 느림
- **1.0**: 정상 속도
- **1.5**: 빠름
- **2.0**: 매우 빠름

## 지원 언어

- 한국어 (ko), 영어 (en), 일본어 (ja), 중국어 (zh)
- 스페인어 (es), 프랑스어 (fr), 독일어 (de), 이탈리아어 (it)
- 포르투갈어 (pt), 러시아어 (ru), 아랍어 (ar), 힌디어 (hi)
- 그 외 29개 이상 언어 지원

## 출력 포맷

기본값은 `mp3_44100_128`이며, 다른 포맷을 사용하려면 API 요청에 `output_format` 쿼리 파라미터를 추가하세요:

- `mp3_44100_192` (고품질 MP3)
- `pcm_44100` (무압축 PCM)
- `wav_44100` (WAV 형식)
- `opus_48000_128` (Opus 코덱)

## 에러 핸들링

- **401 Unauthorized**: API 키 확인
- **422 Unprocessable**: 잘못된 voice_id 또는 파라미터
- **429 Too Many Requests**: 요청 제한 초과, 잠시 대기
- **500 Internal Server Error**: 재시도 권장

## 참고 자료

- [Text-to-Speech API 문서](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [Voice Library](https://elevenlabs.io/voice-library)
- [음성 설정 가이드](https://elevenlabs.io/docs/overview/capabilities/text-to-speech)
