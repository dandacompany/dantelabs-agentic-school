---
name: deploy-openclaw
description: GCP VM 인스턴스를 생성하고 OpenClaw + GOG CLI를 설치하는 단계별 가이드를 실행합니다.
arguments:
  - name: zone
    description: GCP 존 (예: us-central1-a, asia-northeast3-a)
    required: false
    default: "us-central1-a"
  - name: machine-type
    description: VM 머신 타입 (예: e2-small, e2-medium)
    required: false
    default: "e2-small"
  - name: instance-name
    description: VM 인스턴스 이름
    required: false
    default: "openclaw-instance"
---

# /deploy-openclaw

GCP VM 인스턴스에 OpenClaw를 배포하는 전체 과정을 안내합니다.

## Usage

```bash
# 기본 설정으로 배포 가이드 실행
/deploy-openclaw

# 커스텀 설정
/deploy-openclaw --zone asia-northeast3-a --machine-type e2-medium --instance-name my-openclaw

# 서울 리전에 배포
/deploy-openclaw --zone asia-northeast3-a --instance-name openclaw-seoul
```

## What This Command Does

이 명령어는 `gcp-openclaw` 스킬의 배포 가이드를 기반으로 다음 단계를 순차적으로 안내합니다:

### 1. 전제 조건 확인
- Google Cloud CLI (`gcloud`) 설치 여부 확인
- 인증 및 프로젝트 설정 안내

### 2. VM 인스턴스 생성
- 지정된 zone, machine-type, instance-name으로 VM 생성
- Ubuntu 22.04 LTS, 25GB 부트 디스크

### 3. 서버 환경 설정
- Node.js v22+, Go 1.23+ 설치
- 기본 빌드 도구 설치

### 4. OpenClaw 설치 및 초기화
- OpenClaw 전역 설치
- `openclaw onboard` 초기 설정

### 5. GOG CLI 설치 및 인증
- GOG CLI 빌드 및 설치
- Keyring 백엔드 설정 (headless 모드)
- OAuth 인증 (client_secret.json)

### 6. 접속 설정
- SSH 터널링으로 대시보드 접속

## Examples

### Example 1: 기본 배포 (미국 중부)
```bash
/deploy-openclaw
```
`us-central1-a` 존에 `e2-small` 인스턴스를 `openclaw-instance`라는 이름으로 생성합니다.

### Example 2: 서울 리전 배포
```bash
/deploy-openclaw --zone asia-northeast3-a --machine-type e2-medium --instance-name openclaw-kr
```
한국 사용자를 위해 서울 리전에 더 큰 머신 타입으로 배포합니다.

## Related Skills

- `gcp-openclaw`: 전체 배포 가이드 참조 문서

## Notes

- GCP 프로젝트에 결제가 활성화되어 있어야 합니다.
- `e2-small` (2 vCPU, 2GB RAM) 이상의 머신 타입을 권장합니다.
- SSH 터널링을 통해 대시보드에 접속할 수 있습니다.
