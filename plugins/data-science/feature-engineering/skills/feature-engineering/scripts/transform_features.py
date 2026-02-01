#!/usr/bin/env python3
"""
특성 엔지니어링 스크립트

데이터 전처리 및 특성 엔지니어링을 수행하여 모델 학습 준비 완료된 데이터를 생성합니다.

설치:
    # uv 사용 (권장)
    cd plugins/feature-engineering/skills/feature-engineering
    uv pip install --system -r requirements.txt

사용법:
    python transform_features.py \
      --data-path "./data/raw/creditcard.csv" \
      --target-column "Class" \
      --time-features "hour,day,cyclical"

필요 패키지:
    - pandas
    - numpy
    - scikit-learn
    - joblib
"""

import argparse
import os
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler


def load_data(data_path):
    """데이터 로드"""
    print(f"\n데이터 로드 중: {data_path}")
    df = pd.read_csv(data_path)
    print(f"✓ 완료: {len(df):,}건, {len(df.columns)}개 컬럼")
    return df


def extract_time_features(df, time_column='Time', features=['hour', 'day', 'cyclical']):
    """시간 특성 추출"""
    if time_column not in df.columns:
        print(f"⚠️  '{time_column}' 컬럼이 없습니다. 시간 특성 추출 건너뜁니다.")
        return df, []

    print(f"\n시간 특성 추출 중 (원본: {time_column})...")
    new_features = []

    # Hour 추출 (0-23)
    if 'hour' in features:
        df['Hour'] = (df[time_column] / 3600) % 24
        new_features.append('Hour')
        print(f"  ✓ Hour (0-23) 생성")

    # Day 추출
    if 'day' in features:
        df['Day'] = (df[time_column] / 86400).astype(int)
        new_features.append('Day')
        print(f"  ✓ Day 생성")

    # Cyclical Encoding
    if 'cyclical' in features and 'Hour' in df.columns:
        df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
        df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)
        new_features.extend(['Hour_sin', 'Hour_cos'])
        print(f"  ✓ Hour_sin, Hour_cos (주기성 인코딩) 생성")

    # 원본 Time 컬럼 제거
    df = df.drop(columns=[time_column])
    print(f"  ✓ 원본 '{time_column}' 컬럼 제거")

    return df, new_features


def scale_features(df, target_column=None, strategy='robust', exclude_cols=None):
    """수치형 변수 스케일링"""
    print(f"\n스케일링 적용 중 (전략: {strategy})...")

    # 스케일러 선택
    if strategy == 'robust':
        scaler = RobustScaler()
        print("  ✓ RobustScaler 선택 (이상치에 강건)")
    elif strategy == 'standard':
        scaler = StandardScaler()
        print("  ✓ StandardScaler 선택 (평균 0, 분산 1)")
    elif strategy == 'minmax':
        scaler = MinMaxScaler()
        print("  ✓ MinMaxScaler 선택 (0-1 범위)")
    else:
        raise ValueError(f"알 수 없는 전략: {strategy}")

    # 스케일링 대상 컬럼 선택
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # 제외 컬럼
    if target_column and target_column in numeric_cols:
        numeric_cols.remove(target_column)

    if exclude_cols:
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]

    if not numeric_cols:
        print("  ⚠️  스케일링할 수치형 컬럼이 없습니다.")
        return df, None

    print(f"  대상 컬럼: {len(numeric_cols)}개")

    # 스케일링 적용
    scaled_data = scaler.fit_transform(df[numeric_cols])

    # 스케일링된 컬럼 이름
    scaled_col_names = [f"{col}_scaled" if col in ['Amount', 'amount'] else col
                        for col in numeric_cols]

    # DataFrame 생성
    df_scaled = pd.DataFrame(scaled_data, columns=scaled_col_names, index=df.index)

    # 원본 컬럼 제거 (Amount만)
    if 'Amount' in numeric_cols or 'amount' in numeric_cols:
        for col in ['Amount', 'amount']:
            if col in df.columns:
                df = df.drop(columns=[col])
                print(f"  ✓ 원본 '{col}' 컬럼 제거")

    # 스케일링된 컬럼 추가
    for col in df_scaled.columns:
        df[col] = df_scaled[col]

    print(f"  ✓ 스케일링 완료: {len(numeric_cols)}개 변수")

    return df, scaler


def generate_log(
    dataset_name,
    original_shape,
    final_shape,
    scaling_info,
    time_features_info,
    output_path
):
    """변환 로그 생성"""
    log = f"""# 특성 엔지니어링 로그

**생성일**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**원본 데이터**: {dataset_name} ({original_shape[0]:,}건, {original_shape[1]}개 특성)

---

## 적용된 변환

"""

    # 스케일링 정보
    if scaling_info:
        log += f"""### 1. 스케일링 ({scaling_info['strategy']})
- **전략**: {scaling_info['strategy']}
- **대상 변수**: {', '.join(scaling_info['scaled_columns'])}
- **변환 후 컬럼**: {', '.join([f"{col}_scaled" if col in ['Amount', 'amount'] else col for col in scaling_info['scaled_columns']])}

"""

    # 시간 특성 정보
    if time_features_info:
        log += f"""### 2. 시간 특성 추출
- **원본**: {time_features_info['original_column']}
- **생성된 특성**:
"""
        for feature in time_features_info['new_features']:
            log += f"  - {feature}\n"
        log += f"- **원본 컬럼 제거**: ✓\n\n"

    # 변수 요약
    removed = original_shape[1] - final_shape[1] + len(time_features_info.get('new_features', []))
    added = len(time_features_info.get('new_features', []))

    log += f"""### 3. 변수 요약
- **원본 특성**: {original_shape[1]}개
- **최종 특성**: {final_shape[1]}개 ({final_shape[1] - original_shape[1]:+d}개)
- **제거된 특성**: {removed}개
- **추가된 특성**: {added}개

---

## 다음 단계
- `/handle-imbalance`: 클래스 불균형 처리 (SMOTE)
- `/train-models`: 모델 학습

---

**생성 도구**: feature-engineering plugin v1.0.0
"""

    # 로그 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(log)

    return log


def main():
    parser = argparse.ArgumentParser(
        description='특성 엔지니어링 및 데이터 전처리',
        formatter_class=argparse.RawDescriptionHelpFormatter
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
        help='타겟 변수 컬럼명 (전처리에서 제외)'
    )
    parser.add_argument(
        '--scaling-strategy',
        type=str,
        choices=['robust', 'standard', 'minmax'],
        default='robust',
        help='스케일링 전략 (기본값: robust)'
    )
    parser.add_argument(
        '--time-features',
        type=str,
        help='시간 특성 (comma-separated: hour,day,cyclical)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/processed',
        help='전처리 데이터 저장 디렉토리'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("특성 엔지니어링 시작")
    print("=" * 60)

    # 데이터 로드
    df = load_data(args.data_path)
    original_shape = df.shape
    dataset_name = Path(args.data_path).stem

    # 타겟 변수 분리
    if args.target_column and args.target_column in df.columns:
        y = df[args.target_column]
        X = df.drop(columns=[args.target_column])
        print(f"\n타겟 변수 분리: {args.target_column}")
    else:
        X = df
        y = None

    # 시간 특성 추출
    time_features_info = None
    if args.time_features:
        features = [f.strip() for f in args.time_features.split(',')]
        X, new_time_features = extract_time_features(X, features=features)
        if new_time_features:
            time_features_info = {
                'original_column': 'Time',
                'new_features': new_time_features
            }

    # 스케일링
    # V1-V28은 이미 정규화되어 있으므로 제외
    exclude_cols = [f'V{i}' for i in range(1, 29)]  # V1-V28
    X, scaler = scale_features(
        X,
        target_column=None,
        strategy=args.scaling_strategy,
        exclude_cols=exclude_cols
    )

    scaling_info = None
    if scaler is not None:
        scaled_columns = [col for col in X.columns if 'scaled' in col or col == 'Amount']
        scaling_info = {
            'strategy': args.scaling_strategy,
            'scaled_columns': [col.replace('_scaled', '') for col in scaled_columns if '_scaled' in col]
        }

    final_shape = X.shape

    # 출력 디렉토리 생성
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_dir = Path('outputs/models')
    model_dir.mkdir(parents=True, exist_ok=True)

    report_dir = Path('outputs/reports')
    report_dir.mkdir(parents=True, exist_ok=True)

    # 전처리된 데이터 저장
    X_path = output_dir / f"{dataset_name}_processed_X.csv"
    X.to_csv(X_path, index=False)
    print(f"\n✓ 특성 데이터 저장: {X_path}")

    if y is not None:
        y_path = output_dir / f"{dataset_name}_processed_y.csv"
        y.to_csv(y_path, index=False, header=True)
        print(f"✓ 타겟 데이터 저장: {y_path}")

    # 전처리 파이프라인 저장
    if scaler is not None:
        pipeline_path = model_dir / f"{dataset_name}_preprocessing_pipeline.pkl"
        joblib.dump(scaler, pipeline_path)
        print(f"✓ 전처리 파이프라인 저장: {pipeline_path}")

    # 로그 생성
    log_path = report_dir / f"{dataset_name}_feature_engineering_log.md"
    generate_log(
        dataset_name,
        original_shape,
        final_shape,
        scaling_info,
        time_features_info,
        log_path
    )
    print(f"✓ 변환 로그 저장: {log_path}")

    # 요약 출력
    print(f"\n{'=' * 60}")
    print("특성 엔지니어링 완료")
    print(f"{'=' * 60}")
    print(f"\n📊 데이터셋: {dataset_name}")
    print(f"   원본: {original_shape[0]:,}건 × {original_shape[1]}개 특성")
    print(f"   최종: {final_shape[0]:,}건 × {final_shape[1]}개 특성")
    print(f"   변화: {final_shape[1] - original_shape[1]:+d}개 특성")

    print(f"\n📁 출력:")
    print(f"   특성 데이터: {X_path}")
    if y is not None:
        print(f"   타겟 데이터: {y_path}")
    if scaler is not None:
        print(f"   파이프라인: {pipeline_path}")
    print(f"   로그: {log_path}")

    print(f"\n다음 단계:")
    if y is not None and len(pd.Series(y).value_counts()) == 2:
        # 이진 분류인 경우
        value_counts = pd.Series(y).value_counts()
        imbalance_ratio = value_counts.max() / value_counts.min()
        if imbalance_ratio > 10:
            print("   /handle-imbalance --method smote")
    print("   /train-models --algorithms xgboost,lightgbm\n")


if __name__ == "__main__":
    main()
