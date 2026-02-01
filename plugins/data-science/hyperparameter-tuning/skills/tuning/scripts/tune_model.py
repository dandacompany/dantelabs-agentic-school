#!/usr/bin/env python3
"""
하이퍼파라미터 튜닝 스크립트

Optuna를 사용하여 자동으로 최적의 하이퍼파라미터를 찾습니다.

사용법:
    python tune_model.py \
      --X-train-path "./data/processed/X_train_balanced.csv" \
      --y-train-path "./data/processed/y_train_balanced.csv" \
      --algorithm xgboost \
      --n-trials 50 \
      --metric f1
"""

import argparse
import joblib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import optuna
from optuna.integration import XGBoostPruningCallback, LightGBMPruningCallback
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    precision_recall_curve,
    auc as auc_score
)


def load_data(X_train_path, y_train_path):
    """데이터 로드"""
    print(f"\n데이터 로드 중...")
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]

    print(f"✓ Train: {len(X_train):,}건 × {X_train.shape[1]}개 특성")

    return X_train, y_train


def objective_xgboost(trial, X, y, metric='f1'):
    """XGBoost 목적 함수"""
    # 하이퍼파라미터 샘플링
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'random_state': 42,
        'eval_metric': 'logloss'
    }

    # Stratified K-Fold CV
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []

    for train_idx, val_idx in cv.split(X, y):
        X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
        y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]

        model = xgb.XGBClassifier(**params)
        model.fit(
            X_train_cv, y_train_cv,
            eval_set=[(X_val_cv, y_val_cv)],
            verbose=False,
            callbacks=[XGBoostPruningCallback(trial, 'validation_0-logloss')]
        )

        # 평가
        if metric == 'f1':
            y_pred = model.predict(X_val_cv)
            score = f1_score(y_val_cv, y_pred)
        elif metric == 'roc_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            score = roc_auc_score(y_val_cv, y_proba)
        elif metric == 'pr_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            precision, recall, _ = precision_recall_curve(y_val_cv, y_proba)
            score = auc_score(recall, precision)

        scores.append(score)

    return np.mean(scores)


def objective_lightgbm(trial, X, y, metric='f1'):
    """LightGBM 목적 함수"""
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 100),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
        'random_state': 42,
        'verbose': -1
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []

    for train_idx, val_idx in cv.split(X, y):
        X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
        y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]

        model = lgb.LGBMClassifier(**params)
        model.fit(
            X_train_cv, y_train_cv,
            eval_set=[(X_val_cv, y_val_cv)],
            callbacks=[LightGBMPruningCallback(trial, 'binary_logloss')]
        )

        # 평가
        if metric == 'f1':
            y_pred = model.predict(X_val_cv)
            score = f1_score(y_val_cv, y_pred)
        elif metric == 'roc_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            score = roc_auc_score(y_val_cv, y_proba)
        elif metric == 'pr_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            precision, recall, _ = precision_recall_curve(y_val_cv, y_proba)
            score = auc_score(recall, precision)

        scores.append(score)

    return np.mean(scores)


def objective_rf(trial, X, y, metric='f1'):
    """Random Forest 목적 함수"""
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'max_depth': trial.suggest_int('max_depth', 5, 30),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'random_state': 42,
        'n_jobs': -1
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = []

    for train_idx, val_idx in cv.split(X, y):
        X_train_cv, X_val_cv = X.iloc[train_idx], X.iloc[val_idx]
        y_train_cv, y_val_cv = y.iloc[train_idx], y.iloc[val_idx]

        model = RandomForestClassifier(**params)
        model.fit(X_train_cv, y_train_cv)

        # 평가
        if metric == 'f1':
            y_pred = model.predict(X_val_cv)
            score = f1_score(y_val_cv, y_pred)
        elif metric == 'roc_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            score = roc_auc_score(y_val_cv, y_proba)
        elif metric == 'pr_auc':
            y_proba = model.predict_proba(X_val_cv)[:, 1]
            precision, recall, _ = precision_recall_curve(y_val_cv, y_proba)
            score = auc_score(recall, precision)

        scores.append(score)

    return np.mean(scores)


def train_best_model(best_params, X, y, algorithm):
    """최적 파라미터로 최종 모델 학습"""
    print(f"\n최적 파라미터로 최종 모델 학습 중...")

    if algorithm == 'xgboost':
        model = xgb.XGBClassifier(**best_params)
    elif algorithm == 'lightgbm':
        model = lgb.LGBMClassifier(**best_params)
    elif algorithm == 'random_forest':
        model = RandomForestClassifier(**best_params)

    model.fit(X, y)
    print(f"✓ 학습 완료")

    return model


def main():
    parser = argparse.ArgumentParser(description='하이퍼파라미터 튜닝')

    parser.add_argument('--X-train-path', type=str, required=True)
    parser.add_argument('--y-train-path', type=str, required=True)
    parser.add_argument('--algorithm', type=str, default='xgboost',
                        choices=['xgboost', 'lightgbm', 'random_forest'])
    parser.add_argument('--metric', type=str, default='f1',
                        choices=['f1', 'roc_auc', 'pr_auc'])
    parser.add_argument('--n-trials', type=int, default=50,
                        help='최적화 시도 횟수 (기본값: 50)')
    parser.add_argument('--timeout', type=int, default=None,
                        help='최적화 제한 시간 (초)')
    parser.add_argument('--output-dir', type=str, default='outputs/models')

    args = parser.parse_args()

    print("=" * 60)
    print("하이퍼파라미터 튜닝 시작")
    print("=" * 60)

    # 데이터 로드
    X_train, y_train = load_data(args.X_train_path, args.y_train_path)

    # Optuna Study 생성
    print(f"\n최적화 시작 (알고리즘: {args.algorithm}, 지표: {args.metric})")
    print(f"시도 횟수: {args.n_trials}")

    study = optuna.create_study(
        direction='maximize',
        sampler=optuna.samplers.TPESampler(seed=42),
        pruner=optuna.pruners.MedianPruner(n_warmup_steps=10)
    )

    # 목적 함수 선택
    if args.algorithm == 'xgboost':
        objective = lambda trial: objective_xgboost(trial, X_train, y_train, args.metric)
    elif args.algorithm == 'lightgbm':
        objective = lambda trial: objective_lightgbm(trial, X_train, y_train, args.metric)
    elif args.algorithm == 'random_forest':
        objective = lambda trial: objective_rf(trial, X_train, y_train, args.metric)

    # 최적화 실행
    study.optimize(
        objective,
        n_trials=args.n_trials,
        timeout=args.timeout,
        show_progress_bar=True
    )

    # 최적 결과 출력
    print(f"\n{'=' * 60}")
    print("최적화 완료")
    print(f"{'=' * 60}")

    print(f"\n최고 {args.metric.upper()}: {study.best_value:.4f}")
    print(f"\n최적 하이퍼파라미터:")
    for key, value in study.best_params.items():
        print(f"  {key}: {value}")

    # 최종 모델 학습
    best_model = train_best_model(study.best_params, X_train, y_train, args.algorithm)

    # 모델 저장
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / f"{args.algorithm}_tuned_model.pkl"
    joblib.dump(best_model, model_path)
    print(f"\n✓ 모델 저장: {model_path}")

    # 최적화 이력 저장
    history_path = output_dir / f"{args.algorithm}_tuning_history.csv"
    df_history = study.trials_dataframe()
    df_history.to_csv(history_path, index=False)
    print(f"✓ 최적화 이력 저장: {history_path}")

    # 최적 파라미터 저장
    params_path = output_dir / f"{args.algorithm}_best_params.txt"
    with open(params_path, 'w') as f:
        f.write(f"Algorithm: {args.algorithm}\n")
        f.write(f"Metric: {args.metric}\n")
        f.write(f"Best {args.metric.upper()}: {study.best_value:.4f}\n")
        f.write(f"\nBest Parameters:\n")
        for key, value in study.best_params.items():
            f.write(f"  {key}: {value}\n")
        f.write(f"\nOptimization Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"✓ 최적 파라미터 저장: {params_path}")

    print(f"\n{'=' * 60}")
    print("하이퍼파라미터 튜닝 완료")
    print(f"{'=' * 60}")
    print(f"\n📊 최고 성능: {args.metric.upper()} = {study.best_value:.4f}")
    print(f"📁 모델: {model_path}")
    print(f"📁 이력: {history_path}")
    print(f"📁 파라미터: {params_path}\n")


if __name__ == "__main__":
    main()
