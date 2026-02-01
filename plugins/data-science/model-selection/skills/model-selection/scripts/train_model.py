#!/usr/bin/env python3
"""
모델 학습 스크립트

XGBoost, LightGBM, Random Forest 등의 모델을 학습하고 평가합니다.

사용법:
    python train_model.py \
      --X-train-path "./data/processed/X_train_balanced.csv" \
      --y-train-path "./data/processed/y_train_balanced.csv" \
      --X-test-path "./data/processed/X_test.csv" \
      --y-test-path "./data/processed/y_test.csv" \
      --algorithm xgboost
"""

import argparse
import joblib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
    auc as auc_score
)


def load_data(X_train_path, y_train_path, X_test_path, y_test_path):
    """데이터 로드"""
    print(f"\n데이터 로드 중...")
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path).iloc[:, 0]

    print(f"✓ Train: {len(X_train):,}건")
    print(f"✓ Test: {len(X_test):,}건")

    return X_train, y_train, X_test, y_test


def train_model(X_train, y_train, algorithm='xgboost'):
    """모델 학습"""
    print(f"\n모델 학습 중 (알고리즘: {algorithm})...")

    if algorithm == 'xgboost':
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
    elif algorithm == 'lightgbm':
        model = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            verbose=-1
        )
    elif algorithm == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    else:
        raise ValueError(f"알 수 없는 알고리즘: {algorithm}")

    model.fit(X_train, y_train)
    print(f"✓ 학습 완료")

    return model


def evaluate_model(model, X_test, y_test):
    """모델 평가"""
    print(f"\n모델 평가 중...")

    # 예측
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 평가 지표
    print(f"\n{'=' * 60}")
    print("분류 리포트")
    print(f"{'=' * 60}")
    print(classification_report(y_test, y_pred))

    # ROC-AUC
    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC: {roc_auc:.4f}")

    # PR-AUC
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc_score(recall, precision)
    print(f"PR-AUC: {pr_auc:.4f}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:")
    print(f"                Predicted")
    print(f"              0        1")
    print(f"Actual 0  {cm[0][0]:6,}  {cm[0][1]:6,}")
    print(f"Actual 1  {cm[1][0]:6,}  {cm[1][1]:6,}")

    return {
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'confusion_matrix': cm
    }


def main():
    parser = argparse.ArgumentParser(description='모델 학습 및 평가')

    parser.add_argument('--X-train-path', type=str, required=True)
    parser.add_argument('--y-train-path', type=str, required=True)
    parser.add_argument('--X-test-path', type=str, required=True)
    parser.add_argument('--y-test-path', type=str, required=True)
    parser.add_argument('--algorithm', type=str, default='xgboost',
                        choices=['xgboost', 'lightgbm', 'random_forest'])
    parser.add_argument('--output-dir', type=str, default='outputs/models')

    args = parser.parse_args()

    print("=" * 60)
    print("모델 학습 시작")
    print("=" * 60)

    # 데이터 로드
    X_train, y_train, X_test, y_test = load_data(
        args.X_train_path, args.y_train_path,
        args.X_test_path, args.y_test_path
    )

    # 모델 학습
    model = train_model(X_train, y_train, args.algorithm)

    # 모델 평가
    metrics = evaluate_model(model, X_test, y_test)

    # 모델 저장
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / f"{args.algorithm}_model.pkl"
    joblib.dump(model, model_path)
    print(f"\n✓ 모델 저장: {model_path}")

    print(f"\n{'=' * 60}")
    print("모델 학습 완료")
    print(f"{'=' * 60}")
    print(f"\n📊 최종 성능:")
    print(f"   ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"   PR-AUC: {metrics['pr_auc']:.4f}\n")


if __name__ == "__main__":
    main()
