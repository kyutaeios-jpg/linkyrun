'use strict';
(function () {
    const SK = 'namuSpeedrun';
    const STATS_SK = 'linkyRunPersonalStats';

    function load() {
        try { return JSON.parse(localStorage.getItem(SK) || 'null'); } catch (_) { return null; }
    }
    function save(s) { localStorage.setItem(SK, JSON.stringify(s)); }
    function clear() { localStorage.removeItem(SK); }

    /* ── Personal stats ───────────────────────────────────── */
    function loadStats() {
        try { return JSON.parse(localStorage.getItem(STATS_SK) || 'null') || _defaultStats(); }
        catch(_) { return _defaultStats(); }
    }
    function saveStats(s) { localStorage.setItem(STATS_SK, JSON.stringify(s)); }
    function _defaultStats() {
        return { totalGames: 0, wins: 0, streak: 0, bestStreak: 0,
                 bestTime: null, bestHops: null, byDiff: {} };
    }
    function _ensureDiff(stats, diff) {
        if (!stats.byDiff[diff])
            stats.byDiff[diff] = { plays: 0, wins: 0, bestTime: null, bestHops: null };
    }
    function _updateStatsOnWin(elapsed, hops, difficulty) {
        const stats = loadStats();
        stats.totalGames++;
        stats.wins++;
        stats.streak = (stats.streak || 0) + 1;
        if (stats.streak > (stats.bestStreak || 0)) stats.bestStreak = stats.streak;
        if (stats.bestTime === null || elapsed < stats.bestTime) stats.bestTime = elapsed;
        if (stats.bestHops === null || hops < stats.bestHops) stats.bestHops = hops;
        _ensureDiff(stats, difficulty);
        const d = stats.byDiff[difficulty];
        d.plays++; d.wins++;
        if (d.bestTime === null || elapsed < d.bestTime) d.bestTime = elapsed;
        if (d.bestHops === null || hops < d.bestHops) d.bestHops = hops;
        saveStats(stats);
    }
    function _recordGiveUp(difficulty) {
        const stats = loadStats();
        stats.totalGames++;
        stats.streak = 0;
        _ensureDiff(stats, difficulty);
        stats.byDiff[difficulty].plays++;
        saveStats(stats);
    }

    let gs = load();
    let raf = null;

    function fmt(ms) {
        const s = Math.floor(ms / 1000), m = Math.floor(s / 60), ss = s % 60, cs = Math.floor((ms % 1000) / 10);
        return m > 0
            ? `${String(m).padStart(2, '0')}:${String(ss).padStart(2, '0')}`
            : `${String(ss).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
    }

    function tick() {
        if (!gs || !gs.active) return;
        const el = document.getElementById('rh-timer');
        if (el) el.textContent = fmt(Date.now() - gs.startTime);
        raf = requestAnimationFrame(tick);
    }

    function syncHUD() {
        const goalEl = document.getElementById('rh-goal');
        const hopsEl = document.getElementById('rh-hops');
        if (goalEl) goalEl.textContent = (gs && gs.goal) || (typeof GOAL !== 'undefined' ? GOAL : '') || '—';
        if (hopsEl) hopsEl.textContent = gs ? gs.hops : 0;
    }

    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    window.rhTogglePath = function () {
        const el = document.getElementById('rh-path-panel');
        if (!el) return;
        const shown = el.style.display !== 'none';
        el.style.display = shown ? 'none' : 'block';
        if (!shown) renderPath();
    };

    function renderPath() {
        const el = document.getElementById('rh-path-content');
        if (!el) return;
        if (!gs || !gs.path || gs.path.length === 0) {
            el.innerHTML = `<span class="rh-path-item">${t('pathEmpty')}</span>`;
            return;
        }
        el.innerHTML = gs.path.map((p, i) => {
            const cur = i === gs.path.length - 1;
            return (i > 0 ? '<span class="rh-path-arrow">→</span>' : '') +
                `<span class="rh-path-item${cur ? ' rh-path-cur' : ''}">${esc(p)}</span>`;
        }).join('');
        el.scrollLeft = el.scrollWidth;
    }

    window.rhGiveUp = function () {
        const modal = document.getElementById('rh-giveup-modal');
        if (!modal) return;
        const goalBtn = document.getElementById('rh-gu-btn-goal');
        if (goalBtn) {
            const goalName = (gs && gs.goal) || (typeof GOAL !== 'undefined' ? GOAL : '');
            goalBtn.textContent = t('giveUpGoalBtn')(goalName);
        }
        modal.classList.remove('rh-hidden');
    };

    window.rhGiveUpGoal = function () {
        const goal = gs ? gs.goal : (typeof GOAL !== 'undefined' ? GOAL : null);
        const wiki = gs ? (gs.wiki || 'namu') : (typeof WIKI !== 'undefined' ? WIKI : 'namu');
        if (gs && gs.active) _recordGiveUp(gs.difficulty || 'unknown');
        clear();
        if (goal) {
            window.location.href =
                `/page/${encodeURIComponent(goal)}?goal=${encodeURIComponent(goal)}&wiki=${encodeURIComponent(wiki)}`;
        } else {
            window.location.href = '/';
        }
    };

    window.rhGiveUpHome = function () {
        if (gs && gs.active) _recordGiveUp(gs.difficulty || 'unknown');
        clear();
        window.location.href = '/';
    };

    window.rhGiveUpCancel = function () {
        const modal = document.getElementById('rh-giveup-modal');
        if (modal) modal.classList.add('rh-hidden');
    };

    function showVictory() {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        const elapsed = gs ? Date.now() - gs.startTime : 0;
        if (gs) { gs.active = false; gs.elapsed = elapsed; save(gs); }

        // 개인 기록 업데이트
        if (gs) _updateStatsOnWin(elapsed, gs.hops, gs.difficulty || 'unknown');

        const te = document.getElementById('rh-v-time');
        const he = document.getElementById('rh-v-hops');
        const pe = document.getElementById('rh-v-path');
        const ti = document.getElementById('rh-timer');
        if (te) te.textContent = fmt(elapsed);
        if (he) he.textContent = gs ? `${gs.hops}${t('hopsUnit')}` : '—';
        if (ti) ti.textContent = fmt(elapsed);
        if (pe && gs && gs.path) {
            pe.innerHTML = gs.path.map((p, i) => {
                const isG = i === gs.path.length - 1;
                return (i > 0 ? '<span class="rh-vpath-arrow">→</span>' : '') +
                    `<span${isG ? ' class="rh-vpath-goal"' : ''}>${esc(p)}</span>`;
            }).join('');
        }
        // 힌트 사용 횟수 표시
        const hintsUsed = gs ? (gs.hintsUsed || 0) : 0;
        const hintsStat = document.getElementById('rh-v-hints-stat');
        const hintsVal  = document.getElementById('rh-v-hints');
        if (hintsStat && hintsUsed > 0) {
            hintsStat.style.display = '';
            if (hintsVal) hintsVal.textContent = hintsUsed + t('hopsUnit');
        }
        // custom/daily 게임은 랭킹 등록 폼 숨김
        const rankRow = document.getElementById('rh-rank-row');
        const rankTitle = document.querySelector('.rh-rank-title');
        if (gs && (gs.difficulty === 'custom' || gs.difficulty === 'daily')) {
            if (rankRow) rankRow.style.display = 'none';
            if (rankTitle) rankTitle.style.display = 'none';
        }
        const ov = document.getElementById('rh-victory');
        if (ov) ov.style.display = 'flex';
    }

    window.rhPlayAgain = function () { clear(); window.location.href = '/'; };

    window.rhSubmitRank = async function () {
        if (!gs) return;
        const nick = (document.getElementById('rh-nickname')?.value || '').trim();
        if (!nick) { alert(t('alertNoNick')); return; }
        const elapsed = gs.elapsed || (Date.now() - gs.startTime);
        const btn = document.getElementById('rh-rank-btn');
        if (btn) { btn.disabled = true; btn.textContent = t('submitting'); }
        try {
            const res = await fetch('/api/ranking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nickname: nick, start: gs.start, goal: gs.goal,
                    elapsed_ms: Math.round(elapsed), hops: gs.hops,
                    path: gs.path, difficulty: gs.difficulty || 'unknown',
                    wiki: gs.wiki || (typeof WIKI !== 'undefined' ? WIKI : 'namu')
                })
            });
            const d = await res.json();
            if (!d.ok) throw new Error(d.error);
            const wikiParam = gs.wiki || (typeof WIKI !== 'undefined' ? WIKI : 'namu');
            const rk = await fetch(`/api/ranking?wiki=${encodeURIComponent(wikiParam)}&difficulty=${encodeURIComponent(gs.difficulty || '')}&limit=50`).then(r => r.json());
            const rank = rk.rankings.findIndex(r => r.id === d.id) + 1;
            const row = document.getElementById('rh-rank-row');
            const re = document.getElementById('rh-rank-result');
            if (row) row.style.display = 'none';
            if (re) { re.style.display = 'block'; re.textContent = rank > 0 ? t('rankResult')(rank) : t('rankOk'); }
        } catch (_) {
            if (btn) { btn.disabled = false; btn.textContent = t('btnSubmitRank'); }
            alert(t('rankFail'));
        }
    };

    window.rhShare = async function () {
        if (!gs) return;
        const elapsed = gs.elapsed || (Date.now() - gs.startTime);
        let text;
        if (gs.difficulty === 'daily' && gs.dayNum) {
            text = t('dailyShareText')(gs, gs.dayNum, fmt(elapsed));
        } else {
            text = t('shareText')(gs, fmt(elapsed));
        }
        if (navigator.share) { try { await navigator.share({ title: t('shareTitle'), text }); return; } catch (_) { } }
        try { await navigator.clipboard.writeText(text); alert(t('copied')); } catch (_) { alert(text); }
    };

    /* ── 도전장 보내기 ───────────────────────────────────── */
    window.rhChallengeFriend = async function () {
        if (!gs) return;
        const wiki    = gs.wiki || (typeof WIKI !== 'undefined' ? WIKI : 'namu');
        const elapsed = gs.elapsed || (Date.now() - gs.startTime);
        const hops    = gs.hops;
        const url = `${window.location.origin}/?challenge=1` +
            `&start=${encodeURIComponent(gs.start)}` +
            `&goal=${encodeURIComponent(gs.goal)}` +
            `&wiki=${encodeURIComponent(wiki)}` +
            `&hops=${hops}&ms=${Math.round(elapsed)}`;
        const text = t('challengeText')(gs, fmt(elapsed), url);
        try {
            await navigator.clipboard.writeText(text);
            alert(t('challengeCopied'));
        } catch (_) {
            alert(text);
        }
    };

    /* ── 힌트 시스템 ─────────────────────────────────────── */
    window.rhShowHint = async function () {
        if (!gs || !gs.goal) return;
        const used = gs.hintsUsed || 0;
        if (used >= 3) { alert(t('hintNoMore')); return; }

        const n = used + 1;
        const wiki = gs.wiki || (typeof WIKI !== 'undefined' ? WIKI : 'namu');
        const btn = document.querySelector('.rh-btn-hint');
        if (btn) btn.disabled = true;
        try {
            const res = await fetch(
                `/api/hint?title=${encodeURIComponent(gs.goal)}&wiki=${encodeURIComponent(wiki)}&n=${n}`
            );
            const data = await res.json();
            gs.hintsUsed = n;
            save(gs);
            const labels = { 1: '카테고리', 2: '설명', 3: '도달 가능성' };
            alert(`💡 힌트 ${n}/3 — ${labels[n]}\n\n${data.hint}`);
        } catch (_) {
            alert('힌트를 불러오지 못했습니다.');
        } finally {
            if (btn) btn.disabled = false;
        }
    };

    // 위키 도메인 목록
    const WIKI_HOSTS = {
        'namu.wiki':          '/w/',
        'ko.wikipedia.org':   '/wiki/',
        'en.wikipedia.org':   '/wiki/',
        'de.wikipedia.org':   '/wiki/',
        'fr.wikipedia.org':   '/wiki/',
        'ja.wikipedia.org':   '/wiki/',
        'ko.m.wikipedia.org': '/wiki/',
        'en.m.wikipedia.org': '/wiki/',
        'de.m.wikipedia.org': '/wiki/',
        'fr.m.wikipedia.org': '/wiki/',
        'ja.m.wikipedia.org': '/wiki/',
    };

    // 링크 클릭 처리 — 이미 프록시된 /page/ 링크와 미처리 위키 링크 모두 처리
    document.addEventListener('click', function (e) {
        const a = e.target.closest('a');
        if (!a) return;
        const href = a.getAttribute('href') || '';

        // 이미 프록시된 링크
        if (href.startsWith('/page/')) {
            const m = href.match(/^\/page\/([^?#]*)/);
            if (m && gs && gs.active) {
                gs.hops++;
                gs.path.push(decodeURIComponent(m[1]));
                save(gs);
            }
            return;
        }

        // 위키 도메인으로 가는 미처리 링크 차단 후 프록시로 리다이렉트
        let wikiTitle = null;
        try {
            const url = new URL(href, window.location.href);
            const prefix = WIKI_HOSTS[url.hostname];
            if (prefix && url.pathname.startsWith(prefix)) {
                wikiTitle = url.pathname.slice(prefix.length).split('?')[0].split('#')[0];
            }
        } catch (_) {}

        if (wikiTitle) {
            e.preventDefault();
            const currentWiki = typeof WIKI !== 'undefined' ? WIKI : 'namu';
            const currentGoal = typeof GOAL !== 'undefined' ? GOAL : '';
            if (gs && gs.active) {
                gs.hops++;
                gs.path.push(decodeURIComponent(wikiTitle));
                save(gs);
            }
            window.location.href = `/page/${wikiTitle}?goal=${encodeURIComponent(currentGoal)}&wiki=${encodeURIComponent(currentWiki)}`;
        }
    }, false);

    // 초기화
    syncHUD();
    if (gs && gs.active && typeof IS_GOAL !== 'undefined' && !IS_GOAL) {
        raf = requestAnimationFrame(tick);
    }
    if (typeof IS_GOAL !== 'undefined' && IS_GOAL && gs && gs.active && gs.hops > 0) {
        setTimeout(showVictory, 200);
    }

    // 나무위키: SPA 레이아웃 상단 패딩 초기화 (HUD 아래 빈 공간 제거)
    if (typeof WIKI !== 'undefined' && WIKI === 'namu') {
        const app = document.getElementById('app');
        if (app) {
            const reset = el => {
                el.style.setProperty('padding-top', '0', 'important');
                el.style.setProperty('margin-top', '0', 'important');
            };
            reset(app);
            const first = app.firstElementChild;
            if (first) {
                reset(first);
                if (first.firstElementChild) reset(first.firstElementChild);
            }
        }
    }

    // 활성 게임이 없으면 포기 버튼 → 닫기(홈으로), 힌트 버튼 숨김
    if (!gs || !gs.active) {
        const btn = document.querySelector('.rh-btn-danger');
        if (btn) {
            btn.textContent = t('closeBtn');
            btn.onclick = function () { window.location.href = '/'; };
        }
        const hintBtn = document.querySelector('.rh-btn-hint');
        if (hintBtn) hintBtn.style.display = 'none';
    }
}());
