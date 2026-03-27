'use strict';
(function () {
    const SK = 'namuSpeedrun';

    function load() {
        try { return JSON.parse(localStorage.getItem(SK) || 'null'); } catch (_) { return null; }
    }
    function save(s) { localStorage.setItem(SK, JSON.stringify(s)); }
    function clear() { localStorage.removeItem(SK); }

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
            el.innerHTML = '<span class="rh-path-item">이동 경로 없음</span>';
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
        if (!confirm('게임을 포기하시겠습니까?')) return;
        clear();
        window.location.href = '/';
    };

    function showVictory() {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        const elapsed = gs ? Date.now() - gs.startTime : 0;
        if (gs) { gs.active = false; gs.elapsed = elapsed; save(gs); }

        const te = document.getElementById('rh-v-time');
        const he = document.getElementById('rh-v-hops');
        const pe = document.getElementById('rh-v-path');
        const ti = document.getElementById('rh-timer');
        if (te) te.textContent = fmt(elapsed);
        if (he) he.textContent = gs ? gs.hops + '회' : '—';
        if (ti) ti.textContent = fmt(elapsed);
        if (pe && gs && gs.path) {
            pe.innerHTML = gs.path.map((p, i) => {
                const isG = i === gs.path.length - 1;
                return (i > 0 ? '<span class="rh-vpath-arrow">→</span>' : '') +
                    `<span${isG ? ' class="rh-vpath-goal"' : ''}>${esc(p)}</span>`;
            }).join('');
        }
        const ov = document.getElementById('rh-victory');
        if (ov) ov.style.display = 'flex';
    }

    window.rhPlayAgain = function () { clear(); window.location.href = '/'; };

    window.rhSubmitRank = async function () {
        if (!gs) return;
        const nick = (document.getElementById('rh-nickname')?.value || '').trim();
        if (!nick) { alert('닉네임을 입력해주세요.'); return; }
        const elapsed = gs.elapsed || (Date.now() - gs.startTime);
        const btn = document.getElementById('rh-rank-btn');
        if (btn) { btn.disabled = true; btn.textContent = '등록 중…'; }
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
            if (re) { re.style.display = 'block'; re.textContent = rank > 0 ? `🏆 ${rank}위 기록 등록 완료!` : '✅ 등록 완료!'; }
        } catch (_) {
            if (btn) { btn.disabled = false; btn.textContent = '등록'; }
            alert('등록에 실패했습니다.');
        }
    };

    window.rhShare = async function () {
        if (!gs) return;
        const elapsed = gs.elapsed || (Date.now() - gs.startTime);
        const path = (gs.path || []).join(' → ');
        const text = `🐇 Rabbit Hole\n${gs.start} → ${gs.goal}\n⏱ ${fmt(elapsed)}  🔗 ${gs.hops}회\n경로: ${path}`;
        if (navigator.share) { try { await navigator.share({ title: 'Rabbit Hole', text }); return; } catch (_) { } }
        try { await navigator.clipboard.writeText(text); alert('결과가 복사되었습니다! 📋'); } catch (_) { alert(text); }
    };

    // 내부 링크 클릭 처리 (/page/ 경로로 리라우팅된 링크)
    document.addEventListener('click', function (e) {
        const a = e.target.closest('a');
        if (!a) return;
        const href = a.getAttribute('href') || '';
        if (!href.startsWith('/page/')) return;
        const m = href.match(/^\/page\/([^?#]*)/);
        if (!m) return;
        const nextTitle = decodeURIComponent(m[1]);
        if (gs && gs.active) {
            gs.hops++;
            gs.path.push(nextTitle);
            save(gs);
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
}());
