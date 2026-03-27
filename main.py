"""
나무위키 스피드런 — 데스크탑 앱

동작 원리:
  1. Flask: 게임 설정 화면(index.html)만 서빙
  2. 게임 시작 → WebView가 https://namu.wiki/w/{시작페이지} 직접 로드
  3. 나무위키 페이지 로드 후 HUD JavaScript를 주입
  4. history.pushState 인터셉트로 SPA 내비게이션 감지
  5. 목표 페이지 도달 시 승리 오버레이 표시
"""

import json
import socket
import sys
import threading
import time
import urllib.request
from urllib.parse import quote


# ── HUD JavaScript 템플릿 ─────────────────────────────────────
# Python이 __GOAL__ / __START_TIME__ / __HOPS__ / __PATH__ 를 치환 후 주입

HUD_SCRIPT = r"""
(function() {
    if (document.getElementById('__sr_hud')) return;
    if (!location.hostname.includes('namu.wiki')) return;
    if (!location.pathname.startsWith('/w/')) return;

    var GOAL       = __GOAL__;
    var START_TIME = __START_TIME__;
    var hops       = __HOPS__;
    var path       = __PATH__;
    var ended      = false;

    /* ── 유틸 ────────────────────────────────── */
    function fmt(ms) {
        var s = Math.floor(ms / 1000), m = Math.floor(s / 60);
        s %= 60;
        var cs = Math.floor((ms % 1000) / 10);
        return m > 0 ? pad(m)+':'+pad(s) : pad(s)+'.'+pad(cs);
    }
    function pad(n) { return String(n).padStart(2,'0'); }
    function esc(s) {
        return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
    function getTitle() {
        var m = location.pathname.match(/^\/w\/([^?#]+)/);
        return m ? decodeURIComponent(m[1]) : null;
    }

    /* ── CSS ─────────────────────────────────── */
    var css = document.createElement('style');
    css.textContent =
        '#__sr_hud{position:fixed;top:0;left:0;right:0;height:52px;' +
        'background:rgba(13,17,23,.96);color:#e6edf3;display:flex;' +
        'align-items:center;padding:0 14px;justify-content:space-between;' +
        'z-index:2147483647;font:14px/1 -apple-system,system-ui,sans-serif;' +
        'border-bottom:2px solid #00b894;box-sizing:border-box;' +
        'backdrop-filter:blur(8px);}' +
        '#__sr_l{display:flex;align-items:center;gap:14px;flex-shrink:0;}' +
        '#__sr_tm{font-weight:700;color:#00b894;font-variant-numeric:tabular-nums;min-width:58px;}' +
        '#__sr_hp{color:#7d8590;}' +
        '#__sr_c{flex:1;text-align:center;font-size:13px;color:#7d8590;' +
        'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:0 8px;}' +
        '#__sr_c b{color:#ff7b72;}' +
        '#__sr_r{display:flex;gap:6px;flex-shrink:0;}' +
        '#__sr_r button{padding:4px 10px;border-radius:6px;border:1px solid #30363d;' +
        'background:#21262d;color:#e6edf3;font-size:12px;cursor:pointer;font-family:inherit;}' +
        '#__sr_r button:hover{background:#2d333b;}' +
        '#__sr_gbtn:hover{background:rgba(248,81,73,.15)!important;' +
        'color:#f85149!important;border-color:rgba(248,81,73,.4)!important;}' +
        '#__sr_pp{position:fixed;top:52px;left:0;right:0;' +
        'background:rgba(22,27,34,.97);border-bottom:1px solid #30363d;' +
        'padding:8px 14px;z-index:2147483646;box-sizing:border-box;' +
        'font:12px -apple-system,system-ui,sans-serif;color:#7d8590;' +
        'max-height:72px;overflow-y:auto;display:flex;flex-wrap:wrap;' +
        'align-items:center;gap:4px;}' +
        '.sr-pi{background:#21262d;border:1px solid #30363d;border-radius:4px;' +
        'padding:2px 7px;white-space:nowrap;}' +
        '.sr-pi.cur{background:rgba(0,184,148,.1);border-color:rgba(0,184,148,.4);' +
        'color:#00b894;font-weight:700;}' +
        '.sr-ar{color:#484f58;font-size:11px;}' +
        '#__sr_ol{position:fixed;inset:0;background:rgba(0,0,0,.78);' +
        'z-index:2147483647;display:flex;align-items:center;justify-content:center;' +
        'font-family:-apple-system,system-ui,sans-serif;' +
        'animation:srFadeIn .25s ease;}' +
        '@keyframes srFadeIn{from{opacity:0}to{opacity:1}}' +
        '#__sr_vc{background:#161b22;border:1px solid #30363d;border-radius:12px;' +
        'padding:36px 32px;max-width:480px;width:90%;text-align:center;' +
        'box-shadow:0 16px 48px rgba(0,0,0,.55);' +
        'animation:srSlideUp .3s cubic-bezier(.16,1,.3,1);}' +
        '@keyframes srSlideUp{from{transform:translateY(32px);opacity:0}' +
        'to{transform:translateY(0);opacity:1}}' +
        '#__sr_vc h2{margin:0 0 20px;font-size:1.8rem;' +
        'background:linear-gradient(135deg,#00b894,#00cec9);' +
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;' +
        'background-clip:text;}' +
        '.sr-sts{display:flex;justify-content:center;gap:32px;margin-bottom:16px;}' +
        '.sr-sl{color:#7d8590;font-size:.73rem;text-transform:uppercase;' +
        'letter-spacing:.05em;display:block;margin-bottom:4px;}' +
        '.sr-sv{color:#00b894;font-size:1.8rem;font-weight:800;}' +
        '#__sr_vp{background:#0d1117;border-radius:8px;padding:10px 12px;' +
        'margin-bottom:16px;font-size:.8rem;color:#7d8590;text-align:left;' +
        'max-height:72px;overflow-y:auto;word-break:break-all;line-height:1.6;}' +
        '#__sr_rf{background:#0d1117;border:1px solid #30363d;border-radius:8px;' +
        'padding:12px 14px;margin-bottom:16px;text-align:left;}' +
        '#__sr_rf label{display:block;font-size:.72rem;color:#7d8590;text-transform:uppercase;' +
        'letter-spacing:.05em;margin-bottom:8px;}' +
        '#__sr_rir{display:flex;gap:8px;}' +
        '#__sr_ni{flex:1;background:#161b22;border:1px solid #30363d;border-radius:6px;' +
        'color:#e6edf3;padding:8px 12px;font-size:.88rem;font-family:inherit;outline:none;}' +
        '#__sr_ni:focus{border-color:#00b894;}' +
        '#__sr_sb{padding:8px 16px;background:#00b894;color:#000;border:none;' +
        'border-radius:6px;font-size:.88rem;font-weight:700;cursor:pointer;' +
        'font-family:inherit;white-space:nowrap;}' +
        '#__sr_sb:disabled{opacity:.5;cursor:default;}' +
        '#__sr_rr{font-size:.88rem;color:#00b894;margin-top:8px;font-weight:600;}' +
        '.sr-vb{padding:11px 22px;border-radius:8px;border:none;font-size:.92rem;' +
        'font-weight:600;cursor:pointer;font-family:inherit;transition:opacity .15s;}' +
        '.sr-vb:hover{opacity:.85;}' +
        '.sr-vbp{background:#00b894;color:#000;}' +
        '.sr-vbs{background:#21262d;border:1px solid #30363d!important;color:#e6edf3!important;}';
    document.head.appendChild(css);

    /* ── HUD DOM ─────────────────────────────── */
    var hud = document.createElement('div');
    hud.id = '__sr_hud';
    hud.innerHTML =
        '<div id="__sr_l">' +
            '<span id="__sr_tm">00:00</span>' +
            '<span id="__sr_hp">🔗&thinsp;<b id="__sr_hc">' + hops + '</b></span>' +
        '</div>' +
        '<div id="__sr_c">목표&ensp;<b>' + esc(GOAL) + '</b></div>' +
        '<div id="__sr_r">' +
            '<button id="__sr_pbtn">경로</button>' +
            '<button id="__sr_gbtn">포기</button>' +
        '</div>';
    document.documentElement.style.paddingTop = '52px';
    document.body.insertBefore(hud, document.body.firstChild);

    /* ── 타이머 ─────────────────────────────── */
    var _tid = setInterval(function() {
        if (ended) return;
        var el = document.getElementById('__sr_tm');
        if (el) el.textContent = fmt(Date.now() - START_TIME);
    }, 50);

    /* ── SPA 내비게이션 감지 ──────────────────── */
    var lastTitle = getTitle();

    function onNav(title) {
        if (ended) return;
        hops++;
        path.push(title);
        var hc = document.getElementById('__sr_hc');
        if (hc) hc.textContent = hops;

        var pp = document.getElementById('__sr_pp');
        if (pp) renderPath(pp);

        /* Python에 알림 (fire-and-forget) */
        if (window.pywebview && window.pywebview.api)
            window.pywebview.api.on_page_change(title, hops, path);

        if (title === GOAL) {
            ended = true;
            clearInterval(_tid);
            var elapsed = Date.now() - START_TIME;
            var el = document.getElementById('__sr_tm');
            if (el) el.textContent = fmt(elapsed);
            setTimeout(function() { showVictory(elapsed); }, 350);
        }
    }

    /* history.pushState 가로채기 (Vue Router 등 SPA 감지) */
    var _origPS = history.pushState;
    history.pushState = function() {
        _origPS.apply(this, arguments);
        var t = getTitle();
        if (t && t !== lastTitle) {
            lastTitle = t;
            setTimeout(function() { onNav(t); }, 60);
        }
    };
    window.addEventListener('popstate', function() {
        var t = getTitle();
        if (t && t !== lastTitle) {
            lastTitle = t;
            setTimeout(function() { onNav(t); }, 60);
        }
    });

    /* ── 경로 패널 ───────────────────────────── */
    function renderPath(panel) {
        panel.innerHTML = path.map(function(p, i) {
            return (i > 0 ? '<span class="sr-ar">→</span>' : '') +
                '<span class="sr-pi' + (i === path.length - 1 ? ' cur' : '') + '">' + esc(p) + '</span>';
        }).join('');
    }

    document.getElementById('__sr_pbtn').addEventListener('click', function() {
        var pp = document.getElementById('__sr_pp');
        if (pp) {
            pp.remove();
            document.documentElement.style.paddingTop = '52px';
        } else {
            pp = document.createElement('div');
            pp.id = '__sr_pp';
            renderPath(pp);
            document.documentElement.style.paddingTop = '104px';
            hud.insertAdjacentElement('afterend', pp);
        }
    });

    /* ── 포기 ───────────────────────────────── */
    document.getElementById('__sr_gbtn').addEventListener('click', function() {
        if (!confirm('게임을 포기하시겠습니까?')) return;
        ended = true; clearInterval(_tid);
        if (window.pywebview && window.pywebview.api) window.pywebview.api.go_home();
    });

    /* ── 승리 오버레이 ───────────────────────── */
    function showVictory(elapsed) {
        var ol = document.createElement('div');
        ol.id = '__sr_ol';
        ol.innerHTML =
            '<div id="__sr_vc">' +
            '<div style="font-size:3rem;margin-bottom:10px">🎉</div>' +
            '<h2>목표 달성!</h2>' +
            '<div class="sr-sts">' +
                '<div><span class="sr-sl">소요 시간</span>' +
                    '<span class="sr-sv">' + fmt(elapsed) + '</span></div>' +
                '<div><span class="sr-sl">이동 횟수</span>' +
                    '<span class="sr-sv">' + hops + '회</span></div>' +
            '</div>' +
            '<div id="__sr_vp">' + path.map(esc).join(' → ') + '</div>' +
            '<div id="__sr_rf">' +
                '<label>🏆 랭킹에 등록하기</label>' +
                '<div id="__sr_rir">' +
                    '<input id="__sr_ni" type="text" placeholder="닉네임 (최대 20자)" maxlength="20">' +
                    '<button id="__sr_sb">등록</button>' +
                '</div>' +
                '<div id="__sr_rr" style="display:none"></div>' +
            '</div>' +
            '<div style="display:flex;gap:12px;justify-content:center">' +
                '<button class="sr-vb sr-vbp" id="__sr_va">다시 하기</button>' +
                '<button class="sr-vb sr-vbs" id="__sr_vs">공유 📤</button>' +
            '</div></div>';
        document.body.appendChild(ol);

        document.getElementById('__sr_va').onclick = function() {
            if (window.pywebview && window.pywebview.api) window.pywebview.api.go_home();
        };
        document.getElementById('__sr_vs').onclick = function() {
            var txt = '🌳 나무위키 스피드런\n' + path[0] + ' → ' + GOAL +
                '\n⏱ ' + fmt(elapsed) + '  🔗 ' + hops + '회\n경로: ' + path.join(' → ');
            if (navigator.clipboard)
                navigator.clipboard.writeText(txt).then(function() { alert('복사됐습니다! 📋'); });
        };

        var sbtn = document.getElementById('__sr_sb');
        sbtn.onclick = function() {
            var nick = document.getElementById('__sr_ni').value.trim();
            if (!nick) { document.getElementById('__sr_ni').focus(); return; }
            sbtn.disabled = true;
            sbtn.textContent = '등록 중…';
            if (window.pywebview && window.pywebview.api) {
                window.pywebview.api.submit_score(nick, elapsed, hops, path)
                    .then(function(res) {
                        document.getElementById('__sr_rir').style.display = 'none';
                        var rr = document.getElementById('__sr_rr');
                        rr.style.display = 'block';
                        rr.textContent = (res && res.rank > 0)
                            ? '🏆 ' + res.rank + '위 기록 등록 완료!'
                            : '✅ 등록 완료!';
                    })
                    .catch(function() {
                        sbtn.disabled = false;
                        sbtn.textContent = '등록';
                        alert('등록에 실패했습니다.');
                    });
            }
        };
        document.getElementById('__sr_ni').addEventListener('keydown', function(e) {
            if (e.key === 'Enter') sbtn.click();
        });
    }
})();
"""


def make_hud_script(goal: str, start_time: float, hops: int = 0, path=None) -> str:
    """HUD 스크립트에 게임 상태를 주입한 최종 JS 문자열 반환."""
    if path is None:
        path = []
    return (HUD_SCRIPT
            .replace('__GOAL__',       json.dumps(goal))
            .replace('__START_TIME__', str(int(start_time * 1000)))
            .replace('__HOPS__',       str(hops))
            .replace('__PATH__',       json.dumps(path)))


# ── PyWebView ↔ JS 브릿지 ─────────────────────────────────────

class SpeedrunAPI:
    """
    js_api로 등록되어 나무위키 페이지 안의 JS에서 직접 호출됩니다.
    window.pywebview.api.method(args) 형태로 사용.
    """

    def __init__(self):
        self.goal: str = ''
        self.start_time: float = 0.0
        self.hops: int = 0
        self.path: list = []
        self.difficulty: str = 'unknown'
        self._window = None
        self._port: int = 5000

    def _init(self, window, port: int):
        self._window = window
        self._port = port

    def start_game(self, start: str, goal: str, difficulty: str = 'unknown'):
        """index.html → 게임 시작 버튼에서 호출."""
        self.goal = goal.strip()
        self.start_time = time.time()
        self.hops = 0
        self.path = [start.strip()]
        self.difficulty = difficulty or 'unknown'
        self._window.load_url(f'https://namu.wiki/w/{quote(start.strip())}')
        return {'ok': True}

    def on_page_change(self, title: str, hops: int, path: list):
        """HUD JS가 SPA 내비게이션 감지 시 호출."""
        self.hops = int(hops)
        self.path = list(path)
        return {'ok': True}

    def submit_score(self, nickname: str, elapsed_ms: int, hops: int, path: list):
        """HUD JS → 랭킹 등록. Flask API를 통해 DB에 저장."""
        payload = json.dumps({
            'nickname':   str(nickname)[:20],
            'start':      self.path[0] if self.path else '',
            'goal':       self.goal,
            'elapsed_ms': int(elapsed_ms),
            'hops':       int(hops),
            'path':       list(path),
            'difficulty': self.difficulty,
        }).encode()
        req = urllib.request.Request(
            f'http://127.0.0.1:{self._port}/api/ranking',
            data=payload, method='POST',
            headers={'Content-Type': 'application/json'},
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            # 난이도별 순위 계산
            rank_url = (f'http://127.0.0.1:{self._port}/api/ranking'
                        f'?difficulty={quote(self.difficulty)}&limit=50')
            with urllib.request.urlopen(rank_url, timeout=5) as resp:
                rank_data = json.loads(resp.read())
            rank = next(
                (i + 1 for i, r in enumerate(rank_data.get('rankings', []))
                 if r.get('id') == data.get('id')),
                0
            )
            return {'ok': True, 'id': data.get('id'), 'rank': rank}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def go_home(self):
        """포기 / 다시 하기 → 메인 화면으로 복귀."""
        self.goal = ''
        self.hops = 0
        self.path = []
        self.difficulty = 'unknown'
        self._window.load_url(f'http://127.0.0.1:{self._port}/')
        return {'ok': True}


# ── 유틸 ──────────────────────────────────────────────────────

def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def wait_for_server(port: int, timeout: float = 10.0) -> bool:
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=1)
            return True
        except Exception:
            time.sleep(0.15)
    return False


def start_flask(port: int) -> None:
    from app import app
    app.run(host='127.0.0.1', port=port, debug=False,
            use_reloader=False, threaded=True)


# ── 진입점 ────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        import webview
    except ImportError:
        print('pywebview를 설치해주세요: pip install pywebview')
        sys.exit(1)

    port = find_free_port()
    api  = SpeedrunAPI()

    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    if not wait_for_server(port):
        print('[오류] Flask 서버가 시작되지 않았습니다.')
        sys.exit(1)

    window = webview.create_window(
        title='나무위키 스피드런',
        url=f'http://127.0.0.1:{port}',
        js_api=api,
        width=1200,
        height=820,
        resizable=True,
        min_size=(480, 600),
    )

    api._init(window, port)

    def on_loaded():
        """페이지 로드 완료마다 호출 — 나무위키 페이지면 HUD 주입."""
        if api.goal:
            script = make_hud_script(api.goal, api.start_time, api.hops, api.path)
            window.evaluate_js(script)

    window.events.loaded += on_loaded

    print(f'[나무위키 스피드런] 포트 {port} — 창을 엽니다.')
    webview.start()
