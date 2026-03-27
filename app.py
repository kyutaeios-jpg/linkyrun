import os
import re
import json
import random
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from urllib.parse import quote, unquote

import threading
import time as _time

try:
    from curl_cffi import requests as cf_requests
    _USE_CURL_CFFI = True
except ImportError:
    try:
        import requests as cf_requests
        _USE_CURL_CFFI = False
    except ImportError:
        cf_requests = None
        _USE_CURL_CFFI = False

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'namu-speedrun-secret-key-2024')

NAMUWIKI_RAW_URL = "https://namu.wiki/raw/"
DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rankings.db')
)

EXCLUDED_PREFIXES = [
    '파일:', '분류:', 'File:', 'Category:', 'Image:', 'image:',
    '나무위키:', '틀:', 'Template:', '위키:', '사용자:', 'User:',
    '특수기능:', 'Special:', '도움말:', 'Help:',
]

POPULAR_PAGES = [
    "대한민국", "서울특별시", "부산광역시", "고양이", "개", "피자", "축구", "야구",
    "마인크래프트", "포켓몬스터", "BTS", "방탄소년단", "블랙핑크", "아이유",
    "나폴레옹", "스티브 잡스", "일론 머스크", "셰익스피어", "아인슈타인",
    "해리 포터", "반지의 제왕", "스타워즈", "마블 시네마틱 유니버스",
    "인터넷", "컴퓨터", "스마트폰", "유튜브", "넷플릭스", "트위터",
    "지구", "태양", "달", "화성", "우주", "블랙홀",
    "물리학", "화학", "수학", "생물학", "심리학",
    "한국어", "일본", "중국", "미국", "영국", "프랑스", "독일",
    "음악", "영화", "드라마", "애니메이션", "만화",
    "김치", "라면", "치킨", "떡볶이", "삼겹살",
    "조선", "고려", "신라", "고구려", "백제", "로마 제국",
    "제2차 세계 대전", "한국전쟁", "임진왜란", "삼국지",
    "비틀즈", "마이클 잭슨", "레오나르도 다 빈치",
    "농구", "테니스", "올림픽", "월드컵",
]

PRESET_CHALLENGES = [
    {"start": "나무위키:대문", "goal": "대한민국", "name": "홈에서 조국으로"},
    {"start": "고양이",       "goal": "인터넷",   "name": "고양이 인터넷"},
    {"start": "피자",         "goal": "나폴레옹", "name": "피자의 기원"},
    {"start": "마인크래프트", "goal": "스티브 잡스", "name": "게임과 혁신"},
    {"start": "BTS",          "goal": "한국전쟁", "name": "K-POP 역사"},
    {"start": "라면",         "goal": "제2차 세계 대전", "name": "라면의 역사"},
]

# 난이도 기준 (역링크 수 기준, 높을수록 쉬움)
DIFFICULTY_THRESHOLDS = [
    (500, 'easy',      '쉬움',       '#00b894'),
    (100, 'medium',    '보통',       '#fdcb6e'),
    (20,  'hard',      '어려움',     '#e17055'),
    (0,   'very_hard', '매우 어려움', '#d63031'),
]

# 난이도별 페이지 풀 (랜덤 게임 생성용)
PAGES_BY_DIFFICULTY = {
    'easy': [
        "대한민국", "서울특별시", "고양이", "개", "피자", "축구", "야구",
        "마인크래프트", "BTS", "방탄소년단", "블랙핑크", "아이유",
        "나폴레옹", "스티브 잡스", "일론 머스크", "셰익스피어", "아인슈타인",
        "해리 포터", "반지의 제왕", "스타워즈", "마블 시네마틱 유니버스",
        "인터넷", "컴퓨터", "스마트폰", "유튜브", "넷플릭스",
        "지구", "태양", "달", "우주", "수학", "물리학", "화학",
        "한국어", "일본", "중국", "미국", "영국", "프랑스", "독일",
        "음악", "영화", "드라마", "애니메이션", "만화",
        "김치", "라면", "치킨", "떡볶이", "삼겹살",
        "조선", "고려", "로마 제국", "제2차 세계 대전", "한국전쟁",
        "비틀즈", "마이클 잭슨", "올림픽", "월드컵",
        "농구", "테니스", "수영", "포켓몬스터",
    ],
    'medium': [
        "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시",
        "세종대왕", "이순신", "광개토대왕", "장보고", "원효",
        "임진왜란", "병자호란", "동학농민운동", "3.1운동",
        "태권도", "씨름", "바둑", "장기",
        "기후변화", "원자력 발전", "인공지능", "로봇공학", "양자 컴퓨터",
        "모차르트", "베토벤", "바흐", "다윈", "뉴턴",
        "진화론", "빅뱅", "블랙홀", "화성", "목성", "토성",
        "생물학", "심리학", "경제학", "철학", "사회학",
        "페이스북", "애플", "구글", "삼성전자",
        "비빔밥", "냉면", "삼계탕", "갈비", "잡채",
        "고대 이집트", "그리스 신화", "북유럽 신화",
        "프랑스 혁명", "산업혁명", "냉전", "베트남 전쟁",
        "반도체", "블록체인", "가상현실",
        "태풍", "지진", "화산", "쓰나미",
    ],
    'hard': [
        "경복궁", "창덕궁", "수원화성", "불국사", "석굴암",
        "훈민정음", "팔만대장경", "직지심체요절",
        "거북선", "신기전", "화포",
        "단군왕검", "홍익인간", "고조선",
        "가야", "발해", "탐라",
        "왕건", "궁예", "견훤",
        "허준", "정약용", "박지원", "홍대용",
        "신윤복", "김홍도", "안중근", "윤봉길",
        "윤동주", "김소월", "이상", "황순원",
        "고려청자", "조선백자", "분청사기",
        "판소리", "가야금", "거문고", "해금",
        "무궁화", "진달래", "개나리", "벚꽃",
        "에베레스트", "아마존강", "나일강", "미시시피강",
        "바이킹", "십자군 전쟁", "몽골 제국",
        "니콜라 테슬라", "마리 퀴리", "갈릴레오 갈릴레이",
        "메소포타미아", "페르시아 제국", "오스만 제국",
        "양자역학", "열역학", "전자기학",
    ],
    'very_hard': [
        "봉수", "파발", "역참", "조운",
        "주자학", "양명학", "실학", "성리학",
        "국자감", "성균관", "향교", "서원",
        "공민왕", "우왕", "광해군", "연산군",
        "정유재란", "병인양요", "신미양요", "강화도조약",
        "을사조약", "형사정책", "행정법",
        "천문학", "지질학", "고고학", "인류학",
        "언어학", "기호학", "해석학", "위상수학",
        "나선은하", "성운", "중성자별", "백색왜성",
        "세포생물학", "분자생물학", "유전공학",
        "마키아벨리", "홉스", "로크", "루소",
        "임마누엘 칸트", "게오르크 헤겔", "프리드리히 니체",
        "소크라테스", "플라톤", "아리스토텔레스",
        "스콜라 철학", "합리주의", "경험주의",
        "고구려 고분벽화", "첨성대", "측우기",
        "향약집성방", "동의보감", "의방유취",
    ],
}


# ── DB 초기화 ─────────────────────────────────────────────────

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS rankings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname   TEXT    NOT NULL,
            start_page TEXT    NOT NULL,
            goal_page  TEXT    NOT NULL,
            elapsed_ms INTEGER NOT NULL,
            hops       INTEGER NOT NULL,
            path       TEXT    NOT NULL,
            difficulty TEXT    NOT NULL DEFAULT 'unknown',
            created_at TEXT    NOT NULL
        )''')

init_db()


# ── Playwright 브라우저 풀 ─────────────────────────────────────

_pw_lock     = threading.Lock()
_pw_instance = None
_pw_browser  = None
_pw_context  = None
_links_cache: dict = {}   # {title: (links, timestamp)}
CACHE_TTL = 600           # 10분


def _get_pw_context():
    """Playwright 컨텍스트 레이지 초기화 (프로세스 당 1개)."""
    global _pw_instance, _pw_browser, _pw_context
    if _pw_context is not None:
        return _pw_context
    try:
        from playwright.sync_api import sync_playwright
        _pw_instance = sync_playwright().start()
        _pw_browser  = _pw_instance.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox',
                  '--disable-dev-shm-usage', '--single-process'],
        )
        _pw_context = _pw_browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
            locale='ko-KR',
            viewport={'width': 1280, 'height': 800},
        )
    except Exception as e:
        print(f'[Playwright] init error: {e}')
        _pw_context = None
    return _pw_context


def get_page_links(title: str):
    """Playwright로 나무위키 /w/{title} 렌더링 후 내부 링크 추출."""
    now = _time.time()
    if title in _links_cache:
        links, ts = _links_cache[title]
        if now - ts < CACHE_TTL:
            return links

    with _pw_lock:
        try:
            ctx = _get_pw_context()
            if ctx is None:
                return None
            page = ctx.new_page()
            try:
                page.add_init_script(
                    'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
                )
                page.goto(
                    f'https://namu.wiki/w/{quote(title)}',
                    wait_until='domcontentloaded', timeout=15000,
                )
                page.wait_for_selector('a[href^="/w/"]', timeout=12000)

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

                _links_cache[title] = (links, now)
                return links
            finally:
                page.close()
        except Exception as e:
            print(f'[Playwright] {title}: {e}')
            return None


# ── 레거시 scraper (데스크탑 wiki_fetcher 폴백용) ──────────────

_wiki_fetcher = None


def set_wiki_fetcher(fetcher):
    global _wiki_fetcher
    _wiki_fetcher = fetcher


def _fetch(url: str, timeout: int = 10):
    if _USE_CURL_CFFI:
        return cf_requests.get(url, impersonate='chrome124', timeout=timeout)
    if cf_requests:
        return cf_requests.get(url, timeout=timeout)
    raise RuntimeError('no HTTP client available')


# ── 나무위키 fetching ──────────────────────────────────────────

def get_raw_content(title):
    if _wiki_fetcher is not None:
        return _wiki_fetcher(title)
    url = NAMUWIKI_RAW_URL + quote(title)
    try:
        response = _fetch(url)
        if response.status_code != 200:
            return None
        text = response.text
        if text.strip().lower().startswith(('<!doctype', '<html')):
            return None
        return text
    except Exception:
        return None


def get_backlink_count(title: str):
    """나무위키 역링크 수 반환. 실패하면 None."""
    if cf_requests is None:
        return None
    url = f'https://namu.wiki/backlink/{quote(title)}'
    try:
        resp = _fetch(url, timeout=8)
        if resp.status_code != 200:
            return None
        text = resp.text
        if 'Just a moment' in text or 'cf-challenge' in text:
            return None
        m = re.search(r'"totalCount"\s*:\s*(\d+)', text)
        if m:
            return int(m.group(1))
        items = len(re.findall(r'<a [^>]*href="/w/', text))
        return items if items > 0 else None
    except Exception:
        return None


def classify_difficulty(count, title: str):
    """역링크 수(또는 휴리스틱)로 난이도 분류."""
    if count is not None:
        for threshold, key, label, color in DIFFICULTY_THRESHOLDS:
            if count >= threshold:
                return key, label, color
        return 'very_hard', '매우 어려움', '#d63031'
    # Cloudflare 차단 시 휴리스틱 폴백
    if title in POPULAR_PAGES:
        return 'easy', '쉬움', '#00b894'
    return 'medium', '보통', '#fdcb6e'


# ── 링크 파싱 ─────────────────────────────────────────────────

def parse_internal_links(content):
    pattern = r'\[\[([^\[\]]+)\]\]'
    matches = re.findall(pattern, content)

    seen = set()
    links = []

    for match in matches:
        parts = match.split('|')
        raw_link = parts[0].strip()
        display = parts[-1].strip() if len(parts) > 1 else ''
        page_title = raw_link.split('#')[0].strip()

        if not page_title:
            continue
        if any(page_title.startswith(p) for p in EXCLUDED_PREFIXES):
            continue
        if page_title.startswith(('http://', 'https://', '#')):
            continue
        if page_title in seen:
            continue
        seen.add(page_title)

        links.append({
            'title': page_title,
            'display': display if display else page_title,
        })

    return links


# ── Jinja 필터 ────────────────────────────────────────────────

@app.template_filter('encode_uri')
def encode_uri_filter(s):
    return quote(str(s), safe='')


# ── Routes ────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', presets=PRESET_CHALLENGES)


@app.route('/page/<path:title>')
def page(title):
    title = unquote(title)
    goal  = request.args.get('goal', '')

    # 웹 폴백: Playwright로 실제 페이지 링크 추출
    if _wiki_fetcher is not None:
        content = _wiki_fetcher(title)
        links   = parse_internal_links(content) if content else []
        error   = content is None
    else:
        links = get_page_links(title)
        error = links is None
        if error:
            links = []

    is_goal = bool(goal) and title.strip() == goal.strip()
    status  = 404 if error else 200
    return render_template('page.html',
                           title=title, links=links, goal=goal,
                           is_goal=is_goal, error=error), status


@app.route('/api/links/<path:title>')
def api_links(title):
    title = unquote(title)
    if _wiki_fetcher is not None:
        content = _wiki_fetcher(title)
        if content is None:
            return jsonify({'error': 'Page not found'}), 404
        links = parse_internal_links(content)
    else:
        links = get_page_links(title)
        if links is None:
            return jsonify({'error': 'Page not found'}), 404
    return jsonify({'title': title, 'links': links, 'count': len(links)})


@app.route('/api/random')
def api_random():
    count = min(int(request.args.get('count', 5)), 20)
    pages = random.sample(POPULAR_PAGES, min(count, len(POPULAR_PAGES)))
    return jsonify({'pages': pages})


@app.route('/api/random-game')
def api_random_game():
    """난이도에 맞는 랜덤 시작/목표 페이지 쌍 반환."""
    difficulty = request.args.get('difficulty', 'easy')
    pool = PAGES_BY_DIFFICULTY.get(difficulty, PAGES_BY_DIFFICULTY['easy'])
    if len(pool) < 2:
        return jsonify({'error': 'not enough pages'}), 500
    start, goal = random.sample(pool, 2)
    return jsonify({'start': start, 'goal': goal, 'difficulty': difficulty})


@app.route('/api/exists/<path:title>')
def api_exists(title):
    content = get_raw_content(title)
    return jsonify({'exists': content is not None, 'title': title})


@app.route('/api/difficulty/<path:title>')
def api_difficulty(title):
    title = unquote(title)
    count = get_backlink_count(title)
    key, label, color = classify_difficulty(count, title)
    return jsonify({
        'title': title,
        'backlinks': count,
        'difficulty': key,
        'label': label,
        'color': color,
    })


@app.route('/api/ranking', methods=['GET', 'POST'])
def api_ranking():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        nickname = str(data.get('nickname', '')).strip()[:20]
        if not nickname:
            return jsonify({'error': 'nickname required'}), 400

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                '''INSERT INTO rankings
                   (nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (nickname,
                 str(data.get('start', '')),
                 str(data.get('goal', '')),
                 int(data.get('elapsed_ms', 0)),
                 int(data.get('hops', 0)),
                 json.dumps(data.get('path', [])),
                 str(data.get('difficulty', 'unknown')),
                 datetime.utcnow().isoformat())
            )
            new_id = cur.lastrowid

        return jsonify({'ok': True, 'id': new_id})

    # GET
    difficulty = request.args.get('difficulty', '').strip()
    limit = min(int(request.args.get('limit', 20)), 50)

    with sqlite3.connect(DB_PATH) as conn:
        if difficulty:
            rows = conn.execute(
                '''SELECT id, nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, created_at
                   FROM rankings WHERE difficulty = ?
                   ORDER BY elapsed_ms ASC, hops ASC LIMIT ?''',
                (difficulty, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                '''SELECT id, nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, created_at
                   FROM rankings ORDER BY elapsed_ms ASC, hops ASC LIMIT ?''',
                (limit,)
            ).fetchall()

    results = [
        {'id': r[0], 'nickname': r[1], 'start': r[2], 'goal': r[3],
         'elapsed_ms': r[4], 'hops': r[5],
         'path': json.loads(r[6]), 'difficulty': r[7], 'created_at': r[8]}
        for r in rows
    ]
    return jsonify({'rankings': results, 'difficulty': difficulty})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
