#!/usr/bin/env python3
"""
모델 평가 스크립트

학습된 모델의 성능을 종합적으로 평가하고 시각화합니다.

설치:
    cd plugins/model-evaluation/skills/evaluation
    uv pip install -r requirements.txt

사용법:
    python evaluate_model.py --model-path "./models/model.pkl" --test-data "./data/test.csv" --target-column "Class"
    python evaluate_model.py --model-path "./models/model.pkl" --test-data "./data/test.csv" --task-type classification

필요 패키지:
    - pandas
    - scikit-learn
    - matplotlib
    - seaborn
    - joblib
"""

import argparse
import os
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_curve,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import cross_val_score, learning_curve


def print_header(text):
    """헤더 출력"""
    print(f"\n{'=' * 60}")
    print(text)
    print('=' * 60)


def print_section(text):
    """섹션 출력"""
    print(f"\n{'-' * 60}")
    print(text)
    print('-' * 60)


def load_data(data_path, target_column):
    """데이터 로드"""
    print(f"\n✓ 데이터 로드 중: {data_path}")

    file_ext = Path(data_path).suffix.lower()

    if file_ext == '.csv':
        df = pd.read_csv(data_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(data_path)
    elif file_ext == '.parquet':
        df = pd.read_parquet(data_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {file_ext}")

    if target_column not in df.columns:
        raise ValueError(f"타겟 컬럼 '{target_column}'이 데이터에 없습니다.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    print(f"✓ 데이터 로드 완료: {len(df):,}건, {len(X.columns)}개 특성")

    return X, y, df


def load_model(model_path):
    """모델 로드"""
    print(f"\n✓ 모델 로드 중: {model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

    model = joblib.load(model_path)
    print(f"✓ 모델 로드 완료: {type(model).__name__}")

    return model


def plot_feature_importance(model, feature_names, output_dir, top_n=20):
    """특성 중요도 시각화"""
    print_section("특성 중요도 분석")

    # 특성 중요도 추출
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importance = np.abs(model.coef_).flatten()
    else:
        print("⚠️  이 모델은 특성 중요도를 지원하지 않습니다.")
        return

    # 상위 N개 특성
    indices = np.argsort(importance)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_importance = importance[indices]

    # 시각화
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(top_features)), top_importance, align='center')
    plt.yticks(range(len(top_features)), top_features)
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Feature Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'feature_importance.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 특성 중요도 시각화 저장: {output_path}")

    # 콘솔 출력
    print(f"\n상위 {min(10, len(top_features))}개 중요 특성:")
    for i, (feat, imp) in enumerate(zip(top_features[:10], top_importance[:10]), 1):
        print(f"  {i:2d}. {feat:30s}: {imp:.4f}")


def plot_learning_curves(model, X, y, output_dir, cv=5):
    """학습 곡선 시각화"""
    print_section("학습 곡선 분석")

    print("⏳ 학습 곡선 계산 중 (시간이 소요될 수 있습니다)...")

    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, cv=cv, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='f1' if hasattr(model, 'predict_proba') else 'r2'
    )

    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, label='Training score', marker='o')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
    plt.plot(train_sizes, val_mean, label='Validation score', marker='s')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1)

    plt.xlabel('Training Set Size')
    plt.ylabel('Score')
    plt.title('Learning Curves')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'learning_curves.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 학습 곡선 저장: {output_path}")
    print(f"  최종 학습 스코어: {train_mean[-1]:.4f} (±{train_std[-1]:.4f})")
    print(f"  최종 검증 스코어: {val_mean[-1]:.4f} (±{val_std[-1]:.4f})")


def plot_confusion_matrix(y_true, y_pred, output_dir):
    """혼동 행렬 시각화"""
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 혼동 행렬 저장: {output_path}")


def plot_roc_curve(y_true, y_pred_proba, output_dir):
    """ROC 곡선 시각화"""
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = roc_auc_score(y_true, y_pred_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.4f})', linewidth=2)
    plt.plot([0, 1], [0, 1], 'k--', label='Random', linewidth=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'roc_curve.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ ROC 곡선 저장: {output_path}")
    print(f"  ROC AUC: {roc_auc:.4f}")


def plot_precision_recall_curve(y_true, y_pred_proba, output_dir):
    """Precision-Recall 곡선 시각화"""
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, linewidth=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'precision_recall_curve.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Precision-Recall 곡선 저장: {output_path}")


def evaluate_classification(model, X, y, output_dir):
    """분류 모델 평가"""
    print_section("분류 모델 성능 평가")

    # 예측
    y_pred = model.predict(X)

    # 기본 메트릭
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y, y_pred, average='weighted', zero_division=0)

    print(f"\n기본 메트릭:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")

    # Classification Report
    print(f"\n상세 리포트:")
    print(classification_report(y, y_pred))

    # 혼동 행렬
    plot_confusion_matrix(y, y_pred, output_dir)

    # ROC 곡선 (이진 분류인 경우)
    if hasattr(model, 'predict_proba') and len(np.unique(y)) == 2:
        y_pred_proba = model.predict_proba(X)[:, 1]
        plot_roc_curve(y, y_pred_proba, output_dir)
        plot_precision_recall_curve(y, y_pred_proba, output_dir)

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }


def evaluate_regression(model, X, y, output_dir):
    """회귀 모델 평가"""
    print_section("회귀 모델 성능 평가")

    # 예측
    y_pred = model.predict(X)

    # 기본 메트릭
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)

    print(f"\n기본 메트릭:")
    print(f"  MAE:  {mae:.4f}")
    print(f"  MSE:  {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R²:   {r2:.4f}")

    # 예측 vs 실제 시각화
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs Predicted')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'actual_vs_predicted.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Actual vs Predicted 저장: {output_path}")

    # 잔차 플롯
    residuals = y - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--', linewidth=2)
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'residuals.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 잔차 플롯 저장: {output_path}")

    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }


def perform_cross_validation(model, X, y, cv=5):
    """교차 검증"""
    print_section("교차 검증")

    print(f"⏳ {cv}-Fold 교차 검증 수행 중...")

    # 태스크 타입 추정
    if hasattr(model, 'predict_proba'):
        scoring = 'f1_weighted'
        scoring_name = 'F1-Score (Weighted)'
    else:
        scoring = 'r2'
        scoring_name = 'R²'

    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)

    print(f"\n{scoring_name} 스코어 ({cv}-Fold CV):")
    for i, score in enumerate(scores, 1):
        print(f"  Fold {i}: {score:.4f}")
    print(f"\n  평균: {scores.mean():.4f} (±{scores.std():.4f})")

    return scores


def save_evaluation_report(metrics, output_dir, model_name):
    """평가 리포트 저장"""
    report_path = os.path.join(output_dir, f"{model_name}_evaluation_report.md")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 모델 평가 리포트: {model_name}\n\n")
        f.write(f"## 성능 메트릭\n\n")

        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                f.write(f"- **{key.upper()}**: {value:.4f}\n")

        f.write(f"\n## 시각화 결과\n\n")
        f.write(f"- 특성 중요도: `feature_importance.png`\n")
        f.write(f"- 학습 곡선: `learning_curves.png`\n")

        if 'accuracy' in metrics:
            f.write(f"- 혼동 행렬: `confusion_matrix.png`\n")
            f.write(f"- ROC 곡선: `roc_curve.png`\n")
            f.write(f"- Precision-Recall 곡선: `precision_recall_curve.png`\n")
        else:
            f.write(f"- Actual vs Predicted: `actual_vs_predicted.png`\n")
            f.write(f"- 잔차 플롯: `residuals.png`\n")

    print(f"\n✓ 평가 리포트 저장: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='모델 평가 스크립트')
    parser.add_argument('--model-path', type=str, required=True,
                        help='학습된 모델 파일 경로 (.pkl)')
    parser.add_argument('--test-data', type=str, required=True,
                        help='테스트 데이터 경로')
    parser.add_argument('--target-column', type=str, required=True,
                        help='타겟 컬럼명')
    parser.add_argument('--task-type', type=str, choices=['classification', 'regression', 'auto'],
                        default='auto', help='태스크 타입 (기본값: auto)')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='출력 디렉토리')
    parser.add_argument('--cv', type=int, default=5,
                        help='교차 검증 폴드 수 (기본값: 5)')

    args = parser.parse_args()

    print_header("모델 평가 시작")

    # 출력 디렉토리 설정
    if args.output_dir:
        output_dir = args.output_dir
    else:
        # projects/{project-name}/outputs/evaluations 구조 사용
        test_data_path = Path(args.test_data)
        if 'projects' in test_data_path.parts:
            project_idx = test_data_path.parts.index('projects')
            project_name = test_data_path.parts[project_idx + 1]
            output_dir = f"projects/{project_name}/outputs/evaluations"
        else:
            output_dir = "outputs/evaluations"

    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ 출력 디렉토리: {output_dir}")

    # 데이터 로드
    X, y, df = load_data(args.test_data, args.target_column)

    # 모델 로드
    model = load_model(args.model_path)
    model_name = Path(args.model_path).stem

    # 태스크 타입 추정
    if args.task_type == 'auto':
        if hasattr(model, 'predict_proba') or len(np.unique(y)) <= 20:
            task_type = 'classification'
        else:
            task_type = 'regression'
        print(f"\n✓ 자동 태스크 타입 감지: {task_type}")
    else:
        task_type = args.task_type

    # 특성 중요도
    plot_feature_importance(model, X.columns.tolist(), output_dir, top_n=20)

    # 학습 곡선
    plot_learning_curves(model, X, y, output_dir, cv=args.cv)

    # 교차 검증
    cv_scores = perform_cross_validation(model, X, y, cv=args.cv)

    # 모델 평가
    if task_type == 'classification':
        metrics = evaluate_classification(model, X, y, output_dir)
    else:
        metrics = evaluate_regression(model, X, y, output_dir)

    # 리포트 저장
    save_evaluation_report(metrics, output_dir, model_name)

    print_header("모델 평가 완료")
    print(f"\n📁 모든 결과가 저장되었습니다: {output_dir}/")
    print(f"   - 시각화: *.png")
    print(f"   - 리포트: {model_name}_evaluation_report.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
