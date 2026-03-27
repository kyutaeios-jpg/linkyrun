import os
import re
import json
import random
import sqlite3
from datetime import datetime
from html import escape as html_escape
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


# 자동완성용 전체 페이지 풀 (난이도 풀 + 인기 페이지 + 추가)
_extra_pages = [
    "삼성전자", "LG전자", "현대자동차", "카카오", "네이버", "쿠팡",
    "손흥민", "류현진", "김연아", "박지성", "이강인", "류준열",
    "뉴진스", "에스파", "르세라핌", "아이브", "세븐틴", "스트레이 키즈",
    "트와이스", "레드벨벳", "소녀시대", "샤이니", "엑소", "방탄소년단",
    "기생충", "오징어 게임", "이상한 변호사 우영우", "무빙",
    "어벤져스", "인터스텔라", "타이타닉", "조커",
    "닌텐도", "플레이스테이션", "Xbox",
    "리그 오브 레전드", "오버워치", "배틀그라운드", "발로란트", "로블록스",
    "원피스", "나루토", "드래곤볼", "귀멸의 칼날", "진격의 거인",
    "슬램덩크", "헌터X헌터", "강철의 연금술사", "도라에몽",
    "서울대학교", "연세대학교", "고려대학교", "카이스트", "포스텍",
    "소주", "맥주", "막걸리", "와인", "커피", "녹차",
    "불교", "기독교", "이슬람교", "힌두교", "유교",
    "테슬라", "SpaceX", "아마존", "메타", "마이크로소프트", "애플",
    "COVID-19", "인플루엔자", "암", "당뇨병",
    "영어", "중국어", "일본어", "스페인어", "프랑스어", "독일어",
    "피카소", "고흐", "모네", "미켈란젤로",
    "도쿄", "오사카", "베이징", "상하이", "뉴욕", "런던", "파리", "로마",
    "히말라야", "알프스산맥", "태평양", "대서양", "지중해",
    "공룡", "호랑이", "사자", "코끼리", "판다", "펭귄", "돌고래",
    "수소", "산소", "탄소", "금", "은", "철",
    "민주주의", "공산주의", "자본주의", "사회주의",
    "세계대전", "냉전", "십자군", "몽골 제국",
    "셰익스피어", "괴테", "톨스토이", "도스토예프스키",
    "모차르트", "베토벤", "쇼팽", "드뷔시",
    "축구", "야구", "농구", "배구", "테니스", "골프", "수영",
    "올림픽", "월드컵", "NBA", "MLB", "EPL",
]
ALL_PAGES = sorted(set(POPULAR_PAGES) |
                   {p for v in PAGES_BY_DIFFICULTY.values() for p in v} |
                   set(_extra_pages))


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


# ── Playwright 전용 스레드 + 작업 큐 ──────────────────────────
# Playwright sync API는 생성된 스레드에서만 사용 가능.
# 모든 Playwright 작업을 단일 전용 스레드에서 처리한다.

import queue as _queue_mod

_pw_task_queue: '_queue_mod.Queue' = _queue_mod.Queue()
_links_cache: dict = {}   # {title: (links, timestamp)}
_html_cache:  dict = {}   # {title: (html,  timestamp)}
CACHE_TTL = 600           # 10분


def _call_pw(func, timeout: int = 70):
    """Playwright 전용 스레드에 작업을 넘기고 결과를 기다린다."""
    event = threading.Event()
    container = [None]

    def wrapped(ctx):
        try:
            container[0] = func(ctx)
        except Exception as e:
            print(f'[PW-thread] error: {e}', flush=True)
            container[0] = None
        finally:
            event.set()

    _pw_task_queue.put(wrapped)
    event.wait(timeout=timeout)
    return container[0]


def _pw_stealth(pg):
    try:
        from playwright_stealth import stealth_sync
        stealth_sync(pg)
    except ImportError:
        pg.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});"
        )


def _playwright_thread():
    """Playwright 전용 데몬 스레드 — 컨텍스트를 소유하고 큐를 소비한다."""
    from playwright.sync_api import sync_playwright
    try:
        pw  = sync_playwright().start()
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir='/tmp/rabbit-hole-pw',
            headless=True,
            args=[
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
            ],
            user_agent=(
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
                'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                'Version/17.0 Mobile/15E148 Safari/604.1'
            ),
            is_mobile=True, has_touch=True,
            locale='ko-KR', timezone_id='Asia/Seoul',
            viewport={'width': 390, 'height': 844},
            extra_http_headers={'Accept-Language': 'ko-KR,ko;q=0.9'},
        )
        print('[PW-thread] 시작 (mobile Safari)', flush=True)

        # 워밍업 — CF 클리어런스 미리 확보
        _do_warmup(ctx)

        while True:
            func = _pw_task_queue.get()
            if func is None:
                break
            func(ctx)
    except Exception as e:
        print(f'[PW-thread] 초기화 실패: {e}', flush=True)


def _pw_fetch_wiki(ctx, title: str):
    """Playwright로 나무위키 페이지 로드 — CF 처리 포함. ctx 스레드에서 호출."""
    pg = ctx.new_page()
    try:
        _pw_stealth(pg)
        url = f'https://namu.wiki/w/{quote(title)}'
        pg.goto(url, wait_until='domcontentloaded', timeout=35000)
        page_title = (pg.title() or '').lower()
        page_url   = pg.url
        print(f'[PW] {title}: url={page_url}  title={pg.title()!r}', flush=True)
        if '__cf_chl' in page_url or 'just a moment' in page_title:
            print(f'[PW] {title}: CF challenge 감지, 대기 중…', flush=True)
            try:
                pg.wait_for_url(lambda u: '__cf_chl' not in u, timeout=22000)
                print(f'[PW] {title}: CF 통과 → {pg.url}', flush=True)
            except Exception:
                print(f'[PW] {title}: CF 미해결', flush=True)
                return None
            # CF 클리어런스 쿠키 획득 후 실제 페이지 재로드
            pg.goto(url, wait_until='domcontentloaded', timeout=25000)
            print(f'[PW] {title}: 재로드 완료 → {pg.url}', flush=True)
        # React SPA 렌더링 대기
        try:
            pg.wait_for_load_state('networkidle', timeout=10000)
        except Exception:
            pass
        pg.wait_for_selector('a[href^="/w/"]', timeout=20000)
        html = pg.content()
        print(f'[PW] {title}: OK {len(html)}B', flush=True)
        return html
    finally:
        pg.close()


def _do_warmup(ctx):
    title = '대한민국'
    print('[Warmup] CF 클리어런스 워밍업 시작…', flush=True)
    try:
        html = _pw_fetch_wiki(ctx, title)
        if html:
            _html_cache[title] = (html, _time.time())
            print(f'[Warmup] 완료: {len(html)}B', flush=True)
        else:
            print('[Warmup] 실패', flush=True)
    except Exception as e:
        print(f'[Warmup] 실패: {e}', flush=True)


threading.Thread(target=_playwright_thread, daemon=True).start()


def get_page_html(title: str):
    """Playwright 전용 스레드를 통해 나무위키 전체 페이지 HTML 반환."""
    now = _time.time()
    if title in _html_cache:
        html, ts = _html_cache[title]
        if now - ts < CACHE_TTL:
            return html

    def _fetch(ctx):
        html = _pw_fetch_wiki(ctx, title)
        if html:
            _html_cache[title] = (html, _time.time())
        return html

    return _call_pw(_fetch)


def build_proxy_html(wiki_html: str, title: str, goal: str) -> str:
    """나무위키 HTML을 게임 프록시 페이지로 변환."""
    goal_enc = quote(goal, safe='')
    is_goal  = bool(goal) and title.strip() == goal.strip()

    # 1. namu.wiki SPA 스크립트 제거 (재실행 방지)
    html = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', wiki_html)

    # 2. /w/ 내부 링크 → 프록시 경로
    def rewrite_link(m):
        raw  = m.group(1)                            # e.g. /w/%EA%B3%...
        part = raw[3:].split('#')[0].split('?')[0]   # title only
        return f'href="/page/{part}?goal={goal_enc}"'
    html = re.sub(r'href="(/w/[^"]*)"', rewrite_link, html)

    # 3. 나머지 상대 URL (//는 제외, /page/ 도 제외) → 절대 URL
    html = re.sub(
        r'(href|src)="(\/(?!\/|page\/)[^"]*)"',
        lambda m: f'{m.group(1)}="https://namu.wiki{m.group(2)}"',
        html,
    )

    # 4. HUD + 스크립트 주입
    t_json  = json.dumps(title)
    g_json  = json.dumps(goal)
    ig_json = json.dumps(is_goal)

    inject = f'''
<link rel="stylesheet" href="/static/css/hud.css">
<div id="rh-pad"></div>
<header id="rh-hud">
  <div class="rh-hud-left">
    <div class="rh-hud-stat">
      <span class="rh-hud-icon">⏱</span>
      <span class="rh-hud-val" id="rh-timer">00:00</span>
    </div>
    <div class="rh-hud-stat">
      <span class="rh-hud-icon">🔗</span>
      <span class="rh-hud-val" id="rh-hops">0</span>
    </div>
  </div>
  <div class="rh-hud-center">
    <span class="rh-hud-goal-label">목표</span>
    <span class="rh-hud-goal" id="rh-goal">—</span>
  </div>
  <div class="rh-hud-right">
    <button class="rh-btn" onclick="rhTogglePath()">경로</button>
    <button class="rh-btn rh-btn-danger" onclick="rhGiveUp()">포기</button>
  </div>
</header>

<div id="rh-path-panel" style="display:none">
  <div id="rh-path-content"><span class="rh-path-item">이동 경로 없음</span></div>
</div>

<div id="rh-victory" style="display:none">
  <div class="rh-v-card">
    <div class="rh-v-icon">🎉</div>
    <div class="rh-v-title">목표 달성!</div>
    <div class="rh-v-stats">
      <div class="rh-v-stat">
        <div class="rh-v-stat-label">소요 시간</div>
        <div class="rh-v-stat-val" id="rh-v-time">—</div>
      </div>
      <div class="rh-v-stat">
        <div class="rh-v-stat-label">이동 횟수</div>
        <div class="rh-v-stat-val" id="rh-v-hops">—</div>
      </div>
    </div>
    <div>
      <div class="rh-v-path-label">이동 경로</div>
      <div class="rh-v-path" id="rh-v-path"></div>
    </div>
    <div>
      <div class="rh-rank-title">🏆 랭킹에 등록하기</div>
      <div id="rh-rank-row" class="rh-rank-row">
        <input type="text" id="rh-nickname" class="rh-rank-input"
               placeholder="닉네임 (최대 20자)" maxlength="20" autocomplete="off">
        <button class="rh-rank-submit" id="rh-rank-btn" onclick="rhSubmitRank()">등록</button>
      </div>
      <div class="rh-rank-result" id="rh-rank-result" style="display:none"></div>
    </div>
    <div class="rh-v-actions">
      <button class="rh-v-btn rh-v-btn-primary" onclick="rhPlayAgain()">다시 하기</button>
      <button class="rh-v-btn rh-v-btn-secondary" onclick="rhShare()">공유하기 📤</button>
    </div>
  </div>
</div>

<script>
const PAGE_TITLE = {t_json};
const GOAL       = {g_json};
const IS_GOAL    = {ig_json};
</script>
<script src="/static/js/proxy.js"></script>
'''

    if '</body>' in html:
        html = html.replace('</body>', inject + '</body>', 1)
    else:
        html += inject

    return html


def _nm_inline(text: str, goal_enc: str) -> str:
    """namumark 인라인 마크업 → HTML (링크 위주)."""
    saved: list = []

    def save_link(m):
        inner = m.group(1)
        parts = inner.split('|', 1)
        raw   = parts[0].split('#')[0].strip()
        disp  = (parts[1].strip() if len(parts) > 1 else raw)
        idx   = len(saved)
        if not raw or any(raw.startswith(p) for p in EXCLUDED_PREFIXES):
            saved.append(html_escape(disp))
        elif raw.startswith(('http://', 'https://')):
            saved.append(
                f'<a href="{html_escape(raw)}" class="ext-link" target="_blank" rel="noopener">'
                f'{html_escape(disp)}</a>'
            )
        else:
            saved.append(
                f'<a href="/page/{quote(raw, safe="")}?goal={goal_enc}" class="wiki-link">'
                f'{html_escape(disp)}</a>'
            )
        return f'\x00{idx}\x00'

    text = re.sub(r'\[\[([^\[\]]+)\]\]', save_link, text)
    text = html_escape(text)                       # 나머지 텍스트 안전하게 이스케이프
    text = re.sub(r"'''(.+?)'''", r'<strong>\1</strong>', text)
    text = re.sub(r"''(.+?)''",   r'<em>\1</em>',        text)
    text = re.sub(r'~~(.+?)~~',   r'<s>\1</s>',          text)
    text = re.sub(r'__(.+?)__',   r'<u>\1</u>',          text)

    for idx, html in enumerate(saved):
        text = text.replace(f'\x00{idx}\x00', html)

    text = re.sub(r'\{\{\{.*?\}\}\}', '', text)
    text = re.sub(r'\{[^}\n]{0,60}\}', '', text)
    return text


def render_namumark(content: str, title: str, goal: str) -> str:
    """namumark 원문 → 게임용 HTML. curl_cffi로 /raw/ 에서 받은 텍스트를 변환."""
    goal_enc = quote(goal, safe='')

    # 코드 블록 / 표 등 복잡한 블록은 제거
    content = re.sub(r'\{\{\{.*?\}\}\}', '', content, flags=re.DOTALL)

    lines      = content.split('\n')
    out        = []
    in_list    = None

    for line in lines:
        # 제목 (== 제목 ==)
        m = re.match(r'^(={1,6})\s*(.+?)\s*\1\s*$', line)
        if m:
            if in_list: out.append(f'</{in_list}>'); in_list = None
            level = min(len(m.group(1)) + 1, 6)   # h2 ~ h6
            out.append(f'<h{level}>{_nm_inline(m.group(2), goal_enc)}</h{level}>')
            continue

        # 수평선
        if re.match(r'^-{4,}\s*$', line):
            if in_list: out.append(f'</{in_list}>'); in_list = None
            out.append('<hr>')
            continue

        # 비순서 목록
        m = re.match(r'^\s*\*\s+(.+)$', line)
        if m:
            if in_list != 'ul':
                if in_list: out.append(f'</{in_list}>')
                out.append('<ul>'); in_list = 'ul'
            out.append(f'<li>{_nm_inline(m.group(1), goal_enc)}</li>')
            continue

        # 순서 목록
        m = re.match(r'^\s*\d+\.\s+(.+)$', line)
        if m:
            if in_list != 'ol':
                if in_list: out.append(f'</{in_list}>')
                out.append('<ol>'); in_list = 'ol'
            out.append(f'<li>{_nm_inline(m.group(1), goal_enc)}</li>')
            continue

        # 목록 종료
        if in_list:
            out.append(f'</{in_list}>'); in_list = None

        # 인용
        m = re.match(r'^>+\s*(.*)$', line)
        if m:
            inner = m.group(1).strip()
            out.append(f'<blockquote>{_nm_inline(inner, goal_enc) if inner else "&nbsp;"}</blockquote>')
            continue

        # 빈 줄
        if not line.strip():
            out.append('')
            continue

        # 일반 텍스트
        out.append(f'<p>{_nm_inline(line, goal_enc)}</p>')

    if in_list:
        out.append(f'</{in_list}>')

    return '\n'.join(out)


def get_page_links(title: str):
    """나무위키 링크 추출: Playwright 전용 스레드 사용."""
    now = _time.time()
    if title in _links_cache:
        links, ts = _links_cache[title]
        if now - ts < CACHE_TTL:
            return links

    def _fetch(ctx):
        pg = ctx.new_page()
        try:
            _pw_stealth(pg)
            pg.goto(f'https://namu.wiki/w/{quote(title)}',
                    wait_until='domcontentloaded', timeout=30000)
            if '__cf_chl' in pg.url or 'just a moment' in (pg.title() or '').lower():
                try:
                    pg.wait_for_url(lambda u: '__cf_chl' not in u, timeout=20000)
                except Exception:
                    return None
            pg.wait_for_selector('a[href^="/w/"]', timeout=25000)
            raw = pg.eval_on_selector_all(
                'a[href^="/w/"]',
                'els => els.map(e => ({href: e.getAttribute("href"), text: e.innerText.trim()}))',
            )
            seen = set()
            links = []
            for item in raw:
                href = item.get('href', '')
                text = item.get('text', '').strip()
                if not href.startswith('/w/') or not text:
                    continue
                page_title = unquote(href[3:]).split('#')[0].strip()
                if not page_title or any(page_title.startswith(p) for p in EXCLUDED_PREFIXES):
                    continue
                if page_title in seen:
                    continue
                seen.add(page_title)
                links.append({'title': page_title, 'display': text})
            _links_cache[title] = (links, _time.time())
            return links
        finally:
            pg.close()

    return _call_pw(_fetch)


# ── 레거시 scraper (데스크탑 wiki_fetcher 폴백용) ──────────────

_wiki_fetcher = None


def set_wiki_fetcher(fetcher):
    global _wiki_fetcher
    _wiki_fetcher = fetcher


_MOBILE_UA = (
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
    'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
)
_FETCH_HEADERS = {
    'User-Agent': _MOBILE_UA,
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Accept': 'text/plain, */*',
    'Referer': 'https://namu.wiki/',
}


def _fetch(url: str, timeout: int = 15):
    if _USE_CURL_CFFI:
        return cf_requests.get(url, impersonate='safari17_0', timeout=timeout,
                               headers=_FETCH_HEADERS)
    if cf_requests:
        return cf_requests.get(url, timeout=timeout, headers=_FETCH_HEADERS)
    raise RuntimeError('no HTTP client available')


# ── 나무위키 fetching ──────────────────────────────────────────

def get_raw_content(title):
    """namumark 원문 반환: requests 우선, Playwright /raw/ 폴백."""
    if _wiki_fetcher is not None:
        return _wiki_fetcher(title)

    url = NAMUWIKI_RAW_URL + quote(title)

    # 1차: requests (빠름, IP 블록 시 403)
    try:
        response = _fetch(url)
        if response.status_code == 200:
            text = response.text
            if not text.strip().lower().startswith(('<!doctype', '<html')):
                print(f'[Raw] {title}: OK ({len(text)}B)', flush=True)
                return text
        print(f'[Raw] {title}: HTTP {response.status_code}', flush=True)
    except Exception as e:
        print(f'[Raw] {title}: requests 에러 {e}', flush=True)

    # 2차: Playwright로 /raw/ 직접 요청 (전용 스레드 사용)
    def _fetch_raw(ctx):
        pg = ctx.new_page()
        try:
            _pw_stealth(pg)
            pg.goto(url, wait_until='domcontentloaded', timeout=20000)
            if '__cf_chl' in pg.url or 'just a moment' in (pg.title() or '').lower():
                try:
                    pg.wait_for_url(lambda u: '__cf_chl' not in u, timeout=15000)
                except Exception:
                    return None
            content = pg.inner_text('body').strip()
            if content and not content.lower().startswith(('<!doctype', '<html', 'just a moment')):
                print(f'[Raw-PW] {title}: OK ({len(content)}B)', flush=True)
                return content
            return None
        finally:
            pg.close()

    return _call_pw(_fetch_raw)


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
    return render_template('index.html', presets=PRESET_CHALLENGES,
                           all_pages=json.dumps(ALL_PAGES, ensure_ascii=False))


@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'pages': []})
    q_lower = q.lower()
    results = [p for p in ALL_PAGES if q_lower in p.lower()][:12]
    return jsonify({'pages': results})


@app.route('/page/<path:title>')
def page(title):
    title = unquote(title)
    goal  = request.args.get('goal', '')

    # 1차: Playwright 전체 HTML 프록시
    wiki_html = get_page_html(title)
    if wiki_html:
        proxy_html = build_proxy_html(wiki_html, title, goal)
        return proxy_html, 200, {'Content-Type': 'text/html; charset=utf-8'}

    # 2차: 링크 목록 UI 폴백
    is_goal = bool(goal) and title.strip() == goal.strip()
    links = get_page_links(title) or []
    error = not links
    status = 404 if error else 200
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


@app.route('/api/health')
def api_health():
    """서버 상태 및 Playwright 동작 여부 확인."""
    status = {'db': False, 'playwright': False, 'playwright_error': None}
    try:
        with sqlite3.connect(DB_PATH) as c:
            c.execute('SELECT 1')
        status['db'] = True
    except Exception as e:
        status['db_error'] = str(e)

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True, args=['--no-sandbox','--disable-setuid-sandbox','--disable-dev-shm-usage','--single-process'])
            page = b.new_page()
            page.goto('about:blank')
            b.close()
        status['playwright'] = True
    except Exception as e:
        status['playwright_error'] = str(e)

    return jsonify(status)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
