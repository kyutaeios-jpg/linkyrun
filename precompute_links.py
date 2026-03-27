#!/usr/bin/env python3
"""
로컬에서 실행해서 모든 난이도 페이지의 링크를 미리 추출합니다.
결과는 static/precomputed_links.json 에 저장됩니다.
"""
import json
import time
import threading
from urllib.parse import quote, unquote
from app import PAGES_BY_DIFFICULTY, EXCLUDED_PREFIXES

_pw_lock = threading.Lock()

def fetch_links(title: str, browser):
    from playwright.sync_api import TimeoutError as PWTimeout
    try:
        ctx = browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
            locale='ko-KR',
            viewport={'width': 1280, 'height': 800},
        )
        page = ctx.new_page()
        try:
            page.add_init_script(
                'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
            )
            page.goto(
                f'https://namu.wiki/w/{quote(title)}',
                wait_until='domcontentloaded', timeout=30000,
            )
            page.wait_for_selector('a[href^="/w/"]', timeout=20000)
            raw = page.eval_on_selector_all(
                'a[href^="/w/"]',
                'els => els.map(e => ({href: e.getAttribute("href"), '
                'text: e.innerText.trim()}))',
            )
            seen = set()
            links = []
            for item in raw:
                href = item.get('href', '')
                text = item.get('text', '').strip()
                if not href.startswith('/w/') or not text:
                    continue
                page_title = unquote(href[3:]).split('#')[0].strip()
                if not page_title:
                    continue
                if any(page_title.startswith(p) for p in EXCLUDED_PREFIXES):
                    continue
                if page_title in seen:
                    continue
                seen.add(page_title)
                links.append({'title': page_title, 'display': text})
            return links
        finally:
            page.close()
            ctx.close()
    except Exception as e:
        print(f'  FAIL {title}: {e}')
        return None


def main():
    from playwright.sync_api import sync_playwright

    all_pages = set()
    for pages in PAGES_BY_DIFFICULTY.values():
        all_pages.update(pages)
    all_pages = sorted(all_pages)
    print(f'총 {len(all_pages)}개 페이지 추출 시작...')

    result = {}
    failed = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox',
                  '--disable-dev-shm-usage'],
        )
        for i, title in enumerate(all_pages, 1):
            print(f'[{i}/{len(all_pages)}] {title} ...', end=' ', flush=True)
            links = fetch_links(title, browser)
            if links is not None:
                result[title] = links
                print(f'OK ({len(links)}개)')
            else:
                failed.append(title)
                print('FAILED')
            time.sleep(0.5)  # 너무 빠르게 요청하지 않도록

        browser.close()

    out_path = 'static/precomputed_links.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, separators=(',', ':'))

    print(f'\n완료: {len(result)}개 성공, {len(failed)}개 실패')
    if failed:
        print('실패 목록:', failed)
    print(f'저장: {out_path}')


if __name__ == '__main__':
    main()
