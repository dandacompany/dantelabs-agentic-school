#!/usr/bin/env python3
"""
모델 모니터링 스크립트

프로덕션 환경에서 모델 성능을 추적하고 데이터 드리프트를 탐지합니다.

설치:
    cd plugins/model-monitoring/skills/monitoring
    uv pip install -r requirements.txt

사용법:
    python monitor_performance.py --model-path "./models/model.pkl" --reference-data "./data/train.csv" --current-data "./data/prod_2024.csv" --target-column "Class"
    python monitor_performance.py --model-path "./models/model.pkl" --reference-data "./data/train.csv" --current-data "./data/prod_2024.csv" --target-column "Class" --alert-threshold 0.1

필요 패키지:
    - pandas
    - evidently
    - matplotlib
    - scipy
"""

import argparse
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

warnings.filterwarnings('ignore')


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


def load_data(data_path, target_column=None):
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

    if target_column and target_column in df.columns:
        X = df.drop(columns=[target_column])
        y = df[target_column]
        print(f"✓ 데이터 로드 완료: {len(df):,}건, {len(X.columns)}개 특성, 타겟 있음")
        return X, y, df
    else:
        print(f"✓ 데이터 로드 완료: {len(df):,}건, {len(df.columns)}개 특성, 타겟 없음")
        return df, None, df


def load_model(model_path):
    """모델 로드"""
    print(f"\n✓ 모델 로드 중: {model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

    model = joblib.load(model_path)
    print(f"✓ 모델 로드 완료: {type(model).__name__}")

    return model


def calculate_psi(reference, current, bins=10):
    """PSI (Population Stability Index) 계산"""
    # 연속형 변수를 binning
    breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
    breakpoints = np.unique(breakpoints)

    ref_counts, _ = np.histogram(reference, bins=breakpoints)
    cur_counts, _ = np.histogram(current, bins=breakpoints)

    # 0으로 나누기 방지
    ref_percents = (ref_counts + 1) / (len(reference) + bins)
    cur_percents = (cur_counts + 1) / (len(current) + bins)

    psi = np.sum((cur_percents - ref_percents) * np.log(cur_percents / ref_percents))

    return psi


def calculate_ks_statistic(reference, current):
    """KS (Kolmogorov-Smirnov) 통계량 계산"""
    ks_stat, p_value = stats.ks_2samp(reference, current)
    return ks_stat, p_value


def detect_data_drift(X_ref, X_cur, output_dir, threshold=0.1):
    """데이터 드리프트 탐지"""
    print_section("데이터 드리프트 탐지")

    drift_results = []

    for col in X_ref.columns:
        if col not in X_cur.columns:
            print(f"⚠️  '{col}' 컬럼이 현재 데이터에 없습니다.")
            continue

        # 숫자형 컬럼만 처리
        if not np.issubdtype(X_ref[col].dtype, np.number):
            continue

        ref_data = X_ref[col].dropna()
        cur_data = X_cur[col].dropna()

        # PSI 계산
        psi = calculate_psi(ref_data.values, cur_data.values)

        # KS 통계량 계산
        ks_stat, p_value = calculate_ks_statistic(ref_data.values, cur_data.values)

        # 드리프트 판정
        drift_detected = psi > threshold or p_value < 0.05

        drift_results.append({
            'feature': col,
            'psi': psi,
            'ks_statistic': ks_stat,
            'ks_pvalue': p_value,
            'drift_detected': drift_detected
        })

    drift_df = pd.DataFrame(drift_results)
    drift_df = drift_df.sort_values('psi', ascending=False)

    # 드리프트 발생 특성
    drifted_features = drift_df[drift_df['drift_detected']]

    print(f"\n전체 특성: {len(drift_df)}개")
    print(f"드리프트 발생: {len(drifted_features)}개")

    if len(drifted_features) > 0:
        print(f"\n⚠️  드리프트 발생 특성 (상위 5개):")
        for i, row in drifted_features.head(5).iterrows():
            print(f"  - {row['feature']:20s}: PSI={row['psi']:.4f}, KS={row['ks_statistic']:.4f} (p={row['ks_pvalue']:.4f})")
    else:
        print(f"\n✓ 드리프트 발생 없음")

    # 시각화
    plot_drift_summary(drift_df, output_dir, threshold)

    # CSV 저장
    drift_path = os.path.join(output_dir, 'drift_report.csv')
    drift_df.to_csv(drift_path, index=False)
    print(f"\n✓ 드리프트 리포트 저장: {drift_path}")

    return drift_df


def plot_drift_summary(drift_df, output_dir, threshold):
    """드리프트 요약 시각화"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # PSI 분포
    ax1 = axes[0]
    drift_df_sorted = drift_df.sort_values('psi', ascending=True)
    colors = ['red' if x else 'green' for x in drift_df_sorted['drift_detected']]
    ax1.barh(range(len(drift_df_sorted)), drift_df_sorted['psi'], color=colors, alpha=0.7)
    ax1.axvline(x=threshold, color='orange', linestyle='--', linewidth=2, label=f'Threshold ({threshold})')
    ax1.set_yticks(range(len(drift_df_sorted)))
    ax1.set_yticklabels(drift_df_sorted['feature'], fontsize=8)
    ax1.set_xlabel('PSI (Population Stability Index)')
    ax1.set_title('Data Drift - PSI')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # KS 통계량 분포
    ax2 = axes[1]
    drift_df_sorted = drift_df.sort_values('ks_statistic', ascending=True)
    colors = ['red' if x else 'green' for x in drift_df_sorted['drift_detected']]
    ax2.barh(range(len(drift_df_sorted)), drift_df_sorted['ks_statistic'], color=colors, alpha=0.7)
    ax2.set_yticks(range(len(drift_df_sorted)))
    ax2.set_yticklabels(drift_df_sorted['feature'], fontsize=8)
    ax2.set_xlabel('KS Statistic')
    ax2.set_title('Data Drift - KS Test')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = os.path.join(output_dir, 'drift_summary.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 드리프트 요약 시각화 저장: {output_path}")


def track_performance(model, X_cur, y_cur, output_dir, task_type='classification'):
    """성능 추적"""
    print_section("모델 성능 추적")

    y_pred = model.predict(X_cur)

    if task_type == 'classification':
        accuracy = accuracy_score(y_cur, y_pred)
        precision = precision_score(y_cur, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_cur, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_cur, y_pred, average='weighted', zero_division=0)

        print(f"\n분류 성능:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")

        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    else:  # regression
        mae = mean_absolute_error(y_cur, y_pred)
        mse = mean_squared_error(y_cur, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_cur, y_pred)

        print(f"\n회귀 성능:")
        print(f"  MAE:  {mae:.4f}")
        print(f"  MSE:  {mse:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²:   {r2:.4f}")

        metrics = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }

    return metrics


def plot_prediction_distribution(model, X_ref, X_cur, output_dir):
    """예측 분포 비교"""
    print_section("예측 분포 모니터링")

    # 예측 수행
    if hasattr(model, 'predict_proba'):
        y_ref_pred = model.predict_proba(X_ref)[:, 1]
        y_cur_pred = model.predict_proba(X_cur)[:, 1]
        ylabel = 'Predicted Probability'
    else:
        y_ref_pred = model.predict(X_ref)
        y_cur_pred = model.predict(X_cur)
        ylabel = 'Predicted Value'

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.hist(y_ref_pred, bins=50, alpha=0.5, label='Reference', density=True)
    plt.hist(y_cur_pred, bins=50, alpha=0.5, label='Current', density=True)
    plt.xlabel(ylabel)
    plt.ylabel('Density')
    plt.title('Prediction Distribution Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'prediction_distribution.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ 예측 분포 시각화 저장: {output_path}")

    # KS 통계량 계산
    ks_stat, p_value = calculate_ks_statistic(y_ref_pred, y_cur_pred)
    print(f"  예측 분포 KS 통계량: {ks_stat:.4f} (p={p_value:.4f})")

    if p_value < 0.05:
        print(f"  ⚠️  예측 분포에 유의미한 차이가 있습니다!")


def generate_alerts(drift_df, metrics, output_dir, threshold=0.1):
    """알림 생성"""
    print_section("알림 시스템")

    alerts = []

    # 드리프트 알림
    drifted_features = drift_df[drift_df['drift_detected']]
    if len(drifted_features) > 0:
        alerts.append({
            'type': 'DATA_DRIFT',
            'severity': 'WARNING',
            'message': f'{len(drifted_features)}개 특성에서 데이터 드리프트 발생',
            'details': drifted_features['feature'].tolist()
        })

    # 성능 저하 알림 (예시: F1 < 0.7 또는 R² < 0.7)
    if 'f1' in metrics and metrics['f1'] < 0.7:
        alerts.append({
            'type': 'PERFORMANCE_DEGRADATION',
            'severity': 'CRITICAL',
            'message': f'F1-Score가 임계값(0.7) 이하입니다: {metrics["f1"]:.4f}',
            'details': metrics
        })

    if 'r2' in metrics and metrics['r2'] < 0.7:
        alerts.append({
            'type': 'PERFORMANCE_DEGRADATION',
            'severity': 'CRITICAL',
            'message': f'R²가 임계값(0.7) 이하입니다: {metrics["r2"]:.4f}',
            'details': metrics
        })

    # 알림 출력
    if len(alerts) > 0:
        print(f"\n⚠️  {len(alerts)}개 알림 발생:")
        for i, alert in enumerate(alerts, 1):
            print(f"\n  [{i}] {alert['severity']}: {alert['type']}")
            print(f"      {alert['message']}")
    else:
        print(f"\n✓ 알림 없음")

    # JSON 저장
    alerts_path = os.path.join(output_dir, 'alerts.json')
    with open(alerts_path, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, indent=2, ensure_ascii=False)

    print(f"\n✓ 알림 저장: {alerts_path}")

    return alerts


def save_monitoring_report(drift_df, metrics, alerts, output_dir, model_name):
    """모니터링 리포트 저장"""
    report_path = os.path.join(output_dir, f"{model_name}_monitoring_report.md")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 모델 모니터링 리포트: {model_name}\n\n")
        f.write(f"**생성 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # 알림
        f.write(f"## 🚨 알림\n\n")
        if len(alerts) > 0:
            for alert in alerts:
                f.write(f"- **{alert['severity']}**: {alert['message']}\n")
        else:
            f.write(f"- ✓ 알림 없음\n")

        # 성능 메트릭
        f.write(f"\n## 📊 성능 메트릭\n\n")
        for key, value in metrics.items():
            f.write(f"- **{key.upper()}**: {value:.4f}\n")

        # 드리프트 요약
        f.write(f"\n## 📉 데이터 드리프트\n\n")
        drifted = drift_df[drift_df['drift_detected']]
        f.write(f"- 전체 특성: {len(drift_df)}개\n")
        f.write(f"- 드리프트 발생: {len(drifted)}개\n\n")

        if len(drifted) > 0:
            f.write(f"### 드리프트 발생 특성\n\n")
            f.write(f"| 특성 | PSI | KS Statistic | p-value |\n")
            f.write(f"|------|-----|-------------|--------|\n")
            for i, row in drifted.iterrows():
                f.write(f"| {row['feature']} | {row['psi']:.4f} | {row['ks_statistic']:.4f} | {row['ks_pvalue']:.4f} |\n")

        # 시각화
        f.write(f"\n## 📈 시각화\n\n")
        f.write(f"- 드리프트 요약: `drift_summary.png`\n")
        f.write(f"- 예측 분포: `prediction_distribution.png`\n")
        f.write(f"- 드리프트 상세: `drift_report.csv`\n")

    print(f"\n✓ 모니터링 리포트 저장: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='모델 모니터링 스크립트')
    parser.add_argument('--model-path', type=str, required=True,
                        help='학습된 모델 파일 경로 (.pkl)')
    parser.add_argument('--reference-data', type=str, required=True,
                        help='참조 데이터 경로 (학습 데이터)')
    parser.add_argument('--current-data', type=str, required=True,
                        help='현재 데이터 경로 (프로덕션 데이터)')
    parser.add_argument('--target-column', type=str, default=None,
                        help='타겟 컬럼명')
    parser.add_argument('--task-type', type=str, choices=['classification', 'regression', 'auto'],
                        default='auto', help='태스크 타입')
    parser.add_argument('--alert-threshold', type=float, default=0.1,
                        help='드리프트 알림 임계값 (PSI, 기본값: 0.1)')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='출력 디렉토리')

    args = parser.parse_args()

    print_header("모델 모니터링 시작")

    # 출력 디렉토리 설정
    if args.output_dir:
        output_dir = args.output_dir
    else:
        current_data_path = Path(args.current_data)
        if 'projects' in current_data_path.parts:
            project_idx = current_data_path.parts.index('projects')
            project_name = current_data_path.parts[project_idx + 1]
            output_dir = f"projects/{project_name}/outputs/monitoring"
        else:
            output_dir = "outputs/monitoring"

    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ 출력 디렉토리: {output_dir}")

    # 데이터 로드
    X_ref, y_ref, _ = load_data(args.reference_data, args.target_column)
    X_cur, y_cur, _ = load_data(args.current_data, args.target_column)

    # 모델 로드
    model = load_model(args.model_path)
    model_name = Path(args.model_path).stem

    # 태스크 타입 추정
    if args.task_type == 'auto':
        if hasattr(model, 'predict_proba'):
            task_type = 'classification'
        else:
            task_type = 'regression'
        print(f"\n✓ 자동 태스크 타입 감지: {task_type}")
    else:
        task_type = args.task_type

    # 드리프트 탐지
    drift_df = detect_data_drift(X_ref, X_cur, output_dir, threshold=args.alert_threshold)

    # 예측 분포 비교
    plot_prediction_distribution(model, X_ref, X_cur, output_dir)

    # 성능 추적 (타겟이 있는 경우)
    if y_cur is not None:
        metrics = track_performance(model, X_cur, y_cur, output_dir, task_type)
    else:
        print("\n⚠️  타겟 컬럼이 없어 성능 추적을 건너뜁니다.")
        metrics = {}

    # 알림 생성
    alerts = generate_alerts(drift_df, metrics, output_dir, threshold=args.alert_threshold)

    # 리포트 저장
    save_monitoring_report(drift_df, metrics, alerts, output_dir, model_name)

    print_header("모델 모니터링 완료")
    print(f"\n📁 모든 결과가 저장되었습니다: {output_dir}/")
    print(f"   - 시각화: *.png")
    print(f"   - 리포트: {model_name}_monitoring_report.md")
    print(f"   - 드리프트: drift_report.csv")
    print(f"   - 알림: alerts.json")

    return 0


if __name__ == '__main__':
    sys.exit(main())
