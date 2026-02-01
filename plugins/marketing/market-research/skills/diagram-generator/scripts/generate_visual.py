#!/usr/bin/env python3
"""
AI 기반 비즈니스 다이어그램 생성 스크립트

OpenRouter API를 통해 이미지를 생성하고 품질 평가를 수행합니다.

Usage:
    python generate_visual.py "프롬프트" -o output.png
    python generate_visual.py "프롬프트" -o output.png --doc-type report
    python generate_visual.py "프롬프트" -o output.png --threshold 7.5
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests

# OpenRouter API 설정
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 이미지 생성 모델
IMAGE_MODEL = "nano-banana/image-gen-pro"  # 또는 사용 가능한 다른 모델

# 품질 평가 모델
REVIEW_MODEL = "google/gemini-2.0-flash-001"

# 문서 유형별 품질 임계값
QUALITY_THRESHOLDS = {
    "journal": 8.5,
    "conference": 8.0,
    "report": 7.5,
    "presentation": 6.5,
}


def generate_image(prompt: str, output_path: str) -> bool:
    """
    OpenRouter API를 통해 이미지 생성

    Args:
        prompt: 이미지 생성 프롬프트
        output_path: 출력 파일 경로

    Returns:
        성공 여부
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다.")
        return False

    # 비즈니스 다이어그램을 위한 프롬프트 강화
    enhanced_prompt = f"""Professional business diagram for corporate documents:
{prompt}

Style requirements:
- Clean, professional business style
- High contrast for readability
- Clear labels and annotations
- Corporate color palette
- Print-ready quality (300 DPI)
- No decorative elements
- White or light gray background
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": IMAGE_MODEL,
        "prompt": enhanced_prompt,
        "n": 1,
        "size": "1024x1024",
    }

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        result = response.json()

        # 이미지 데이터 추출 및 저장
        if "data" in result and len(result["data"]) > 0:
            image_data = result["data"][0]

            if "b64_json" in image_data:
                # Base64 인코딩된 이미지
                image_bytes = base64.b64decode(image_data["b64_json"])
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                return True
            elif "url" in image_data:
                # URL로 제공된 이미지
                img_response = requests.get(image_data["url"], timeout=60)
                img_response.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                return True

        print("Error: 이미지 데이터를 찾을 수 없습니다.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"Error: API 요청 실패 - {e}")
        return False
    except Exception as e:
        print(f"Error: 이미지 생성 실패 - {e}")
        return False


def evaluate_quality(image_path: str, prompt: str) -> float:
    """
    생성된 이미지의 품질 평가

    Args:
        image_path: 이미지 파일 경로
        prompt: 원본 프롬프트

    Returns:
        품질 점수 (0-10)
    """
    if not OPENROUTER_API_KEY:
        return 5.0  # 기본값 반환

    try:
        # 이미지를 Base64로 인코딩
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        evaluation_prompt = f"""이 비즈니스 다이어그램을 평가해주세요.

원본 요청: {prompt}

다음 기준으로 1-10점 척도로 평가하고, 최종 점수만 숫자로 응답해주세요:
1. 명확성: 텍스트가 읽기 쉬운가?
2. 정확성: 요청한 내용이 정확히 표현되었는가?
3. 전문성: 비즈니스 문서에 적합한 스타일인가?
4. 완성도: 레이블, 범례 등이 완비되어 있는가?

최종 점수 (숫자만):"""

        payload = {
            "model": REVIEW_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": evaluation_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 10
        }

        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()
        score_text = result["choices"][0]["message"]["content"].strip()

        # 숫자 추출
        score = float("".join(c for c in score_text if c.isdigit() or c == "."))
        return min(max(score, 0), 10)

    except Exception as e:
        print(f"Warning: 품질 평가 실패 - {e}")
        return 5.0  # 기본값 반환


def generate_with_iteration(
    prompt: str,
    output_path: str,
    threshold: float,
    max_iterations: int
) -> bool:
    """
    품질 임계값을 만족할 때까지 반복 생성

    Args:
        prompt: 이미지 생성 프롬프트
        output_path: 출력 파일 경로
        threshold: 품질 임계값
        max_iterations: 최대 반복 횟수

    Returns:
        성공 여부
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    best_score = 0
    best_path = None

    for i in range(max_iterations):
        print(f"\n[반복 {i+1}/{max_iterations}] 이미지 생성 중...")

        # 임시 파일 경로
        temp_path = str(output_dir / f"temp_{i}.png")

        if not generate_image(prompt, temp_path):
            continue

        # 품질 평가
        score = evaluate_quality(temp_path, prompt)
        print(f"품질 점수: {score:.1f}/10 (임계값: {threshold})")

        if score > best_score:
            best_score = score
            if best_path and Path(best_path).exists():
                Path(best_path).unlink()
            best_path = temp_path
        else:
            Path(temp_path).unlink()

        if best_score >= threshold:
            print(f"✓ 품질 임계값 달성!")
            break

    if best_path:
        # 최종 파일로 이동
        Path(best_path).rename(output_path)
        print(f"\n✓ 저장 완료: {output_path}")
        print(f"  최종 품질 점수: {best_score:.1f}/10")
        return True

    print("\n✗ 이미지 생성 실패")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="AI 기반 비즈니스 다이어그램 생성"
    )
    parser.add_argument(
        "prompt",
        help="다이어그램 생성 프롬프트"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="출력 파일 경로 (예: figures/diagram.png)"
    )
    parser.add_argument(
        "--doc-type",
        choices=["journal", "conference", "report", "presentation"],
        default="report",
        help="문서 유형 (품질 임계값 자동 설정)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        help="커스텀 품질 임계값 (0-10)"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3,
        help="최대 반복 횟수 (기본: 3)"
    )

    args = parser.parse_args()

    # 품질 임계값 결정
    if args.threshold is not None:
        threshold = args.threshold
    else:
        threshold = QUALITY_THRESHOLDS.get(args.doc_type, 7.5)

    print(f"다이어그램 생성 시작")
    print(f"  프롬프트: {args.prompt[:50]}...")
    print(f"  출력: {args.output}")
    print(f"  문서 유형: {args.doc_type}")
    print(f"  품질 임계값: {threshold}")

    success = generate_with_iteration(
        args.prompt,
        args.output,
        threshold,
        args.max_iterations
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
