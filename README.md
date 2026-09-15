# Toss Stock Monitor

토스증권 Open API 기반의 모바일 친화형 주식 시세 모니터입니다.

## 현재 기능
- 관심종목 현재가 조회
- 5초 자동 새로고침
- 관심종목을 휴대폰 브라우저에 저장
- 국내/미국 주식 심볼 지원
- API 자격증명은 서버 환경변수로만 관리

## 환경변수

`.env.example`을 참고하세요.

- `TOSS_ACCESS_TOKEN`: 이미 발급된 액세스 토큰이 있으면 사용
- `TOSS_CLIENT_ID`: Client ID
- `TOSS_CLIENT_SECRET`: Client Secret

액세스 토큰이 있으면 Client ID/Secret보다 우선 사용합니다.

## 실행

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

브라우저에서 `http://localhost:8000` 접속.

## 보안
Client Secret, Access Token, 계좌번호는 GitHub 저장소에 올리지 마세요.
