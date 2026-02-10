# DanteLabs Agentic School

에이전틱 비즈니스 교육 및 실무를 위한 Claude Code 플러그인 마켓플레이스입니다.

## 개요

이 프로젝트는 **GTM Agents 스타일의 전략 에이전트**와 **실제 생성/분석 도구**를 통합하여, **엔드투엔드 비즈니스 자동화**를 제공합니다.

현재 **마케팅 자동화**(8개), **데이터 사이언스**(9개), **GCP 클라우드**(1개), **미디어 제작**(1개) 플러그인이 구현되어 있으며, 향후 **일반 비즈니스** 등으로 확장될 예정입니다.

## 지원 영역

| 영역 | 상태 | 설명 | 플러그인 수 |
| --- | --- | --- | --- |
| 🎯 Marketing | ✅ 구현완료 | 브랜드 분석 → 크리에이티브 제작 | 8개 |
| 📊 Data Science | ✅ 구현완료 | 데이터 분석 → 모델 학습 → 배포 | 9개 |
| ☁️ GCP | ✅ 구현완료 | GCP VM 배포 가이드 및 자동화 | 1개 |
| 🎵 Media | ✅ 구현완료 | AI 음성 생성, 사운드 이펙트, 비디오 편집 | 1개 |
| 💼 Business Ops | 🔜 예정 | 워크플로우 → 자동화 → 리포팅 | - |

## 특징

- **모듈식 플러그인 아키텍처**: 영역별 독립적인 플러그인 구성
- **전문 에이전트**: 각 단계별 전문성을 갖춘 AI 에이전트
- **실행 커맨드**: 직접 실행 가능한 작업 커맨드
- **전문 스킬**: 도메인 지식 및 프레임워크
- **AI 생성 도구 내장**: kie-image-generator, kie-video-generator (common 플러그인)
- **완전 자동화 파이프라인**: 엔드투엔드 자동화 (마케팅 6단계, 데이터 사이언스 10단계)

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
| `--target, -t` | 타겟 플랫폼 (claude, gemini, antigravity, codex, opencode, agents) |
| `--force, -f` | 기존 파일 덮어쓰기 |
| `--no-common` | common 유틸리티 제외 |
| `--dry-run` | 미리보기 (실제 설치 안함) |
| `--json` | JSON 형식 출력 (list, info) |
| `-v, --verbose` | 상세 정보 표시 |
| `-l, --lang` | 언어 설정 (en, ko) - 기본: en |

### 멀티플랫폼 설치

`--target` 옵션으로 다양한 AI 코딩 도구에 플러그인을 설치할 수 있습니다.

```bash
# Claude Code (기본값, --target 생략 가능)
npx dantelabs-agentic-school install gcp-openclaw

# Gemini CLI
npx dantelabs-agentic-school install gcp-openclaw --target gemini

# Google Antigravity IDE
npx dantelabs-agentic-school install gcp-openclaw --target antigravity

# OpenAI Codex CLI
npx dantelabs-agentic-school install gcp-openclaw --target codex

# OpenCode
npx dantelabs-agentic-school install gcp-openclaw --target opencode
```

#### 플랫폼별 호환성

| 플랫폼 | 디렉토리 | Skills | Agents | Commands |
| --- | --- | --- | --- | --- |
| `claude` (기본) | `.claude/` | ✅ | ✅ | ✅ |
| `gemini` | `.gemini/` | ✅ | ✅ | ❌ skip |
| `antigravity` | `.agent/` | ✅ | ❌ skip | ❌ skip |
| `codex` | `.agents/` | ✅ | ❌ skip | ❌ skip |
| `opencode` | `.opencode/` | ✅ | ✅ | ✅ |
| `agents` | `.agents/` | ✅ | ❌ skip | ❌ skip |

> **Note**: 모든 플러그인의 Skills는 모든 플랫폼에서 설치됩니다. Agents/Commands는 해당 플랫폼이 지원하지 않으면 자동으로 skip됩니다.

### 샘플 다운로드

학습용 샘플 파일을 다운로드하여 마케팅 자동화 파이프라인을 직접 체험해볼 수 있습니다.

```bash
# 사용 가능한 샘플 목록 보기
npx dantelabs-agentic-school sample --list

# 특정 샘플 다운로드
npx dantelabs-agentic-school sample marketing

# 전체 샘플 다운로드
npx dantelabs-agentic-school sample --all

# 다운로드 경로 지정
npx dantelabs-agentic-school sample marketing --path ./my-project

# 기존 파일 덮어쓰기
npx dantelabs-agentic-school sample marketing --force
```

샘플을 다운로드하면 `samples/` 폴더에 학습 자료가 저장됩니다:

```text
samples/
├── marketing/
│   ├── dante-coffee-agentic-marketing-scenario.md  # 마케팅 시나리오 가이드
│   └── dante-coffee-brand-brief.md                 # 브랜드 브리프 예시
└── datascience/
    └── creditcard.csv                              # 신용카드 사기 탐지 데이터셋
```

> **Tip**: 다운로드한 브랜드 브리프를 사용하여 `/analyze-brand --brand-doc ./samples/marketing/dante-coffee-brand-brief.md` 명령어로 전체 파이프라인을 실행해볼 수 있습니다.

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

# 설치된 커맨드 예시 (마케팅)
/analyze-brand --brand-doc ./brand-brief.md
/create-segments
/build-persona --segment "워라밸 직장인"

# 설치된 커맨드 예시 (데이터 사이언스)
/profile-data --data-path "./data/creditcard.csv"
/train-model --algorithm xgboost
/deploy-model --model-path "./models/model.pkl"
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
| 플러그인 | 20개 (common 1 + marketing 8 + data-science 9 + gcp 1 + media 1) |
| 에이전트 | 15개 |
| 커맨드 | 23개 |
| 스킬 | 31개 (common 6 + marketing 13 + data-science 9 + gcp 1 + media 2) |

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

---

## 📊 Data Science Plugins ⭐ NEW

데이터 분석부터 모델 학습, 배포까지 10단계 자동화 파이프라인을 제공합니다.

### 기본 파이프라인 (4개)

| # | 플러그인 | 설명 | 주요 기능 |
| --- | --- | --- | --- |
| 1 | **data-profiling** | 데이터 품질 검증 및 EDA | ydata-profiling, A4 전략 레포트 |
| 2 | **feature-engineering** | 특성 변환 및 전처리 | RobustScaler, 시간 특성, 파이프라인 저장 |
| 3 | **imbalance-handling** | 클래스 불균형 처리 | SMOTE, ADASYN, BorderlineSMOTE |
| 4 | **model-selection** | 모델 학습 및 평가 | XGBoost, LightGBM, Random Forest |

### 고급 파이프라인 (5개) ⭐

| # | 플러그인 | 설명 | 주요 기능 |
| --- | --- | --- | --- |
| 5 | **hyperparameter-tuning** | 자동 하이퍼파라미터 최적화 | Optuna TPE, Median Pruner, +2-4% 성능 향상 |
| 6 | **model-evaluation** | 모델 성능 심층 분석 | Feature Importance, Learning Curves, CV |
| 7 | **shap-analysis** | 예측 설명 및 해석 | SHAP Values, Waterfall Plot, Force Plot |
| 8 | **model-monitoring** | 프로덕션 모델 추적 | Data Drift (PSI, KS), Alert System |
| 9 | **model-deployment** | API 배포 | FastAPI, Swagger UI, Docker |

### 파이프라인 구조

```text
Raw Data
    ↓
1️⃣  Data Profiling (HTML Report)
    ↓
2️⃣  EDA Analysis (A4 Strategy Report)
    ↓
3️⃣  Feature Engineering (Scaling, Time Features)
    ↓
4️⃣  Imbalance Handling (SMOTE)
    ↓
5️⃣  Model Training (XGBoost, LightGBM, RF)
    ↓
6️⃣  Hyperparameter Tuning (Optuna, 50-100 trials) ⭐
    ↓
7️⃣  Model Evaluation (Feature Importance, Curves) ⭐
    ↓
8️⃣  SHAP Analysis (Prediction Explanation) ⭐
    ↓
9️⃣  Model Monitoring (Drift Detection, Alerts) ⭐
    ↓
🔟 Model Deployment (FastAPI, Docker) ⭐
    ↓
Production API Server
```

### 사용 예시

#### 프로젝트 초기화

```bash
# 새 데이터 사이언스 프로젝트 생성
python scripts/init_project.py --name my-ml-project

# 데이터 복사
cp /path/to/data.csv projects/my-ml-project/data/raw/
```

#### 기본 파이프라인 (1-4단계)

```bash
# 1. 데이터 프로파일링
/profile-data --data-path "projects/my-ml-project/data/raw/data.csv" --target-column "target"

# 2. EDA 분석
/analyze-profile --data-path "projects/my-ml-project/data/raw/data.csv" --target-column "target"

# 3. 특성 엔지니어링
/engineer-features --data-path "projects/my-ml-project/data/raw/data.csv" --target-column "target"

# 4. 불균형 처리
/balance-data \
  --X-path "projects/my-ml-project/data/processed/data_processed_X.csv" \
  --y-path "projects/my-ml-project/data/processed/data_processed_y.csv" \
  --method smote
```

#### 고급 파이프라인 (5-10단계) ⭐

```bash
# 5. 모델 학습 (베이스라인)
/train-model \
  --X-train-path "projects/my-ml-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-ml-project/data/processed/y_train_balanced.csv" \
  --X-test-path "projects/my-ml-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-ml-project/data/processed/y_test.csv" \
  --algorithm xgboost

# 6. 하이퍼파라미터 튜닝
/tune-hyperparameters \
  --X-train-path "projects/my-ml-project/data/processed/X_train_balanced.csv" \
  --y-train-path "projects/my-ml-project/data/processed/y_train_balanced.csv" \
  --n-trials 50

# 7. 모델 평가
/evaluate-model \
  --model-path "projects/my-ml-project/outputs/models/xgboost_tuned_model.pkl" \
  --X-test-path "projects/my-ml-project/data/processed/X_test.csv" \
  --y-test-path "projects/my-ml-project/data/processed/y_test.csv"

# 8. SHAP 분석
/analyze-shap \
  --model-path "projects/my-ml-project/outputs/models/xgboost_tuned_model.pkl" \
  --X-test-path "projects/my-ml-project/data/processed/X_test.csv"

# 9. 모델 모니터링
/monitor-model \
  --model-path "projects/my-ml-project/outputs/models/xgboost_tuned_model.pkl" \
  --reference-data "projects/my-ml-project/data/processed/X_train_balanced.csv" \
  --current-data "projects/my-ml-project/data/production/prod_data.csv"

# 10. API 배포
/deploy-model \
  --model-path "projects/my-ml-project/outputs/models/xgboost_tuned_model.pkl" \
  --X-sample-path "projects/my-ml-project/data/processed/X_train_balanced.csv"
```

### 성능 개선 과정

**신용카드 사기 탐지 예시** (284,807건, 1:578 불균형)

| 단계 | F1-Score | PR-AUC | 개선 |
| --- | --- | --- | --- |
| 베이스라인 (XGBoost) | 0.83 | 0.87 | - |
| + 하이퍼파라미터 튜닝 | 0.86 | 0.89 | +3.6% |
| + Feature Selection | 0.87 | 0.90 | +4.8% |
| + Threshold 최적화 | 0.88 | 0.91 | +6.0% |

### 프로젝트 구조

```text
projects/{project-name}/
├── data/
│   ├── raw/              # 원본 데이터
│   ├── processed/        # 전처리 데이터
│   └── production/       # 프로덕션 데이터 (모니터링용)
├── outputs/
│   ├── models/           # 학습/튜닝 모델
│   ├── reports/          # HTML/Markdown 리포트
│   ├── evaluations/      # 평가 시각화
│   ├── shap/            # SHAP 분석
│   └── monitoring/       # Drift 리포트
├── deployment/          # FastAPI 서버
│   ├── app.py
│   ├── Dockerfile
│   └── docker-compose.yml
└── notebooks/           # Jupyter 노트북
```

### 활용 시나리오

| 시나리오 | 소요 시간 | 예상 성능 | 산출물 |
| --- | --- | --- | --- |
| **신속 프로토타입** | 3시간 | F1 0.80-0.85 | 베이스라인 모델 |
| **프로덕션 모델** | 3일 | F1 0.85-0.90 | 튜닝 모델 + 평가 |
| **엔터프라이즈** | 1주 | F1 0.90+ | API + 모니터링 + 문서 |

### 상세 가이드

- [기본 파이프라인 가이드](./DATA_SCIENCE_PIPELINE.md)
- [고급 파이프라인 가이드](./ADVANCED_DATA_SCIENCE_PIPELINE.md)
- [프로젝트 구조 가이드](./PROJECTS.md)

---

## ☁️ GCP Plugins

Google Cloud Platform 배포 가이드 및 자동화 도구를 제공합니다.

### gcp-openclaw

GCP VM 인스턴스에 OpenClaw를 배포하는 포괄적인 가이드입니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Command | /deploy-openclaw | GCP VM 생성 및 OpenClaw 배포 가이드 실행 |
| Skill | gcp-openclaw | GCP 배포 전체 워크플로 (VM, SSH, OpenClaw, GOG CLI) |

#### 사용 예시

```bash
# 기본 설정으로 배포 가이드 실행
/deploy-openclaw

# 서울 리전에 커스텀 설정으로 배포
/deploy-openclaw --zone asia-northeast3-a --machine-type e2-medium --instance-name openclaw-kr
```

#### 배포 파이프라인

```text
1. GCP 인증 및 프로젝트 설정
    ↓
2. VM 인스턴스 생성 (Ubuntu 22.04 LTS)
    ↓
3. SSH 구성 및 접속
    ↓
4. 의존성 설치 (Node.js v22+, Go 1.23+)
    ↓
5. OpenClaw 설치 및 초기화
    ↓
6. GOG CLI 설치 및 인증
    ↓
7. SSH 터널링으로 대시보드 접속
```

---

## 🎵 Media Plugins

AI 기반 오디오 제작 및 비디오 편집 도구를 제공합니다.

### media-fx

ElevenLabs AI API를 통한 고품질 음성 생성, 사운드 이펙트, AI 비디오 편집 도구입니다.

| 컴포넌트 | 이름 | 설명 |
| --- | --- | --- |
| Command | /generate-speech | 텍스트를 자연스러운 음성으로 변환 (29개 언어) |
| Command | /generate-sound-effect | 텍스트 설명으로 사운드 이펙트 생성 |
| Command | /list-voices | 사용 가능한 음성 목록 조회 및 필터링 |
| Skill | elevenlabs-api | ElevenLabs API 전체 가이드 (TTS, Sound Effects, Voice Cloning) |
| Skill | video-editor | Whisper STT + ElevenLabs TTS 기반 자동 비디오 편집 |

#### 주요 기능

**1. Text-to-Speech (TTS)**
- 29개 이상 언어 지원 (한국어, 영어, 일본어 등)
- 음성 설정 커스터마이징 (stability, similarity, style, speed)
- 다양한 출력 포맷 (MP3, WAV, PCM, Opus)
- 스트리밍 TTS (WebSocket)

**2. Sound Effects**
- 텍스트 설명으로 사운드 이펙트 생성
- 0.5~30초 길이 조절 가능
- 루프 사운드 생성 지원
- 게임, 영화, Foley 사운드 등 다양한 용도

**3. Voice Management**
- 사용 가능한 음성 목록 조회
- 필터링 (성별, 억양, 나이, 용도)
- 음성 샘플 다운로드
- 커스텀 음성 클론 (Instant & Professional)

**4. Video Editor**
- Whisper STT로 무음/재촬영/쓰레기 구간 자동 감지 및 제거
- ElevenLabs TTS로 나레이션 자동 교체
- 한국어 텍스트 분석 기반 동적 무음 트리밍
- 스크린 녹화, 강의 영상, 나레이션 영상에 최적화

#### 사용 예시

```bash
# 플러그인 설치
npx dantelabs-agentic-school install media-fx

# 텍스트를 음성으로 변환
/generate-speech --text "안녕하세요, ElevenLabs 음성입니다." --output hello.mp3

# 사운드 이펙트 생성
/generate-sound-effect --description "빗소리와 천둥소리" --duration 10.0 --output rain.mp3

# 음성 목록 조회
/list-voices --gender female --accent american

# 비디오 편집 (Whisper 분석 → 편집 → TTS 나레이션 → 무음 트리밍)
python ~/.claude/skills/video-editor/scripts/video_editor.py analyze recording.mp4
python ~/.claude/skills/video-editor/scripts/video_editor.py execute recording.mp4 recording_edit_plan.json
```

#### 인증 설정

`~/.claude/auth/elevenlabs.env` 파일 생성:

```bash
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_BASE_URL=https://api.elevenlabs.io/v1/
```

#### 활용 시나리오

| 시나리오 | 용도 | 예시 |
| --- | --- | --- |
| **팟캐스트/오디오북** | 내레이션 생성 | 긴 텍스트를 자연스러운 음성으로 변환 |
| **게임 개발** | 효과음/대사 | 캐릭터 대사, 배경음, 효과음 생성 |
| **영상 제작** | 보이스오버/편집 | 다국어 보이스오버, 자동 비디오 편집 |
| **마케팅** | 광고 음성 | 제품 홍보 음성, 브랜드 음성 클론 |
| **강의 녹화** | 후처리 | 무음/재촬영 제거, TTS 나레이션 교체 |

---

## 🔜 Coming Soon

### 💼 Business Ops Plugins (예정)

비즈니스 워크플로우 자동화

- workflow-automation: 워크플로우 자동화
- reporting: 리포팅 및 문서 생성
- integration: 외부 시스템 연동

---

## 요구사항

- Claude Code CLI
- Node.js 18.0.0 이상 (NPX CLI용)
- Python 3.8+ (데이터 사이언스 플러그인)

> 이미지/비디오 생성 스킬(`kie-image-generator`, `kie-video-generator`)은 common 플러그인에 포함되어 있습니다.
> API 키 설정은 [auth-manager 스킬](#auth-manager-스킬) 참조

## 라이선스

MIT License

## 제작

Dante Labs

- Website: [dante-labs.com](https://dante-labs.com)
- YouTube: [@dante-labs](https://youtube.com/@dante-labs)
- Email: <datapod.k@gmail.com>
- Discord: [Dante Labs Community](https://discord.com/invite/rXyy5e9ujs)

---

☕ 커피 한 잔 후원: [buymeacoffee.com/dante.labs](https://buymeacoffee.com/dante.labs)
