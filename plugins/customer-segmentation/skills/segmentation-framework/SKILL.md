---
name: segmentation-framework
description: 고객 세그먼테이션 방법론 및 프레임워크 가이드
version: 1.0.0
author: Dante Labs
tags:
  - segmentation
  - customer
  - targeting
---

# Customer Segmentation Framework

효과적인 고객 세그먼테이션을 위한 체계적인 방법론을 제공합니다.

## Segmentation Criteria (STP)

### 1. Segmenting (세분화)

#### 인구통계적 세분화 (Demographic)
| 기준 | 예시 |
|------|------|
| 연령 | 20대, 30대, 40대+ |
| 성별 | 남성, 여성 |
| 소득 | 저소득, 중산층, 고소득 |
| 직업 | 학생, 직장인, 자영업, 프리랜서 |
| 가구 | 1인 가구, 2인 가구, 가족 |

#### 심리적 세분화 (Psychographic)
| 기준 | 예시 |
|------|------|
| 라이프스타일 | 건강지향, 편의추구, 가성비 |
| 가치관 | 품질, 경험, 가격, 지속가능성 |
| 성격 | 모험적, 보수적, 트렌디 |
| 관심사 | 카페문화, 홈카페, 바리스타 |

#### 행동적 세분화 (Behavioral)
| 기준 | 예시 |
|------|------|
| 사용 빈도 | Heavy/Medium/Light User |
| 구매 동기 | 일상, 선물, 특별한 날 |
| 브랜드 충성도 | 충성, 스위칭, 신규 |
| 채널 선호 | 온라인, 오프라인, 옴니채널 |

#### 지리적 세분화 (Geographic)
| 기준 | 예시 |
|------|------|
| 지역 | 수도권, 광역시, 지방 |
| 도시 규모 | 대도시, 중소도시, 소도시 |
| 기후 | 사계절, 열대 |

### 2. Targeting (타겟팅)

#### 세그먼트 평가 기준
1. **Size (규모)**: 충분한 시장 크기인가?
2. **Growth (성장성)**: 성장 잠재력이 있는가?
3. **Accessibility (접근성)**: 효과적으로 도달 가능한가?
4. **Profitability (수익성)**: 수익을 낼 수 있는가?
5. **Fit (적합성)**: 브랜드와 잘 맞는가?

#### 타겟팅 전략
- **집중화 (Concentrated)**: 단일 세그먼트 집중
- **차별화 (Differentiated)**: 복수 세그먼트 각각 대응
- **비차별화 (Undifferentiated)**: 대량 마케팅

### 3. Positioning (포지셔닝)

각 세그먼트에 맞는 포지셔닝 전략 수립

## Segment Profile Template

```markdown
## 세그먼트: [세그먼트명]

### 한 줄 정의
> [세그먼트를 한 문장으로 정의]

### 인구통계적 특성
- 연령:
- 성별:
- 직업:
- 소득 수준:
- 거주 지역:

### 심리적 특성
- 라이프스타일:
- 가치관:
- 관심사:
- 미디어 소비:

### 행동적 특성
- 구매 빈도:
- 선호 채널:
- 의사결정 요인:
- 정보 탐색 행동:

### 니즈 (Needs)
1.
2.
3.

### 페인포인트 (Pain Points)
1.
2.
3.

### 브랜드 접점
- 인지 채널:
- 구매 채널:
- 관계 유지:

### 세그먼트 크기
- 추정 규모:
- 성장률:
- 브랜드 적합도: ★★★★☆
```

## Segmentation Validation Checklist

- [ ] 각 세그먼트가 명확히 구분되는가?
- [ ] 세그먼트 크기가 충분한가?
- [ ] 세그먼트에 접근 가능한가?
- [ ] 세그먼트가 측정 가능한가?
- [ ] 세그먼트별 차별화 전략이 가능한가?
- [ ] 세그먼트가 시간에 따라 안정적인가?

## Example: Coffee Brand Segments

| 세그먼트 | 특성 | 니즈 | 채널 |
|---------|------|------|------|
| 워라밸 직장인 | 30대, 바쁜 일상 | 편리 + 품질 | 온라인, 오피스 |
| 트렌드세터 | 2030, SNS 활발 | 경험 + 공유 | 인스타, 카페 |
| 프리미엄 애호가 | 40대+, 전문성 | 최고 품질 | 전문점, DM |
| 홈카페 마니아 | 전 연령, DIY | 도구 + 원두 | 유튜브, 커뮤니티 |

## File Storage

세그먼트 분석 문서는 프로젝트의 표준 디렉토리 구조에 저장합니다.

```
{project}/
├── reports/
│   └── strategy/         # 전략 문서 저장 위치
│       ├── segment-profiles.md
│       └── targeting-strategy.md
└── tmp/                  # 초안 및 임시 파일
```

### 파일 명명 규칙

```
{project}/reports/strategy/{document-type}-{date}.md

예시:
reports/strategy/segment-profiles-20240115.md
reports/strategy/targeting-strategy-20240115.md
```

## Usage

이 스킬은 `segmentation-architect` 에이전트가 세그먼트 설계 시 참조합니다.
