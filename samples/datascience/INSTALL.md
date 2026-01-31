# 설치 가이드

## uv 패키지 매니저 설치 (권장)

**uv**는 Rust로 작성된 초고속 Python 패키지 매니저로, pip보다 10-100배 빠릅니다.

### uv 설치

```bash
# Linux/macOS (권장)
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS (Homebrew)
brew install uv

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pip를 통한 설치 (권장하지 않음)
pip install uv
```

### 설치 확인

```bash
uv --version
# 출력: uv 0.x.x
```

---

## Python 패키지 설치

### 방법 1: uv 사용 (권장 ⚡)

```bash
cd samples/datascience

# requirements.txt로 한 번에 설치
uv pip install -r requirements.txt

# 또는 개별 패키지 설치
uv pip install pandas numpy ydata-profiling \
    scikit-learn xgboost lightgbm \
    imbalanced-learn shap \
    matplotlib seaborn plotly
```

**장점**:
- ⚡ 10-100배 빠른 설치 속도
- 🔒 자동 의존성 해결
- 💾 디스크 캐싱으로 재설치 시 즉시 완료

### 방법 2: pip 사용 (기존 방식)

```bash
cd samples/datascience

# requirements.txt로 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install pandas numpy ydata-profiling \
    scikit-learn xgboost lightgbm \
    imbalanced-learn shap \
    matplotlib seaborn plotly
```

---

## 설치 확인

```bash
python3 << 'EOF'
import pandas as pd
import ydata_profiling
import sklearn
import xgboost
import lightgbm
import imblearn
import shap

print("✓ 모든 패키지가 정상적으로 설치되었습니다!")
print(f"  pandas: {pd.__version__}")
print(f"  ydata-profiling: {ydata_profiling.__version__}")
print(f"  scikit-learn: {sklearn.__version__}")
print(f"  xgboost: {xgboost.__version__}")
print(f"  lightgbm: {lightgbm.__version__}")
print(f"  imbalanced-learn: {imblearn.__version__}")
print(f"  shap: {shap.__version__}")
EOF
```

---

## 플러그인별 설치

각 플러그인의 skill 폴더에는 별도의 `requirements.txt`가 있습니다.

### data-profiling 플러그인

```bash
cd plugins/data-profiling/skills/profiling

# uv 사용
uv pip install -r requirements.txt

# pip 사용
pip install -r requirements.txt
```

**포함 패키지**:
- `pandas` - 데이터 처리
- `ydata-profiling` - 자동화된 EDA

---

## 가상환경 사용 (권장)

### uv로 가상환경 관리

```bash
# 가상환경 생성 및 활성화 (한 번에)
uv venv

# 가상환경 활성화
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

# 패키지 설치
uv pip install -r requirements.txt

# 비활성화
deactivate
```

### venv로 가상환경 관리 (기존 방식)

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# 비활성화
deactivate
```

---

## 문제 해결

### uv 관련

#### 문제: "command not found: uv"
```bash
# PATH 추가 (설치 후 터미널 재시작)
export PATH="$HOME/.cargo/bin:$PATH"

# 또는 쉘 재시작
source ~/.bashrc  # bash
source ~/.zshrc   # zsh
```

#### 문제: uv pip 명령어가 느림
```bash
# 캐시 삭제 후 재설치
uv cache clean
uv pip install -r requirements.txt
```

### ydata-profiling 관련

#### 문제: "ModuleNotFoundError: No module named 'ydata_profiling'"
```bash
# uv로 재설치
uv pip install --force-reinstall ydata-profiling

# 또는 pip로 재설치
pip install --force-reinstall ydata-profiling
```

#### 문제: 설치 시간이 너무 오래 걸림
```bash
# uv 사용 (pip보다 훨씬 빠름)
uv pip install ydata-profiling
```

### 메모리 부족 에러

```bash
# 프로파일링 시 샘플링 사용
python generate_profile.py \
  --data-path "./data.csv" \
  --sample-size 10000 \
  --mode minimal
```

### 브라우저 자동 오픈 실패

```bash
# 수동으로 열기
# macOS
open outputs/reports/creditcard_profile_report.html

# Linux
xdg-open outputs/reports/creditcard_profile_report.html

# Windows
start outputs/reports/creditcard_profile_report.html
```

---

## 성능 비교: uv vs pip

| 작업 | pip | uv | 속도 향상 |
|------|-----|----|----|
| ydata-profiling 설치 | ~2분 | ~10초 | **12배** |
| requirements.txt 전체 설치 | ~5분 | ~30초 | **10배** |
| 재설치 (캐시 활용) | ~3분 | ~3초 | **60배** |

**💡 팁**: 대규모 프로젝트일수록 uv의 성능 이점이 큽니다!

---

## 추가 리소스

- [uv 공식 문서](https://docs.astral.sh/uv/)
- [ydata-profiling 공식 문서](https://docs.profiling.ydata.ai/)
- [scikit-learn 공식 문서](https://scikit-learn.org/)

---

**생성일**: 2026-01-31
**업데이트**: uv 패키지 매니저 지원 추가
