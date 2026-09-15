import os
import re
import time
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

BASE_URL = "https://openapi.tossinvest.com"
TOKEN_URL = f"{BASE_URL}/oauth2/token"
SYMBOL_RE = re.compile(r"^[A-Za-z0-9.\-]+$")
STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Toss Stock Monitor", version="0.1.0")

_token_cache = {
    "value": None,
    "expires_at": 0.0,
}


async def get_access_token() -> str:
    direct_token = os.getenv("TOSS_ACCESS_TOKEN", "").strip()
    if direct_token:
        return direct_token

    now = time.time()
    cached = _token_cache["value"]
    if cached and now < _token_cache["expires_at"] - 60:
        return cached

    client_id = os.getenv("TOSS_CLIENT_ID", "").strip()
    client_secret = os.getenv("TOSS_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=503,
            detail="TOSS_ACCESS_TOKEN 또는 TOSS_CLIENT_ID/TOSS_CLIENT_SECRET 환경변수가 필요합니다.",
        )

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=httpx.BasicAuth(client_id, client_secret),
            headers={"Accept": "application/json"},
        )

    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail=f"토스증권 액세스 토큰 발급 실패: HTTP {response.status_code}",
        )

    data = response.json()
    token: Optional[str] = data.get("access_token") or data.get("accessToken")
    if not token:
        raise HTTPException(status_code=502, detail="토큰 응답에서 access_token을 찾지 못했습니다.")

    expires_in = int(data.get("expires_in") or data.get("expiresIn") or 3600)
    _token_cache["value"] = token
    _token_cache["expires_at"] = now + expires_in
    return token


def parse_symbols(raw: str) -> list[str]:
    symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]
    if not symbols:
        raise HTTPException(status_code=400, detail="종목 심볼이 필요합니다.")
    if len(symbols) > 200:
        raise HTTPException(status_code=400, detail="한 번에 최대 200개 종목까지 조회할 수 있습니다.")
    invalid = [s for s in symbols if not SYMBOL_RE.fullmatch(s)]
    if invalid:
        raise HTTPException(status_code=400, detail=f"잘못된 종목 심볼: {', '.join(invalid[:5])}")
    return symbols


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.get("/api/prices")
async def prices(symbols: str = Query(..., description="쉼표로 구분한 종목 심볼")):
    parsed = parse_symbols(symbols)
    token = await get_access_token()

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{BASE_URL}/api/v1/prices",
            params={"symbols": ",".join(parsed)},
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="토스증권 API 호출 한도를 초과했습니다.")
    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail=f"토스증권 시세 조회 실패: HTTP {response.status_code}",
        )

    return response.json()


@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
