---
name: elevenlabs-api
description: ElevenLabs AI API를 통한 고품질 음성 생성, 사운드 이펙트, 음성 클론 가이드
version: 1.0.0
tags: [audio, tts, voice, sound-effects, ai, elevenlabs]
---

# ElevenLabs API Skill

ElevenLabs AI API를 활용하여 고품질 음성 생성, 사운드 이펙트, 음성 클론 등 다양한 오디오 제작 작업을 수행하는 포괄적인 가이드입니다.

## 📥 스킬 다운로드

```bash
# NPX로 플러그인 설치 (권장)
npx dantelabs-agentic-school install media-fx

# 또는 전체 플러그인 설치
npx dantelabs-agentic-school install
```

## 🔐 인증 설정

### API 키 발급

1. [ElevenLabs 웹사이트](https://elevenlabs.io/)에서 계정 생성
2. Profile → API Keys에서 새 API 키 발급
3. API 키를 안전하게 보관

### 환경 변수 설정

**`~/.claude/auth/elevenlabs.env` 파일 생성:**

```bash
# ElevenLabs API Key
ELEVENLABS_API_KEY=your_api_key_here

# Optional: Base URL (기본값: https://api.elevenlabs.io/v1/)
ELEVENLABS_BASE_URL=https://api.elevenlabs.io/v1/
```

**인증 정보 로드:**

```bash
# Secure auth loader를 사용한 안전한 로드
source ~/.claude/skills/auth-loader/scripts/secure-load-auth.sh elevenlabs

# 또는 직접 로드
source ~/.claude/auth/elevenlabs.env
```

## 🎯 주요 기능

### 1. Text-to-Speech (TTS)

텍스트를 자연스러운 음성으로 변환합니다.

**엔드포인트:**
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
```

**기본 사용:**

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "안녕하세요. ElevenLabs AI 음성입니다.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75,
      "style": 0.0,
      "use_speaker_boost": true
    }
  }' \
  --output speech.mp3
```

**주요 파라미터:**

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `text` | string | required | 변환할 텍스트 |
| `model_id` | string | eleven_multilingual_v2 | 사용할 모델 ID |
| `voice_settings.stability` | float | 0.5 | 감정 범위 (0~1, 낮을수록 감정 변화 큼) |
| `voice_settings.similarity_boost` | float | 0.75 | 원본 음성 유사도 (0~1) |
| `voice_settings.style` | float | 0.0 | 스타일 강조 (0~1) |
| `voice_settings.speed` | float | 1.0 | 재생 속도 (0.5~2.0) |
| `voice_settings.use_speaker_boost` | boolean | true | 음성 유사도 향상 (지연시간 증가) |

**Query 파라미터:**

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `enable_logging` | boolean | true | 히스토리 기록 활성화 |
| `optimize_streaming_latency` | integer | None | 스트리밍 지연 최적화 (0~4) |
| `output_format` | string | mp3_44100_128 | 출력 오디오 형식 |

**출력 포맷 옵션:**

- **MP3**: `mp3_22050_32`, `mp3_44100_128`, `mp3_44100_192` 등
- **Opus**: `opus_48000_128`, `opus_48000_192` 등
- **PCM**: `pcm_16000`, `pcm_24000`, `pcm_44100` 등
- **WAV**: `wav_16000`, `wav_44100`, `wav_48000` 등

### 2. Streaming TTS (WebSocket)

실시간 스트리밍으로 음성을 생성합니다.

**엔드포인트:**
```
wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream
```

**예제:**

```python
import websocket
import json

def on_message(ws, message):
    # 오디오 청크 수신
    with open("stream_output.mp3", "ab") as f:
        f.write(message)

def on_open(ws):
    # 텍스트 전송
    ws.send(json.dumps({
        "text": "스트리밍 음성 테스트입니다.",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }))

ws = websocket.WebSocketApp(
    f"wss://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream",
    header=[f"xi-api-key: {os.getenv('ELEVENLABS_API_KEY')}"],
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

### 3. Sound Effects

텍스트 설명으로 사운드 이펙트를 생성합니다.

**엔드포인트:**
```
POST https://api.elevenlabs.io/v1/sound-generation
```

**기본 사용:**

```bash
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "경쾌한 종소리와 박수 소리",
    "duration_seconds": 5.0,
    "prompt_influence": 0.3,
    "model_id": "eleven_text_to_sound_v2"
  }' \
  --output sound_effect.mp3
```

**주요 파라미터:**

| 파라미터 | 타입 | 제약 | 설명 |
|---------|------|------|------|
| `text` | string | required | 사운드 설명 |
| `duration_seconds` | float | 0.5~30.0 | 생성할 사운드 길이 (초) |
| `prompt_influence` | float | 0.0~1.0 | 프롬프트 영향력 (기본값: 0.3) |
| `model_id` | string | — | eleven_text_to_sound_v2 권장 |
| `loop` | boolean | false | 루프 사운드 생성 (v2만 지원) |

**사용 예시:**

- 게임 효과음: "총소리와 폭발음"
- 영화 사운드: "빗소리와 천둥소리"
- Foley 사운드: "발자국 소리와 문 여닫는 소리"
- 환경음: "숲속 새소리와 바람 소리"

### 4. Voice Management

사용 가능한 음성을 조회하고 관리합니다.

#### 4.1 음성 목록 조회

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/voices
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

**Query 파라미터:**

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `page_size` | integer | 페이지당 결과 수 (기본값: 30) |
| `page_token` | string | 페이지네이션 토큰 |
| `voice_ids` | array | 특정 Voice ID 목록 조회 (최대 100개) |

**응답 예시:**

```json
{
  "voices": [
    {
      "voice_id": "21m00Tcm4TlvDq8ikWAM",
      "name": "Rachel",
      "category": "premade",
      "labels": {
        "accent": "american",
        "age": "young",
        "gender": "female",
        "use case": "narration"
      }
    }
  ],
  "has_more": false,
  "next_page_token": null
}
```

#### 4.2 특정 음성 조회

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/voices/{voice_id}
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/voices/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

#### 4.3 음성 샘플 오디오 다운로드

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/voices/{voice_id}/samples/{sample_id}/audio
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/voices/21m00Tcm4TlvDq8ikWAM/samples/sample123/audio" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  --output voice_sample.mp3
```

### 5. Voice Cloning

사용자 음성을 학습하여 커스텀 음성을 생성합니다.

#### 5.1 Instant Voice Cloning (IVC)

**엔드포인트:**
```
POST https://api.elevenlabs.io/v1/voices/add
```

**기본 사용 (파일 업로드):**

```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/add" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "name=My Custom Voice" \
  -F "description=클론된 음성" \
  -F "files=@sample1.mp3" \
  -F "files=@sample2.mp3" \
  -F "files=@sample3.mp3"
```

**요구 사항:**

- 최소 1개, 권장 3~5개의 오디오 샘플
- 각 샘플: 최소 30초, 권장 1~2분
- 깨끗한 음질, 배경 소음 최소화
- 다양한 감정과 톤 포함

#### 5.2 Professional Voice Cloning (PVC)

더 높은 품질의 음성 클론을 위해 ElevenLabs 팀이 직접 처리합니다.

**요구 사항:**
- 최소 30분 분량의 고품질 오디오
- 전문 마이크 녹음 권장
- 다양한 감정, 톤, 속도 포함

**프로세스:**
1. 샘플 업로드 및 요청 제출
2. ElevenLabs 팀 검토 (1~2주 소요)
3. 음성 클론 완료 및 활성화

### 6. History Management

생성한 오디오 히스토리를 조회하고 관리합니다.

#### 6.1 히스토리 목록 조회

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/history
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/history?page_size=10" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

#### 6.2 히스토리 오디오 다운로드

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/history/{history_item_id}/audio
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/history/history123/audio" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  --output history_audio.mp3
```

#### 6.3 히스토리 항목 삭제

**엔드포인트:**
```
DELETE https://api.elevenlabs.io/v1/history/{history_item_id}
```

**기본 사용:**

```bash
curl -X DELETE "https://api.elevenlabs.io/v1/history/history123" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## 🔧 고급 기능

### 다국어 지원

ElevenLabs는 29개 이상의 언어를 지원합니다.

**언어 코드 지정 (ISO 639-1):**

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "こんにちは、ElevenLabsです。",
    "model_id": "eleven_multilingual_v2",
    "language_code": "ja"
  }' \
  --output japanese_speech.mp3
```

**지원 언어:**
- 한국어 (ko), 영어 (en), 일본어 (ja), 중국어 (zh)
- 스페인어 (es), 프랑스어 (fr), 독일어 (de), 이탈리아어 (it)
- 포르투갈어 (pt), 러시아어 (ru), 아랍어 (ar), 힌디어 (hi)
- 그 외 다수 언어 지원

### 컨텍스트 연속성

이전/다음 텍스트를 지정하여 자연스러운 연결을 보장합니다.

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "이것이 현재 문장입니다.",
    "previous_text": "이것이 이전 문장입니다.",
    "next_text": "이것이 다음 문장입니다.",
    "model_id": "eleven_multilingual_v2"
  }' \
  --output context_speech.mp3
```

### 발음 사전 (Pronunciation Dictionary)

커스텀 발음 규칙을 적용합니다.

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AWS는 아마존 웹 서비스입니다.",
    "model_id": "eleven_multilingual_v2",
    "pronunciation_dictionary_locators": [
      {
        "pronunciation_dictionary_id": "dict_id_123",
        "version_id": "v1"
      }
    ]
  }' \
  --output custom_pronunciation.mp3
```

### Deterministic Sampling (Seed)

동일한 입력에 대해 재현 가능한 출력을 생성합니다.

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "재현 가능한 음성입니다.",
    "model_id": "eleven_multilingual_v2",
    "seed": 12345
  }' \
  --output deterministic_speech.mp3
```

## 📊 사용량 및 할당량 확인

**엔드포인트:**
```
GET https://api.elevenlabs.io/v1/user/subscription
```

**기본 사용:**

```bash
curl -X GET "https://api.elevenlabs.io/v1/user/subscription" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

**응답 예시:**

```json
{
  "tier": "free",
  "character_count": 5000,
  "character_limit": 10000,
  "can_extend_character_limit": true,
  "allowed_to_extend_character_limit": true,
  "next_character_count_reset_unix": 1709251200,
  "voice_limit": 3,
  "professional_voice_limit": 0,
  "can_use_instant_voice_cloning": true
}
```

## 🛠️ SDK 사용 (선택사항)

### Python SDK

**설치:**

```bash
pip install elevenlabs
```

**기본 사용:**

```python
from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs(api_key="your_api_key")

# Text-to-Speech
audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="안녕하세요, ElevenLabs입니다.",
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.0,
        use_speaker_boost=True
    )
)

# 파일 저장
with open("output.mp3", "wb") as f:
    f.write(audio)
```

### Node.js SDK

**설치:**

```bash
npm install @elevenlabs/elevenlabs-js
```

**기본 사용:**

```javascript
import { ElevenLabs } from "@elevenlabs/elevenlabs-js";

const client = new ElevenLabs({
  apiKey: "your_api_key",
});

// Text-to-Speech
const audio = await client.textToSpeech.convert({
  voiceId: "21m00Tcm4TlvDq8ikWAM",
  text: "안녕하세요, ElevenLabs입니다.",
  modelId: "eleven_multilingual_v2",
  voiceSettings: {
    stability: 0.5,
    similarityBoost: 0.75,
    style: 0.0,
    useSpeakerBoost: true,
  },
});

// 파일 저장
import fs from "fs";
const buffer = await audio.arrayBuffer();
fs.writeFileSync("output.mp3", Buffer.from(buffer));
```

## 💡 베스트 프랙티스

### 1. 음성 설정 최적화

- **안정성 (stability)**: 0.3~0.7 권장 (낮을수록 감정 변화 많음)
- **유사도 (similarity_boost)**: 0.7~0.9 권장 (높을수록 원본 유사)
- **스타일 (style)**: 0.0~0.5 권장 (높을수록 과장됨)
- **속도 (speed)**: 0.8~1.2 권장 (자연스러운 범위)

### 2. 출력 포맷 선택

- **MP3**: 일반적인 용도, 파일 크기 작음
- **WAV/PCM**: 고품질 편집, 후처리 작업
- **Opus**: 낮은 대역폭, 스트리밍 최적화

### 3. 비용 최적화

- `enable_logging=false`로 히스토리 기록 비활성화
- 필요한 경우에만 `use_speaker_boost=true` 사용
- 적절한 `output_format` 선택 (샘플레이트 vs 품질)

### 4. 에러 핸들링

**공통 에러 코드:**

- `401 Unauthorized`: API 키 오류
- `422 Unprocessable Entity`: 잘못된 요청 파라미터
- `429 Too Many Requests`: 요청 제한 초과
- `500 Internal Server Error`: 서버 오류

**재시도 로직:**

```bash
for i in {1..3}; do
  if curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/..." \
    -H "xi-api-key: $ELEVENLABS_API_KEY" \
    --output output.mp3 --fail; then
    break
  fi
  echo "재시도 $i/3..."
  sleep 2
done
```

## 🔗 참고 자료

- **공식 문서**: [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference/introduction)
- **API Explorer**: [Interactive API Testing](https://elevenlabs.io/docs/api-reference)
- **Voice Library**: [Pre-made Voices](https://elevenlabs.io/voice-library)
- **Sound Effects Guide**: [Sound Effects Documentation](https://elevenlabs.io/docs/overview/capabilities/sound-effects)
- **Pricing**: [Plan Comparison](https://elevenlabs.io/pricing)
- **Status Page**: [API Status](https://status.elevenlabs.io/)

## 📞 지원 및 커뮤니티

- **Discord**: [ElevenLabs Community](https://discord.gg/elevenlabs)
- **Support**: support@elevenlabs.io
- **GitHub**: [ElevenLabs SDKs](https://github.com/elevenlabs)

---

**© 2026 Dante Labs | [dante-labs.com](https://dante-labs.com)**
