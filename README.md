# Toss Stock Monitor

토스증권 Open API 기반 모바일 주식 시세 모니터입니다.

## 가장 쉬운 실행 방법

아래 버튼을 눌러 Render에 바로 배포합니다.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/songhajonga-cpu/toss-stock-monitor)

배포 화면에서 아래 2개만 입력하면 됩니다.

- `TOSS_CLIENT_ID` : 토스증권 Client ID
- `TOSS_CLIENT_SECRET` : 토스증권 Client Secret

Secret 값은 GitHub 파일이나 공개 화면에 올리지 마세요.

배포가 끝나면 Render가 `https://...onrender.com` 주소를 만들어 줍니다.
그 주소를 휴대폰 홈 화면에 추가해서 사용하면 됩니다.

## 현재 기능

- 관심종목 현재가 조회
- 5초 자동 새로고침
- 관심종목 브라우저 저장
- 모바일 화면 지원
- API 자격증명 서버 환경변수 관리

## 로컬 실행

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 참고

Render 무료 Web Service는 일정 시간 사용하지 않으면 절전 상태가 될 수 있습니다.
다시 접속하면 자동으로 다시 시작합니다.
