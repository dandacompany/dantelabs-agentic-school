---
name: list-voices
description: 사용 가능한 ElevenLabs 음성 목록 조회
arguments:
  - name: format
    required: false
    description: 출력 포맷 (table/json, 기본값: table)
  - name: category
    required: false
    description: 카테고리 필터 (premade/cloned/professional)
  - name: gender
    required: false
    description: 성별 필터 (male/female)
  - name: accent
    required: false
    description: 억양 필터 (american/british/australian 등)
  - name: age
    required: false
    description: 나이대 필터 (young/middle_aged/old)
  - name: use-case
    required: false
    description: 용도 필터 (narration/video_games/audiobook 등)
  - name: output
    required: false
    description: JSON 파일로 저장할 경로 (선택사항)
---

# List Voices Command

ElevenLabs에서 사용 가능한 모든 음성을 조회하고 필터링하는 명령어입니다.

## 사용 방법

### 기본 사용 (전체 목록)

```bash
/list-voices
```

### 포맷 지정

```bash
# 테이블 형식 (기본값)
/list-voices --format table

# JSON 형식
/list-voices --format json
```

### 필터링

```bash
# 여성 음성만
/list-voices --gender female

# 미국 억양, 내레이션용
/list-voices --accent american --use-case narration

# 젊은 남성 음성
/list-voices --age young --gender male

# 프로페셔널 클론 음성
/list-voices --category professional
```

### JSON 파일로 저장

```bash
/list-voices --format json --output voices.json
```

## 실행 단계

1. **인증 확인**: `~/.claude/auth/elevenlabs.env`에서 API 키 로드
2. **API 호출**: ElevenLabs Voices API로 GET 요청
3. **필터 적용**: 지정된 필터 조건에 맞는 음성만 선택
4. **포맷팅**: 테이블 또는 JSON 형식으로 포맷
5. **출력**: 콘솔 출력 및 파일 저장 (선택사항)

## API 요청 예시

```bash
# 전체 음성 목록
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"

# 특정 음성 ID로 상세 정보 조회
curl -X GET "https://api.elevenlabs.io/v1/voices/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## 응답 예시

### 테이블 형식

```
┌────────────────────────┬──────────┬───────────┬──────────┬─────────┬───────────────┐
│ Name                   │ Voice ID │ Category  │ Gender   │ Accent  │ Use Case      │
├────────────────────────┼──────────┼───────────┼──────────┼─────────┼───────────────┤
│ Rachel                 │ 21m00... │ premade   │ female   │ american│ narration     │
│ Adam                   │ pNInz... │ premade   │ male     │ american│ narration     │
│ Domi                   │ AZnzl... │ premade   │ female   │ american│ video_games   │
│ Bella                  │ EXAVI... │ premade   │ female   │ american│ audiobook     │
│ Antoni                 │ ErXwo... │ premade   │ male     │ american│ narration     │
└────────────────────────┴──────────┴───────────┴──────────┴─────────┴───────────────┘
```

### JSON 형식

```json
{
  "voices": [
    {
      "voice_id": "21m00Tcm4TlvDq8ikWAM",
      "name": "Rachel",
      "category": "premade",
      "labels": {
        "accent": "american",
        "description": "calm",
        "age": "young",
        "gender": "female",
        "use case": "narration"
      },
      "samples": [
        {
          "sample_id": "sample1",
          "file_name": "rachel_sample1.mp3",
          "mime_type": "audio/mpeg",
          "size_bytes": 123456,
          "hash": "abc123..."
        }
      ],
      "preview_url": "https://storage.googleapis.com/...",
      "settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": true
      }
    }
  ],
  "has_more": false,
  "next_page_token": null
}
```

## 음성 카테고리

### Premade (사전 제작)
ElevenLabs에서 제공하는 프로페셔널 음성들

**인기 음성:**
- **Rachel**: 차분한 여성 음성, 내레이션
- **Adam**: 깊은 남성 음성, 내레이션
- **Domi**: 활기찬 여성 음성, 게임
- **Bella**: 부드러운 여성 음성, 오디오북
- **Antoni**: 따뜻한 남성 음성, 내레이션
- **Elli**: 감정적인 여성 음성, 드라마
- **Josh**: 캐주얼한 남성 음성, 팟캐스트
- **Arnold**: 강인한 남성 음성, 액션
- **Charlotte**: 세련된 여성 음성, 비즈니스
- **Matilda**: 영국 억양 여성, 오디오북

### Cloned (클론)
사용자가 Instant Voice Cloning으로 생성한 음성들

### Professional (프로페셔널 클론)
ElevenLabs 팀이 직접 처리한 고품질 클론 음성들

## 음성 레이블 (Labels)

### Gender (성별)
- `male`: 남성
- `female`: 여성

### Accent (억양)
- `american`: 미국 영어
- `british`: 영국 영어
- `australian`: 호주 영어
- `indian`: 인도 영어
- 기타 다양한 억양

### Age (나이대)
- `young`: 젊은
- `middle_aged`: 중년
- `old`: 노년

### Use Case (용도)
- `narration`: 내레이션
- `video_games`: 비디오 게임
- `audiobook`: 오디오북
- `conversational`: 대화형
- `characters`: 캐릭터
- `news`: 뉴스
- `meditation`: 명상
- `animation`: 애니메이션

### Description (설명)
- `calm`: 차분한
- `raspy`: 거친
- `soft`: 부드러운
- `deep`: 깊은
- `warm`: 따뜻한
- `strong`: 강한
- 기타 다양한 특성

## 음성 샘플 다운로드

특정 음성의 샘플을 다운로드하려면:

```bash
# 음성 정보 조회 (샘플 ID 확인)
curl -X GET "https://api.elevenlabs.io/v1/voices/21m00Tcm4TlvDq8ikWAM" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"

# 샘플 다운로드
curl -X GET "https://api.elevenlabs.io/v1/voices/21m00Tcm4TlvDq8ikWAM/samples/sample_id/audio" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  --output voice_sample.mp3
```

## 음성 선택 가이드

### 내레이션 (Narration)
- **Rachel**: 차분하고 명확한 여성 음성
- **Adam**: 권위있고 깊은 남성 음성
- **Matilda**: 세련된 영국 억양

### 오디오북 (Audiobook)
- **Bella**: 부드럽고 편안한 여성 음성
- **Antoni**: 따뜻하고 친근한 남성 음성

### 비디오 게임 (Video Games)
- **Domi**: 활기차고 에너제틱한 음성
- **Arnold**: 강인하고 액션에 적합한 음성

### 대화형 AI (Conversational)
- **Josh**: 캐주얼하고 친근한 음성
- **Charlotte**: 프로페셔널한 비즈니스 톤

### 뉴스 (News)
- **Grace**: 명료하고 전문적인 음성
- **Daniel**: 신뢰감 있는 뉴스 앵커 톤

## 커스텀 음성 생성

### Instant Voice Cloning (IVC)

```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/add" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "name=My Voice" \
  -F "description=커스텀 음성" \
  -F "files=@sample1.mp3" \
  -F "files=@sample2.mp3"
```

**요구 사항:**
- 최소 1개, 권장 3~5개의 오디오 샘플
- 각 샘플: 30초~2분
- 깨끗한 음질, 배경 소음 최소화

### Professional Voice Cloning (PVC)

고품질 음성 클론을 원하면 PVC 서비스 신청:
1. 최소 30분 분량의 고품질 오디오 준비
2. ElevenLabs 팀에 PVC 요청
3. 1~2주 내 음성 클론 완료

## 음성 관리

### 음성 편집

```bash
curl -X POST "https://api.elevenlabs.io/v1/voices/{voice_id}/edit" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "새 이름",
    "description": "새 설명"
  }'
```

### 음성 삭제

```bash
curl -X DELETE "https://api.elevenlabs.io/v1/voices/{voice_id}" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## 페이지네이션

많은 수의 음성이 있을 경우 페이지네이션 사용:

```bash
# 첫 페이지
curl -X GET "https://api.elevenlabs.io/v1/voices?page_size=30" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"

# 다음 페이지
curl -X GET "https://api.elevenlabs.io/v1/voices?page_size=30&page_token=next_token_here" \
  -H "xi-api-key: $ELEVENLABS_API_KEY"
```

## 출력 예시 스크립트

### Python

```python
import requests
import json

api_key = "your_api_key"
url = "https://api.elevenlabs.io/v1/voices"
headers = {"xi-api-key": api_key}

response = requests.get(url, headers=headers)
voices = response.json()

# 테이블 형식 출력
print(f"{'Name':<20} {'Voice ID':<25} {'Category':<12} {'Gender':<8}")
print("-" * 70)
for voice in voices["voices"]:
    name = voice["name"]
    voice_id = voice["voice_id"]
    category = voice.get("category", "N/A")
    gender = voice.get("labels", {}).get("gender", "N/A")
    print(f"{name:<20} {voice_id:<25} {category:<12} {gender:<8}")
```

### JavaScript

```javascript
const apiKey = "your_api_key";
const url = "https://api.elevenlabs.io/v1/voices";

fetch(url, {
  headers: { "xi-api-key": apiKey }
})
  .then(res => res.json())
  .then(data => {
    console.log("Available Voices:");
    data.voices.forEach(voice => {
      console.log(`- ${voice.name} (${voice.voice_id})`);
      console.log(`  Category: ${voice.category}`);
      console.log(`  Labels:`, voice.labels);
    });
  });
```

## 에러 핸들링

- **401 Unauthorized**: API 키 확인
- **429 Too Many Requests**: 요청 제한 초과, 잠시 대기
- **500 Internal Server Error**: 재시도 권장

## 참고 자료

- [Voices API 문서](https://elevenlabs.io/docs/api-reference/voices/search)
- [Voice Library](https://elevenlabs.io/voice-library)
- [Voice Cloning 가이드](https://elevenlabs.io/docs/developers/guides/cookbooks/voices/instant-voice-cloning)
- [Voice 설정 최적화](https://elevenlabs.io/docs/overview/capabilities/text-to-speech)
