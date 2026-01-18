# DanteLabs Agentic School

에이전틱 비즈니스 교육 및 실무를 위한 Claude Code 플러그인 마켓플레이스입니다.

## 개요

이 프로젝트는 **GTM Agents 스타일의 전략 에이전트**와 **실제 생성/분석 도구**를 통합하여, **엔드투엔드 비즈니스 자동화**를 제공합니다.

현재 **마케팅 자동화** 플러그인이 구현되어 있으며, 향후 **데이터 분석**, **AI/ML**, **일반 비즈니스** 등으로 확장될 예정입니다.

## 지원 영역

| 영역 | 상태 | 설명 |
| --- | --- | --- |
| 🎯 Marketing | ✅ 구현완료 | 브랜드 분석 → 크리에이티브 제작 |
| 📊 Data Analytics | 🔜 예정 | 데이터 수집 → 시각화 → 인사이트 |
| 🤖 AI/ML | 🔜 예정 | 모델 선택 → 학습 → 배포 |
| 💼 Business Ops | 🔜 예정 | 워크플로우 → 자동화 → 리포팅 |

## 특징

- **모듈식 플러그인 아키텍처**: 영역별 독립적인 플러그인 구성
- **전문 에이전트**: 각 단계별 전문성을 갖춘 AI 에이전트
- **실행 커맨드**: 직접 실행 가능한 작업 커맨드
- **전문 스킬**: 도메인 지식 및 프레임워크
- **AI 생성 도구 내장**: kie-image-generator, kie-video-generator (common 플러그인)

## 설치

### NPX로 빠른 설치 (권장)

```bash
# 전체 플러그인 설치
npx dantelabs-agentic-school install

# 특정 플러그인만 설치
npx dantelabs-agentic-school install brand-analytics

# 설치 경로 지정
npx dantelabs-agentic-school install --path ./my-project

# 플러그인 목록 보기
npx dantelabs-agentic-school list

# 플러그인 상세 정보
npx dantelabs-agentic-school info content-creation

# 플러그인 삭제
npx dantelabs-agentic-school uninstall brand-analytics
```

### CLI 옵션

| 옵션 | 설명 |
| --- | --- |
| `--path, -p` | 설치 경로 (기본: 현재 디렉토리) |
| `--force, -f` | 기존 파일 덮어쓰기 |
| `--no-common` | common 유틸리티 제외 |
| `--dry-run` | 미리보기 (실제 설치 안함) |
| `--json` | JSON 형식 출력 (list, info) |
| `-v, --verbose` | 상세 정보 표시 |
| `-l, --lang` | 언어 설정 (en, ko) - 기본: en |

### Claude Code에서 플러그인 사용

#### 방법 1: 프로젝트별 설치 (권장)

NPX로 설치하면 프로젝트의 `.claude/` 폴더에 플러그인이 설치됩니다.

```bash
# 프로젝트 폴더에서 실행
cd my-project
npx dantelabs-agentic-school install

# Claude Code 실행 - 자동으로 .claude/ 폴더 인식
claude
```

설치 후 구조:

```text
my-project/
├── .claude/
│   ├── agents/           # 에이전트 정의
│   │   └── brand-analytics/
│   │       └── brand-strategist.md
│   ├── commands/         # 슬래시 명령어
│   │   └── brand-analytics/
│   │       └── analyze-brand.md
│   └── skills/           # 스킬 (스크립트 포함)
│       ├── brand-positioning/
│       └── pptx/
└── ...
```

#### 방법 2: 플러그인 디렉토리 직접 지정

레포지토리를 클론하여 플러그인 디렉토리로 사용:

```bash
# 레포지토리 클론
git clone https://github.com/dandacompany/dantelabs-agentic-school.git

# Claude Code 실행 시 플러그인 디렉토리 지정
claude --plugin-dir ./dantelabs-agentic-school
```

#### 방법 3: 전역 설치

홈 디렉토리의 `.claude/`에 설치하여 모든 프로젝트에서 사용:

```bash
# 홈 디렉토리에 설치
npx dantelabs-agentic-school install --path ~

# 이후 모든 프로젝트에서 플러그인 사용 가능
claude
```

#### 방법 4: Claude Code 세션 내 마켓플레이스 설치

Claude Code 실행 중 슬래시 명령어로 직접 마켓플레이스를 등록하고 플러그인을 설치할 수 있습니다.

**1. 마켓플레이스 추가**

```bash
# GitHub 저장소로 추가
/plugin marketplace add dandacompany/dantelabs-agentic-school
```

**2. 플러그인 설치**

```bash
# 특정 플러그인 설치
/plugin install brand-analytics@dantelabs-agentic-school

# 또는 /plugin 실행 후 Discover 탭에서 검색하여 설치
/plugin
```

**3. 설치된 플러그인 확인**

```bash
# 플러그인 목록 확인
/plugin
```

> **Tip**: `/plugin` 명령어 실행 후 **Discover** 탭에서 마켓플레이스의 모든 플러그인을 검색하고 설치할 수 있습니다.

### 플러그인 사용 확인

Claude Code 실행 후 `/help` 명령어로 설치된 커맨드를 확인할 수 있습니다:

```bash
# Claude Code 내에서
/help

# 설치된 커맨드 예시
/analyze-brand --brand-doc ./brand-brief.md
/create-segments
/build-persona --segment "워라밸 직장인"
```

---

## 🔧 Common Plugins

여러 플러그인에서 공통으로 사용하는 유틸리티 스킬을 제공합니다.

## common

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Skill | auth-manager | API 키 및 인증 정보 관리 가이드 |
| Skill | pptx | 마케팅 프레젠테이션 제작 도구 |
| Skill | pdf | 마케팅 PDF 문서 제작 및 처리 도구 |
| Skill | docx | 마케팅 Word 문서 제작 도구 |
| Skill | kie-image-generator | Kie.ai 기반 AI 이미지 생성 |
| Skill | kie-video-generator | Kie.ai 기반 AI 비디오 생성 |

### auth-manager 스킬

외부 서비스 API 키를 안전하게 관리하는 방법을 안내합니다.

#### 지원 서비스

| 서비스 | 환경변수 | 용도 |
| --- | --- | --- |
| Kie.ai | `KIEAI_API_KEY`, `KIE_AI_API_KEY` | 이미지/비디오 생성 |
| OpenRouter | `OPENROUTER_API_KEY` | LLM API 라우팅 |
| OpenAI | `OPENAI_API_KEY` | GPT API |

#### 인증 설정 (권장)

```bash
# ~/.claude/auth/kie-ai.env 파일 생성
KIEAI_API_KEY=your_api_key_here
KIE_AI_API_KEY=your_api_key_here
```

#### 크레딧 확인

```bash
# 이미지 생성 크레딧
python ~/.claude/skills/kie-image-generator/scripts/generate_image.py --credits

# 비디오 생성 크레딧
python ~/.claude/skills/kie-video-generator/scripts/generate_video.py --credits
```

### 문서 제작 스킬

마케팅 문서, 프레젠테이션, PDF를 생성하고 편집하는 도구입니다.

#### pptx 스킬

마케팅 프레젠테이션 제작을 위한 PowerPoint 생성/편집 도구입니다.

| 기능 | 설명 |
| --- | --- |
| 새 프레젠테이션 생성 | HTML → PPTX 변환 |
| 기존 파일 편집 | OOXML 직접 편집 |
| 템플릿 기반 생성 | 기업 템플릿 활용 |

**지원 프레젠테이션 유형**:

- 캠페인 제안서
- 브랜드 소개서
- 분석 리포트

#### pdf 스킬

마케팅 PDF 문서 제작 및 처리를 위한 종합 도구입니다.

| 기능 | 설명 |
| --- | --- |
| 텍스트/테이블 추출 | PDF → 텍스트/CSV |
| PDF 병합/분할 | 캠페인 패키지 생성 |
| PDF 생성 | Markdown/HTML → PDF |

**지원 문서 유형**:

- 캠페인 리포트
- 브랜드 브로슈어
- 경쟁사 분석 리포트

#### docx 스킬

마케팅 문서 제작을 위한 Word 문서 생성/편집 도구입니다.

| 기능 | 설명 |
| --- | --- |
| 새 문서 생성 | Markdown → DOCX |
| 기존 문서 편집 | OOXML 편집, 템플릿 변수 치환 |
| 변경 추적 | Redlining 지원 |

**지원 문서 유형**:

- 마케팅 기획서
- 브랜드 가이드라인
- 캠페인 브리프

---

## 🎯 Marketing Plugins

브랜드 분석부터 크리에이티브 제작까지 6단계 마케팅 파이프라인을 제공합니다.

## 컴포넌트 현황

| 항목 | 개수 |
| --- | --- |
| 플러그인 | 9개 (common 1 + marketing 8) |
| 에이전트 | 15개 |
| 커맨드 | 10개 |
| 스킬 | 19개 (common 6 + marketing 13) |

## 플러그인 목록

### 1. brand-analytics

브랜드 소개서를 분석하여 전략 브리프를 생성합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | brand-strategist | 브랜드 전략 분석 |
| Agent | competitive-analyst | 경쟁사 분석 |
| Command | /analyze-brand | 브랜드 분석 실행 |
| Skill | brand-positioning | 포지셔닝 프레임워크 |

### 2. customer-segmentation

데이터 기반 고객 세그먼트를 설계합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | segmentation-architect | 세그먼트 설계 |
| Agent | data-analyst | 데이터 분석 |
| Command | /create-segments | 세그먼트 생성 |
| Skill | segmentation-framework | 세그먼테이션 방법론 |
| Skill | activation-map | 세그먼트 활성화 맵 |

### 3. persona-builder

타겟 세그먼트의 상세 페르소나를 생성합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | persona-architect | 페르소나 설계 |
| Agent | customer-insights-partner | 고객 인사이트 |
| Command | /build-persona | 페르소나 카드 생성 |
| Skill | persona-framework | 페르소나 작성 가이드 |

### 4. social-strategy

페르소나 기반 채널 전략을 수립합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | social-strategy-director | 채널 전략 총괄 |
| Agent | channel-analyst | 채널별 분석 |
| Command | /plan-channels | 채널 전략 수립 |
| Skill | channel-roadmap | 채널 로드맵 |
| Skill | content-pillars | 콘텐츠 필러 설계 |

### 5. content-creation

채널별 홍보 카피와 스크립트를 생성합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | copy-strategist | 카피 전략 |
| Agent | conversion-copywriter | 전환 카피 작성 |
| Agent | script-writer | 영상 스크립트 |
| Command | /generate-copy | 카피 생성 |
| Command | /write-script | 스크립트 작성 |
| Skill | message-architecture | 메시지 구조 |
| Skill | hook-formulas | 훅 작성 공식 |

### 6. creative-production

실제 이미지와 비디오를 생성합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | creative-director | 크리에이티브 총괄 |
| Agent | production-coordinator | 제작 조율 |
| Command | /create-image | AI 이미지 생성 |
| Command | /create-video | AI 비디오 생성 |
| Skill | image-prompt-guide | 이미지 프롬프트 가이드 |
| Skill | video-production | 비디오 제작 가이드 |

> **Note**: 이미지/비디오 생성을 위한 `kie-image-generator`, `kie-video-generator` 스킬은 common 플러그인에 포함되어 있습니다.

### 7. campaign-orchestration

전체 마케팅 파이프라인을 통합 실행합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Agent | campaign-director | 캠페인 총괄 |
| Agent | workflow-coordinator | 워크플로우 조율 |
| Command | /run-full-pipeline | 전체 파이프라인 실행 |
| Command | /run-phase | 특정 단계 실행 |
| Skill | pipeline-framework | 파이프라인 프레임워크 |

### 8. market-research

시장 분석 리포트 및 데이터 시각화를 생성합니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Skill | analysis-reports | 시장 분석 리포트 템플릿 |
| Skill | diagram-generator | 데이터 시각화 다이어그램 생성 |

## 사용 예시

### 전체 캠페인 실행

```bash
/run-full-pipeline --brand-doc "./brand-brief.md"
```

### 단계별 실행

```bash
# 1. 브랜드 분석
/analyze-brand --brand-doc "./brand-brief.md"

# 2. 세그먼트 생성
/create-segments --brand-doc "./brand-strategy-brief.md"

# 3. 페르소나 생성
/build-persona --segment "워라밸 직장인"

# 4. 채널 전략
/plan-channels --persona "김지현"

# 5. 카피 생성
/generate-copy --channel instagram --persona "김지현"

# 6. 이미지/비디오 생성
/create-image --concept "커피 라이프스타일" --type lifestyle
/create-video --concept "드립백 추출" --duration 15s
```

## 파이프라인 구조

```text
Brand Document
       ↓
┌─────────────────┐
│ Phase 1: Brand  │ → Brand Strategy Brief
│    Analysis     │
└─────────────────┘
       ↓
┌─────────────────┐
│ Phase 2: Seg-   │ → Segment Profiles
│  mentation      │
└─────────────────┘
       ↓
┌─────────────────┐
│ Phase 3:        │ → Persona Cards
│  Persona        │
└─────────────────┘
       ↓
┌─────────────────┐
│ Phase 4: Channel│ → Channel Plan, Calendar
│   Strategy      │
└─────────────────┘
       ↓
┌─────────────────┐
│ Phase 5: Content│ → Copy, Scripts
│   Creation      │
└─────────────────┘
       ↓
┌─────────────────┐
│ Phase 6: Creative│ → Images, Videos
│   Production    │
└─────────────────┘
       ↓
Complete Campaign Assets
```

## 에이전트 트리거 예시

| 요청 | 활성화 에이전트 |
| --- | --- |
| "브랜드 분석해줘" | brand-strategist |
| "고객 세그먼트 나눠줘" | segmentation-architect |
| "페르소나 만들어줘" | persona-architect |
| "SNS 전략 수립해줘" | social-strategy-director |
| "인스타그램 카피 써줘" | conversion-copywriter |
| "영상 스크립트 작성해줘" | script-writer |
| "제품 이미지 만들어줘" | creative-director |

---

## 🔜 Coming Soon

## 📊 Data Analytics Plugins (예정)

데이터 수집부터 시각화, 인사이트 도출까지의 파이프라인

- data-collection: 데이터 수집 및 전처리
- exploratory-analysis: 탐색적 데이터 분석
- visualization: 대시보드 및 시각화
- insight-generation: 인사이트 도출

## 🤖 AI/ML Plugins (예정)

AI 모델 선택부터 학습, 배포까지의 파이프라인

- model-selection: 모델 선택 및 평가
- training-pipeline: 학습 파이프라인
- deployment: 모델 배포

## 💼 Business Ops Plugins (예정)

비즈니스 워크플로우 자동화

- workflow-automation: 워크플로우 자동화
- reporting: 리포팅 및 문서 생성
- integration: 외부 시스템 연동

---

## 요구사항

- Claude Code CLI
- Node.js 18.0.0 이상 (NPX CLI용)

> 이미지/비디오 생성 스킬(`kie-image-generator`, `kie-video-generator`)은 common 플러그인에 포함되어 있습니다.
> API 키 설정은 [auth-manager 스킬](#auth-manager-스킬) 참조

## 라이선스

MIT License

## 제작

Dante Labs

- Website: [dante-datalab.com](https://dante-datalab.com)
- YouTube: [@dante-labs](https://youtube.com/@dante-labs)
- Email: <datapod.k@gmail.com>
- Discord: [Dante Labs Community](https://discord.com/invite/rXyy5e9ujs)

---

☕ 커피 한 잔 후원: [buymeacoffee.com/dante.labs](https://buymeacoffee.com/dante.labs)
