#!/usr/bin/env python3
"""
분석 리포트용 시각자료 생성 스크립트

diagram-generator 스킬의 래퍼로, 분석 리포트에 필요한 시각자료를 생성합니다.

Usage:
    python generate_visual.py "프롬프트" -o figures/output.png
    python generate_visual.py "프롬프트" -o figures/output.png --doc-type report
"""

import subprocess
import sys
from pathlib import Path

# diagram-generator 스크립트 경로
DIAGRAM_GENERATOR_PATH = Path(__file__).parent.parent.parent / "diagram-generator" / "scripts" / "generate_visual.py"


def main():
    """diagram-generator 스크립트 호출"""
    if not DIAGRAM_GENERATOR_PATH.exists():
        print(f"Error: diagram-generator 스크립트를 찾을 수 없습니다.")
        print(f"  예상 경로: {DIAGRAM_GENERATOR_PATH}")
        sys.exit(1)

    # 모든 인자를 그대로 전달
    cmd = [sys.executable, str(DIAGRAM_GENERATOR_PATH)] + sys.argv[1:]

    try:
        result = subprocess.run(cmd, check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
