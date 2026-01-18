---
name: auth-manager
description: 외부 서비스 API 키 및 인증 정보 관리 가이드
version: 1.0.0
author: Dante Labs
tags:
  - auth
  - api-key
  - credentials
  - common
---

# Auth Manager

외부 서비스 API 키 및 인증 정보를 안전하게 관리하는 방법을 안내합니다.

## Overview

DanteLabs Agentic School 플러그인들은 다양한 외부 서비스와 연동됩니다. 이 스킬은 API 키와 인증 정보를 안전하고 일관성 있게 관리하는 방법을 제공합니다.

## 지원 서비스

| 서비스 | 용도 | 환경변수 | 발급 URL |
| --- | --- | --- | --- |
| Kie.ai | 이미지/비디오 생성 | `KIEAI_API_KEY`, `KIE_AI_API_KEY` | https://kie.ai |
| OpenRouter | LLM API 라우팅 | `OPENROUTER_API_KEY` | https://openrouter.ai |
| OpenAI | GPT API | `OPENAI_API_KEY` | https://platform.openai.com |
| Anthropic | Claude API | `ANTHROPIC_API_KEY` | https://console.anthropic.com |

## 인증 관리 방법

### 방법 1: 중앙화된 인증 (권장)

`~/.claude/auth/` 디렉토리에 서비스별 환경 파일을 생성합니다.

```
~/.claude/auth/
├── kie-ai.env          # Kie.ai API 키
├── openrouter.env      # OpenRouter API 키
├── openai.env          # OpenAI API 키
└── anthropic.env       # Anthropic API 키
```

#### Kie.ai 설정

```bash
# ~/.claude/auth/kie-ai.env
KIEAI_API_KEY=your_api_key_here
KIE_AI_API_KEY=your_api_key_here
```

#### OpenRouter 설정

```bash
# ~/.claude/auth/openrouter.env
OPENROUTER_API_KEY=your_api_key_here
```

### 방법 2: 스킬 디렉토리별 .env

각 스킬 디렉토리에 개별 `.env` 파일을 생성합니다.

```bash
# ~/.claude/skills/kie-image-generator/.env
KIEAI_API_KEY=your_api_key_here

# ~/.claude/skills/kie-video-generator/.env
KIE_AI_API_KEY=your_api_key_here
```

### 방법 3: 시스템 환경변수

셸 프로파일에 직접 설정합니다.

```bash
# ~/.zshrc 또는 ~/.bashrc
export KIEAI_API_KEY=your_api_key_here
export KIE_AI_API_KEY=your_api_key_here
export OPENROUTER_API_KEY=your_api_key_here
```

## 환경 파일 로드

### 스크립트에서 로드

```python
from dotenv import load_dotenv
import os

# 중앙화된 인증 파일 로드
load_dotenv(os.path.expanduser("~/.claude/auth/kie-ai.env"))

# 또는 스킬 디렉토리의 .env 로드
load_dotenv()

api_key = os.getenv("KIEAI_API_KEY")
```

### 셸에서 로드

```bash
# 단일 서비스
source ~/.claude/auth/kie-ai.env

# 모든 인증 파일 로드
for f in ~/.claude/auth/*.env; do source "$f"; done
```

## 보안 가이드라인

### 권장 사항

1. **Git 제외**: `.env` 파일을 `.gitignore`에 추가
   ```
   # .gitignore
   .env
   *.env
   ```

2. **파일 권한**: 인증 파일은 본인만 읽을 수 있도록 설정
   ```bash
   chmod 600 ~/.claude/auth/*.env
   ```

3. **백업**: 인증 파일은 안전한 곳에 백업
   ```bash
   cp -r ~/.claude/auth ~/.claude/auth.backup
   ```

### 금지 사항

- API 키를 코드에 하드코딩하지 마세요
- API 키를 Git에 커밋하지 마세요
- API 키를 공개 채널에 공유하지 마세요
- 스크린샷에 API 키가 노출되지 않도록 주의하세요

## 크레딧/사용량 확인

### Kie.ai 크레딧 확인

```bash
# 이미지 생성 크레딧
python ~/.claude/skills/kie-image-generator/scripts/generate_image.py --credits

# 비디오 생성 크레딧
python ~/.claude/skills/kie-video-generator/scripts/generate_video.py --credits
```

### 사용량 모니터링

```bash
# 생성 후 출력 예시
💰 Credits used: 45.0 ($0.23)
   Remaining: 837.5 credits ($4.19)
```

## 문제 해결

### API 키 오류

| 오류 코드 | 원인 | 해결 방법 |
| --- | --- | --- |
| 401 | 잘못된 API 키 | API 키 재확인 |
| 402 | 크레딧 부족 | 크레딧 충전 |
| 403 | 권한 없음 | API 키 권한 확인 |

### 환경변수 로드 확인

```bash
# 환경변수 설정 확인
echo $KIEAI_API_KEY

# .env 파일 내용 확인 (주의: 터미널 기록에 남음)
cat ~/.claude/auth/kie-ai.env
```

## auth-loader 스킬 연동

`auth-loader` 스킬이 설치되어 있다면, 대화형으로 인증 정보를 관리할 수 있습니다.

```bash
# 서비스 목록 확인
/auth-loader list

# 새 서비스 추가
/auth-loader add kie-ai

# 인증 정보 검증
/auth-loader validate kie-ai
```

## 프로젝트 디렉토리 구조

모든 에이전트와 스킬은 산출물을 아래 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── assets/           # 이미지, 비디오 등 정적 에셋
│   ├── images/       # AI 생성 이미지
│   └── videos/       # AI 생성 비디오
├── reports/          # 마케팅 문서 및 분석 리포트
│   ├── brand/        # 브랜드 분석 문서
│   ├── persona/      # 페르소나 카드
│   ├── strategy/     # 전략 문서
│   └── content/      # 카피, 스크립트
├── scripts/          # 실행 스크립트
│   └── automation/   # 자동화 스크립트
└── tmp/              # 임시 파일 (작업 완료 후 삭제 가능)
```

### 디렉토리 설명

| 디렉토리 | 용도 | 예시 |
| --- | --- | --- |
| `assets/` | 이미지, 비디오 등 정적 에셋 | `product-hero.png`, `brand-video.mp4` |
| `reports/` | 마케팅 문서 및 분석 결과 | `brand-strategy-brief.md`, `persona-card.md` |
| `scripts/` | 자동화 및 유틸리티 스크립트 | `generate_thumbnails.py` |
| `tmp/` | 임시 파일 (중간 결과물) | `draft-v1.md`, `temp-image.png` |

### 디렉토리 자동 생성

에이전트가 파일 생성 시, 해당 디렉토리가 없으면 자동으로 생성합니다.

```bash
# 필요 시 디렉토리 생성
mkdir -p assets/images assets/videos
mkdir -p reports/brand reports/persona reports/strategy reports/content
mkdir -p scripts/automation
mkdir -p tmp
```

## 관련 스킬

- `kie-image-generator`: AI 이미지 생성 (Kie.ai API 사용)
- `kie-video-generator`: AI 비디오 생성 (Kie.ai API 사용)
- `auth-loader`: 대화형 인증 관리 도구
