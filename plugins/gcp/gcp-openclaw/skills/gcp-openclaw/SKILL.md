---
name: gcp-openclaw
description: VM 설정, SSH 구성, OpenClaw 설치 및 GOG CLI 설정을 포함하여 Google Cloud Platform에 OpenClaw를 배포하는 포괄적인 가이드입니다.
---

# GCP OpenClaw 배포 가이드

이 스킬은 Google Cloud Platform (GCP) VM 인스턴스에 OpenClaw를 배포하기 위한 단계별 워크플로를 제공합니다. 초기 GCP 설정부터 OpenClaw 및 GOG CLI 구성까지 모든 과정을 다룹니다.

## 1. 전제 조건 (로컬 머신)

로컬 컴퓨터에 Google Cloud CLI (`gcloud`)가 설치되어 있고 인증이 완료되었는지 확인하십시오.

### 1.1 Google Cloud 인증
```bash
gcloud auth login --no-launch-browser
```
출력된 URL을 브라우저에서 열어 인증하고, 확인 코드를 터미널에 붙여넣습니다.

### 1.2 프로젝트 및 결제 설정
```bash
# 프로젝트 ID 설정
gcloud config set project [YOUR_PROJECT_ID]

# 필요한 서비스 활성화
gcloud services enable compute.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

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

npm을 사용하여 OpenClaw를 전역으로 설치합니다.

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
대화형 설정 마법사를 따라 에이전트를 구성합니다.

## 6. GOG CLI 설치

Google 서비스 CLI 도구(`gogcli`)를 설치합니다.

```bash
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

### 6.2 보안 Keyring 구성 (중요)
대화형 비밀번호 입력 없이 `gogcli`를 사용하려면(headless 모드), Keyring 백엔드를 **파일(file)**로 설정해야 합니다.

1.  **환경 변수 설정 (영구 적용)**
    OpenClaw 편의 기능과 GOG CLI 보안 설정을 위해 `~/.bashrc` 파일 하단에 다음 내용을 추가합니다:
    ```bash
    # OpenClaw 자동 완성
    source "$HOME/.openclaw/completions/openclaw.bash"

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

## 7. 구성 및 인증

### 7.1 Client Secret 설정
Google Cloud Console에서 다운로드한 `client_secret.json` 파일을 서버로 업로드합니다.
**로컬 머신에서 실행:**
```bash
gcloud compute scp /local/path/to/client_secret.json openclaw-instance:~/client_secret.json --zone=us-central1-a
```

### 7.2 GOG CLI 인증 (Headless 모드)
**원격 서버에서 실행:**

원격 서버에서는 브라우저를 실행할 수 없으므로 수동 인증 방식을 사용해야 합니다.

```bash
# 업로드한 시크릿 파일을 사용하여 인증 (이메일 주소 지정 권장)
gog auth login [YOUR_EMAIL@gmail.com] --client-secret ~/client_secret.json
```

1. 명령어를 실행하면 터미널에 **인증 URL**이 출력됩니다.
2. 해당 URL을 **로컬 컴퓨터의 브라우저**에 복사하여 붙여넣고 로그인합니다.
3. 화면에 표시된 **인증 코드**를 복사하여 터미널에 붙여넣습니다.

> **참고:** 만약 브라우저가 열리려고 시도하다 실패한다면 `--manual` 플래그를 추가해 보십시오 (버전에 따라 다를 수 있음).


### 7.3 텔레그램 봇 구성 (선택 사항)
텔레그램을 통해 에이전트를 제어하려면 다음 단계를 따르세요:

1.  **봇 생성:**
    - 텔레그램을 열고 **@BotFather**를 검색합니다.
    - `/newbot`을 보내고 안내에 따라 진행하여 **HTTP API Token**을 발급받습니다.

2.  **OpenClaw 구성:**
    - 구성 마법사를 실행합니다:
      ```bash
      openclaw configure --section telegram
      ```
    - 프롬프트에 **HTTP API Token**을 붙여넣습니다.
    - 텔레그램 통합을 활성화합니다.

## 8. 웹 액세스 (SSH 터널링)

로컬 머신에서 OpenClaw 대시보드에 안전하게 접속하려면 다음 명령어를 사용하십시오:

**로컬 머신에서 실행:**
```bash
# 원격 포트 18789를 로컬 포트 18790으로 포워딩
gcloud compute ssh openclaw-instance --zone=us-central1-a -- -L 18790:localhost:18789 -N -f
```
대시보드 접속 주소: http://localhost:18790

## 9. 문제 해결 팁

- **메모리 문제:** `npm install` 실패 시 인스턴스 사양이 최소 `e2-small` (2GB RAM) 이상인지 확인하십시오. 스왑(swap) 파일을 추가하는 것도 방법입니다.
- **Go 버전:** `gogcli` 빌드 실패 시 `go version`을 확인하십시오. 반드시 1.22 버전 이상이어야 합니다.
- **포트 충돌:** 로컬에서 18789 포트가 이미 사용 중이라면 다른 포트를 사용하십시오 (예: `-L 18790:localhost:18789`).
