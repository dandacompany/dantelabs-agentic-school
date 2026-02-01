#!/usr/bin/env python3
"""
SHAP 분석 스크립트

SHAP(SHapley Additive exPlanations)를 사용하여 모델 예측을 설명합니다.

설치:
    cd plugins/shap-analysis/skills/shap-analysis
    uv pip install -r requirements.txt

사용법:
    python analyze_shap.py --model-path "./models/model.pkl" --test-data "./data/test.csv" --target-column "Class"
    python analyze_shap.py --model-path "./models/model.pkl" --test-data "./data/test.csv" --target-column "Class" --sample-size 1000

필요 패키지:
    - pandas
    - shap
    - matplotlib
    - scikit-learn
"""

import argparse
import os
import sys
import warnings
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

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


def load_data(data_path, target_column, sample_size=None):
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

    # 샘플링
    if sample_size and len(X) > sample_size:
        print(f"  샘플링: {len(X):,}건 → {sample_size:,}건")
        indices = np.random.choice(len(X), sample_size, replace=False)
        X = X.iloc[indices]
        y = y.iloc[indices]

    print(f"✓ 데이터 로드 완료: {len(X):,}건, {len(X.columns)}개 특성")

    return X, y, df


def load_model(model_path):
    """모델 로드"""
    print(f"\n✓ 모델 로드 중: {model_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

    model = joblib.load(model_path)
    print(f"✓ 모델 로드 완료: {type(model).__name__}")

    return model


def create_explainer(model, X_train):
    """SHAP Explainer 생성"""
    print_section("SHAP Explainer 생성")

    model_type = type(model).__name__

    print(f"모델 타입: {model_type}")
    print("⏳ Explainer 생성 중...")

    # Tree-based models
    if model_type in ['XGBClassifier', 'XGBRegressor', 'LGBMClassifier', 'LGBMRegressor',
                      'RandomForestClassifier', 'RandomForestRegressor',
                      'GradientBoostingClassifier', 'GradientBoostingRegressor']:
        explainer = shap.TreeExplainer(model)
        print(f"✓ TreeExplainer 생성 완료")

    # Linear models
    elif model_type in ['LogisticRegression', 'LinearRegression', 'Ridge', 'Lasso']:
        explainer = shap.LinearExplainer(model, X_train)
        print(f"✓ LinearExplainer 생성 완료")

    # Deep learning models (if using sklearn's MLPClassifier)
    elif model_type in ['MLPClassifier', 'MLPRegressor']:
        explainer = shap.KernelExplainer(model.predict, shap.sample(X_train, 100))
        print(f"✓ KernelExplainer 생성 완료 (100 샘플 사용)")

    # Default: Kernel SHAP (model-agnostic but slow)
    else:
        print(f"⚠️  알려지지 않은 모델 타입, KernelExplainer 사용 (느릴 수 있음)")
        explainer = shap.KernelExplainer(model.predict, shap.sample(X_train, 100))
        print(f"✓ KernelExplainer 생성 완료")

    return explainer


def calculate_shap_values(explainer, X):
    """SHAP 값 계산"""
    print_section("SHAP 값 계산")

    print(f"⏳ {len(X):,}개 샘플에 대한 SHAP 값 계산 중...")

    try:
        shap_values = explainer.shap_values(X)

        # 이진 분류의 경우 양성 클래스만 사용
        if isinstance(shap_values, list) and len(shap_values) == 2:
            shap_values = shap_values[1]

        print(f"✓ SHAP 값 계산 완료")
        print(f"  Shape: {np.array(shap_values).shape}")

        return shap_values

    except Exception as e:
        print(f"❌ SHAP 값 계산 실패: {e}")
        raise


def plot_summary(shap_values, X, output_dir):
    """Summary Plot 생성"""
    print_section("Summary Plot 생성")

    plt.figure()
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'shap_summary_plot.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Summary Plot 저장: {output_path}")
    print(f"  상위 특성들의 SHAP 값 분포를 보여줍니다.")


def plot_bar(shap_values, X, output_dir):
    """Bar Plot 생성 (평균 절댓값)"""
    print_section("Bar Plot 생성")

    plt.figure()
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'shap_bar_plot.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Bar Plot 저장: {output_path}")
    print(f"  특성 중요도(평균 절댓값)를 보여줍니다.")


def plot_waterfall(explainer, shap_values, X, output_dir, instance_idx=0):
    """Waterfall Plot 생성 (개별 예측 설명)"""
    print_section(f"Waterfall Plot 생성 (인스턴스 {instance_idx})")

    plt.figure()

    # SHAP 0.42.0+ API
    try:
        explanation = shap.Explanation(
            values=shap_values[instance_idx],
            base_values=explainer.expected_value if hasattr(explainer, 'expected_value') else 0,
            data=X.iloc[instance_idx].values,
            feature_names=X.columns.tolist()
        )
        shap.waterfall_plot(explanation, show=False)
    except:
        # Fallback for older versions
        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[instance_idx],
                base_values=0,
                data=X.iloc[instance_idx].values,
                feature_names=X.columns.tolist()
            ),
            show=False
        )

    plt.tight_layout()

    output_path = os.path.join(output_dir, f'shap_waterfall_plot_instance_{instance_idx}.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Waterfall Plot 저장: {output_path}")
    print(f"  개별 예측에 대한 특성별 기여도를 보여줍니다.")


def plot_force(explainer, shap_values, X, output_dir, instance_idx=0):
    """Force Plot 생성 (개별 예측 설명)"""
    print_section(f"Force Plot 생성 (인스턴스 {instance_idx})")

    # Force plot을 이미지로 저장
    shap.initjs()

    base_value = explainer.expected_value if hasattr(explainer, 'expected_value') else 0

    # 이진 분류인 경우 양성 클래스 base value 사용
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[1] if len(base_value) > 1 else base_value[0]

    force_plot = shap.force_plot(
        base_value,
        shap_values[instance_idx],
        X.iloc[instance_idx],
        show=False,
        matplotlib=True
    )

    output_path = os.path.join(output_dir, f'shap_force_plot_instance_{instance_idx}.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Force Plot 저장: {output_path}")
    print(f"  개별 예측의 시각적 설명을 보여줍니다.")


def plot_dependence(shap_values, X, output_dir, feature_name=None):
    """Dependence Plot 생성 (특성 의존성)"""
    if feature_name is None:
        # 가장 중요한 특성 자동 선택
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_idx = np.argmax(mean_abs_shap)
        feature_name = X.columns[feature_idx]

    print_section(f"Dependence Plot 생성 ({feature_name})")

    plt.figure()
    shap.dependence_plot(feature_name, shap_values, X, show=False)
    plt.tight_layout()

    output_path = os.path.join(output_dir, f'shap_dependence_plot_{feature_name}.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Dependence Plot 저장: {output_path}")
    print(f"  {feature_name} 특성의 값에 따른 SHAP 값 변화를 보여줍니다.")


def explain_instance(model, X, y, shap_values, instance_idx, output_dir):
    """개별 인스턴스 설명"""
    print_section(f"인스턴스 {instance_idx} 예측 설명")

    instance = X.iloc[instance_idx]
    true_label = y.iloc[instance_idx]
    pred_label = model.predict(X.iloc[[instance_idx]])[0]

    print(f"\n실제 레이블: {true_label}")
    print(f"예측 레이블: {pred_label}")

    # SHAP 값이 높은 상위 5개 특성
    instance_shap = shap_values[instance_idx]
    top_indices = np.argsort(np.abs(instance_shap))[::-1][:5]

    print(f"\n상위 5개 영향 특성:")
    for i, idx in enumerate(top_indices, 1):
        feat_name = X.columns[idx]
        feat_value = instance.iloc[idx]
        shap_value = instance_shap[idx]
        direction = "양성" if shap_value > 0 else "음성"

        print(f"  {i}. {feat_name:20s}: {feat_value:10.4f} (SHAP: {shap_value:+.4f}, {direction} 기여)")

    # 설명 저장
    explanation_path = os.path.join(output_dir, f'instance_{instance_idx}_explanation.txt')
    with open(explanation_path, 'w', encoding='utf-8') as f:
        f.write(f"인스턴스 {instance_idx} 예측 설명\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(f"실제 레이블: {true_label}\n")
        f.write(f"예측 레이블: {pred_label}\n\n")
        f.write(f"상위 5개 영향 특성:\n")
        for i, idx in enumerate(top_indices, 1):
            feat_name = X.columns[idx]
            feat_value = instance.iloc[idx]
            shap_value = instance_shap[idx]
            direction = "양성" if shap_value > 0 else "음성"
            f.write(f"  {i}. {feat_name}: {feat_value:.4f} (SHAP: {shap_value:+.4f}, {direction} 기여)\n")

    print(f"\n✓ 설명 저장: {explanation_path}")


def save_shap_report(shap_values, X, output_dir, model_name):
    """SHAP 분석 리포트 저장"""
    report_path = os.path.join(output_dir, f"{model_name}_shap_report.md")

    # 전역 특성 중요도 계산
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': mean_abs_shap
    }).sort_values('importance', ascending=False)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# SHAP 분석 리포트: {model_name}\n\n")

        f.write(f"## 전역 특성 중요도 (상위 10개)\n\n")
        f.write(f"| 순위 | 특성 | SHAP 중요도 |\n")
        f.write(f"|------|------|------------|\n")
        for i, row in feature_importance.head(10).iterrows():
            f.write(f"| {i+1} | {row['feature']} | {row['importance']:.4f} |\n")

        f.write(f"\n## 시각화 결과\n\n")
        f.write(f"- Summary Plot: `shap_summary_plot.png`\n")
        f.write(f"- Bar Plot: `shap_bar_plot.png`\n")
        f.write(f"- Waterfall Plot: `shap_waterfall_plot_instance_*.png`\n")
        f.write(f"- Force Plot: `shap_force_plot_instance_*.png`\n")
        f.write(f"- Dependence Plot: `shap_dependence_plot_*.png`\n")

        f.write(f"\n## SHAP 값 해석\n\n")
        f.write(f"- **양수 SHAP 값**: 예측을 양성 클래스 방향으로 증가시킴\n")
        f.write(f"- **음수 SHAP 값**: 예측을 음성 클래스 방향으로 감소시킴\n")
        f.write(f"- **절댓값**: 특성의 영향력 크기\n")

    print(f"\n✓ SHAP 리포트 저장: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='SHAP 분석 스크립트')
    parser.add_argument('--model-path', type=str, required=True,
                        help='학습된 모델 파일 경로 (.pkl)')
    parser.add_argument('--test-data', type=str, required=True,
                        help='테스트 데이터 경로')
    parser.add_argument('--target-column', type=str, required=True,
                        help='타겟 컬럼명')
    parser.add_argument('--sample-size', type=int, default=1000,
                        help='SHAP 계산에 사용할 샘플 크기 (기본값: 1000)')
    parser.add_argument('--instance-idx', type=int, default=0,
                        help='설명할 인스턴스 인덱스 (기본값: 0)')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='출력 디렉토리')

    args = parser.parse_args()

    print_header("SHAP 분석 시작")

    # 출력 디렉토리 설정
    if args.output_dir:
        output_dir = args.output_dir
    else:
        test_data_path = Path(args.test_data)
        if 'projects' in test_data_path.parts:
            project_idx = test_data_path.parts.index('projects')
            project_name = test_data_path.parts[project_idx + 1]
            output_dir = f"projects/{project_name}/outputs/shap"
        else:
            output_dir = "outputs/shap"

    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ 출력 디렉토리: {output_dir}")

    # 데이터 로드
    X, y, df = load_data(args.test_data, args.target_column, args.sample_size)

    # 모델 로드
    model = load_model(args.model_path)
    model_name = Path(args.model_path).stem

    # Explainer 생성
    explainer = create_explainer(model, X)

    # SHAP 값 계산
    shap_values = calculate_shap_values(explainer, X)

    # 시각화
    plot_summary(shap_values, X, output_dir)
    plot_bar(shap_values, X, output_dir)
    plot_waterfall(explainer, shap_values, X, output_dir, args.instance_idx)
    plot_force(explainer, shap_values, X, output_dir, args.instance_idx)
    plot_dependence(shap_values, X, output_dir)

    # 개별 인스턴스 설명
    explain_instance(model, X, y, shap_values, args.instance_idx, output_dir)

    # 리포트 저장
    save_shap_report(shap_values, X, output_dir, model_name)

    print_header("SHAP 분석 완료")
    print(f"\n📁 모든 결과가 저장되었습니다: {output_dir}/")
    print(f"   - 시각화: *.png")
    print(f"   - 리포트: {model_name}_shap_report.md")
    print(f"   - 개별 설명: instance_*_explanation.txt")

    return 0


if __name__ == '__main__':
    sys.exit(main())
