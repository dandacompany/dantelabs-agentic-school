# 키움증권 REST API 엔드포인트 레퍼런스

## 인증 (OAuth)

### au10001 - 접근토큰 발급

**Method**: POST
**URL**: `/oauth2/token`
**Content-Type**: application/json

**Request Body**:
```json
{
  "grant_type": "client_credentials",
  "appkey": "YOUR_API_KEY",
  "secretkey": "YOUR_SECRET_KEY"
}
```

**Response**:
```json
{
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다",
  "token_type": "Bearer",
  "token": "ACCESS_TOKEN",
  "expires_dt": "20260206140112"
}
```

---

## 국내주식 - 종목정보

### ka10001 - 주식기본정보요청

**Method**: POST
**URL**: `/api/dostk/stkinfo`
**Content-Type**: application/json;charset=UTF-8

**Request Headers**:
```json
{
  "api-id": "ka10001",
  "authorization": "Bearer {access_token}",
  "Content-Type": "application/json;charset=UTF-8"
}
```

**Request Body**:
```json
{
  "stk_cd": "005930"  // 종목코드 (KRX:005930, NXT:039490_NX, SOR:039490_AL)
}
```

**Response Body (주요 필드)**:
```json
{
  "stk_cd": "005930",           // 종목코드
  "stk_nm": "삼성전자",           // 종목명
  "cur_prc": "-160400",         // 현재가
  "pred_pre": "-8700",          // 전일대비
  "flu_rt": "-5.14",            // 등락률
  "trde_qty": "31734276",       // 거래량
  "mac": "9512858",             // 시가총액
  "per": "32.47",               // PER
  "eps": "4950",                // EPS
  "pbr": "2.77",                // PBR
  "roe": "9.0",                 // ROE
  "bps": "57930",               // BPS
  "250hgst": "+169400",         // 52주 최고가
  "250lwst": "-50800",          // 52주 최저가
  "setl_mm": "12",              // 결산월
  "fav": "100",                 // 액면가
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

### ka10004 - 주식호가요청

**Method**: POST
**URL**: `/api/dostk/stkquot`
**Headers**: api-id=ka10004, authorization

### ka10005 - 주식일주월시분요청

**Method**: POST
**URL**: `/api/dostk/stkchrt`
**Headers**: api-id=ka10005, authorization

---

## 국내주식 - 계좌

### kt00004 - 계좌평가현황요청

**Method**: POST
**URL**: `/api/dostk/acnt`
**Headers**: api-id=kt00004, authorization

### kt00005 - 체결잔고요청

**Method**: POST
**URL**: `/api/dostk/acnt`
**Headers**: api-id=kt00005, authorization

---

## 국내주식 - 거래 (⚠️ 주의)

### kt10000 - 주식 매수주문

**Method**: POST
**URL**: `/api/dostk/order`
**Headers**: api-id=kt10000, authorization

⚠️ **경고**: 실제 계좌에서 실행됨!

### kt10001 - 주식 매도주문

**Method**: POST
**URL**: `/api/dostk/order`
**Headers**: api-id=kt10001, authorization

⚠️ **경고**: 실제 계좌에서 실행됨!

---

## Rate Limiting

모의투자 및 실전투자 환경 모두 요청 횟수 제한이 있습니다.

**권장 사항**:
- 요청 간 최소 0.5~1초 대기
- 연속 조회 시 delay 추가
- HTTP 429 오류 발생 시 대기 시간 증가

**오류 메시지**:
```json
{
  "return_msg": "허용된 요청 개수를 초과하였습니다[1700:허용된 요청 개수를 초과하였습니다. API ID=ka10001]",
  "return_code": 5
}
```

---

## 종목코드 형식

```python
# KRX (국내 주식)
"005930"        # 삼성전자

# NASDAQ
"039490_NX"     # 셀트리온

# NYSE
"039490_AL"     # 셀트리온
```

---

## 응답 코드

| return_code | 의미 |
|-------------|------|
| 0 | 정상 처리 |
| 2 | 입력 값 오류 |
| 3 | 인증 실패 |
| 5 | Rate Limit 초과 |

---

## 참고 문서

- 키움 REST API 문서.xlsx (프로젝트 루트)
- [키움증권 OpenAPI 포털](https://openapi.kiwoom.com/)
