import os
import re
import json
import difflib
import random
import string
import sqlite3
from contextlib import contextmanager
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

import subprocess as _subprocess
try:
    _APP_VER = _subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD'], stderr=_subprocess.DEVNULL
    ).decode().strip()
except Exception:
    import time as _t; _APP_VER = str(int(_t.time()))

@app.context_processor
def _inject_version():
    return {'ver': _APP_VER}

NAMUWIKI_RAW_URL = "https://namu.wiki/raw/"
DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rankings.db')
)
DATABASE_URL = os.environ.get('DATABASE_URL', '')

# PostgreSQL 사용 가능 여부
_USE_PG = bool(DATABASE_URL)
if _USE_PG:
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        _USE_PG = False

@contextmanager
def _db_conn():
    """SQLite 또는 PostgreSQL 커넥션을 컨텍스트 매니저로 반환."""
    if _USE_PG:
        conn = psycopg2.connect(DATABASE_URL)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        with sqlite3.connect(DB_PATH) as conn:
            yield conn

def _ph(n=1):
    """플레이스홀더: PostgreSQL=%s, SQLite=?"""
    return '%s' if _USE_PG else '?'

def _execute(conn, sql, params=()):
    if _USE_PG:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur
    else:
        return conn.execute(sql, params)

EXCLUDED_PREFIXES = [
    '파일:', '분류:', 'File:', 'Category:', 'Image:', 'image:',
    '나무위키:', '틀:', 'Template:', '위키:', '사용자:', 'User:',
    '특수기능:', 'Special:', '도움말:', 'Help:',
]

# 위키별 설정
WIKI_CONFIGS = {
    'namu': {
        'name':          '나무위키',
        'base_url':      'https://namu.wiki/w/',
        'host':          'namu.wiki',
        'link_prefix':   '/w/',
        'link_selector': 'a[href^="/w/"]',
    },
    'ko': {
        'name':          '위키백과 (한국어)',
        'base_url':      'https://ko.wikipedia.org/wiki/',
        'host':          'ko.wikipedia.org',
        'link_prefix':   '/wiki/',
        'link_selector': 'a[href^="/wiki/"]',
        'wp_excluded':   ['위키백과:', '위키낱말사전:', '위키문헌:', '토론:', '사용자:', '특수:', '도움말:', '포털:', '파일:', '분류:'],
    },
    'en': {
        'name':          'Wikipedia (English)',
        'base_url':      'https://en.wikipedia.org/wiki/',
        'host':          'en.wikipedia.org',
        'link_prefix':   '/wiki/',
        'link_selector': 'a[href^="/wiki/"]',
        'wp_excluded':   ['Wikipedia:', 'Talk:', 'User:', 'Special:', 'Help:', 'Portal:', 'File:', 'Category:', 'Template:', 'MediaWiki:'],
    },
    'de': {
        'name':          'Wikipedia (Deutsch)',
        'base_url':      'https://de.wikipedia.org/wiki/',
        'host':          'de.wikipedia.org',
        'link_prefix':   '/wiki/',
        'link_selector': 'a[href^="/wiki/"]',
        'wp_excluded':   ['Wikipedia:', 'Diskussion:', 'Benutzer:', 'Spezial:', 'Hilfe:', 'Portal:', 'Datei:', 'Kategorie:', 'Vorlage:'],
    },
    'fr': {
        'name':          'Wikipédia (Français)',
        'base_url':      'https://fr.wikipedia.org/wiki/',
        'host':          'fr.wikipedia.org',
        'link_prefix':   '/wiki/',
        'link_selector': 'a[href^="/wiki/"]',
        'wp_excluded':   ['Wikipédia:', 'Discussion:', 'Utilisateur:', 'Spécial:', 'Aide:', 'Portail:', 'Fichier:', 'Catégorie:', 'Modèle:'],
    },
    'ja': {
        'name':          'ウィキペディア (日本語)',
        'base_url':      'https://ja.wikipedia.org/wiki/',
        'host':          'ja.wikipedia.org',
        'link_prefix':   '/wiki/',
        'link_selector': 'a[href^="/wiki/"]',
        'wp_excluded':   ['Wikipedia:', 'ウィキペディア:', 'ノート:', '利用者:', '特別:', 'ヘルプ:', 'Portal:', 'ファイル:', 'カテゴリ:', 'Template:'],
    },
}

# ── Wikipedia 위키별 난이도 페이지 풀 ──────────────────────────
WIKI_PAGES_BY_DIFFICULTY = {
    'ko': {
        'easy': [
            "대한민국", "서울", "일본", "미국", "중국", "영국", "프랑스", "독일",
            "수학", "물리학", "화학", "생물학", "음악", "영화", "축구", "야구",
            "농구", "올림픽", "인터넷", "컴퓨터", "고양이", "개",
            "나폴레옹", "아인슈타인", "셰익스피어", "피자", "커피",
        ],
        'medium': [
            "부산", "인천", "대구", "광주", "대전", "조선", "고려", "신라",
            "세종대왕", "이순신", "임진왜란", "한국전쟁", "3·1 운동",
            "태권도", "바둑", "기후변화", "인공지능", "블랙홀", "화성",
            "모차르트", "베토벤", "다윈", "뉴턴", "진화", "빅뱅",
        ],
        'hard': [
            "경복궁", "훈민정음", "팔만대장경", "거북선", "광개토왕",
            "발해", "가야", "동학 농민 운동", "병자호란", "강화도 조약",
            "허준", "정약용", "판소리", "가야금",
            "바이킹", "십자군 전쟁", "몽골 제국", "오스만 제국",
        ],
        'very_hard': [
            "성리학", "실학", "공민왕", "을사조약", "신미양요",
            "양자역학", "열역학", "위상수학", "분자생물학", "유전공학",
            "임마누엘 칸트", "게오르크 헤겔", "플라톤", "아리스토텔레스",
        ],
    },
    'en': {
        'easy': [
            "United States", "Japan", "China", "United Kingdom", "France", "Germany",
            "Mathematics", "Physics", "Chemistry", "Biology", "Music", "Film",
            "Football", "Basketball", "Olympics", "Internet", "Computer",
            "Cat", "Dog", "Pizza", "Coffee", "Albert Einstein", "Napoleon",
        ],
        'medium': [
            "World War II", "World War I", "Cold War", "French Revolution",
            "Industrial Revolution", "Solar System", "Black hole", "Evolution",
            "Climate change", "Artificial intelligence", "Quantum mechanics",
            "Democracy", "Capitalism", "Socialism", "Buddhism", "Islam",
        ],
        'hard': [
            "Byzantine Empire", "Mongol Empire", "Ottoman Empire", "Roman Republic",
            "Renaissance", "Age of Enlightenment", "American Civil War",
            "Plate tectonics", "Periodic table", "DNA", "Photosynthesis",
            "Immanuel Kant", "Plato", "Aristotle", "Sigmund Freud",
        ],
        'very_hard': [
            "Scholasticism", "Neoplatonism", "Stoicism", "Empiricism",
            "Topology", "Number theory", "Complex analysis", "Thermodynamics",
            "Electromagnetism", "Standard Model", "General relativity",
            "Anthropology", "Epistemology", "Phenomenology",
        ],
    },
    'de': {
        'easy': [
            "Deutschland", "Berlin", "Bayern", "Hamburg", "Österreich", "Schweiz",
            "Mathematik", "Physik", "Chemie", "Musik", "Film", "Fußball",
            "Olympische Spiele", "Internet", "Computer", "Katze", "Hund",
            "Albert Einstein", "Napoleon Bonaparte", "Beethoven", "Mozart",
        ],
        'medium': [
            "Zweiter Weltkrieg", "Erster Weltkrieg", "Kalter Krieg",
            "Französische Revolution", "Industrielle Revolution",
            "Sonnensystem", "Schwarzes Loch", "Evolution", "Klimawandel",
            "Demokratie", "Kapitalismus", "Buddhismus", "Islam",
        ],
        'hard': [
            "Byzantinisches Reich", "Osmanisches Reich", "Römische Republik",
            "Renaissance", "Aufklärung", "Quantenmechanik", "Relativitätstheorie",
            "Periodensystem", "DNS", "Immanuel Kant", "Georg Wilhelm Friedrich Hegel",
        ],
        'very_hard': [
            "Scholastik", "Neuplatonismus", "Transzendentalphilosophie",
            "Topologie", "Zahlentheorie", "Thermodynamik", "Elektrodynamik",
            "Anthropologie", "Epistemologie", "Phänomenologie",
        ],
    },
    'fr': {
        'easy': [
            "France", "Paris", "Allemagne", "Royaume-Uni", "États-Unis",
            "Mathématiques", "Physique", "Chimie", "Musique", "Cinéma",
            "Football", "Jeux olympiques", "Internet", "Ordinateur",
            "Albert Einstein", "Napoléon Bonaparte", "Ludwig van Beethoven",
        ],
        'medium': [
            "Seconde Guerre mondiale", "Première Guerre mondiale", "Guerre froide",
            "Révolution française", "Révolution industrielle",
            "Système solaire", "Trou noir", "Évolution", "Changement climatique",
            "Démocratie", "Capitalisme", "Bouddhisme", "Islam",
        ],
        'hard': [
            "Empire byzantin", "Empire ottoman", "République romaine",
            "Renaissance", "Siècle des Lumières", "Mécanique quantique",
            "Relativité générale", "Tableau périodique", "ADN", "Emmanuel Kant",
        ],
        'very_hard': [
            "Scolastique", "Néoplatonisme", "Empirisme", "Rationalisme",
            "Topologie", "Théorie des nombres", "Thermodynamique",
            "Épistémologie", "Phénoménologie",
        ],
    },
    'ja': {
        'easy': [
            "日本", "東京", "大阪", "京都", "アメリカ合衆国", "中国", "韓国",
            "数学", "物理学", "化学", "音楽", "映画", "サッカー", "野球",
            "オリンピック", "インターネット", "コンピュータ", "ネコ",
            "アルベルト・アインシュタイン", "ナポレオン・ボナパルト",
        ],
        'medium': [
            "第二次世界大戦", "第一次世界大戦", "冷戦", "フランス革命",
            "産業革命", "太陽系", "ブラックホール", "進化論", "気候変動",
            "民主主義", "資本主義", "仏教", "イスラム教",
        ],
        'hard': [
            "ビザンティン帝国", "オスマン帝国", "ローマ共和国",
            "ルネサンス", "啓蒙主義", "量子力学", "相対性理論",
            "周期表", "DNA", "イマヌエル・カント",
        ],
        'very_hard': [
            "スコラ学", "新プラトン主義", "経験主義", "合理主義",
            "位相幾何学", "数論", "熱力学", "電磁気学",
            "認識論", "現象学",
        ],
    },
}

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

# 위키별 역링크 수 기반 난이도 임계값
# 각 항목: (최소 역링크 수, 난이도 키)
# very_hard 최소값을 3으로 설정 — 역링크 0~2개는 도달 자체가 거의 불가능하므로 제외
WIKI_DIFFICULTY_THRESHOLDS = {
    'namu': [(500, 'easy'), (120, 'medium'), (40, 'hard'), (10, 'very_hard')],
    'en':   [(500, 'easy'), (120, 'medium'), (40, 'hard'), (10, 'very_hard')],
    'ko':   [(200, 'easy'), (60,  'medium'), (25, 'hard'), (10, 'very_hard')],
    'de':   [(300, 'easy'), (90,  'medium'), (30, 'hard'), (10, 'very_hard')],
    'fr':   [(300, 'easy'), (90,  'medium'), (30, 'hard'), (10, 'very_hard')],
    'ja':   [(400, 'easy'), (120, 'medium'), (40, 'hard'), (10, 'very_hard')],
}
# 유효한 목표 페이지의 최소 역링크 수 (이 미만이면 목표로 사용하지 않음)
MIN_GOAL_BACKLINKS = 10

# 난이도별 페이지 풀 (랜덤 게임 생성용)
PAGES_BY_DIFFICULTY = {
    'easy': [
        # 국가·도시
        "대한민국", "서울특별시", "일본", "중국", "미국", "영국", "프랑스", "독일",
        "이탈리아", "스페인", "캐나다", "호주", "브라질", "러시아", "인도", "멕시코",
        "뉴욕", "런던", "파리", "도쿄", "베이징", "로마", "시드니", "두바이",
        "싱가포르", "방콕", "바르셀로나", "암스테르담", "베를린", "모스크바",
        # K-pop·엔터
        "BTS", "방탄소년단", "블랙핑크", "아이유", "뉴진스", "에스파", "르세라핌",
        "아이브", "세븐틴", "스트레이 키즈", "트와이스", "엑소", "샤이니",
        "레드벨벳", "소녀시대", "빅뱅", "2NE1", "원더걸스", "슈퍼주니어",
        # 드라마·영화
        "오징어 게임", "기생충", "이상한 변호사 우영우", "무빙", "더 글로리",
        "태양의 후예", "도깨비", "사랑의 불시착", "별에서 온 그대",
        "어벤져스", "타이타닉", "해리 포터", "반지의 제왕", "스타워즈",
        "인터스텔라", "조커", "라라랜드", "보헤미안 랩소디",
        # 음악
        "비틀즈", "마이클 잭슨", "퀸", "에미넴", "테일러 스위프트", "에드 시런",
        "아리아나 그란데", "저스틴 비버", "레이디 가가", "드레이크",
        # 스포츠
        "축구", "야구", "농구", "테니스", "수영", "올림픽", "월드컵", "NBA", "EPL",
        "손흥민", "류현진", "김연아", "박지성", "이강인", "황희찬",
        "호날두", "메시", "르브론 제임스", "마이클 조던", "타이거 우즈",
        # 음식
        "김치", "라면", "치킨", "떡볶이", "삼겹살", "비빔밥", "순두부찌개",
        "초밥", "파스타", "피자", "햄버거", "타코", "카레", "짜장면", "족발",
        # 게임·애니
        "마인크래프트", "포켓몬스터", "슈퍼마리오", "젤다의 전설", "GTA",
        "리그 오브 레전드", "오버워치", "배틀그라운드", "발로란트", "로블록스",
        "원피스", "나루토", "드래곤볼", "귀멸의 칼날", "진격의 거인",
        "슬램덩크", "강철의 연금술사", "도라에몽", "짱구는 못말려",
        # 과학·기술
        "인터넷", "컴퓨터", "스마트폰", "유튜브", "넷플릭스", "인스타그램",
        "인공지능", "기후변화", "블록체인", "가상현실", "메타버스",
        "지구", "태양", "달", "우주", "블랙홀", "수학", "물리학", "화학",
        "삼성전자", "애플", "구글", "메타", "아마존", "마이크로소프트",
        "테슬라", "SpaceX", "나사",
        # 역사·인물
        "조선", "고려", "로마 제국", "제2차 세계 대전", "한국전쟁",
        "나폴레옹", "스티브 잡스", "일론 머스크", "셰익스피어", "아인슈타인",
        "레오나르도 다 빈치", "피카소", "미켈란젤로", "반 고흐",
        # 동물·자연
        "고양이", "개", "공룡", "호랑이", "사자", "코끼리", "판다", "돌고래",
        "상어", "펭귄", "독수리", "나비", "히말라야", "에베레스트", "태평양",
        # 기타
        "불교", "기독교", "이슬람교", "힌두교", "유교",
        "민주주의", "자본주의", "공산주의",
        "소주", "커피", "초콜릿", "아이스크림",
    ],
    'medium': [
        # 한국 지역·도시
        "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시",
        "울산광역시", "수원시", "고양시", "창원시", "성남시", "청주시",
        "전주시", "제주특별자치도", "강릉시", "경주시", "안동시",
        # 한국 역사 인물
        "세종대왕", "이순신", "광개토대왕", "장보고", "원효", "의상",
        "김유신", "을지문덕", "강감찬", "권율", "신사임당", "유관순",
        "김구", "안창호", "안중근", "윤봉길", "박정희", "김대중",
        # 한국 역사 사건
        "임진왜란", "병자호란", "동학농민운동", "3.1운동", "4.19혁명",
        "한국전쟁", "6.25전쟁", "5.18민주화운동", "IMF 경제위기",
        "조선 건국", "고려 건국", "삼국통일", "임진왜란", "일제강점기",
        # 한국 스포츠·문화
        "태권도", "씨름", "바둑", "장기", "유도", "탁구", "양궁",
        "판소리", "사물놀이", "한복", "한옥", "한글", "태극기",
        "설날", "추석", "단오", "한식",
        # 세계 역사
        "프랑스 혁명", "산업혁명", "냉전", "베트남 전쟁", "걸프 전쟁",
        "제1차 세계 대전", "십자군 전쟁", "몽골 제국", "대항해시대",
        "미국 독립", "남북전쟁", "식민지배", "아프리카 분할",
        "고대 이집트", "그리스 신화", "북유럽 신화", "로마 신화",
        "메소포타미아", "페르시아 제국", "그리스 문명",
        # 과학
        "진화론", "빅뱅", "화성", "목성", "토성", "명왕성", "혜성",
        "DNA", "RNA", "단백질", "세포", "바이러스", "박테리아", "항생제",
        "원자력 발전", "태양광", "풍력", "수소에너지",
        "반도체", "GPS", "인터넷 프로토콜", "광섬유", "양자 컴퓨터",
        "로봇공학", "나노기술", "생명공학", "유전자 편집",
        # 음악·예술
        "모차르트", "베토벤", "바흐", "쇼팽", "드뷔시", "차이콥스키",
        "헨델", "비발디", "슈베르트", "브람스", "말러", "라흐마니노프",
        "모네", "렘브란트", "달리", "앤디 워홀", "뭉크", "클림트",
        "뮤지컬", "오페라", "발레", "클래식 음악", "재즈", "록음악",
        # 인물
        "다윈", "뉴턴", "마리 퀴리", "스티븐 호킹", "리처드 파인만",
        "프로이트", "아들러", "융", "파블로프", "스키너",
        "마르크스", "에라스무스", "괴테", "톨스토이", "도스토예프스키",
        "헤밍웨이", "카프카", "조지 오웰", "버지니아 울프",
        # 학문
        "생물학", "심리학", "경제학", "철학", "사회학", "인류학",
        "지리학", "정치학", "법학", "의학", "천문학", "지질학",
        "언어학", "고고학", "역사학", "미술사학",
        # 세계 지리
        "사하라 사막", "아마존 열대우림", "시베리아", "남극", "북극",
        "아마존강", "나일강", "양쯔강", "갠지스강", "미시시피강",
        "알프스산맥", "안데스산맥", "로키산맥", "우랄산맥",
        "지중해", "카리브해", "홍해", "흑해", "카스피해",
        "네덜란드", "벨기에", "스위스", "오스트리아", "폴란드",
        "체코", "헝가리", "그리스", "터키", "이란", "이라크", "사우디아라비아",
        "이집트", "남아프리카공화국", "나이지리아", "에티오피아",
        "아르헨티나", "칠레", "페루", "콜롬비아", "베네수엘라",
        # 음식·음료
        "냉면", "삼계탕", "갈비", "잡채", "된장찌개", "삼겹살",
        "떡국", "갈비탕", "청국장", "막걸리", "와인", "위스키",
        "초밥", "라멘", "우동", "덴푸라", "야키토리",
        # 경제·사회
        "주식", "채권", "암호화폐", "비트코인", "이더리움",
        "GDP", "인플레이션", "금리", "환율", "무역", "세계무역기구",
        "유럽연합", "ASEAN", "G7", "G20", "유엔",
        "카카오", "네이버", "삼성", "현대자동차", "SK", "LG",
        # 자연현상
        "태풍", "지진", "화산", "쓰나미", "오로라", "번개",
        "빙하", "사막", "열대우림", "산호초", "맹그로브",
        # 대학·교육
        "서울대학교", "연세대학교", "고려대학교", "카이스트", "포스텍",
        "하버드대학교", "MIT", "옥스퍼드대학교", "케임브리지대학교",
        "도쿄대학교", "베이징대학교", "칭화대학교",
    ],
    'hard': [
        "경복궁", "창덕궁", "수원화성", "불국사", "석굴암", "해인사",
        "훈민정음", "팔만대장경", "직지심체요절", "조선왕조실록",
        "거북선", "신기전", "화포", "비격진천뢰",
        "단군왕검", "홍익인간", "고조선", "위만조선",
        "가야", "발해", "탐라", "우산국",
        "왕건", "궁예", "견훤", "장수왕", "근초고왕",
        "허준", "정약용", "박지원", "홍대용", "유형원", "이익",
        "신윤복", "김홍도", "안견", "정선",
        "안중근", "윤봉길", "김구", "안창호", "유관순",
        "윤동주", "김소월", "이상", "황순원", "박경리", "이육사",
        "고려청자", "조선백자", "분청사기", "청동기",
        "판소리", "가야금", "거문고", "해금", "대금", "향피리",
        "무궁화", "진달래", "개나리", "은행나무",
        "바이킹", "십자군 전쟁", "몽골 제국", "훈족", "흉노",
        "페르시아 제국", "오스만 제국", "비잔틴 제국", "아케메네스 왕조",
        "양자역학", "열역학", "전자기학", "상대성이론", "핵물리학",
        "프로이트", "칼 융", "파블로프", "스키너",
        "마르크스", "레닌", "트로츠키", "마오쩌둥",
        "중세 유럽", "봉건제도", "교황청", "종교개혁",
        "르네상스", "계몽주의", "낭만주의", "인상주의",
        "아프리카 분할", "식민지배", "제국주의",
        "수에즈 운하", "파나마 운하", "실크로드",
        "만리장성", "피라미드", "콜로세움", "파르테논 신전",
        "흑사병", "스페인 독감", "HIV", "말라리아",
        "빙하기", "판구조론", "대멸종", "캄브리아기",
    ],
    'very_hard': [
        "봉수", "파발", "역참", "조운", "조창",
        "주자학", "양명학", "실학", "성리학", "도교", "선종",
        "국자감", "성균관", "향교", "서원", "과거제도",
        "공민왕", "우왕", "광해군", "연산군", "선조", "효종",
        "정유재란", "병인양요", "신미양요", "강화도조약", "제물포조약",
        "을사조약", "경술국치", "형사정책", "행정법", "헌법재판소",
        "위상수학", "해석학", "대수기하학", "수론", "범주론",
        "나선은하", "성운", "중성자별", "백색왜성", "퀘이사",
        "세포생물학", "분자생물학", "유전공학", "단백질 접힘", "후성유전학",
        "임마누엘 칸트", "게오르크 헤겔", "프리드리히 니체", "쇼펜하우어",
        "소크라테스", "플라톤", "아리스토텔레스", "에피쿠로스", "스토아철학",
        "스콜라 철학", "합리주의", "경험주의", "관념론", "유물론",
        "고구려 고분벽화", "첨성대", "측우기", "자격루", "혼천의",
        "향약집성방", "동의보감", "의방유취", "향약구급방",
        "함무라비 법전", "마그나카르타", "나폴레옹 법전",
        "루터", "칼뱅", "츠빙글리", "예수회", "공의회",
        "후기인상주의", "야수파", "입체파", "다다이즘", "초현실주의",
        "조세르", "람세스 2세", "네페르티티", "투탕카멘",
        "퓨리탄", "청교도 혁명", "명예혁명", "권리장전",
        "드레퓌스 사건", "파쇼다 사건", "모로코 위기",
        "로마노프 왕조", "합스부르크 왕조", "오스만 왕조",
        "베르됭 전투", "솜 전투", "갈리폴리 전투",
        "코민테른", "코민포름", "마셜 플랜", "트루먼 독트린",
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
    if _USE_PG:
        create_sql = '''CREATE TABLE IF NOT EXISTS rankings (
            id         SERIAL  PRIMARY KEY,
            nickname   TEXT    NOT NULL,
            start_page TEXT    NOT NULL,
            goal_page  TEXT    NOT NULL,
            elapsed_ms INTEGER NOT NULL,
            hops       INTEGER NOT NULL,
            path       TEXT    NOT NULL,
            difficulty TEXT    NOT NULL DEFAULT 'unknown',
            wiki       TEXT    NOT NULL DEFAULT 'namu',
            created_at TEXT    NOT NULL
        )'''
    else:
        create_sql = '''CREATE TABLE IF NOT EXISTS rankings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname   TEXT    NOT NULL,
            start_page TEXT    NOT NULL,
            goal_page  TEXT    NOT NULL,
            elapsed_ms INTEGER NOT NULL,
            hops       INTEGER NOT NULL,
            path       TEXT    NOT NULL,
            difficulty TEXT    NOT NULL DEFAULT 'unknown',
            wiki       TEXT    NOT NULL DEFAULT 'namu',
            created_at TEXT    NOT NULL
        )'''
    challenge_sql = '''CREATE TABLE IF NOT EXISTS challenge_links (
        code       TEXT    PRIMARY KEY,
        start_page TEXT    NOT NULL,
        goal_page  TEXT    NOT NULL,
        wiki       TEXT    NOT NULL DEFAULT 'namu',
        hops       INTEGER,
        ms         INTEGER,
        created_at TEXT    NOT NULL
    )'''
    with _db_conn() as conn:
        _execute(conn, create_sql)
        _execute(conn, challenge_sql)
        if not _USE_PG:
            try:
                _execute(conn, "ALTER TABLE rankings ADD COLUMN wiki TEXT NOT NULL DEFAULT 'namu'")
            except Exception:
                pass

def _gen_challenge_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

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
            user_data_dir='/tmp/linky-run-pw',
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


def _is_cf_page(pg):
    """현재 페이지가 CF 챌린지 페이지인지 확인."""
    title = (pg.title() or '').lower()
    url   = pg.url
    if '__cf_chl' in url:
        return True
    if 'just a moment' in title or '보안 확인' in title or '잠시만' in title:
        return True
    return False


def _pw_fetch_wiki(ctx, title: str, wiki: str = 'namu'):
    """Playwright로 위키 페이지 로드 — CF 처리 포함. ctx 스레드에서 호출."""
    cfg = WIKI_CONFIGS.get(wiki, WIKI_CONFIGS['namu'])
    pg = ctx.new_page()
    try:
        _pw_stealth(pg)
        url = cfg['base_url'] + quote(title)
        pg.goto(url, wait_until='domcontentloaded', timeout=35000)
        print(f'[PW:{wiki}] {title}: url={pg.url}  title={pg.title()!r}', flush=True)

        # CF 챌린지 감지 시 실제 위키 콘텐츠가 로드될 때까지 대기
        if _is_cf_page(pg):
            print(f'[PW:{wiki}] {title}: CF 감지, 실제 콘텐츠 대기 중…', flush=True)
            try:
                # 타이틀이 CF 관련 문구에서 벗어날 때까지 대기
                pg.wait_for_function(
                    """() => {
                        const t = document.title;
                        return t.length > 0 && !t.includes('Just a moment') && !t.includes('보안 확인') && !t.includes('잠시만');
                    }""",
                    timeout=45000
                )
                # 추가로 networkidle 대기 (JS 리다이렉트 완료)
                try:
                    pg.wait_for_load_state('networkidle', timeout=10000)
                except Exception:
                    pass
                print(f'[PW:{wiki}] {title}: CF 통과 → {pg.url}  title={pg.title()!r}', flush=True)
            except Exception:
                print(f'[PW:{wiki}] {title}: CF 미해결', flush=True)
                return None

        # 최종 CF 체크
        if _is_cf_page(pg):
            print(f'[PW:{wiki}] {title}: CF 최종 해제 실패', flush=True)
            return None

        # 나무위키 SPA "잠시만 기다리십시오" → 실제 콘텐츠 렌더 대기
        cur_title = (pg.title() or '').lower()
        if '잠시만' in cur_title:
            print(f'[PW:{wiki}] {title}: SPA 로딩 중, 콘텐츠 대기…', flush=True)
            try:
                pg.wait_for_function(
                    "() => !document.title.includes('잠시만') && !document.title.includes('just a moment')",
                    timeout=30000
                )
            except Exception:
                print(f'[PW:{wiki}] {title}: SPA 렌더 타임아웃', flush=True)

        # 실제 위키 링크 렌더 대기 (SPA 완료 기준)
        try:
            pg.wait_for_selector(cfg['link_selector'], timeout=35000)
        except Exception:
            print(f'[PW:{wiki}] {title}: link_selector 미탐지 (페이지 반환)', flush=True)

        html = pg.content()
        print(f'[PW:{wiki}] {title}: OK {len(html)}B', flush=True)
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


def _warmup_loop():
    """8분마다 CF 클리어런스를 갱신한다."""
    while True:
        _time.sleep(480)
        print('[Warmup-loop] 정기 재워밍업…', flush=True)
        def _task(ctx):
            _do_warmup(ctx)
        _call_pw(_task, timeout=90)

threading.Thread(target=_warmup_loop, daemon=True).start()


WORKER_URL   = os.environ.get('WORKER_URL', 'https://linkyrun-proxy.linkyrun.workers.dev/')
WORKER_TOKEN = os.environ.get('WORKER_TOKEN', 'linkyrun-worker-secret-2024')

# 리다이렉트 맵: redirect_title → canonical_title (예: '안철수' → '안철수 (정치인)')
_redirect_map: dict = {}
# 리다이렉트 여부를 확인한 페이지 목록 (재확인 방지)
_redirect_checked: set = set()


def _worker_fetch_namu(title: str):
    """Cloudflare Worker를 통해 namu.wiki 페이지 HTML 반환."""
    import urllib.request, urllib.parse
    params = urllib.parse.urlencode({'token': WORKER_TOKEN, 'title': title})
    url = WORKER_URL + '?' + params
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LinkyRun/1.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode('utf-8', errors='replace')
            status = r.status
            final_url = r.headers.get('X-Namu-Url', '')
            print(f'[Worker:namu] {title}: {status} {len(html)}B final={final_url}', flush=True)
            if status != 200 or len(html) < 1000:
                return None
            if 'Just a moment' in html or '보안 확인' in html:
                print(f'[Worker:namu] {title}: CF 챌린지 수신', flush=True)
                return None
            # 리다이렉트 감지: 최종 URL이 요청 제목과 다르면 리다이렉트 맵 저장
            _namu_prefix = 'https://namu.wiki/w/'
            if final_url.startswith(_namu_prefix):
                canonical = unquote(final_url[len(_namu_prefix):].split('?')[0].split('#')[0])
                if canonical and canonical != title:
                    _redirect_map[title] = canonical
                    print(f'[Worker:namu] 리다이렉트 감지: {title!r} → {canonical!r}', flush=True)
            return html
    except Exception as e:
        print(f'[Worker:namu] {title}: 에러 {e}', flush=True)
        return None


def get_page_html(title: str, wiki: str = 'namu'):
    """위키 페이지 HTML 반환 — namu는 Worker, 나머지는 Playwright."""
    cache_key = f'{wiki}:{title}'
    now = _time.time()
    if cache_key in _html_cache:
        html, ts = _html_cache[cache_key]
        if now - ts < CACHE_TTL:
            return html

    if wiki == 'namu':
        html = _worker_fetch_namu(title)
        if html:
            _html_cache[cache_key] = (html, _time.time())
        return html

    def _fetch(ctx):
        html = _pw_fetch_wiki(ctx, title, wiki)
        if html:
            _html_cache[cache_key] = (html, _time.time())
        return html

    return _call_pw(_fetch, timeout=120)


def build_proxy_html(wiki_html: str, title: str, goal: str, wiki: str = 'namu', is_goal: bool = None) -> str:
    """위키 HTML을 게임 프록시 페이지로 변환."""
    cfg      = WIKI_CONFIGS.get(wiki, WIKI_CONFIGS['namu'])
    host     = cfg['host']
    prefix   = cfg['link_prefix']   # '/w/' or '/wiki/'
    goal_enc = quote(goal, safe='')
    wiki_enc = quote(wiki, safe='')
    if is_goal is None:
        is_goal = bool(goal) and title.strip() == goal.strip()

    # 1. 스크립트 제거
    html = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', wiki_html)

    # 위키별 CSS를 <head>에 주입 (존재할 때만)
    if wiki == 'namu' and '</head>' in html:
        namu_fix = '''<style>
/* Reset namu.wiki nav-compensation padding */
#app,#app>div:first-child,#app>div:first-child>div:first-child{
    padding-top:0!important;margin-top:0!important
}
/* 다크모드: 위키 표 인라인 배경색(라이트모드 하드코딩) override */
@media(prefers-color-scheme:dark){
    td,th{background-color:#1e1e24!important;color:inherit}
    tr{background-color:transparent!important}
    table{border-color:#3a3a42!important}
}
</style>'''
        html = html.replace('</head>', namu_fix + '</head>', 1)
    elif wiki != 'namu' and '</head>' in html:
        wp_hide = '''<style>
.header-container,.minerva-header,.mw-header,.page-actions-menu,
.talk-namespace-header,.mw-footer,#mw-mf-page-left,.mw-wiki-logo,
.navigation-drawer,.menu,.mw-portlet-personal,.vector-menu,
.searchform,.search-form,#searchInput,.minerva-search-form {
    display:none!important;
}
.content-header-suffix,.pre-content { padding-top:0!important; }
</style>'''
        html = html.replace('</head>', wp_hide + '</head>', 1)

    # 2. lazy-load 이미지: data-src → src
    def fix_lazy(m):
        tag, attrs = m.group(1), m.group(2)
        # 기존 src="" (placeholder) 제거 후 data-src 값을 src로 승격
        attrs_clean = re.sub(r'\s+src="[^"]*"', '', attrs)
        data_src = re.search(r'data-src="([^"]*)"', m.group(0))
        if data_src:
            attrs_clean = re.sub(r'\s+data-src="[^"]*"', '', attrs_clean)
            attrs_clean += f' src="{data_src.group(1)}"'
        return f'<{tag}{attrs_clean}>'
    html = re.sub(r'<(img)(\b[^>]*?\bdata-src="[^"]*"[^>]*)>', fix_lazy, html)

    # 3. 내부 위키 링크 → 프록시 경로 (제외 접두사는 원본 URL로 유지)
    wp_excluded = cfg.get('wp_excluded', [])
    escaped_prefix = re.escape(prefix)
    escaped_host   = re.escape(host)

    def rewrite_link(m):
        raw  = m.group(2)  # /w/... 또는 /wiki/... 부분
        quote_char = m.group(1)
        part = raw[len(prefix):].split('#')[0].split('?')[0]
        decoded = unquote(part)
        if any(decoded.startswith(p) for p in EXCLUDED_PREFIXES + wp_excluded):
            return f'href={quote_char}https://{host}{raw}{quote_char} target="_blank" rel="noopener"'
        return f'href={quote_char}/page/{part}?goal={goal_enc}&wiki={wiki_enc}{quote_char}'

    # 상대 경로 링크: href="/w/..." 또는 href='/w/...'
    html = re.sub(
        rf'href=(["\'])({escaped_prefix}[^"\']*)\1',
        rewrite_link, html
    )
    # 절대 경로 링크: href="https://namu.wiki/w/..." (PC 버전에서 제공)
    html = re.sub(
        rf'href=(["\'])https?://{escaped_host}({escaped_prefix}[^"\']*)\1',
        rewrite_link, html
    )

    # 4-a. 나무위키 이미지: SSR HTML에 실제 CDN URL이 없음 (Vue 런타임 로딩)
    # → 현재 구조에서는 이미지 프록시 불가. 스킵.

    # 4-b. 나머지 상대 URL → 절대 URL (/page/ 제외)
    html = re.sub(
        r'(href|src)="(\/(?!\/|page\/)[^"]*)"',
        lambda m: f'{m.group(1)}="https://{host}{m.group(2)}"',
        html,
    )
    html = re.sub(
        r"(href|src)='(\/(?!\/|page\/)[^']*)'",
        lambda m: f"{m.group(1)}='https://{host}{m.group(2)}'",
        html,
    )

    # 5. HUD + 스크립트 주입
    t_json  = json.dumps(title)
    g_json  = json.dumps(goal)
    ig_json = json.dumps(is_goal)
    w_json  = json.dumps(wiki)

    inject = f'''
<link rel="stylesheet" href="/static/css/hud.css?v={_APP_VER}">
<script src="/static/js/i18n.js?v={_APP_VER}"></script>
<div id="rh-pad"></div>
<header id="rh-hud">
  <div class="rh-hud-left">
    <div class="rh-hud-stat">
      <span class="rh-hud-icon">⏱</span>
      <span class="rh-hud-val" id="rh-timer">00:00</span>
    </div>
    <div class="rh-hud-sep"></div>
    <div class="rh-hud-stat">
      <span class="rh-hud-icon">🔗</span>
      <span class="rh-hud-val" id="rh-hops">0</span>
    </div>
  </div>
  <button class="rh-hud-center" id="rh-hud-center" onclick="rhTogglePath()">
    <span class="rh-hud-goal-label" data-i18n="hudGoalLabel">목표</span>
    <span class="rh-hud-goal" id="rh-goal">—</span>
    <span class="rh-hud-path-toggle" id="rh-path-toggle">▾</span>
  </button>
  <div class="rh-hud-right">
    <button class="rh-btn rh-btn-danger" onclick="rhGiveUp()" data-i18n="btnGiveUp">포기</button>
  </div>
</header>

<div id="rh-path-panel" style="display:none">
  <div id="rh-path-content"><span class="rh-path-item" data-i18n="pathEmpty">이동 경로 없음</span></div>
</div>

<div id="rh-giveup-modal" class="rh-hidden">
  <div class="rh-gu-card">
    <div class="rh-gu-title" data-i18n="giveUpTitle">게임을 포기하시겠습니까?</div>
    <div class="rh-gu-actions">
      <button class="rh-gu-btn rh-gu-btn-goal" id="rh-gu-btn-goal" onclick="rhGiveUpGoal()"></button>
      <button class="rh-gu-btn rh-gu-btn-home" onclick="rhGiveUpHome()" data-i18n="giveUpHome">홈으로 이동</button>
      <button class="rh-gu-btn rh-gu-btn-cancel" onclick="rhGiveUpCancel()" data-i18n="giveUpCancel">아니오</button>
    </div>
  </div>
</div>

<div id="rh-victory" style="display:none">
  <div class="rh-v-card">
    <div class="rh-v-icon">🎉</div>
    <div class="rh-v-title" data-i18n="victoryTitle">목표 달성!</div>
    <div class="rh-v-stats">
      <div class="rh-v-stat">
        <div class="rh-v-stat-label" data-i18n="statTime">소요 시간</div>
        <div class="rh-v-stat-val" id="rh-v-time">—</div>
      </div>
      <div class="rh-v-stat">
        <div class="rh-v-stat-label" data-i18n="statHops">이동 횟수</div>
        <div class="rh-v-stat-val" id="rh-v-hops">—</div>
      </div>

    </div>
    <div>
      <div class="rh-v-path-label" data-i18n="pathLabel">이동 경로</div>
      <div class="rh-v-path" id="rh-v-path"></div>
    </div>
    <div>
      <div class="rh-rank-title" data-i18n="rankingFormTitle">🏆 랭킹에 등록하기</div>
      <div id="rh-rank-row" class="rh-rank-row">
        <input type="text" id="rh-nickname" class="rh-rank-input"
               data-i18n-placeholder="nicknamePlaceholder"
               placeholder="닉네임 (최대 20자)" maxlength="20" autocomplete="off">
        <button class="rh-rank-submit" id="rh-rank-btn" onclick="rhSubmitRank()" data-i18n="btnSubmitRank">등록</button>
      </div>
      <div class="rh-rank-result" id="rh-rank-result" style="display:none"></div>
    </div>
    <div class="rh-v-actions">
      <button class="rh-v-btn rh-v-btn-primary" onclick="rhPlayAgain()" data-i18n="btnPlayAgain">다시 하기</button>
      <button class="rh-v-btn rh-v-btn-secondary" onclick="rhShare()" data-i18n="btnShare">공유하기 📤</button>
      <button class="rh-v-btn rh-v-btn-ghost" onclick="rhChallengeFriend()" data-i18n-html="btnChallenge">도전장<br>보내기 📨</button>
    </div>
  </div>
</div>

<script>
const PAGE_TITLE = {t_json};
const GOAL       = {g_json};
const IS_GOAL    = {ig_json};
const WIKI       = {w_json};
window._WIKI = {{'namu':'namu','ko':'namu','en':'en','de':'de','fr':'fr','ja':'ja'}}[WIKI] || 'namu';
applyI18n();
</script>
<script src="/static/js/proxy.js?v={_APP_VER}"></script>
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


def get_wikipedia_html(title: str, wiki: str) -> str:
    """Wikipedia 모바일 페이지를 requests로 직접 가져옴 (Playwright 불필요)."""
    cache_key = f'{wiki}:{title}'
    now = _time.time()
    if cache_key in _html_cache:
        html, ts = _html_cache[cache_key]
        if now - ts < CACHE_TTL:
            return html

    cfg  = WIKI_CONFIGS[wiki]
    # 모바일 서브도메인으로 변환 (ko.m.wikipedia.org 등)
    mobile_host = cfg['host'].replace('.wikipedia.org', '.m.wikipedia.org')
    url  = f'https://{mobile_host}/wiki/{quote(title)}'
    lang = wiki  # 'ko', 'en', 'de', 'fr', 'ja'
    headers = {
        'User-Agent': _MOBILE_UA,
        'Accept-Language': f'{lang},en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml',
    }
    try:
        if cf_requests:
            resp = cf_requests.get(url, timeout=15, headers=headers)
        else:
            raise RuntimeError('no HTTP client')
        if resp.status_code == 200:
            html = resp.text
            _html_cache[cache_key] = (html, now)
            print(f'[Wiki:{wiki}] {title}: OK {len(html)}B', flush=True)
            return html
        print(f'[Wiki:{wiki}] {title}: HTTP {resp.status_code}', flush=True)
        return None
    except Exception as e:
        print(f'[Wiki:{wiki}] {title}: {e}', flush=True)
        return None


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
    """나무위키 역링크 수 반환. Worker API 경유. 실패하면 None."""
    import urllib.request as _ureq, urllib.parse as _uparse
    try:
        params = _uparse.urlencode({'token': WORKER_TOKEN, 'type': 'backlink', 'title': title})
        req = _ureq.Request(WORKER_URL + '?' + params, headers={'User-Agent': 'LinkyRun/1.0'})
        with _ureq.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='replace')
        # namu.wiki backlink API JSON: {"totalCount": N, ...}
        m = re.search(r'"totalCount"\s*:\s*(\d+)', text)
        if m:
            return int(m.group(1))
        # 폴백: HTML 파싱
        items = len(re.findall(r'<a [^>]*href="/w/', text))
        return items if items > 0 else 0
    except Exception as e:
        print(f'[backlink:{title}] 에러: {e}', flush=True)
        return None


def get_wikipedia_backlink_count(title: str, lang: str):
    """Wikipedia MediaWiki API로 역링크 수 반환. 실패 시 None."""
    import urllib.request as _ureq, urllib.parse as _uparse
    try:
        params = _uparse.urlencode({
            'action': 'query',
            'list': 'backlinks',
            'bltitle': title,
            'bllimit': '500',
            'format': 'json',
        })
        url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
        req = _ureq.Request(url, headers={'User-Agent': 'LinkyRun/1.0 (speedrun game)'})
        with _ureq.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        bls = data.get('query', {}).get('backlinks', [])
        # continue 키가 있으면 500개 초과
        if 'continue' in data:
            return 500
        return len(bls)
    except Exception as e:
        print(f'[wp-backlink:{lang}/{title}] 에러: {e}', flush=True)
        return None


def get_backlink_count_for_wiki(title: str, wiki: str):
    """위키에 따라 적합한 역링크 수 조회 함수를 호출."""
    if wiki == 'namu':
        return get_backlink_count(title)
    else:
        return get_wikipedia_backlink_count(title, wiki)


def classify_difficulty_for_wiki(count, wiki: str):
    """위키별 임계값으로 역링크 수를 난이도로 분류. (key, label, color) 반환."""
    thresholds = WIKI_DIFFICULTY_THRESHOLDS.get(wiki, WIKI_DIFFICULTY_THRESHOLDS['namu'])
    if count is not None:
        for threshold, key in thresholds:
            if count >= threshold:
                for t, k, label, color in DIFFICULTY_THRESHOLDS:
                    if k == key:
                        return key, label, color
    return 'medium', '보통', '#fdcb6e'


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
    wiki_all_pages = {'namu': ALL_PAGES}
    for wk, diff_pools in WIKI_PAGES_BY_DIFFICULTY.items():
        pages = sorted(set(p for pool in diff_pools.values() for p in pool))
        wiki_all_pages[wk] = pages
    return render_template('index.html', presets=PRESET_CHALLENGES,
                           all_pages=json.dumps(ALL_PAGES, ensure_ascii=False),
                           wiki_all_pages=json.dumps(wiki_all_pages, ensure_ascii=False))


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
    wiki  = request.args.get('wiki', 'namu')
    if wiki not in WIKI_CONFIGS:
        wiki = 'namu'

    # 페이지 HTML 가져오기: Wikipedia는 requests, 나무위키는 Playwright
    if wiki == 'namu':
        wiki_html = get_page_html(title, wiki)
    else:
        wiki_html = get_wikipedia_html(title, wiki)

    if wiki_html:
        # Wikipedia 링크 내 언더스코어를 공백으로 정규화해서 is_goal 판단
        norm = lambda s: unquote(s).replace('_', ' ').strip().lower()
        _strip_paren = lambda s: re.sub(r'\s*\([^)]*\)\s*$', '', s).strip()

        def _is_goal_match(t, g):
            """4-layer goal detection"""
            nt, ng = norm(t), norm(g)
            # Layer 1: 직접 일치
            if nt == ng:
                return True
            # Layer 2: 리다이렉트 맵
            if norm(_redirect_map.get(g, g)) == nt:
                return True
            if norm(_redirect_map.get(t, t)) == ng:
                return True
            # Layer 3: 괄호 제거 후 비교 (동음이의어 구분자 제거)
            st, sg = _strip_paren(nt), _strip_paren(ng)
            if st and sg and st == sg:
                return True
            # Layer 4: 유사도 매칭 (0.88 이상, 양쪽 모두 4자 이상)
            if len(nt) >= 4 and len(ng) >= 4:
                ratio = difflib.SequenceMatcher(None, nt, ng).ratio()
                if ratio >= 0.88:
                    return True
            return False

        if bool(goal):
            is_goal = _is_goal_match(title, goal)
            # 지연 리다이렉트 확인: goal 페이지가 아직 미확인이면 Worker로 리다이렉트 여부 확인
            # (예: goal='서울' redirect→'서울특별시', player가 '서울특별시'에 도달했을 때)
            if not is_goal and wiki == 'namu' and goal not in _redirect_checked:
                _redirect_checked.add(goal)
                _worker_fetch_namu(goal)  # _redirect_map[goal] 갱신 가능
                is_goal = _is_goal_match(title, goal)
                if is_goal:
                    print(f'[redirect-goal] {goal!r} → {_redirect_map.get(goal)!r}, player at {title!r}', flush=True)
            if is_goal:
                print(f'[goal-match] title={title!r} goal={goal!r}', flush=True)
        else:
            is_goal = False
        proxy_html = build_proxy_html(wiki_html, title, goal, wiki, is_goal=is_goal)
        return proxy_html, 200, {'Content-Type': 'text/html; charset=utf-8'}

    # 폴백: 나무위키만 링크 목록 UI 제공
    is_goal = bool(goal) and title.strip() == goal.strip()
    links = get_page_links(title) or [] if wiki == 'namu' else []
    error = not links
    status = 404 if error else 200
    cfg = WIKI_CONFIGS.get(wiki, WIKI_CONFIGS['namu'])
    wiki_url = cfg['base_url'] + quote(title, safe='')
    return render_template('page.html',
                           title=title, links=links, goal=goal,
                           is_goal=is_goal, error=error,
                           wiki=wiki, wiki_url=wiki_url), status


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


WIKI_RANDOM_URLS = {
    'ko': 'https://ko.wikipedia.org/wiki/Special:Random',
    'en': 'https://en.wikipedia.org/wiki/Special:Random',
    'de': 'https://de.wikipedia.org/wiki/Special:Random',
    'fr': 'https://fr.wikipedia.org/wiki/Special:Random',
    'ja': 'https://ja.wikipedia.org/wiki/Special:Random',
}


def _fetch_random_wiki_title(wiki: str):
    """위키의 랜덤 페이지 제목을 반환. 실패 시 None."""
    import urllib.request as _ureq, urllib.parse as _uparse
    try:
        if wiki == 'namu':
            params = _uparse.urlencode({'token': WORKER_TOKEN, 'type': 'random'})
            req = _ureq.Request(WORKER_URL + '?' + params, headers={'User-Agent': 'LinkyRun/1.0'})
            with _ureq.urlopen(req, timeout=15) as r:
                final_url = r.headers.get('X-Namu-Url', '')
                prefix = 'https://namu.wiki/w/'
                if final_url.startswith(prefix):
                    title = unquote(final_url[len(prefix):].split('?')[0].split('#')[0])
                    # 하위 문서(예: '이스핀 샤를/작중 행적') → 상위 문서로 대체
                    if '/' in title:
                        title = title.split('/')[0].strip()
                    if title and not any(title.startswith(p) for p in EXCLUDED_PREFIXES):
                        return title
        else:
            random_url = WIKI_RANDOM_URLS.get(wiki)
            if not random_url:
                return None
            req = _ureq.Request(random_url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; LinkyRun/1.0)',
            })
            with _ureq.urlopen(req, timeout=10) as r:
                final_url = r.url
                cfg = WIKI_CONFIGS.get(wiki, {})
                prefix = cfg.get('base_url', '')
                if prefix and final_url.startswith(prefix):
                    title = unquote(final_url[len(prefix):].split('?')[0].split('#')[0])
                    # Wikipedia 하위 문서(/ 포함)는 건너뜀
                    if title and '/' not in title:
                        return title
    except Exception as e:
        print(f'[random-title:{wiki}] 에러: {e}', flush=True)
    return None


@app.route('/api/random-game')
def api_random_game():
    """랜덤 시작 + 역링크 수 기반 난이도별 목표 페이지 반환."""
    difficulty = request.args.get('difficulty', 'easy')
    wiki       = request.args.get('wiki', 'namu')

    # 목표 페이지: 랜덤 페이지를 뽑아 역링크 수가 난이도에 맞는지 확인 (최대 8회 시도)
    goal = None
    for _ in range(8):
        t = _fetch_random_wiki_title(wiki)
        if not t:
            continue
        # 리다이렉트 페이지면 제외 (이미 맵에 있거나, 이 호출로 등록됨)
        if wiki == 'namu' and t in _redirect_map:
            continue
        count = get_backlink_count_for_wiki(t, wiki)
        # 역링크가 너무 적으면 도달 불가 — 제외
        if count is not None and count < MIN_GOAL_BACKLINKS:
            continue
        key, _, _ = classify_difficulty_for_wiki(count, wiki)
        if key == difficulty:
            goal = t
            break

    # 랜덤 시도 실패 시 기존 정적 풀로 폴백 (리다이렉트 페이지 제외)
    if not goal:
        if wiki == 'namu':
            fallback = PAGES_BY_DIFFICULTY.get(difficulty, PAGES_BY_DIFFICULTY['easy'])
        else:
            wiki_pool = WIKI_PAGES_BY_DIFFICULTY.get(wiki, {})
            fallback = wiki_pool.get(difficulty, wiki_pool.get('easy', []))
        candidates = [p for p in fallback if p not in _redirect_map]
        goal = random.choice(candidates) if candidates else (random.choice(fallback) if fallback else None)

    if not goal:
        return jsonify({'error': 'goal page not found'}), 500

    # 시작 페이지: 위키 랜덤 URL (최대 3회 시도)
    start = None
    for _ in range(3):
        t = _fetch_random_wiki_title(wiki)
        if t and t != goal:
            start = t
            break

    # 실패 시 정적 풀에서 폴백
    if not start:
        if wiki == 'namu':
            pool = PAGES_BY_DIFFICULTY.get(difficulty, PAGES_BY_DIFFICULTY['easy'])
        else:
            wiki_pool = WIKI_PAGES_BY_DIFFICULTY.get(wiki, {})
            pool = wiki_pool.get(difficulty, wiki_pool.get('easy', []))
        candidates = [p for p in pool if p != goal]
        start = random.choice(candidates) if candidates else goal

    return jsonify({'start': start, 'goal': goal, 'difficulty': difficulty, 'wiki': wiki})



@app.route('/api/daily')
def api_daily():
    import hashlib
    wiki = request.args.get('wiki', 'namu')
    today = datetime.utcnow().strftime('%Y-%m-%d')
    day_num = (datetime.utcnow() - datetime(2024, 1, 1)).days + 1

    if wiki == 'namu':
        pool = POPULAR_PAGES
    else:
        wiki_pool = WIKI_PAGES_BY_DIFFICULTY.get(wiki, {})
        pool = [p for diff_list in wiki_pool.values() for p in diff_list]
        if not pool:
            pool = POPULAR_PAGES

    # 리다이렉트 페이지 제외
    filtered_pool = [p for p in pool if p not in _redirect_map] or pool

    seed_s = hashlib.sha256(f'{today}:{wiki}:start'.encode()).digest()
    seed_g = hashlib.sha256(f'{today}:{wiki}:goal'.encode()).digest()
    idx_s = int.from_bytes(seed_s[:4], 'big') % len(filtered_pool)
    idx_g = int.from_bytes(seed_g[:4], 'big') % len(filtered_pool)
    if idx_s == idx_g:
        idx_g = (idx_g + 1) % len(filtered_pool)

    return jsonify({'start': filtered_pool[idx_s], 'goal': filtered_pool[idx_g],
                    'day': day_num, 'date': today, 'wiki': wiki})


@app.route('/api/exists/<path:title>')
def api_exists(title):
    content = get_raw_content(title)
    return jsonify({'exists': content is not None, 'title': title})


@app.route('/api/difficulty/<path:title>')
def api_difficulty(title):
    title = unquote(title)
    wiki = request.args.get('wiki', 'namu')
    count = get_backlink_count_for_wiki(title, wiki)
    key, label, color = classify_difficulty_for_wiki(count, wiki)
    return jsonify({
        'title': title,
        'wiki': wiki,
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

        wiki_val = str(data.get('wiki', 'namu'))
        ph = _ph()
        if _USE_PG:
            insert_sql = f'''INSERT INTO rankings
               (nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, wiki, created_at)
               VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph}) RETURNING id'''
        else:
            insert_sql = f'''INSERT INTO rankings
               (nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, wiki, created_at)
               VALUES ({ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph},{ph})'''
        params = (nickname,
                  str(data.get('start', '')),
                  str(data.get('goal', '')),
                  int(data.get('elapsed_ms', 0)),
                  int(data.get('hops', 0)),
                  json.dumps(data.get('path', [])),
                  str(data.get('difficulty', 'unknown')),
                  wiki_val,
                  datetime.utcnow().isoformat())
        with _db_conn() as conn:
            cur = _execute(conn, insert_sql, params)
            if _USE_PG:
                new_id = cur.fetchone()[0]
            else:
                new_id = cur.lastrowid

        return jsonify({'ok': True, 'id': new_id})

    # GET
    difficulty = request.args.get('difficulty', '').strip()
    wiki_filter = request.args.get('wiki', '').strip()
    limit = min(int(request.args.get('limit', 20)), 50)

    ph = _ph()
    with _db_conn() as conn:
        conditions = []
        params: list = []
        if difficulty:
            conditions.append(f'difficulty = {ph}')
            params.append(difficulty)
        if wiki_filter:
            conditions.append(f'wiki = {ph}')
            params.append(wiki_filter)
        where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''
        params.append(limit)
        cur = _execute(conn,
            f'''SELECT id, nickname, start_page, goal_page, elapsed_ms, hops, path, difficulty, wiki, created_at
                FROM rankings {where}
                ORDER BY elapsed_ms ASC, hops ASC LIMIT {ph}''',
            params
        )
        rows = cur.fetchall()

    results = [
        {'id': r[0], 'nickname': r[1], 'start': r[2], 'goal': r[3],
         'elapsed_ms': r[4], 'hops': r[5],
         'path': json.loads(r[6]), 'difficulty': r[7], 'wiki': r[8], 'created_at': r[9]}
        for r in rows
    ]
    return jsonify({'rankings': results, 'difficulty': difficulty, 'wiki': wiki_filter})



@app.route('/api/challenge', methods=['POST'])
def api_challenge_create():
    """도전장 단축 코드 생성."""
    data = request.get_json(silent=True) or {}
    start = (data.get('start') or '').strip()
    goal  = (data.get('goal')  or '').strip()
    wiki  = (data.get('wiki')  or 'namu').strip()
    hops  = data.get('hops')
    ms    = data.get('ms')
    if not start or not goal:
        return jsonify({'error': 'missing params'}), 400
    # 중복 코드 방지를 위해 최대 5회 시도
    for _ in range(5):
        code = _gen_challenge_code(6)
        try:
            with _db_conn() as conn:
                _execute(conn, '''INSERT INTO challenge_links
                    (code, start_page, goal_page, wiki, hops, ms, created_at)
                    VALUES (?,?,?,?,?,?,?)''' if not _USE_PG else '''INSERT INTO challenge_links
                    (code, start_page, goal_page, wiki, hops, ms, created_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                    (code, start, goal, wiki, hops, ms, datetime.utcnow().isoformat()))
            return jsonify({'code': code})
        except Exception:
            continue
    return jsonify({'error': 'code generation failed'}), 500


@app.route('/api/challenge/<code>')
def api_challenge_get(code):
    """도전장 코드로 파라미터 조회."""
    with _db_conn() as conn:
        row = _execute(conn, 'SELECT start_page, goal_page, wiki, hops, ms FROM challenge_links WHERE code=?' if not _USE_PG
                       else 'SELECT start_page, goal_page, wiki, hops, ms FROM challenge_links WHERE code=%s',
                       (code,)).fetchone()
    if not row:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'start': row[0], 'goal': row[1], 'wiki': row[2], 'hops': row[3], 'ms': row[4]})


@app.route('/api/health')
def api_health():
    """서버 상태 및 Playwright 동작 여부 확인."""
    status = {'db': False, 'playwright': False, 'playwright_error': None}
    try:
        with _db_conn() as c:
            _execute(c, 'SELECT 1')
        status['db'] = True
        status['db_type'] = 'postgresql' if _USE_PG else 'sqlite'
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
