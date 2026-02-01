---
name: plan-channels
description: 페르소나 기반 소셜 미디어 채널 전략을 수립합니다.
arguments:
  - name: persona
    description: 타겟 페르소나 이름 또는 파일 경로
    required: true
  - name: channels
    description: 분석할 채널 목록 (콤마 구분, 기본값: instagram,youtube,tiktok)
    required: false
    default: "instagram,youtube,tiktok"
  - name: include-calendar
    description: 콘텐츠 캘린더 포함 여부 (기본값: true)
    required: false
    default: "true"
---

# /plan-channels

페르소나의 미디어 소비 패턴을 분석하여 최적의 채널 전략을 수립합니다.

## Usage

```bash
/plan-channels --persona "김지현"
/plan-channels --persona "./persona-jihyun.md" --channels "instagram,naver,kakao"
/plan-channels --persona "트렌드세터" --include-calendar true
```

## What This Command Does

1. **페르소나 미디어 분석**
   - 미디어 소비 습관 파악
   - 선호 콘텐츠 유형 분석

2. **채널 선정**
   - `social-strategy-director`가 채널 믹스 설계
   - Primary/Secondary/Support 분류

3. **콘텐츠 전략**
   - 채널별 콘텐츠 필러 정의
   - 콘텐츠 포맷 및 빈도 설정

4. **캘린더 생성** (옵션)
   - 주간 콘텐츠 캘린더 템플릿
   - 포스팅 일정 권장

## Output Structure

```markdown
# Social Media Strategy

## 타겟 페르소나
- 이름: [페르소나명]
- 미디어 소비 특성: [특성 요약]

---

## 채널 전략

### Primary Channel: Instagram

**역할**: 브랜드 인지도 구축, 비주얼 스토리텔링
**목표 지표**: 팔로워 +1,000/월, 참여율 3%+

| 포맷 | 빈도 | 콘텐츠 유형 |
|------|------|-----------|
| 피드 | 주 3회 | 제품 사진, 라이프스타일 |
| 릴스 | 주 2회 | 레시피, 일상 |
| 스토리 | 매일 | 비하인드, 설문 |

**콘텐츠 필러**:
1. 제품 소개 (20%)
2. 브랜드 스토리 (20%)
3. 라이프스타일 (30%)
4. 교육 콘텐츠 (20%)
5. UGC (10%)

---

### Secondary Channel: YouTube

**역할**: 심층 콘텐츠, 신뢰 구축
**목표 지표**: 구독자 +500/월, 평균 조회 1,000+

| 포맷 | 빈도 | 콘텐츠 유형 |
|------|------|-----------|
| 롱폼 | 주 1회 | 원두 리뷰, 추출 가이드 |
| 쇼츠 | 주 2회 | 빠른 팁, 레시피 |

---

### Support Channel: KakaoTalk

**역할**: CRM, 프로모션
**목표**: 채널 친구 5,000+

---

## 콘텐츠 캘린더 (주간)

| 요일 | 채널 | 포맷 | 콘텐츠 아이디어 | 필러 |
|------|------|------|---------------|------|
| 월 | IG | 피드 | 새로운 한 주 시작 | 라이프스타일 |
| 화 | IG | 릴스 | 3분 레시피 | 교육 |
| 수 | IG | 스토리 | 설문: 오늘의 커피 | 인터랙션 |
| 목 | YouTube | 쇼츠 | 빠른 팁 | 교육 |
| 금 | IG | 피드 | 주말 추천 원두 | 제품 |
| 토 | YouTube | 롱폼 | 원두 리뷰 | 교육 |
| 일 | IG | 스토리 | UGC 리포스트 | UGC |

---

## 해시태그 전략

### 브랜드 해시태그
- #단테커피 #DanteCoffee #한잔의여유

### 카테고리 해시태그
- #스페셜티커피 #홈카페 #드립커피 #커피스타그램

### 트렌드 해시태그
- (시즌별 업데이트)

---

## KPI 및 측정

| 채널 | 지표 | 목표 | 측정 주기 |
|------|------|------|---------|
| Instagram | 팔로워 성장 | +1,000/월 | 주간 |
| | 참여율 | 3%+ | 주간 |
| YouTube | 구독자 | +500/월 | 주간 |
| | 평균 조회 | 1,000+ | 주간 |

---

## 다음 단계
- 카피 생성: `/generate-copy --channel instagram --persona "[페르소나]"`
- 이미지 생성: `/create-image --concept "라이프스타일 커피"`
```

## Example

```bash
/plan-channels --persona "김지현 (워라밸 직장인)"
```

## Related Commands

- `/build-persona`: 페르소나 생성 (선행)
- `/generate-copy`: 카피 생성 (후속)
- `/create-image`: 이미지 생성 (후속)

## Skills Used

- `channel-roadmap`: 채널 로드맵 프레임워크
- `content-pillars`: 콘텐츠 필러 설계

## Agents Used

- `social-strategy-director` (필수)
- `channel-analyst` (보조)
