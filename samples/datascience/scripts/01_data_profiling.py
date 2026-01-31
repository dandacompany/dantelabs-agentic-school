#!/usr/bin/env python3
"""
신용카드 사기 탐지 - 데이터 프로파일링

이 스크립트는 ydata-profiling을 사용하여 자동화된 EDA 리포트를 생성합니다.

사용법:
    python scripts/01_data_profiling.py

출력:
    outputs/reports/data_profile_report.html
"""

import pandas as pd
import os
from pathlib import Path

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "creditcard.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "reports" / "data_profile_report.html"

def main():
    print("=" * 60)
    print("신용카드 사기 탐지 - 데이터 프로파일링")
    print("=" * 60)

    # 데이터 로드
    print(f"\n데이터 로드 중: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"✓ 완료: {len(df):,}건, {len(df.columns)}개 컬럼")

    # 기본 정보 출력
    print(f"\n{'─' * 60}")
    print("기본 정보")
    print(f"{'─' * 60}")

    print(f"\n전체 거래 건수: {len(df):,}건")
    print(f"특성 개수: {len(df.columns)}개")
    print(f"결측치: {df.isnull().sum().sum()}개")

    print(f"\n클래스 분포:")
    class_counts = df['Class'].value_counts()
    print(f"  정상 거래 (Class 0): {class_counts[0]:,}건 ({class_counts[0]/len(df)*100:.2f}%)")
    print(f"  사기 거래 (Class 1): {class_counts[1]:,}건 ({class_counts[1]/len(df)*100:.2f}%)")
    print(f"  불균형 비율: 1:{class_counts[0]/class_counts[1]:.0f}")

    # ydata-profiling 설치 확인
    try:
        from ydata_profiling import ProfileReport
    except ImportError:
        print("\n⚠️  ydata-profiling이 설치되지 않았습니다.")
        print("설치 명령어: pip install ydata-profiling")
        print("\n대신 pandas-profiling을 시도합니다...")
        try:
            from pandas_profiling import ProfileReport
        except ImportError:
            print("⚠️  pandas-profiling도 설치되지 않았습니다.")
            print("기본 통계만 출력하고 종료합니다.")
            print(f"\n{df.describe()}")
            return

    # 프로파일링 리포트 생성
    print(f"\n{'─' * 60}")
    print("프로파일링 리포트 생성 중...")
    print(f"{'─' * 60}")
    print("⏳ 약 2-3분 소요될 수 있습니다...")

    # 샘플링 옵션 (전체 데이터가 너무 크면 주석 해제)
    # df_sample = df.sample(n=50000, random_state=42)
    df_sample = df

    profile = ProfileReport(
        df_sample,
        title="신용카드 사기 탐지 - 데이터 프로파일링 리포트",
        explorative=True,
        minimal=False
    )

    # 리포트 저장
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    profile.to_file(OUTPUT_PATH)

    print(f"\n✓ 완료!")
    print(f"📊 리포트 저장 위치: {OUTPUT_PATH}")
    print(f"\n브라우저에서 열기: open {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
