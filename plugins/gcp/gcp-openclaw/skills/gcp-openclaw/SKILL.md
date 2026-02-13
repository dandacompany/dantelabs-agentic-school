---
name: gcp-openclaw
description: VM 설정, SSH 구성, OpenClaw 설치 및 GOG CLI 설정을 포함하여 Google Cloud Platform에 OpenClaw를 배포하는 포괄적인 가이드입니다.
---

# GCP OpenClaw 배포 가이드

이 스킬은 Google Cloud Platform (GCP) VM 인스턴스에 OpenClaw를 배포하기 위한 단계별 워크플로를 제공합니다. 초기 GCP 설정부터 OpenClaw 및 GOG CLI 구성까지 모든 과정을 다룹니다.

## 0. 스킬 다운로드

이 스킬을 프로젝트 루트에 다운로드합니다.

```bash
npx dlabs install gcp-openclaw --target agents
```

> 다른 플랫폼 타겟: `--target claude`, `--target gemini`, `--target antigravity` 등

## 1. 전제 조건 (로컬 머신)

로컬 컴퓨터에 Google Cloud CLI (`gcloud`)가 설치되어 있고 인증이 완료되었는지 확인하십시오.

### 1.1 Google Cloud CLI 설치 확인

먼저 `gcloud`가 설치되어 있는지 확인합니다.

```bash
gcloud version
```

명령어가 정상 실행되면 **1.3 단계로 건너뜁니다**. `command not found` 에러가 발생하면 아래 설치 과정을 진행합니다.

### 1.2 Google Cloud CLI 설치

#### macOS

```bash
# Homebrew로 설치 (권장)
brew install --cask google-cloud-sdk

# 또는 공식 스크립트로 설치
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### Linux (Debian/Ubuntu)

```bash
# 패키지 소스 추가
sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

# 설치
sudo apt-get update && sudo apt-get install -y google-cloud-cli
```

#### Linux (RHEL/CentOS/Fedora)

```bash
# 패키지 소스 추가
sudo tee /etc/yum.repos.d/google-cloud-sdk.repo << 'EOF'
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

# 설치
sudo dnf install -y google-cloud-cli
```

#### Windows

```powershell
# winget으로 설치
winget install Google.CloudSDK

# 또는 공식 인스톨러 다운로드
# https://cloud.google.com/sdk/docs/install#windows
```

설치 후 `gcloud version`으로 정상 설치를 확인합니다.

### 1.3 Google Cloud 인증

```bash
gcloud auth login --no-launch-browser
```
출력된 URL을 브라우저에서 열어 인증하고, 확인 코드를 터미널에 붙여넣습니다.

### 1.4 프로젝트 및 결제 설정

https://console.cloud.google.com 에 접속하여 새 프로젝트를 생성합니다.

```bash
# 프로젝트 ID 설정
gcloud config set project [YOUR_PROJECT_ID]

# 필요한 서비스 활성화
gcloud services enable compute.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

> **Tip**: `gcloud config configurations`를 활용하면 프로젝트/계정별로 여러 설정 프로필을 관리할 수 있습니다.
> ```bash
> # 새 설정 프로필 생성
> gcloud config configurations create openclaw-dev
> gcloud config set project my-openclaw-project
> gcloud config set compute/zone asia-northeast3-a
>
> # 프로필 전환
> gcloud config configurations activate openclaw-dev
> ```

## 2. VM 인스턴스 생성

충분한 리소스를 가진 VM 인스턴스를 생성합니다.
**권장 사양:** `e2-small` (2 vCPU, 2GB RAM) 또는 `e2-medium` (2 vCPU, 4GB RAM).
**운영체제:** Ubuntu 22.04 LTS

```bash
gcloud compute instances create openclaw-instance \
    --zone=us-central1-a \
    --machine-type=e2-small \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=25GB \
    --boot-disk-type=pd-balanced \
    --labels=env=dev,app=openclaw
```

## 3. SSH 구성

VM에 쉽게 접속할 수 있도록 SSH를 구성합니다.

### 3.1 키 생성 및 접속
```bash
# 키 자동 생성 및 접속
gcloud compute ssh openclaw-instance --zone=us-central1-a
```

### 3.2 표준 SSH 별칭 (선택 사항이지만 권장됨)
로컬 `~/.ssh/config` 파일에 다음 내용을 추가합니다:
```
Host openclaw
    HostName [EXTERNAL_IP]
    User [YOUR_USERNAME]
    IdentityFile ~/.ssh/google_compute_engine
```

## 4. 의존성 및 도구 설치 (원격 서버)

서버에 SSH로 접속하여 필요한 도구를 설치합니다.

```bash
# 서버 접속
gcloud compute ssh openclaw-instance --zone=us-central1-a

# 업데이트 및 기본 도구 설치
sudo apt-get update
sudo apt-get install -y git curl make build-essential
```

### 4.1 Node.js 설치 (v22 이상)
OpenClaw는 Node.js v22 이상이 필요합니다.
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 4.2 Go 설치 (최신 버전 필수)
GOG CLI 빌드를 위해서는 **반드시 최신 버전의 Go (1.23 이상)**가 필요합니다. 운영체제 기본 패키지(예: `apt install golang`)는 버전이 낮아 빌드에 실패할 수 있으므로, 아래와 같이 수동 설치를 권장합니다.
```bash
wget https://go.dev/dl/go1.23.6.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.23.6.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

## 5. OpenClaw 설치

OpenClaw를 전역으로 설치합니다.

```bash
# OpenClaw 설치
curl -fsSL https://openclaw.ai/install.sh | bash
# 또는 수동 설치:
# sudo npm install -g openclaw@latest
```

### 5.1 OpenClaw 초기화
```bash
openclaw onboard
```

대화형 설정 마법사가 시작됩니다. 아래 순서대로 진행합니다:

#### Step 1: 설정 모드 선택
**QuickStart**를 선택합니다.

#### Step 2: AI 프로바이더 선택
이 가이드에서는 Google Antigravity OAuth로 Gemini 구독 계정의 모델을 사용하므로, **Google**을 선택합니다.

#### Step 3: 인증 방식 선택
**Google Antigravity OAuth**를 선택합니다.

#### Step 4: Google 계정 인증
1. "Copy this Url" 아래 나오는 링크를 **Ctrl을 누른 상태에서 클릭**하면 브라우저가 열립니다.
2. 원하는 구글 계정으로 로그인을 진행합니다.
3. 로그인 후 "사이트에 연결할 수 없음"이라고 나와도 당황하지 말고, **주소표시줄의 URL을 전체 복사**합니다.
4. 다시 터미널 창으로 와서, 복사한 URL을 **붙여넣고 Enter**를 누릅니다.

#### Step 5: 모델 선택
인증이 완료되면 모델을 선택할 수 있습니다. 예시: `google-antigravity/gemini-3-flash`

#### Step 6: 메신저 선택 (텔레그램)
메신저를 선택하는 단계에서 **Telegram**을 선택합니다.

1. 텔레그램(데스크톱 앱 또는 웹)에서 **BotFather**를 검색합니다.
2. BotFather를 열고 **Start** 버튼을 누릅니다.
3. `/newbot`을 클릭하여 새 봇을 생성합니다.
4. **이름**과 **username**을 입력합니다 (username은 반드시 `_bot` 또는 `Bot`으로 끝나야 함).
5. 봇 생성이 완료되면 **HTTP API Token**이 표시됩니다. 클릭하여 복사합니다.
6. 복사한 Token을 터미널에 **붙여넣고 Enter**를 누릅니다.

> **참고:** 이 시점에서 텔레그램 봇 채팅창에 메시지를 보내도 응답하지 않습니다. OpenClaw TUI에서 해당 사용자와의 대화를 승인해야 대화가 가능해집니다.

#### Step 7: 스킬 설정
스킬은 추후 별도로 구성할 수 있으므로, 여기서는 **스킵**합니다.

#### Step 8: 실행 모드 선택
- **Hatch in TUI**: 터미널 환경에서 바로 OpenClaw와 대화를 시작합니다 (권장).
- **Open the web UI**: 원격 서버의 경우 SSH 터널링이 필요합니다 (8-2 참조).

#### Step 9: 페르소나 설정
OpenClaw는 첫 대화 시 페르소나를 부여해주기를 요청합니다. 역할, 성격, 주 사용 이모지 등을 지정하면 해당 캐릭터로 대화를 이어갑니다.

## 6. GOG CLI 설치

Google 서비스 CLI 도구(`gogcli`)를 설치합니다. (GCP VM 환경에서 진행)

```bash
# VM 접속 (이미 접속된 상태면 스킵)
gcloud compute ssh openclaw-instance --zone=us-central1-a

# 리포지토리 복제
git clone https://github.com/steipete/gogcli.git
cd gogcli

# 바이너리 빌드
make

# 전역 설치 (심볼릭 링크)
sudo ln -sf $(pwd)/bin/gog /usr/local/bin/gog

# 설치 확인
gog --help
```

### 6.1 보안 Keyring 구성 (중요)
gog-cli는 별도의 설정이 없으면 매번 명령 수행 시 비밀번호를 물어보게 됩니다. 자동화 처리를 위해 Keyring 백엔드를 **파일(file)**로 설정해야 합니다.

1.  **환경 변수 설정 (영구 적용)**

    `~/.bashrc` 파일 하단에 다음 내용을 추가합니다:

    ```bash
    # nano 편집기로 파일 열기
    nano ~/.bashrc
    ```

    열린 문서 가장 하단에 아래 내용을 붙여넣고, `Ctrl+O` → `Enter` → `Ctrl+X`로 저장 후 종료합니다:

    ```bash
    # Go 언어 경로 (앞서 추가하지 않았다면)
    export PATH=$PATH:/usr/local/go/bin

    # GOG CLI 설정 (File Backend & Headless)
    export GOG_KEYRING_BACKEND=file
    export GOG_KEYRING_PASSWORD='your_secure_password' # 강력한 비밀번호로 변경하세요
    export GOG_ACCOUNT='your_email@gmail.com'          # 이메일 반복 입력을 피하기 위해 설정
    ```

    변경 사항 적용:
    ```bash
    source ~/.bashrc
    ```

2.  **구성 확인**
    설정이 올바르게 적용되었는지 확인합니다:
    ```bash
    gog config list
    ```

gog 인증은 아래 7번 항목에서 이어갑니다.

## 7. 구성 및 인증

구글 인증키 생성 과정은 아래 유튜브 영상을 참고하시면 자세하게 확인할 수 있습니다.

> **참고 영상:** [오픈클로(OpenClaw) 설치, 서버 없이 구글에서 30분 만에 끝내기!](https://youtu.be/_5R0ahdT0ew?t=407)
> - 06:46 | 구글 클라우드 설정
> - 14:11 | 구글 결제계정 등록
> - 30:00 | OpenClaw에서 구글서비스 사용하기

### 7.1 Client Secret 설정
Google Cloud Console에서 다운로드한 `client_secret.json` 파일을 서버로 업로드합니다.

**로컬 머신에서 실행:**
```bash
gcloud compute scp ./keys/client_secret.json openclaw-instance:~/client_secret.json --zone=us-central1-a
```

### 7.2 GOG CLI 인증 (Headless 모드)
**원격 서버에서 실행:**

원격 서버에서는 브라우저를 실행할 수 없으므로 수동 인증 방식(`--manual`)을 사용합니다.

```bash
# 업로드한 시크릿 파일을 사용하여 인증 (이메일 주소 지정 권장)
gog auth login [YOUR_EMAIL@gmail.com] --client-secret ~/client_secret.json --manual
```

1. 명령어를 실행하면 터미널에 **인증 URL**이 출력됩니다.
2. 해당 URL을 **로컬 컴퓨터의 브라우저**에 복사하여 붙여넣고 로그인합니다.
3. 화면에 표시된 **인증 코드**를 복사하여 터미널에 붙여넣습니다.

## 8. OpenClaw 실행

### 8-1. TUI 모드 (권장)

```bash
# 원격서버 접속
gcloud compute ssh openclaw-instance --zone=us-central1-a

# TUI 실행
openclaw tui
```

### 8-2. 웹 액세스 - SSH 터널링 (선택 사항)

로컬 머신에서 OpenClaw 대시보드에 안전하게 접속하려면 다음 명령어를 사용하십시오:

**로컬 머신에서 실행:**
```bash
# 원격 포트 18789를 로컬 포트 18790으로 포워딩
gcloud compute ssh openclaw-instance --zone=us-central1-a -- -L 18790:localhost:18789 -N -f
```
대시보드 접속 주소: http://localhost:18790

## 9. 문제 해결 팁

- **gcloud 설치 확인:** `gcloud version` 실행 시 `command not found`가 나오면 1.2 단계의 OS별 설치 가이드를 따르십시오.
- **gcloud 인증 만료:** `gcloud auth login` 또는 `gcloud auth application-default login`으로 재인증하십시오.
- **메모리 문제:** `npm install` 실패 시 인스턴스 사양이 최소 `e2-small` (2GB RAM) 이상인지 확인하십시오. 스왑(swap) 파일을 추가하는 것도 방법입니다.
- **Go 버전:** `gogcli` 빌드 실패 시 `go version`을 확인하십시오. 반드시 1.22 버전 이상이어야 합니다.
- **포트 충돌:** 로컬에서 18789 포트가 이미 사용 중이라면 다른 포트를 사용하십시오 (예: `-L 18790:localhost:18789`).

## 참고 링크

- [OpenClaw 홈페이지](https://openclaw.ai)
- [OpenClaw Repository](https://github.com/openclaw/openclaw)
- [gog-cli 홈페이지](https://gogcli.sh/)
- [gog-cli Repository](https://github.com/steipete/gogcli)
- [Gcloud CLI 공식 문서](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Telegram Web](https://web.telegram.org/)
