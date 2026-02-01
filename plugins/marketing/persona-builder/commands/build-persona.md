---
name: build-persona
description: 세그먼트를 기반으로 상세한 페르소나 카드를 생성합니다.
arguments:
  - name: segment
    description: 페르소나를 생성할 세그먼트 이름 또는 설명
    required: true
  - name: brand-context
    description: 브랜드 관련 컨텍스트 파일 경로 (선택)
    required: false
  - name: include-empathy-map
    description: 공감 맵 포함 여부 (기본값: true)
    required: false
    default: "true"
  - name: include-image-prompt
    description: AI 이미지 생성용 프롬프트 포함 여부 (기본값: true)
    required: false
    default: "true"
---

# /build-persona

세그먼트 특성을 구체적인 인물로 형상화하여 상세한 페르소나 카드를 생성합니다.

## Usage

```bash
/build-persona --segment "워라밸 직장인"
/build-persona --segment "트렌드세터" --brand-context "./brand-brief.md"
/build-persona --segment "프리미엄 애호가" --include-empathy-map true
```

## What This Command Does

1. **세그먼트 분석**
   - 세그먼트 핵심 특성 추출
   - 브랜드 컨텍스트 반영

2. **페르소나 설계**
   - `persona-architect` 에이전트가 인물 설계
   - 배경 스토리 및 일상 시나리오 작성

3. **공감 맵 작성** (옵션)
   - Says/Thinks/Does/Feels 프레임워크
   - 고객 여정 터치포인트

4. **이미지 프롬프트 생성** (옵션)
   - AI 이미지 생성용 상세 프롬프트
   - `kie-image-generator` 연동 가능

## Output Structure

```markdown
# 페르소나: [이름]

## 프로필 이미지 프롬프트
> Professional photo of a [나이]s Korean [성별], [직업],
> wearing [복장], in [환경], warm and professional expression,
> lifestyle photography style

## 기본 정보
| 항목 | 내용 |
|------|------|
| 이름 | 김지현 |
| 나이 | 32세 |
| 직업 | IT 회사 마케터 |
| 거주지 | 서울 성수동 |
| 가족 | 미혼, 반려묘 1마리 |

## 한 줄 소개
> "바쁜 하루 속에서도 나만의 작은 여유는 포기할 수 없어요"

## 성격 및 가치관
- [성격 특성]
- [가치관]

## 하루 일과
| 시간 | 활동 | 커피 접점 |
|------|------|----------|
| 07:00 | 기상, 홈카페 루틴 | ☕ 드립백 |
| 08:30 | 출근 | |
| 15:00 | 오후 회의 전 | ☕ 테이크아웃 |
| ... | | |

## 니즈 & 페인포인트
### 니즈 (Needs)
1. 간편하지만 품질 좋은 커피
2. 일상 속 작은 여유
3. SNS 공유할 만한 경험

### 페인포인트 (Pain Points)
1. 아침 시간 부족
2. 프랜차이즈 커피 맛에 질림
3. 홈카페 도구 관리 번거로움

## 공감 맵 (Empathy Map)
| Says | Thinks |
|------|--------|
| "오늘도 바빠서 점심 못 먹을 것 같아" | "조금이라도 나만의 시간이 있으면 좋겠다" |

| Does | Feels |
|------|-------|
| 인스타그램에 카페 사진 업로드 | 일과 삶의 균형에 대한 갈등 |

## 미디어 소비
- **SNS**: 인스타그램, 유튜브
- **앱**: 배달의민족, 마켓컬리
- **콘텐츠**: 라이프스타일 브이로그, 카페 투어

## 브랜드 여정 (Customer Journey)
| 단계 | 터치포인트 | 감정 | 기회 |
|------|-----------|------|------|
| 인지 | 인스타그램 광고 | 호기심 | 매력적인 비주얼 |
| 고려 | 리뷰 검색 | 비교 | 진정성 있는 후기 |
| 구매 | 스마트스토어 | 기대 | 간편한 UX |
| 사용 | 집에서 추출 | 만족 | 쉬운 사용법 |
| 재구매 | 정기배송 | 편안 | 할인 혜택 |

## 마케팅 시사점
1. **메시지**: "간편하게, 하지만 프리미엄하게"
2. **채널**: 인스타그램 집중
3. **오퍼**: 첫 정기구독 할인
4. **콘텐츠**: 출근 전 3분 루틴 영상

## 다음 단계
- 채널 전략: `/plan-channels --persona "김지현"`
- 카피 생성: `/generate-copy --persona "김지현"`
- 이미지 생성: `/create-image --prompt "[프로필 이미지 프롬프트]"`
```

## Example

```bash
# 워라밸 직장인 페르소나 생성
/build-persona --segment "워라밸 직장인" --brand-context "./dante-coffee-brand-brief.md"

# 결과: 페르소나 "김지현" 카드 생성
```

## Related Commands

- `/create-segments`: 세그먼트 생성 (선행)
- `/plan-channels`: 채널 전략 (후속)
- `/generate-copy`: 카피 생성 (후속)
- `/create-image`: 페르소나 이미지 생성 (선택)

## Agents Used

- `persona-architect` (필수)
- `customer-insights-partner` (보완)
