# 🐇 Rabbit Hole

위키 링크를 타고 목표 페이지까지 도달하는 스피드런 게임.
나무위키, 한국어/영어/독일어/프랑스어/일본어 위키백과를 지원합니다.

---

## 목차

- [게임 방법](#게임-방법)
- [지원 위키](#지원-위키)
- [프로젝트 구조](#프로젝트-구조)
- [아키텍처](#아키텍처)
- [주요 기술 결정](#주요-기술-결정)
- [환경변수](#환경변수)
- [로컬 개발](#로컬-개발)
- [Railway 배포](#railway-배포)
- [랭킹 DB 관리](#랭킹-db-관리)
- [API 레퍼런스](#api-레퍼런스)

---

## 게임 방법

1. 위키를 선택한다 (나무위키 / 위키백과 6개 언어)
2. **랜덤 게임**: 난이도를 선택하면 시작·목표 페이지가 자동 배정
3. **직접 설정**: 원하는 시작·목표 페이지를 직접 입력
4. 페이지 안의 내부 링크를 클릭해 목표 페이지까지 이동
5. 최단 시간·최소 홉으로 도달하면 랭킹 등록 가능

---

## 지원 위키

| 키 | 위키 | 페이지 로딩 방식 |
|----|------|----------------|
| `namu` | 나무위키 | Playwright (Cloudflare 우회) |
| `ko` | 위키백과 한국어 | requests (모바일 서브도메인) |
| `en` | Wikipedia English | requests (모바일 서브도메인) |
| `de` | Wikipedia Deutsch | requests (모바일 서브도메인) |
| `fr` | Wikipédia Français | requests (모바일 서브도메인) |
| `ja` | ウィキペディア 日本語 | requests (모바일 서브도메인) |

---

## 프로젝트 구조

```
rabbit-hole/
├── app.py                  # Flask 앱 (메인 서버)
├── requirements.txt        # Python 의존성
├── Dockerfile              # Railway 배포용 컨테이너
├── Procfile                # (미사용, Dockerfile 우선)
├── railway.toml            # Railway 설정
├── static/
│   ├── css/
│   │   ├── style.css       # 메인 UI 스타일 (홈 화면)
│   │   └── hud.css         # 게임 중 HUD 스타일 (프록시 페이지)
│   ├── js/
│   │   └── proxy.js        # 게임 클라이언트 로직
│   ├── icon.svg
│   ├── manifest.json       # PWA 매니페스트
│   └── sw.js               # 서비스 워커
└── templates/
    └── index.html          # 홈 화면 (위키 선택 / 게임 설정 / 랭킹)
```

---

## 아키텍처

### 서버 구성

```
gunicorn (1 worker, 4 threads)
    └── Flask app
         ├── Playwright 전용 데몬 스레드  ← 나무위키 전용
         │    └── task queue (_pw_task_queue)
         ├── requests 기반 Wikipedia 페치  ← 나머지 위키
         └── PostgreSQL (랭킹 DB)
```

### 나무위키 페이지 로딩 흐름

나무위키는 Railway 데이터센터 IP를 Cloudflare가 차단하기 때문에 Playwright + 모바일 Safari UA로 우회합니다.

```
요청 → _call_pw(func) → _pw_task_queue → _playwright_thread()
    → new_page() → goto(url) → CF 챌린지 감지
    → wait_for_url(CF 해제 대기) → page.content() 반환
    → build_proxy_html() → 응답
```

**핵심**: Playwright sync API는 생성된 스레드에서만 사용 가능합니다.
gunicorn의 여러 요청 스레드에서 직접 호출하면 `cannot switch to a different thread` 에러가 발생합니다.
이를 해결하기 위해 단일 Playwright 데몬 스레드 + `queue.Queue`로 모든 Playwright 작업을 직렬화합니다.

### Wikipedia 페이지 로딩 흐름

Wikipedia는 CF 차단이 없어 `requests`로 모바일 서브도메인(`{lang}.m.wikipedia.org`)에서 직접 fetch합니다.

```
요청 → get_wikipedia_html() → requests.get(mobile URL)
    → build_proxy_html() → 응답
```

### build_proxy_html() 처리 내용

위키 원본 HTML을 게임용으로 변환합니다:

1. `<script>` 태그 제거 (보안)
2. `data-src` → `src` 변환 (lazy-load 이미지 수정)
3. 내부 위키 링크 → `/page/{title}?goal=...&wiki=...` 재작성
4. 분류·틀·파일 등 제외 prefix 링크 → `target="_blank"` 외부 링크로 처리 (큐 막힘 방지)
5. Wikipedia: 검색바·헤더 숨기는 CSS 주입
6. HUD HTML + `proxy.js` 주입 (`PAGE_TITLE`, `GOAL`, `IS_GOAL`, `WIKI` JS 변수 포함)

### 클라이언트 게임 로직 (proxy.js)

게임 상태는 `localStorage` (`namuSpeedrun` 키)에 저장됩니다.

```js
{
  start: "시작 페이지",
  goal: "목표 페이지",
  wiki: "namu",           // 위키 키
  difficulty: "easy",
  startTime: 1234567890,  // Date.now()
  hops: 3,
  path: ["시작", "중간1", "중간2", "목표"],
  active: true,
  elapsed: null           // 완료 시 ms
}
```

**주요 함수:**

| 함수 | 역할 |
|------|------|
| `rhGiveUp()` | 포기 모달 표시 |
| `rhGiveUpGoal()` | 포기 후 목표 페이지로 이동 |
| `rhGiveUpHome()` | 포기 후 홈으로 이동 |
| `rhGiveUpCancel()` | 포기 모달 닫기 |
| `rhSubmitRank()` | 랭킹 등록 (`/api/ranking` POST) |
| `rhShare()` | 결과 공유 (Web Share API / 클립보드) |
| `showVictory()` | 목표 달성 오버레이 표시 |
| `tick()` | `requestAnimationFrame` 기반 타이머 |

**활성 게임이 없을 때** (포기 후 목표 페이지 방문 등): HUD의 "포기" 버튼이 자동으로 "닫기"로 변경됩니다.

---

## 주요 기술 결정

### 왜 단일 Playwright 스레드인가?

Playwright sync API는 생성된 OS 스레드에 바인딩됩니다. gunicorn gthread 모드는 요청마다 다른 스레드를 사용하므로, Playwright를 직접 호출하면 충돌합니다. 해결책: 전용 데몬 스레드 1개가 Playwright 인스턴스를 소유하고, 모든 페이지 로드 요청을 `queue.Queue`로 받아 직렬 처리합니다.

### 왜 분류·틀 링크를 외부 링크로 처리하는가?

나무위키의 분류(`분류:`) 및 틀(`틀:`) 페이지에는 게임에 필요한 내부 링크 선택자가 없습니다. 게임 링크로 재작성하면 해당 페이지 로드 시 Playwright가 25초간 타임아웃 대기하며 큐가 막힙니다. 이런 페이지는 `target="_blank"`로 외부 링크 처리하여 게임 흐름을 보호합니다.

### 왜 Wikipedia는 requests를 쓰는가?

Wikipedia는 Cloudflare 차단이 없어 Playwright 없이도 접근 가능합니다. 모바일 서브도메인(`*.m.wikipedia.org`)은 검색창 등 불필요한 UI가 적어 게임에 적합합니다.

### 랭킹 영구 저장

초기에는 SQLite(`/data/rankings.db`)를 사용했으나 Railway 배포 시 파일시스템이 초기화되어 데이터가 소실되는 문제가 있었습니다. Railway PostgreSQL 서비스로 마이그레이션하여 영구 저장을 구현했습니다.
코드는 `DATABASE_URL` 환경변수 유무에 따라 PostgreSQL / SQLite를 자동 선택합니다 (로컬 개발 시 SQLite 사용 가능).

---

## 환경변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 연결 URL (Railway 자동 주입) | 없으면 SQLite 사용 |
| `DB_PATH` | SQLite 파일 경로 (DATABASE_URL 없을 때) | `rankings.db` |
| `SECRET_KEY` | Flask 세션 시크릿 키 | `namu-speedrun-secret-key-2024` |
| `PORT` | gunicorn 바인딩 포트 (Railway 자동 주입) | `8080` |

---

## 로컬 개발

### 사전 조건

- Python 3.10+
- Playwright 브라우저 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

### 실행

```bash
python app.py
# 또는
gunicorn app:app --workers 1 --threads 4 --timeout 120
```

로컬에서는 `DATABASE_URL`이 없으므로 SQLite(`rankings.db`)를 자동 사용합니다.

---

## Railway 배포

### 서비스 구성

- **Rabbit-Hole**: 메인 앱 (Dockerfile 기반)
- **PostgreSQL**: Railway 기본 제공 DB 서비스 (DATABASE_URL 자동 주입)

### 배포 명령

```bash
railway up --detach --service "Rabbit-Hole"
```

### 로그 확인

```bash
railway logs --service "Rabbit-Hole"
```

### Dockerfile 구성

```
베이스 이미지: mcr.microsoft.com/playwright/python:v1.58.0-jammy
  → Playwright + Chromium + Python 3.10 포함
  → 노토 CJK 폰트 추가 설치 (나무위키 한글 렌더링)
gunicorn: 1 worker / 4 threads / timeout 120s
```

**왜 1 worker인가?** Playwright 인스턴스가 프로세스에 1개만 존재해야 합니다. worker를 늘리면 각 프로세스마다 별도 Playwright 인스턴스가 생성되어 메모리 과부하가 발생합니다.

---

## 랭킹 DB 관리

### 조회

Railway 대시보드 → PostgreSQL 서비스 → **Data** 탭 → `rankings` 테이블

### 초기화 / 삭제

Railway 대시보드 → PostgreSQL 서비스 → **Query** 탭에서 SQL 실행:

```sql
-- 전체 초기화
DELETE FROM rankings;

-- 특정 위키만
DELETE FROM rankings WHERE wiki = 'namu';

-- 특정 난이도만
DELETE FROM rankings WHERE difficulty = 'easy';
```

### 스키마

```sql
CREATE TABLE rankings (
    id         SERIAL  PRIMARY KEY,
    nickname   TEXT    NOT NULL,
    start_page TEXT    NOT NULL,
    goal_page  TEXT    NOT NULL,
    elapsed_ms INTEGER NOT NULL,
    hops       INTEGER NOT NULL,
    path       TEXT    NOT NULL,  -- JSON 배열 문자열
    difficulty TEXT    NOT NULL DEFAULT 'unknown',
    wiki       TEXT    NOT NULL DEFAULT 'namu',
    created_at TEXT    NOT NULL   -- ISO 8601 UTC
);
```

---

## API 레퍼런스

### `GET /page/<title>`

위키 페이지를 게임용 HTML로 변환하여 반환합니다.

| 파라미터 | 설명 |
|----------|------|
| `goal` | 목표 페이지 이름 |
| `wiki` | 위키 키 (`namu` / `ko` / `en` / `de` / `fr` / `ja`) |

### `GET /api/random-game`

난이도에 맞는 랜덤 시작·목표 페이지 쌍을 반환합니다.

| 파라미터 | 설명 |
|----------|------|
| `difficulty` | `easy` / `medium` / `hard` / `very_hard` |
| `wiki` | 위키 키 |

**응답:**
```json
{ "start": "시작 페이지", "goal": "목표 페이지", "difficulty": "easy" }
```

### `POST /api/ranking`

랭킹 등록.

**요청 바디:**
```json
{
  "nickname": "플레이어",
  "start": "시작 페이지",
  "goal": "목표 페이지",
  "elapsed_ms": 12345,
  "hops": 3,
  "path": ["시작", "중간", "목표"],
  "difficulty": "easy",
  "wiki": "namu"
}
```

**응답:**
```json
{ "ok": true, "id": 42 }
```

### `GET /api/ranking`

랭킹 조회 (elapsed_ms 오름차순, 동점 시 hops 오름차순).

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `wiki` | 위키 필터 | 전체 |
| `difficulty` | 난이도 필터 | 전체 |
| `limit` | 최대 개수 | 20 (최대 50) |

**응답:**
```json
{
  "rankings": [
    {
      "id": 1,
      "nickname": "플레이어",
      "start": "고양이",
      "goal": "블랙홀",
      "elapsed_ms": 12345,
      "hops": 3,
      "path": ["고양이", "우주", "블랙홀"],
      "difficulty": "medium",
      "wiki": "namu",
      "created_at": "2026-03-28T00:00:00"
    }
  ]
}
```

### `GET /api/health`

서버 상태 확인 (DB 연결 및 Playwright 동작 여부).

```json
{ "db": true, "playwright": true }
```
