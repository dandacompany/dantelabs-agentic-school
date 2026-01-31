#!/usr/bin/env python3
"""
클래스 불균형 처리 스크립트

SMOTE 등의 기법을 사용하여 클래스 불균형을 해결합니다.

설치:
    uv pip install --system -r requirements.txt

사용법:
    python balance_data.py \
      --X-path "./data/processed/creditcard_processed_X.csv" \
      --y-path "./data/processed/creditcard_processed_y.csv" \
      --method smote \
      --ratio 0.1

필요 패키지:
    - pandas, numpy, imbalanced-learn, scikit-learn
"""

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek
from sklearn.model_selection import train_test_split


def load_data(X_path, y_path):
    """데이터 로드"""
    print(f"\n데이터 로드 중...")
    X = pd.read_csv(X_path)
    y = pd.read_csv(y_path).iloc[:, 0]  # 첫 컬럼만
    print(f"✓ X: {X.shape[0]:,}건 × {X.shape[1]}개 특성")
    print(f"✓ y: {len(y):,}건")
    return X, y


def apply_resampling(X_train, y_train, method='smote', ratio=0.1):
    """리샘플링 적용"""
    print(f"\n리샘플링 적용 중 (방법: {method}, 비율: {ratio})...")

    original_counts = y_train.value_counts()
    print(f"  원본 분포: {dict(original_counts)}")

    if method == 'smote':
        sampler = SMOTE(sampling_strategy=ratio, random_state=42)
    elif method == 'adasyn':
        sampler = ADASYN(sampling_strategy=ratio, random_state=42)
    elif method == 'borderline':
        sampler = BorderlineSMOTE(sampling_strategy=ratio, random_state=42)
    elif method == 'undersample':
        sampler = RandomUnderSampler(sampling_strategy=ratio, random_state=42)
    elif method == 'smote_tomek':
        sampler = SMOTETomek(sampling_strategy=ratio, random_state=42)
    else:
        raise ValueError(f"알 수 없는 방법: {method}")

    X_resampled, y_resampled = sampler.fit_resample(X_train, y_train)

    new_counts = pd.Series(y_resampled).value_counts()
    print(f"  변환 후 분포: {dict(new_counts)}")
    print(f"  생성된 샘플: {len(X_resampled) - len(X_train):,}건")

    return X_resampled, y_resampled


def main():
    parser = argparse.ArgumentParser(description='클래스 불균형 처리')

    parser.add_argument('--X-path', type=str, required=True, help='특성 데이터 경로')
    parser.add_argument('--y-path', type=str, required=True, help='타겟 데이터 경로')
    parser.add_argument('--method', type=str, default='smote',
                        choices=['smote', 'adasyn', 'borderline', 'undersample', 'smote_tomek'],
                        help='리샘플링 방법')
    parser.add_argument('--ratio', type=float, default=0.1, help='샘플링 비율')
    parser.add_argument('--test-size', type=float, default=0.2, help='테스트 비율')
    parser.add_argument('--output-dir', type=str, default='data/processed',
                        help='출력 디렉토리')

    args = parser.parse_args()

    print("=" * 60)
    print("클래스 불균형 처리 시작")
    print("=" * 60)

    # 데이터 로드
    X, y = load_data(args.X_path, args.y_path)

    # Train/Test 분리
    print(f"\nTrain/Test 분리 (test_size={args.test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )
    print(f"✓ Train: {len(X_train):,}건, Test: {len(X_test):,}건")

    # 리샘플링 적용 (Train만)
    X_train_resampled, y_train_resampled = apply_resampling(
        X_train, y_train, args.method, args.ratio
    )

    # 저장
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X_train_path = output_dir / 'X_train_balanced.csv'
    y_train_path = output_dir / 'y_train_balanced.csv'
    X_test_path = output_dir / 'X_test.csv'
    y_test_path = output_dir / 'y_test.csv'

    pd.DataFrame(X_train_resampled, columns=X.columns).to_csv(X_train_path, index=False)
    pd.Series(y_train_resampled).to_csv(y_train_path, index=False, header=True)
    X_test.to_csv(X_test_path, index=False)
    y_test.to_csv(y_test_path, index=False, header=True)

    print(f"\n✓ 저장 완료:")
    print(f"   {X_train_path}")
    print(f"   {y_train_path}")
    print(f"   {X_test_path}")
    print(f"   {y_test_path}")

    print(f"\n{'=' * 60}")
    print("클래스 불균형 처리 완료")
    print(f"{'=' * 60}")
    print(f"\n다음 단계:")
    print("   /train-models --algorithms xgboost,lightgbm\n")


if __name__ == "__main__":
    main()
