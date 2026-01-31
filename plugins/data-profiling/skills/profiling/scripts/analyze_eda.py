#!/usr/bin/env python3
"""
EDA 분석 레포트 생성 스크립트

프로파일링 리포트와 원본 데이터를 분석하여 데이터 전처리, 추가 분석, 모델링 지침을 담은
A4 한 장 분량의 레포트를 생성합니다.

설치:
    # uv 사용 (권장)
    cd plugins/data-profiling/skills/profiling
    uv pip install --system -r requirements.txt

사용법:
    python analyze_eda.py \
      --profile-path "./outputs/reports/creditcard_profile_report.html" \
      --data-path "./data/raw/creditcard.csv" \
      --target-column "Class"

    # PDF 출력 (pandoc 필요)
    python analyze_eda.py \
      --data-path "./data/raw/creditcard.csv" \
      --target-column "Class" \
      --output-format pdf

필요 패키지:
    - pandas
    - numpy
"""

import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def analyze_dataset(df, target_column=None):
    """데이터셋 기본 분석"""
    analysis = {
        'n_rows': len(df),
        'n_cols': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'n_missing': df.isnull().sum().sum(),
        'n_duplicates': df.duplicated().sum(),
    }

    # 타겟 컬럼 분석
    if target_column and target_column in df.columns:
        value_counts = df[target_column].value_counts()
        analysis['target_distribution'] = value_counts.to_dict()

        if len(value_counts) == 2:
            majority = value_counts.max()
            minority = value_counts.min()
            analysis['imbalance_ratio'] = majority / minority

    # 결측치 분석
    missing_cols = df.isnull().sum()
    analysis['missing_columns'] = missing_cols[missing_cols > 0].to_dict()

    # 수치형/범주형 분리
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    analysis['numeric_cols'] = numeric_cols
    analysis['categorical_cols'] = categorical_cols

    # 스케일 차이 분석
    if len(numeric_cols) > 1:
        scales = df[numeric_cols].std()
        scales = scales[scales > 0]  # 0 제거
        if len(scales) > 1:
            analysis['scale_ratio'] = scales.max() / scales.min()

    # 상관관계 분석
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        # 대각선 제외
        corr_matrix = corr_matrix.where(
            ~np.triu(np.ones(corr_matrix.shape)).astype(bool)
        )
        high_corr = corr_matrix[corr_matrix > 0.9].stack()
        analysis['high_corr_pairs'] = len(high_corr)

    return analysis


def detect_problem_type(df, target_column):
    """문제 유형 자동 감지"""
    if target_column is None:
        return "unsupervised"

    if target_column not in df.columns:
        return "unknown"

    target_dtype = df[target_column].dtype
    n_unique = df[target_column].nunique()

    # 분류 vs 회귀
    if target_dtype in ['int64', 'int32'] and n_unique <= 20:
        return "classification"
    elif target_dtype in ['object', 'category']:
        return "classification"
    elif target_dtype in ['float64', 'float32']:
        return "regression"
    else:
        return "unknown"


def generate_preprocessing_guide(analysis, problem_type):
    """데이터 전처리 지침 생성"""
    guides = []

    # 1. 스케일링
    if analysis.get('scale_ratio', 0) > 100:
        guides.append({
            'priority': 'High',
            'title': '스케일링',
            'description': f"변수 간 스케일 차이가 큽니다 (최대/최소 = {analysis['scale_ratio']:.0f}배)",
            'code': """from sklearn.preprocessing import RobustScaler

# 이상치에 강건한 RobustScaler 권장
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X[numeric_cols])"""
        })

    # 2. 클래스 불균형
    if problem_type == "classification" and analysis.get('imbalance_ratio', 0) > 10:
        ratio = analysis['imbalance_ratio']
        guides.append({
            'priority': 'Critical',
            'title': '클래스 불균형 처리',
            'description': f"불균형 비율 1:{ratio:.0f}",
            'code': f"""from imblearn.over_sampling import SMOTE

# SMOTE로 소수 클래스 오버샘플링
smote = SMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 또는 Class weights 조정
from xgboost import XGBClassifier
model = XGBClassifier(scale_pos_weight={ratio:.0f})"""
        })

    # 3. 결측치
    if analysis['n_missing'] > 0:
        missing_pct = (analysis['n_missing'] / (analysis['n_rows'] * analysis['n_cols'])) * 100
        guides.append({
            'priority': 'Medium',
            'title': '결측치 처리',
            'description': f"전체 데이터의 {missing_pct:.2f}%가 결측",
            'code': """from sklearn.impute import SimpleImputer

# 수치형: 중앙값으로 대체
imputer_num = SimpleImputer(strategy='median')
X[numeric_cols] = imputer_num.fit_transform(X[numeric_cols])

# 범주형: 최빈값으로 대체
imputer_cat = SimpleImputer(strategy='most_frequent')
X[cat_cols] = imputer_cat.fit_transform(X[cat_cols])"""
        })

    return guides


def generate_analysis_recommendations(df, analysis, problem_type):
    """추가 분석 권고사항 생성"""
    recommendations = []

    # 1. Feature Importance
    if problem_type in ['classification', 'regression']:
        recommendations.append({
            'title': 'Feature Importance 분석',
            'description': '중요 변수 식별 및 차원 축소',
            'code': """import xgboost as xgb

model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# 변수 중요도 시각화
xgb.plot_importance(model, max_num_features=15)
plt.tight_layout()
plt.show()

# 상위 변수만 선택
from sklearn.feature_selection import SelectFromModel
selector = SelectFromModel(model, prefit=True, threshold='median')
X_selected = selector.transform(X)"""
        })

    # 2. 시간 변수 분석 (Time 컬럼 존재 시)
    if 'Time' in df.columns or 'time' in df.columns:
        recommendations.append({
            'title': '시간 특성 추출',
            'description': 'Time 변수에서 유용한 파생 변수 생성',
            'code': """# 시간대 추출
X['Hour'] = (X['Time'] / 3600) % 24
X['Day'] = (X['Time'] / 86400).astype(int)

# 주기성 인코딩 (Cyclical encoding)
X['Hour_sin'] = np.sin(2 * np.pi * X['Hour'] / 24)
X['Hour_cos'] = np.cos(2 * np.pi * X['Hour'] / 24)

# 시간대별 패턴 분석
fraud_by_hour = df.groupby('Hour')['Class'].mean()
fraud_by_hour.plot(kind='bar', title='Target Rate by Hour')"""
        })

    # 3. SHAP 분석
    if problem_type in ['classification', 'regression']:
        recommendations.append({
            'title': 'SHAP 분석 (모델 해석)',
            'description': '예측에 기여하는 변수와 방향성 이해',
            'code': """import shap

# Tree 기반 모델용
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test)

# Force plot (개별 예측 설명)
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])"""
        })

    # 4. 상관관계 분석
    if analysis.get('high_corr_pairs', 0) > 0:
        recommendations.append({
            'title': '다중공선성 제거',
            'description': f"높은 상관관계 변수 쌍: {analysis['high_corr_pairs']}개",
            'code': """# 상관관계 매트릭스
corr_matrix = X.corr().abs()

# 높은 상관관계 변수 찾기 (>0.9)
high_corr = (corr_matrix > 0.9).sum()
vars_to_drop = high_corr[high_corr > 1].index

# 제거
X_reduced = X.drop(columns=vars_to_drop)"""
        })

    return recommendations


def generate_modeling_strategy(problem_type, analysis):
    """모델링 전략 생성"""
    strategy = {
        'algorithms': [],
        'metrics': [],
        'cv_strategy': None,
        'hyperparameters': []
    }

    if problem_type == 'classification':
        # 알고리즘 추천
        strategy['algorithms'] = [
            {
                'rank': 1,
                'name': 'XGBoost',
                'reason': '불균형 데이터 강점, Feature importance',
                'code': """from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=578,  # 불균형 비율
    random_state=42
)
model.fit(X_train, y_train)"""
            },
            {
                'rank': 2,
                'name': 'LightGBM',
                'reason': '빠른 학습 속도, 대용량 데이터 효율',
                'code': """from lightgbm import LGBMClassifier

model = LGBMClassifier(
    n_estimators=100,
    is_unbalance=True,  # 불균형 자동 처리
    random_state=42
)
model.fit(X_train, y_train)"""
            },
            {
                'rank': 3,
                'name': 'Random Forest',
                'reason': '안정적 성능, 해석 가능',
                'code': """from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)"""
            }
        ]

        # 평가 지표
        if analysis.get('imbalance_ratio', 0) > 10:
            strategy['metrics'] = [
                '**F1-Score** (Precision-Recall 균형)',
                '**PR-AUC** (불균형 데이터 최적)',
                '**Recall** (False Negative 비용 높음)',
                '**Precision** (False Positive 비용 높음)',
                '⚠️ Accuracy 사용 금지 (불균형으로 무의미)'
            ]
        else:
            strategy['metrics'] = [
                '**Accuracy**',
                '**F1-Score**',
                '**ROC-AUC**'
            ]

        # CV 전략
        strategy['cv_strategy'] = """from sklearn.model_selection import StratifiedKFold

# 클래스 비율 유지하며 5-fold CV
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)"""

    elif problem_type == 'regression':
        strategy['algorithms'] = [
            {'rank': 1, 'name': 'XGBoost Regressor', 'reason': '높은 성능'},
            {'rank': 2, 'name': 'Random Forest Regressor', 'reason': '안정성'},
            {'rank': 3, 'name': 'LightGBM Regressor', 'reason': '속도'}
        ]
        strategy['metrics'] = ['RMSE', 'MAE', 'R-squared']
        strategy['cv_strategy'] = 'KFold(n_splits=5)'

    return strategy


def generate_markdown_report(df, analysis, problem_type, target_column, dataset_name):
    """Markdown 레포트 생성"""

    # 전처리 가이드
    preprocessing_guides = generate_preprocessing_guide(analysis, problem_type)

    # 추가 분석 권고사항
    recommendations = generate_analysis_recommendations(df, analysis, problem_type)

    # 모델링 전략
    modeling = generate_modeling_strategy(problem_type, analysis)

    # Executive Summary 생성
    exec_summary = []
    if analysis.get('imbalance_ratio', 0) > 10:
        exec_summary.append(f"극심한 클래스 불균형 (1:{analysis['imbalance_ratio']:.0f})")
    if analysis.get('scale_ratio', 0) > 100:
        exec_summary.append(f"변수 스케일 차이 ({analysis['scale_ratio']:.0f}배)")
    if 'Time' in df.columns:
        exec_summary.append("시간 변수 활용 가능")

    # Markdown 생성
    report = f"""# EDA 분석 리포트: {dataset_name}

**생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**분석 대상**: {dataset_name} ({analysis['n_rows']:,}건)
**문제 유형**: {problem_type.title()}

---

## 📊 Executive Summary

"""

    if exec_summary:
        for item in exec_summary:
            report += f"- {item}\n"
    else:
        report += "- 데이터 품질 양호\n- 표준 전처리 파이프라인 적용 가능\n"

    report += f"""
---

## 📋 데이터 개요

| 항목 | 값 |
|------|-----|
| 전체 건수 | {analysis['n_rows']:,}건 |
| 특성 개수 | {analysis['n_cols']}개 |
| 결측치 | {analysis['n_missing']:,}개 |
| 중복 | {analysis['n_duplicates']:,}건 |
| 메모리 | {analysis['memory_mb']:.1f} MB |
| 수치형 변수 | {len(analysis['numeric_cols'])}개 |
| 범주형 변수 | {len(analysis['categorical_cols'])}개 |
"""

    # 타겟 분포
    if target_column and 'target_distribution' in analysis:
        report += f"\n**타겟 분포** (`{target_column}`):\n"
        for cls, count in analysis['target_distribution'].items():
            pct = count / analysis['n_rows'] * 100
            report += f"- 클래스 {cls}: {count:,}건 ({pct:.2f}%)\n"

        if 'imbalance_ratio' in analysis:
            report += f"- 불균형 비율: **1:{analysis['imbalance_ratio']:.0f}** ⚠️\n"

    report += "\n---\n\n## 🔍 주요 발견사항\n\n"

    # 주요 이슈
    findings = []
    if analysis.get('imbalance_ratio', 0) > 10:
        findings.append({
            'severity': 'Critical',
            'title': '클래스 불균형',
            'description': f"사기 거래가 전체의 {100/analysis['imbalance_ratio']:.2f}%에 불과합니다. Accuracy 지표는 무의미하며, Precision-Recall 중심 평가가 필요합니다."
        })

    if analysis.get('scale_ratio', 0) > 100:
        findings.append({
            'severity': 'High',
            'title': '변수 스케일 차이',
            'description': f"변수 간 스케일 차이가 {analysis['scale_ratio']:.0f}배입니다. 스케일링 필수입니다."
        })

    if analysis['n_missing'] > 0:
        missing_pct = (analysis['n_missing'] / (analysis['n_rows'] * analysis['n_cols'])) * 100
        findings.append({
            'severity': 'Medium',
            'title': '결측치 존재',
            'description': f"전체 데이터의 {missing_pct:.2f}%가 결측치입니다."
        })

    for idx, finding in enumerate(findings, 1):
        report += f"### {idx}. {finding['title']} ({finding['severity']})\n{finding['description']}\n\n"

    report += "---\n\n## 📋 데이터 전처리 지침\n\n"

    for guide in preprocessing_guides:
        report += f"### {guide['priority']} Priority: {guide['title']}\n\n"
        report += f"{guide['description']}\n\n"
        report += f"```python\n{guide['code']}\n```\n\n"

    report += "---\n\n## 🔍 추가 분석 권고사항\n\n"

    for idx, rec in enumerate(recommendations, 1):
        report += f"### {idx}. {rec['title']}\n\n"
        report += f"{rec['description']}\n\n"
        report += f"```python\n{rec['code']}\n```\n\n"

    report += "---\n\n## 🤖 모델링 전략\n\n"

    # 알고리즘 추천
    if modeling['algorithms']:
        report += "### 추천 알고리즘\n\n"
        for algo in modeling['algorithms']:
            report += f"**{algo['rank']}순위: {algo['name']}**\n"
            report += f"- 선택 이유: {algo['reason']}\n"
            if 'code' in algo:
                report += f"\n```python\n{algo['code']}\n```\n"
            report += "\n"

    # 평가 지표
    if modeling['metrics']:
        report += "### 평가 지표\n\n"
        for metric in modeling['metrics']:
            report += f"- {metric}\n"
        report += "\n"

    # CV 전략
    if modeling['cv_strategy']:
        report += f"### 교차 검증\n\n```python\n{modeling['cv_strategy']}\n```\n\n"

    report += """---

## 📌 다음 단계 (Next Steps)

### 우선순위 1 (즉시 실행)
"""

    if preprocessing_guides:
        report += f"- [ ] 데이터 전처리: `/engineer-features`\n"

    if problem_type == 'classification' and analysis.get('imbalance_ratio', 0) > 10:
        report += "- [ ] 클래스 불균형 처리: `/handle-imbalance --method smote`\n"

    report += "- [ ] 베이스라인 모델 학습: `/train-models --algorithms xgboost`\n"

    report += """
### 우선순위 2 (모델 학습 후)
- [ ] Feature importance 분석
- [ ] SHAP 분석으로 모델 해석
- [ ] Threshold 최적화

### 우선순위 3 (성능 개선)
- [ ] 하이퍼파라미터 튜닝 (Optuna)
- [ ] Ensemble 모델
- [ ] 추가 특성 엔지니어링

---

**생성 도구**: data-profiling plugin v1.0.0
**다음 커맨드**: `/engineer-features`, `/handle-imbalance`, `/train-models`
"""

    return report


def main():
    parser = argparse.ArgumentParser(
        description='EDA 분석 레포트 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--profile-path',
        type=str,
        help='프로파일링 HTML 리포트 경로 (선택)'
    )
    parser.add_argument(
        '--data-path',
        type=str,
        required=True,
        help='원본 데이터 파일 경로'
    )
    parser.add_argument(
        '--target-column',
        type=str,
        help='타겟 변수 컬럼명'
    )
    parser.add_argument(
        '--output-format',
        type=str,
        choices=['markdown', 'pdf'],
        default='markdown',
        help='출력 형식 (기본값: markdown)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs/reports',
        help='리포트 저장 디렉토리'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("EDA 분석 시작")
    print("=" * 60)

    # 데이터 로드
    print(f"\n데이터 로드 중: {args.data_path}")
    df = pd.read_csv(args.data_path)
    print(f"✓ 완료: {len(df):,}건, {len(df.columns)}개 컬럼")

    # 분석 수행
    print("\n분석 수행 중...")
    analysis = analyze_dataset(df, args.target_column)
    problem_type = detect_problem_type(df, args.target_column)

    print(f"✓ 문제 유형: {problem_type.title()}")

    # 레포트 생성
    dataset_name = Path(args.data_path).stem
    report = generate_markdown_report(
        df, analysis, problem_type, args.target_column, dataset_name
    )

    # 저장
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{dataset_name}_eda_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Markdown 레포트 저장: {md_path}")

    # PDF 변환 (pandoc 사용)
    if args.output_format == 'pdf':
        pdf_path = output_dir / f"{dataset_name}_eda_report.pdf"
        try:
            subprocess.run([
                'pandoc', str(md_path),
                '-o', str(pdf_path),
                '--pdf-engine=xelatex',
                '-V', 'geometry:margin=1in'
            ], check=True)
            print(f"✓ PDF 레포트 저장: {pdf_path}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  pandoc이 설치되지 않아 PDF 변환 실패")
            print("   설치: brew install pandoc")

    # 요약 출력
    print(f"\n{'=' * 60}")
    print("EDA 분석 완료")
    print(f"{'=' * 60}")
    print(f"\n📊 데이터셋: {dataset_name} ({analysis['n_rows']:,}건)")

    if analysis.get('imbalance_ratio'):
        print(f"\n⚠️  클래스 불균형: 1:{analysis['imbalance_ratio']:.0f}")

    if analysis.get('scale_ratio'):
        print(f"⚠️  스케일 차이: {analysis['scale_ratio']:.0f}배")

    print(f"\n📁 레포트: {md_path}")
    print(f"\n다음 단계:")
    print("   /engineer-features")
    if problem_type == 'classification' and analysis.get('imbalance_ratio', 0) > 10:
        print("   /handle-imbalance")
    print("   /train-models\n")


if __name__ == "__main__":
    main()
