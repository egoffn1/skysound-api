from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import httpx
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote

app = FastAPI(title="SkySound Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = "https://skysound7.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

@app.get("/search")
async def search(q: str = Query(...)):
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as c:
        r = await c.get(f"{BASE}/api/search?query={quote(q)}", headers=HEADERS)
        if r.status_code != 200:
            return {"error": "search failed"}
        data = r.json()
        url = data.get("url", "")
        # fetch the artist page
        r2 = await c.get(url, headers=HEADERS)
        if r2.status_code != 200:
            return {"error": "page load failed"}
        try:
            j = r2.json()
        except:
            return {"error": "not json"}
        html = j.get("xx1_content", "")
        if not html:
            return {"error": "no content"}
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for li in soup.select("li.__adv_list_track"):
            artist_el = li.select_one(".playlist-name-artist")
            title_el = li.select_one(".playlist-name-title em")
            dur_el = li.select_one(".playlist-duration")
            stream_el = li.select_one(".playlist-play")
            down_el = li.select_one(".playlist-down")
            artist = artist_el.get_text(strip=True) if artist_el else ""
            title = title_el.get_text(strip=True) if title_el else ""
            duration = dur_el.get_text(strip=True) if dur_el else ""
            stream_url = stream_el.get("data-url") if stream_el else ""
            down_page = down_el.get("href") if down_el else ""
            results.append({
                "artist": artist,
                "title": title,
                "duration": duration,
                "stream_url": stream_url,
                "download_page": down_page,
            })
        return {"query": q, "results": results}

@app.get("/stream")
async def stream(url: str = Query(...)):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        r = await c.get(url)
        return Response(content=r.content, media_type=r.headers.get("content-type", "audio/mpeg"))

@app.get("/download")
async def download(url: str = Query(...)):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        r = await c.get(url)
        return Response(content=r.content, media_type=r.headers.get("content-type", "audio/mpeg"),
                        headers={"Content-Disposition": 'attachment'})

@app.get("/track-url")
async def track_url(url: str = Query(...)):
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as c:
        r = await c.get(url, headers=HEADERS)
        if r.status_code != 200:
            return {"error": "page not found"}
        try:
            j = r.json()
            html = j.get("xx1_content", "")
            if not html:
                html = j.get("content", "")
        except:
            return {"error": "not json"}
        if not html:
            return {"error": "no content"}
        soup = BeautifulSoup(html, "html.parser")
        artist_el = soup.select_one(".onesongblock-name-artist")
        title_el = soup.select_one(".onesongblock-name-title")
        down_link = soup.select_one('a[href*="fine.sunproxy.net"]')
        stream_el = soup.select_one('[data-urlsong]')
        artist = artist_el.get_text(strip=True) if artist_el else ""
        title = title_el.get_text(strip=True) if title_el else ""
        download_url = down_link.get("href") if down_link else ""
        stream_url = stream_el.get("data-urlsong") if stream_el else ""
        return {
            "artist": artist,
            "title": title,
            "download_url": download_url,
            "stream_url": stream_url,
        }
