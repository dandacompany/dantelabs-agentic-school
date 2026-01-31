#!/usr/bin/env python3
"""
데이터 프로파일링 스크립트

ydata-profiling을 사용하여 자동화된 EDA 리포트를 생성하고 브라우저에서 엽니다.

설치:
    # uv 사용 (권장 - 10-100배 빠름)
    cd plugins/data-profiling/skills/profiling
    uv pip install -r requirements.txt

    # 또는 pip 사용
    pip install -r requirements.txt

사용법:
    python generate_profile.py --data-path "./data/raw/creditcard.csv" --target-column "Class"
    python generate_profile.py --data-path "./data.csv" --sample-size 50000 --mode minimal

필요 패키지:
    - pandas
    - ydata-profiling
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def open_in_browser(filepath):
    """운영체제에 맞게 브라우저에서 HTML 파일 열기"""
    system = platform.system()
    abs_path = os.path.abspath(filepath)

    try:
        if system == 'Darwin':  # macOS
            subprocess.run(['open', abs_path], check=True)
        elif system == 'Linux':
            subprocess.run(['xdg-open', abs_path], check=True)
        elif system == 'Windows':
            os.startfile(abs_path)
        else:
            print(f"⚠️  자동 브라우저 오픈을 지원하지 않는 운영체제입니다: {system}")
            print(f"   수동으로 열기: {abs_path}")
            return False
        return True
    except Exception as e:
        print(f"⚠️  브라우저 자동 오픈 실패: {e}")
        print(f"   수동으로 열기: {abs_path}")
        return False


def load_data(data_path, sample_size=None):
    """다양한 형식의 데이터 파일 로드"""
    file_ext = Path(data_path).suffix.lower()

    print(f"\n데이터 로드 중: {data_path}")

    # 파일 형식에 따라 로드
    if file_ext == '.csv':
        df = pd.read_csv(data_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(data_path)
    elif file_ext == '.parquet':
        df = pd.read_parquet(data_path)
    elif file_ext == '.json':
        df = pd.read_json(data_path)
    elif file_ext == '.feather':
        df = pd.read_feather(data_path)
    elif file_ext in ['.h5', '.hdf5']:
        df = pd.read_hdf(data_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {file_ext}")

    # 샘플링 (지정된 경우)
    if sample_size and len(df) > sample_size:
        print(f"⚠️  샘플링: {len(df):,}건 → {sample_size:,}건")
        df = df.sample(n=sample_size, random_state=42)

    print(f"✓ 완료: {len(df):,}건, {len(df.columns)}개 컬럼")
    return df


def print_basic_info(df, target_column=None):
    """기본 정보 출력"""
    print(f"\n{'─' * 60}")
    print("기본 정보")
    print(f"{'─' * 60}")

    print(f"\n전체 행 수: {len(df):,}건")
    print(f"전체 열 수: {len(df.columns)}개")
    print(f"메모리 사용량: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"결측치: {df.isnull().sum().sum():,}개")

    # 타겟 컬럼 정보 (분류 문제인 경우)
    if target_column and target_column in df.columns:
        print(f"\n타겟 컬럼: {target_column}")

        # 클래스 분포 확인
        if df[target_column].dtype in ['int64', 'int32', 'object', 'category']:
            value_counts = df[target_column].value_counts()
            print(f"클래스 분포:")
            for cls, count in value_counts.items():
                pct = count / len(df) * 100
                print(f"  클래스 {cls}: {count:,}건 ({pct:.2f}%)")

            # 불균형 비율 계산
            if len(value_counts) == 2:
                majority = value_counts.max()
                minority = value_counts.min()
                imbalance_ratio = majority / minority
                print(f"  불균형 비율: 1:{imbalance_ratio:.0f}")


def generate_profile_report(df, output_path, mode='explorative', title=None):
    """ydata-profiling을 사용하여 프로파일 리포트 생성"""
    try:
        from ydata_profiling import ProfileReport
    except ImportError:
        try:
            from pandas_profiling import ProfileReport
            print("⚠️  pandas_profiling은 deprecated되었습니다. ydata-profiling으로 업그레이드하세요.")
            print("   pip install ydata-profiling")
        except ImportError:
            print("\n❌ 에러: ydata-profiling이 설치되지 않았습니다.")
            print("   설치 명령어: pip install ydata-profiling")
            sys.exit(1)

    print(f"\n{'─' * 60}")
    print("프로파일링 리포트 생성 중...")
    print(f"{'─' * 60}")
    print(f"모드: {mode}")
    print("⏳ 수 분 소요될 수 있습니다...")

    # 모드에 따른 설정
    if mode == 'minimal':
        minimal = True
        explorative = False
    elif mode == 'explorative':
        minimal = False
        explorative = True
    else:  # default
        minimal = False
        explorative = False

    # 프로파일 생성
    profile = ProfileReport(
        df,
        title=title or "Data Profiling Report",
        minimal=minimal,
        explorative=explorative
    )

    # HTML 저장
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile.to_file(output_path)

    print(f"\n✓ 완료!")
    print(f"📊 리포트 저장 위치: {output_path}")

    return output_path


def print_summary_recommendations(df, target_column=None):
    """주요 발견사항 및 권고사항 출력"""
    print(f"\n{'─' * 60}")
    print("⚠️  주요 발견사항 및 권고사항")
    print(f"{'─' * 60}")

    # 결측치 확인
    missing_counts = df.isnull().sum()
    missing_cols = missing_counts[missing_counts > 0]
    if len(missing_cols) > 0:
        missing_pct = (missing_counts.sum() / (len(df) * len(df.columns))) * 100
        print(f"\n⚠️  결측치: {missing_pct:.2f}% ({len(missing_cols)}개 컬럼)")
        print("   권고: /engineer-features로 결측치 처리")

    # 클래스 불균형 확인 (타겟 컬럼이 있는 경우)
    if target_column and target_column in df.columns:
        value_counts = df[target_column].value_counts()
        if len(value_counts) == 2:
            majority = value_counts.max()
            minority = value_counts.min()
            imbalance_ratio = majority / minority
            if imbalance_ratio > 10:
                print(f"\n⚠️  클래스 불균형: 1:{imbalance_ratio:.0f}")
                print("   권고: /handle-imbalance로 불균형 처리 (SMOTE, Undersampling)")

    # 수치형 변수 스케일 차이 확인
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 1:
        scales = df[numeric_cols].std()
        if scales.max() / scales.min() > 100:
            print(f"\n⚠️  변수 간 스케일 차이가 큽니다 (최대/최소 = {scales.max() / scales.min():.0f}배)")
            print("   권고: /engineer-features로 스케일링 (StandardScaler, MinMaxScaler)")

    # 상관관계 확인
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        # 대각선 제외하고 높은 상관관계 찾기
        corr_matrix = corr_matrix.where(
            ~np.triu(np.ones(corr_matrix.shape)).astype(bool)
        )
        high_corr = corr_matrix[corr_matrix > 0.9].stack()
        if len(high_corr) > 0:
            print(f"\n⚠️  높은 상관관계 (>0.9): {len(high_corr)}개 변수 쌍")
            print("   권고: 다중공선성 문제 가능 - 변수 제거 고려")

    print(f"\n💡 다음 단계:")
    print("   /engineer-features: 특성 엔지니어링 및 전처리")
    if target_column:
        print("   /handle-imbalance: 클래스 불균형 처리")
    print("   /train-models: 모델 학습")


def main():
    parser = argparse.ArgumentParser(
        description='데이터 프로파일링 및 자동화된 EDA 리포트 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 기본 사용법
  python generate_profile.py --data-path "./data/raw/creditcard.csv"

  # 타겟 컬럼 지정
  python generate_profile.py --data-path "./data.csv" --target-column "Class"

  # 대용량 데이터 샘플링
  python generate_profile.py --data-path "./data.csv" --sample-size 50000 --mode minimal

  # 브라우저 자동 오픈 비활성화
  python generate_profile.py --data-path "./data.csv" --no-browser
        """
    )

    parser.add_argument(
        '--data-path',
        type=str,
        required=True,
        help='분석할 데이터 파일 경로 (CSV, Excel, Parquet 등)'
    )
    parser.add_argument(
        '--target-column',
        type=str,
        help='타겟 변수 컬럼명 (분류/회귀 문제인 경우)'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        help='샘플링 크기 (대용량 데이터인 경우)'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['minimal', 'default', 'explorative'],
        default='explorative',
        help='프로파일링 모드 (기본값: explorative)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs/reports',
        help='리포트 저장 디렉토리 (기본값: outputs/reports)'
    )
    parser.add_argument(
        '--no-browser',
        action='store_true',
        help='브라우저 자동 오픈 비활성화'
    )

    args = parser.parse_args()

    # 헤더 출력
    print("=" * 60)
    print("데이터 프로파일링 시작")
    print("=" * 60)

    # 데이터 로드
    df = load_data(args.data_path, args.sample_size)

    # 메모리 사용량 출력
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"✓ 메모리 사용량: {memory_mb:.1f} MB")

    # 기본 정보 출력
    print_basic_info(df, args.target_column)

    # 출력 파일명 생성
    dataset_name = Path(args.data_path).stem
    output_filename = f"{dataset_name}_profile_report.html"
    output_path = Path(args.output_dir) / output_filename

    # 프로파일 리포트 생성
    report_path = generate_profile_report(
        df,
        output_path,
        mode=args.mode,
        title=f"Data Profiling Report: {dataset_name}"
    )

    # 브라우저에서 열기
    if not args.no_browser:
        print("\n🌐 브라우저에서 리포트를 여는 중...")
        success = open_in_browser(report_path)
        if success:
            print("✓ 브라우저에서 리포트가 열렸습니다.")
    else:
        print(f"\n수동으로 열기: {report_path.absolute()}")

    # 요약 및 권고사항
    print_summary_recommendations(df, args.target_column)

    print(f"\n{'=' * 60}")
    print("프로파일링 완료")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
