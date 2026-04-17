'use strict';

/* ── Translations ─────────────────────────────────────────────
   Keys used via data-i18n / data-i18n-html / data-i18n-placeholder
   attributes in HTML, and via t() in JS.
─────────────────────────────────────────────────────────────── */
window.I18N = {
    namu: {
        /* ── index: intro ── */
        subtitle:         '링크를 타고 목표 페이지까지 달려가세요',
        howToPlay:        '게임 방법',
        rule1:            '난이도 선택 → <strong>시작·목표 페이지</strong> 자동 배정<br>또는 직접 원하는 페이지 입력',
        rule2:            '<strong>내부 링크만</strong> 클릭해서 목표 페이지까지 이동',
        rule3:            '최단 시간 · 최소 클릭으로 도달하면 승리!',
        rule4:            '뒤로 가기 · 검색 · 외부 링크 사용 금지',
        btnStart:         '게임 시작하기',
        btnRankingFull:   '🏆 랭킹 보기',
        /* ── index: difficulty ── */
        btnBack:          '← 뒤로',
        screenDiffTitle:  '게임 시작',
        btnRanking:       '🏆 랭킹',
        randomGameTitle:  '랜덤 게임',
        randomGameDesc:   '난이도를 고르면 출발지는 랜덤으로, 목표지는 난이도에 맞게 배정됩니다.',
        diffEasy:         '쉬움',
        diffEasyDetail:   '인기 페이지',
        diffMedium:       '보통',
        diffMediumDetail: '중간 페이지',
        diffHard:         '어려움',
        diffHardDetail:   '마니아용',
        diffVeryHard:     '매우 어려움',
        diffVeryHardDetail: '고수 도전',
        customTitle:      '직접 설정',
        labelStart:       '시작',
        labelGoal:        '목표',
        placeholderPage:  '페이지 이름',
        btnCustomStart:   '게임 시작',
        /* ── leaderboard ── */
        modalRankingTitle: '🏆 랭킹',
        tabEasy:          '🟢 쉬움',
        tabMedium:        '🟡 보통',
        tabHard:          '🟠 어려움',
        tabVeryHard:      '🔴 매우 어려움',
        lbRank:           '순위',
        lbNick:           '닉네임',
        lbRoute:          '경로',
        lbHops:           '이동',
        lbTime:           '시간',
        lbDifficulty:     '난이도',
        lbEmpty:          '아직 기록이 없습니다.<br>첫 번째 도전자가 되어보세요! 🏆',
        lbLoading:        '불러오는 중…',
        lbFail:           '불러오기 실패',
        lbSelect:         '탭을 선택해서 랭킹을 확인하세요',
        /* ── index alerts / loading ── */
        alertSamePage:    '시작과 목표 페이지가 같습니다.',
        alertLoadFail:    '게임을 불러오지 못했습니다. 다시 시도해주세요.',
        alertNoStart:     '시작 페이지를 입력해주세요.',
        alertNoGoal:      '목표 페이지를 입력해주세요.',
        loadingText:      '페이지 불러오는 중…',
        loadingSearching: '난이도에 맞는 페이지 탐색 중…',
        /* ── page / app.js ── */
        hudGoalLabel:     '목표',
        btnPath:          '경로',
        btnGiveUp:        '포기',
        pathEmpty:        '이동 경로 없음',
        errorTitle:       '페이지를 찾을 수 없습니다',
        errorDesc:        '페이지가 존재하지 않거나 접근할 수 없습니다.',
        emptyLinks:       '이 페이지에는 내부 링크가 없습니다.',
        victoryTitle:     '목표 달성!',
        statTime:         '소요 시간',
        statHops:         '이동 횟수',
        pathLabel:        '이동 경로',
        rankingFormTitle: '🏆 랭킹에 등록하기',
        nicknamePlaceholder: '닉네임 (최대 20자)',
        btnSubmitRank:    '등록',
        btnPlayAgain:     '다시 하기',
        btnShare:         '공유하기 📤',
        confirmGiveUp:    '게임을 포기하시겠습니까?',
        alertNoNick:      '닉네임을 입력해주세요.',
        submitting:       '등록 중…',
        rankFail:         '등록에 실패했습니다.',
        rankOk:           '✅ 등록 완료!',
        shareTitle:       'Linky Run',
        copied:           '결과가 클립보드에 복사되었습니다! 📋',
        hopsUnit:         '회',
        countUnit:        '개',
        linkSearchPlaceholder: '링크 검색… (단축키: /)',
        wikiSelectTitle:  '위키 선택',
        wikiExtLabel:     '나무위키 ↗',
        wikiExtTitle:     '나무위키에서 원문 보기',
        giveUpTitle:      '게임을 포기하시겠습니까?',
        giveUpHome:       '홈으로 이동',
        giveUpCancel:     '아니오',
        closeBtn:         '닫기',
        giveUpGoalBtn:    (goal) => goal ? `목표 페이지로 이동 (${goal})` : '목표 페이지로 이동',
        /* functions */
        loadingPreparing: (p)    => `${p} 준비 중`,
        rankResult:       (rank) => `🏆 ${rank}위 기록 등록 완료!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops}회\n경로: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── daily challenge ── */
        tabDaily:              '📅 데일리',
        dailyBadge:            '오늘의 챌린지',
        dailyDay:              (n) => `Day ${n}`,
        btnDailyStart:         '오늘의 챌린지 시작',
        /* ── challenge a friend ── */
        btnChallenge:          '도전장<br>보내기 📨',
        challengeCopied:       '도전장이 복사됐습니다! 친구에게 공유하세요 🔗',
        challengeBannerTitle:  '🔥 도전장이 도착했습니다!',
        challengeBannerDesc:   (s, g) => `${s} → ${g} 구간을 클리어하세요!`,
        challengeAccept:       '도전 수락 ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Linky Run 도전장!\n${gs.start} → ${gs.goal}\n내 기록: ⏱ ${time}  🔗 ${gs.hops}회\n이 기록 깰 수 있어?\n🌐 ${url}`,
        /* ── personal stats ── */
        btnStats:              '내 기록 📊',
        statsTitle:            '내 게임 기록',
        statsEmpty:            '아직 플레이 기록이 없습니다.',
        statsTotalGames:       '총 게임',
        statsWins:             '승리',
        statsWinRate:          '승률',
        statsStreak:           '현재 연승',
        statsBestStreak:       '최고 연승',
        statsOverallBest:      '전체 최고 기록',
        statsBestTime:         '최단 시간',
        statsBestHops:         '최소 이동',
        statsByDiff:           '난이도별 기록',
        statsResetConfirm:     '기록을 초기화하시겠습니까?',
        btnStatsReset:         '기록 초기화',
        /* ── daily share ── */
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Day ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops}회\n경로: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── SEO / AdSense 콘텐츠 ── */
        seoAbout: `<h2 class="section-title">링키런(Linky Run)이란?</h2>
<p>링키런은 위키백과의 내부 링크만을 이용해 출발 페이지에서 목표 페이지까지 최단 경로로 도달하는 온라인 스피드런 게임입니다. 단순히 검색창에 목표를 입력해 바로 이동하는 것이 아니라, 현재 페이지 본문에 걸린 <strong>파란색 링크</strong>만 따라가며 목표까지 가는 방식이라 지식의 연결 구조를 자연스럽게 체험할 수 있습니다.</p>
<p>예를 들어 <em>"고양이"</em>에서 출발해 <em>"블랙홀"</em>까지 가야 한다면, 고양이 페이지 안에서 관련 키워드(포유류 → 생물학 → 물리학 → 천체물리학 → 블랙홀)를 찾아 클릭하며 주제의 다리를 놓아야 합니다. 먼 주제를 얼마나 짧은 경로로 연결하는지가 이 게임의 핵심 재미이며, 플레이하다 보면 세상의 모든 지식이 의외로 가까이 연결되어 있다는 사실을 발견하게 됩니다.</p>`,
        seoHowToPlay: `<h2 class="section-title">자세한 플레이 방법</h2>
<ol class="content-list">
<li><strong>위키 선택</strong> — 한국어·영어·독일어·프랑스어·일본어·스페인어·포르투갈어·이탈리아어 위키백과 중 원하는 언어를 고르세요. 언어마다 문서 수와 링크 밀도가 달라 난이도와 재미가 조금씩 다릅니다.</li>
<li><strong>난이도 선택 또는 직접 설정</strong> — 랜덤 모드에서는 난이도(쉬움·보통·어려움·매우 어려움)에 맞는 시작·목표 페이지가 자동으로 배정됩니다. 직접 설정 모드에서는 원하는 두 페이지를 직접 입력해 도전할 수 있습니다.</li>
<li><strong>링크만 따라가기</strong> — 페이지 본문 안의 파란색 내부 링크만 클릭해서 이동하세요. 브라우저 뒤로 가기, 주소창 직접 입력, 검색, 외부 링크는 사용할 수 없습니다. 이 제약이 바로 게임의 핵심 규칙입니다.</li>
<li><strong>목표 도달 & 기록 등록</strong> — 목표 페이지에 도착하면 경과 시간과 이동 횟수(홉 수)가 자동 기록됩니다. 닉네임을 입력해 글로벌 랭킹에 올리거나, 결과를 친구에게 공유 링크로 보낼 수 있습니다.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">난이도별 가이드</h2>
<ul class="content-list">
<li><strong>쉬움(Easy)</strong> — 시작·목표 페이지가 의미적으로 가까운 카테고리에서 추려집니다. 보통 2~4회 클릭이면 도달할 수 있어 규칙에 익숙해지기 좋은 단계입니다. 처음 플레이한다면 쉬움부터 시작해서 내부 링크를 찾는 감각을 익히세요.</li>
<li><strong>보통(Medium)</strong> — 서로 다른 분야를 연결해야 하는 경우가 많습니다. 인물↔지역, 사건↔개념처럼 직접 링크가 걸려 있지 않지만 한두 단계만 우회하면 닿는 페어들이 주로 출제됩니다.</li>
<li><strong>어려움(Hard)</strong> — 서로 관련 없어 보이는 두 주제가 짝지어집니다. "허브 페이지"(역사·국가·과학 등 링크가 많은 페이지)를 경유지로 활용하는 전략이 중요해집니다.</li>
<li><strong>매우 어려움(Very Hard)</strong> — 경로가 전혀 보이지 않는 먼 주제 쌍입니다. 숙련자라면 공통 허브를 직감적으로 떠올릴 수 있지만, 일반적으로는 시행착오가 필요한 도전적 모드입니다.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">공략 팁과 전략</h2>
<ul class="content-list">
<li><strong>허브 페이지를 노려라</strong> — 국가, 세기(20세기 등), 큰 학문 분야 페이지는 수백~수천 개의 링크를 가집니다. 목표가 멀게 느껴질 때 허브로 먼저 이동한 뒤 좁혀 들어가면 홉 수는 늘어도 탐색이 훨씬 빨라집니다.</li>
<li><strong>상위 개념으로 올라가기</strong> — 구체적 항목에서 막혔다면 상위 분류(예: 특정 곤충 → 곤충 → 절지동물)로 올라가서 다른 가지로 내려오는 방식을 시도해 보세요.</li>
<li><strong>첫 화면의 도입부를 먼저 읽기</strong> — 문서 앞부분에는 그 주제를 정의하는 가장 중요한 링크들이 모여 있습니다. 하단 "관련 항목"이나 외부 링크보다 본문 첫 단락을 먼저 훑는 것이 효율적입니다.</li>
<li><strong>시간보다 방향성</strong> — 초보 단계에서는 빠른 클릭보다 "이 페이지에서 어떤 분야로 넘어갈 수 있는가"를 판단하는 연습이 더 중요합니다. 같은 목표라도 경로 선택에 따라 30초와 5분이 갈립니다.</li>
<li><strong>모바일에서는 가로 스크롤 주의</strong> — 위키 표와 인포박스 안의 링크도 정상적으로 동작합니다. 놓치기 쉬우니 좌우 스크롤도 한 번씩 확인하세요.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">지원하는 위키 소개</h2>
<p>링키런은 세계 주요 언어권의 위키백과를 지원합니다. 각 위키는 문서 수, 링크 밀도, 문화적 주제 분포가 달라 같은 난이도라도 체감 난이도와 경로가 달라집니다.</p>
<ul class="content-list">
<li><strong>🇰🇷 한국어 위키백과</strong> — 한국 문화·역사·인물 주제가 풍부하고, 영어판 대비 문서 길이가 짧아 링크가 더 빠르게 읽힙니다. 입문하기 좋은 선택입니다.</li>
<li><strong>🇺🇸 English Wikipedia</strong> — 전 세계에서 가장 큰 위키백과로 문서 수가 압도적이며, 경로 다양성이 가장 높습니다. 영어 숙련자에게 추천합니다.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — 유럽 역사와 철학 주제가 탄탄합니다. 학술적 링크 구조가 잘 정리되어 있습니다.</li>
<li><strong>🇯🇵 日本語</strong> — 서브컬처·애니메이션·게임 관련 문서의 밀도가 매우 높습니다. 대중문화 주제로 놀기 좋습니다.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — 라틴 문화권의 풍부한 예술·음악·스포츠 주제로 색다른 경험을 제공합니다.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">자주 묻는 질문 (FAQ)</h2>
<dl class="faq-list">
<dt>검색창이나 뒤로 가기를 써도 되나요?</dt>
<dd>안 됩니다. 게임 규칙상 <strong>현재 문서 본문 안의 내부 링크 클릭</strong>만 허용됩니다. 검색·주소창 입력·브라우저 뒤로 가기를 사용하면 정상 기록으로 인정되지 않습니다.</dd>
<dt>경로가 존재하지 않으면 어떻게 되나요?</dt>
<dd>링크 기반으로 생성된 페어라 이론적으로 경로가 존재합니다. 다만 특정 페이지(카테고리·틀·이미지 등)는 게임에서 제외되며, 만약 막다른 길에 도달하면 언제든 "포기"를 눌러 목표 페이지를 열람하거나 홈으로 돌아갈 수 있습니다.</dd>
<dt>랭킹은 어떻게 정렬되나요?</dt>
<dd>경과 시간(ms) 오름차순을 기본으로, 동점이면 이동 횟수(홉) 오름차순으로 정렬됩니다. 즉 빠르게 + 짧게 도달한 기록이 상위에 올라갑니다.</dd>
<dt>모바일에서도 잘 되나요?</dt>
<dd>네. 링키런은 모바일 웹을 우선 고려해 설계됐고, 홈 화면에 추가해 PWA(앱처럼 사용)로도 실행할 수 있습니다. iOS Safari와 Android Chrome에서 정상 동작합니다.</dd>
<dt>내 기록은 어디에 저장되나요?</dt>
<dd>글로벌 랭킹은 서버의 PostgreSQL 데이터베이스에 저장되며, 개인 통계(플레이 횟수·최단 기록 등)는 브라우저 로컬 스토리지에 저장됩니다. 자세한 내용은 <a href="/privacy">개인정보 처리방침</a>을 참고하세요.</dd>
<dt>친구와 같은 경로로 대결할 수 있나요?</dt>
<dd>가능합니다. 목표 달성 후 "공유" 버튼을 누르면 동일한 시작·목표 페이지로 진입하는 도전장 링크가 생성됩니다. 친구가 이 링크를 열면 곧바로 같은 조건의 게임이 시작됩니다.</dd>
</dl>`,
    },

    /* ko는 namu와 동일한 한국어 번역 사용 */
    get ko() { return this.namu; },

    en: {
        subtitle:         'Follow links to reach the goal page',
        howToPlay:        'How to Play',
        rule1:            'Choose difficulty → <strong>Start & goal pages</strong> assigned automatically<br>or enter pages manually',
        rule2:            'Click only <strong>internal links</strong> to navigate to the goal',
        rule3:            'Win by reaching it fastest with fewest clicks!',
        rule4:            'No back button, search, or external links',
        btnStart:         'Start Game',
        btnRankingFull:   '🏆 Leaderboard',
        btnBack:          '← Back',
        screenDiffTitle:  'Start Game',
        btnRanking:       '🏆 Ranking',
        randomGameTitle:  'Random Game',
        randomGameDesc:   'Choose a difficulty — start is random, goal is matched to difficulty.',
        diffEasy:         'Easy',
        diffEasyDetail:   'Popular pages',
        diffMedium:       'Normal',
        diffMediumDetail: 'Mid-tier pages',
        diffHard:         'Hard',
        diffHardDetail:   'For enthusiasts',
        diffVeryHard:     'Very Hard',
        diffVeryHardDetail: 'Expert challenge',
        customTitle:      'Custom Setup',
        labelStart:       'Start',
        labelGoal:        'Goal',
        placeholderPage:  'Page name',
        btnCustomStart:   'Start',
        modalRankingTitle: '🏆 Ranking',
        tabEasy:          '🟢 Easy',
        tabMedium:        '🟡 Normal',
        tabHard:          '🟠 Hard',
        tabVeryHard:      '🔴 Very Hard',
        lbRank:           'Rank',
        lbNick:           'Nickname',
        lbRoute:          'Route',
        lbHops:           'Hops',
        lbTime:           'Time',
        lbDifficulty:     'Difficulty',
        lbEmpty:          'No records yet.<br>Be the first to play! 🏆',
        lbLoading:        'Loading…',
        lbFail:           'Failed to load',
        lbSelect:         'Select a tab to view rankings',
        alertSamePage:    'Start and goal pages are the same.',
        alertLoadFail:    'Failed to load game. Please try again.',
        alertNoStart:     'Please enter a start page.',
        alertNoGoal:      'Please enter a goal page.',
        loadingText:      'Loading page…',
        loadingSearching: 'Searching for matching pages…',
        hudGoalLabel:     'Goal',
        btnPath:          'Path',
        btnGiveUp:        'Give Up',
        pathEmpty:        'No path yet',
        errorTitle:       'Page Not Found',
        errorDesc:        'This page does not exist or cannot be accessed.',
        emptyLinks:       'This page has no internal links.',
        victoryTitle:     'Goal Reached!',
        statTime:         'Time',
        statHops:         'Hops',
        pathLabel:        'Path',
        rankingFormTitle: '🏆 Submit Score',
        nicknamePlaceholder: 'Nickname (max 20 chars)',
        btnSubmitRank:    'Submit',
        btnPlayAgain:     'Play Again',
        btnShare:         'Share 📤',
        confirmGiveUp:    'Give up on this game?',
        alertNoNick:      'Please enter a nickname.',
        submitting:       'Submitting…',
        rankFail:         'Submission failed.',
        rankOk:           '✅ Submitted!',
        shareTitle:       'Linky Run',
        copied:           'Result copied to clipboard! 📋',
        hopsUnit:         '',
        countUnit:        ' links',
        linkSearchPlaceholder: 'Search links… (shortcut: /)',
        wikiSelectTitle:  'Select Wiki',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'View on Wikipedia',
        giveUpTitle:      'Give up on this game?',
        giveUpHome:       'Go Home',
        giveUpCancel:     'Cancel',
        closeBtn:         'Close',
        giveUpGoalBtn:    (goal) => goal ? `Go to goal page (${goal})` : 'Go to goal page',
        loadingPreparing: (p)    => `Preparing ${p}`,
        rankResult:       (rank) => `🏆 Ranked #${rank}!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} hops\nPath: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Daily',
        dailyBadge:            "Today's Challenge",
        dailyDay:              (n) => `Day ${n}`,
        btnDailyStart:         "Start Today's Challenge",
        btnChallenge:          'Send Challenge 📨',
        challengeCopied:       'Challenge copied! Share it with a friend 🔗',
        challengeBannerTitle:  '🔥 Challenge Received!',
        challengeBannerDesc:   (s, g) => `Clear the route: ${s} → ${g}!`,
        challengeAccept:       'Accept ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Linky Run Challenge!\n${gs.start} → ${gs.goal}\nMy record: ⏱ ${time}  🔗 ${gs.hops} hops\nCan you beat it?\n🌐 ${url}`,
        btnStats:              'My Stats 📊',
        statsTitle:            'My Game Stats',
        statsEmpty:            'No stats yet. Play some games!',
        statsTotalGames:       'Total Games',
        statsWins:             'Wins',
        statsWinRate:          'Win Rate',
        statsStreak:           'Current Streak',
        statsBestStreak:       'Best Streak',
        statsOverallBest:      'Overall Best',
        statsBestTime:         'Best Time',
        statsBestHops:         'Fewest Hops',
        statsByDiff:           'By Difficulty',
        statsResetConfirm:     'Reset all stats?',
        btnStatsReset:         'Reset Stats',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Day ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} hops\nPath: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── SEO / AdSense content ── */
        seoAbout: `<h2 class="section-title">What is Linky Run?</h2>
<p>Linky Run is an online speedrun game where you travel from a starting Wikipedia page to a goal page using only the <strong>internal blue links</strong> inside the article. Instead of typing the target into the search bar, you must discover a chain of related topics that connects two pages — turning every session into a small journey through the map of human knowledge.</p>
<p>For example, if you must go from <em>"Cat"</em> to <em>"Black hole"</em>, you might hop Cat → Mammal → Biology → Physics → Astrophysics → Black hole. The shorter the path you discover, the higher your score. After a few rounds, you start to see just how closely seemingly unrelated subjects are actually connected.</p>`,
        seoHowToPlay: `<h2 class="section-title">How to Play — Step by Step</h2>
<ol class="content-list">
<li><strong>Pick a wiki</strong> — Choose between Korean, English, German, French, Japanese, Spanish, Portuguese, or Italian Wikipedia. Each language has a different article count and link density, which changes both the difficulty and the flavor of the puzzles.</li>
<li><strong>Random or custom match</strong> — In Random mode a start and goal page are assigned based on the chosen difficulty (Easy, Medium, Hard, Very Hard). In Custom mode you type in any two pages you want to race between.</li>
<li><strong>Follow links only</strong> — Navigate by clicking the blue internal links inside the article body. Using the browser back button, the address bar, search, or external links is not allowed. That single rule is the heart of the game.</li>
<li><strong>Reach the goal & submit</strong> — When you land on the goal page, your time and hop count are captured automatically. Enter a nickname to submit your result to the global leaderboard, or share a challenge link with a friend.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Difficulty Guide</h2>
<ul class="content-list">
<li><strong>Easy</strong> — The start and goal pages come from closely related categories. Most runs can be finished in 2–4 clicks, making this the perfect level to learn how internal links work. Start here if you are new.</li>
<li><strong>Medium</strong> — You are asked to bridge two different fields, e.g. a person and a place, or an event and a concept. There is no direct link but only one or two detours are usually enough.</li>
<li><strong>Hard</strong> — The two topics look unrelated at first glance. Using "hub pages" — articles about countries, centuries, or broad scientific fields that contain lots of links — becomes a key strategy.</li>
<li><strong>Very Hard</strong> — Topics so far apart that no path is obvious. Expert players rely on intuition about common hubs; everyone else will need a healthy amount of trial and error.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Tips & Strategy</h2>
<ul class="content-list">
<li><strong>Hunt for hub pages</strong> — Countries, centuries (e.g. "20th century"), and major academic fields contain hundreds or thousands of links. When the goal feels unreachable, detour through a hub first and narrow down from there.</li>
<li><strong>Go up before going across</strong> — Stuck on a specific article? Climb to a broader category (a specific insect → Insect → Arthropod) and then descend a different branch.</li>
<li><strong>Read the intro first</strong> — The opening paragraphs of any Wikipedia article hold the most important defining links. Scan them before scrolling to "See also" or external sections.</li>
<li><strong>Direction beats speed</strong> — Especially for beginners, choosing the right direction matters more than clicking fast. The same goal can take 30 seconds or 5 minutes depending on path selection.</li>
<li><strong>Check tables and infoboxes</strong> — Links inside infoboxes and tables are active. They are easy to miss on mobile, so scroll sideways and look at the side panels too.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Supported Wikis</h2>
<p>Linky Run supports the major world Wikipedias. Each has its own article count, link density, and cultural focus, so the same difficulty level feels different depending on the language you pick.</p>
<ul class="content-list">
<li><strong>🇰🇷 Korean Wikipedia</strong> — Strong in Korean culture, history, and biographies. Articles are shorter than the English edition, so link lists are faster to scan. A gentle entry point.</li>
<li><strong>🇺🇸 English Wikipedia</strong> — The largest encyclopedia on Earth, with unmatched article count and path diversity. Best for fluent English speakers.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Excellent coverage of European history and philosophy with tidy, scholarly link structures.</li>
<li><strong>🇯🇵 日本語</strong> — Exceptionally dense coverage of subculture, anime, and games — a paradise for pop-culture puzzles.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Rich art, music, and sports topics from the Latin world for a different flavour of speedrun.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Frequently Asked Questions (FAQ)</h2>
<dl class="faq-list">
<dt>Can I use the search bar or the back button?</dt>
<dd>No. The rules only allow <strong>clicking internal links inside the current article</strong>. Using search, the address bar, or the browser back button invalidates the run.</dd>
<dt>What if no path exists?</dt>
<dd>Pairs are generated from the live link graph, so a path always exists in theory. Some pages (categories, templates, images) are excluded from the game. If you hit a dead end you can always press "Give up" to reveal the goal page or return home.</dd>
<dt>How are rankings sorted?</dt>
<dd>Primarily by elapsed time in milliseconds, ascending. Ties are broken by hop count, ascending. Fastest and shortest wins.</dd>
<dt>Does it work on mobile?</dt>
<dd>Yes. Linky Run is designed mobile-first and can be installed as a PWA from the home screen. It works in iOS Safari and Android Chrome.</dd>
<dt>Where is my data stored?</dt>
<dd>Global rankings are stored in a PostgreSQL database on the server. Personal stats (play count, best times, etc.) live in your browser's local storage. See the <a href="/privacy">privacy policy</a> for details.</dd>
<dt>Can I challenge a friend on the same route?</dt>
<dd>Yes. After finishing a round, tap "Share" to generate a challenge link that launches an identical game (same start and goal). Whoever opens the link drops straight into the same match.</dd>
</dl>`,
    },

    de: {
        subtitle:         'Folge Links bis zur Zielseite',
        howToPlay:        'Spielanleitung',
        rule1:            'Schwierigkeit wählen → <strong>Start- & Zielseite</strong> werden zugewiesen<br>oder Seiten manuell eingeben',
        rule2:            'Nur <strong>interne Links</strong> anklicken, um zum Ziel zu navigieren',
        rule3:            'Gewinne mit der kürzesten Zeit und wenigsten Klicks!',
        rule4:            'Kein Zurück-Knopf, keine Suche, keine externen Links',
        btnStart:         'Spiel starten',
        btnRankingFull:   '🏆 Rangliste',
        btnBack:          '← Zurück',
        screenDiffTitle:  'Spiel starten',
        btnRanking:       '🏆 Rangliste',
        randomGameTitle:  'Zufallsspiel',
        randomGameDesc:   'Schwierigkeit wählen — Start ist zufällig, Ziel passend zur Schwierigkeit.',
        diffEasy:         'Einfach',
        diffEasyDetail:   'Beliebte Seiten',
        diffMedium:       'Mittel',
        diffMediumDetail: 'Mittlere Seiten',
        diffHard:         'Schwer',
        diffHardDetail:   'Für Fans',
        diffVeryHard:     'Sehr schwer',
        diffVeryHardDetail: 'Experten-Herausforderung',
        customTitle:      'Eigene Einstellung',
        labelStart:       'Start',
        labelGoal:        'Ziel',
        placeholderPage:  'Seitenname',
        btnCustomStart:   'Starten',
        modalRankingTitle: '🏆 Rangliste',
        tabEasy:          '🟢 Einfach',
        tabMedium:        '🟡 Mittel',
        tabHard:          '🟠 Schwer',
        tabVeryHard:      '🔴 Sehr schwer',
        lbRank:           'Rang',
        lbNick:           'Spitzname',
        lbRoute:          'Route',
        lbHops:           'Klicks',
        lbTime:           'Zeit',
        lbDifficulty:     'Schwierigkeit',
        lbEmpty:          'Noch keine Einträge.<br>Sei der Erste! 🏆',
        lbLoading:        'Lade…',
        lbFail:           'Laden fehlgeschlagen',
        lbSelect:         'Tab auswählen für Rangliste',
        alertSamePage:    'Start- und Zielseite sind identisch.',
        alertLoadFail:    'Spiel konnte nicht geladen werden. Bitte erneut versuchen.',
        alertNoStart:     'Bitte Startseite eingeben.',
        alertNoGoal:      'Bitte Zielseite eingeben.',
        loadingText:      'Seite wird geladen…',
        loadingSearching: 'Passende Seiten werden gesucht…',
        hudGoalLabel:     'Ziel',
        btnPath:          'Pfad',
        btnGiveUp:        'Aufgeben',
        pathEmpty:        'Noch kein Pfad',
        errorTitle:       'Seite nicht gefunden',
        errorDesc:        'Diese Seite existiert nicht oder ist nicht erreichbar.',
        emptyLinks:       'Diese Seite hat keine internen Links.',
        victoryTitle:     'Ziel erreicht!',
        statTime:         'Zeit',
        statHops:         'Klicks',
        pathLabel:        'Pfad',
        rankingFormTitle: '🏆 In Rangliste eintragen',
        nicknamePlaceholder: 'Spitzname (max. 20 Zeichen)',
        btnSubmitRank:    'Eintragen',
        btnPlayAgain:     'Nochmal spielen',
        btnShare:         'Teilen 📤',
        confirmGiveUp:    'Spiel aufgeben?',
        alertNoNick:      'Bitte Spitznamen eingeben.',
        submitting:       'Wird eingetragen…',
        rankFail:         'Eintragung fehlgeschlagen.',
        rankOk:           '✅ Eingetragen!',
        shareTitle:       'Linky Run',
        copied:           'Ergebnis in Zwischenablage kopiert! 📋',
        hopsUnit:         ' Klicks',
        countUnit:        ' Links',
        linkSearchPlaceholder: 'Links suchen… (Shortcut: /)',
        wikiSelectTitle:  'Wiki auswählen',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'Auf Wikipedia ansehen',
        giveUpTitle:      'Spiel aufgeben?',
        giveUpHome:       'Zur Startseite',
        giveUpCancel:     'Abbrechen',
        closeBtn:         'Schließen',
        giveUpGoalBtn:    (goal) => goal ? `Zur Zielseite (${goal})` : 'Zur Zielseite',
        loadingPreparing: (p)    => `${p} wird vorbereitet`,
        rankResult:       (rank) => `🏆 Platz ${rank} eingetragen!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} Klicks\nPfad: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Täglich',
        dailyBadge:            'Tages-Challenge',
        dailyDay:              (n) => `Tag ${n}`,
        btnDailyStart:         'Tages-Challenge starten',
        btnChallenge:          'Herausforderung senden 📨',
        challengeCopied:       'Herausforderung kopiert! Teile sie mit einem Freund 🔗',
        challengeBannerTitle:  '🔥 Herausforderung erhalten!',
        challengeBannerDesc:   (s, g) => `Schaffst du die Route: ${s} → ${g}?`,
        challengeAccept:       'Annehmen ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Linky Run Herausforderung!\n${gs.start} → ${gs.goal}\nMeine Zeit: ⏱ ${time}  🔗 ${gs.hops} Klicks\nKannst du das schlagen?\n🌐 ${url}`,
        btnStats:              'Meine Statistik 📊',
        statsTitle:            'Meine Statistik',
        statsEmpty:            'Noch keine Statistik. Spiel los!',
        statsTotalGames:       'Spiele gesamt',
        statsWins:             'Siege',
        statsWinRate:          'Siegrate',
        statsStreak:           'Aktuelle Serie',
        statsBestStreak:       'Beste Serie',
        statsOverallBest:      'Gesamtbestes',
        statsBestTime:         'Beste Zeit',
        statsBestHops:         'Wenigste Klicks',
        statsByDiff:           'Nach Schwierigkeit',
        statsResetConfirm:     'Statistik zurücksetzen?',
        btnStatsReset:         'Zurücksetzen',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Tag ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} Klicks\nPfad: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── SEO / AdSense Inhalt ── */
        seoAbout: `<h2 class="section-title">Was ist Linky Run?</h2>
<p>Linky Run ist ein Online-Speedrun-Spiel, bei dem du von einer Startseite zu einer Zielseite auf Wikipedia gelangen musst — ausschließlich über die <strong>blauen internen Links</strong> innerhalb des Artikels. Du tippst das Ziel nicht in die Suche, sondern entdeckst eine Kette verwandter Themen, die zwei Seiten verbindet.</p>
<p>Wenn du etwa von <em>"Katze"</em> zu <em>"Schwarzes Loch"</em> reisen sollst, könntest du Katze → Säugetier → Biologie → Physik → Astrophysik → Schwarzes Loch klicken. Je kürzer die Kette, desto besser das Ergebnis. Nach wenigen Runden merkst du, wie eng scheinbar fremde Themen tatsächlich verbunden sind.</p>`,
        seoHowToPlay: `<h2 class="section-title">So spielst du</h2>
<ol class="content-list">
<li><strong>Wiki wählen</strong> — Koreanisch, Englisch, Deutsch, Französisch, Japanisch, Spanisch, Portugiesisch oder Italienisch. Jede Sprache hat eine andere Artikelzahl und Linkdichte.</li>
<li><strong>Zufall oder Eigene Wahl</strong> — Im Zufallsmodus werden Start und Ziel passend zur Schwierigkeit (Leicht, Mittel, Schwer, Sehr schwer) zugewiesen. Im Eigene-Wahl-Modus trägst du beliebige Seiten ein.</li>
<li><strong>Nur Links</strong> — Navigiere ausschließlich über die blauen internen Links im Artikeltext. Zurück-Button, Adressleiste, Suche und externe Links sind nicht erlaubt. Genau diese Regel macht das Spiel aus.</li>
<li><strong>Ziel erreichen & einreichen</strong> — Sobald du die Zielseite öffnest, werden Zeit und Klicks automatisch gespeichert. Gib einen Spitznamen ein, um dich in die globale Rangliste einzutragen, oder teile einen Link mit Freunden.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Schwierigkeitsstufen</h2>
<ul class="content-list">
<li><strong>Leicht (Easy)</strong> — Start und Ziel stammen aus eng verwandten Kategorien. Meist reichen 2–4 Klicks. Ideal, um die Regeln zu lernen.</li>
<li><strong>Mittel (Medium)</strong> — Verbindung zweier verschiedener Bereiche: Person ↔ Ort oder Ereignis ↔ Konzept. Kein direkter Link, aber ein oder zwei Umwege genügen in der Regel.</li>
<li><strong>Schwer (Hard)</strong> — Zwei auf den ersten Blick unverwandte Themen. "Hub-Seiten" (Länder, Jahrhunderte, große Fachgebiete) als Zwischenstation werden jetzt wichtig.</li>
<li><strong>Sehr schwer (Very Hard)</strong> — Themen, die kaum erreichbar scheinen. Erfahrene Spieler erraten einen gemeinsamen Hub, alle anderen brauchen Geduld und Experimentierfreude.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Tipps & Strategie</h2>
<ul class="content-list">
<li><strong>Hubs ausnutzen</strong> — Länder, Jahrhunderte und große Fachgebiete enthalten hunderte oder tausende Links. Wenn das Ziel fern scheint, gehe erst über einen Hub und nähere dich dann an.</li>
<li><strong>Nach oben abstrahieren</strong> — Steckst du fest, steige zur übergeordneten Kategorie auf (Insekt → Gliederfüßer) und wähle einen anderen Ast.</li>
<li><strong>Einleitung zuerst lesen</strong> — Die ersten Absätze enthalten die wichtigsten definierenden Links. Scanne sie, bevor du zu "Siehe auch" oder externen Links scrollst.</li>
<li><strong>Richtung schlägt Tempo</strong> — Gerade für Einsteiger ist die richtige Richtungsentscheidung wichtiger als schnelles Klicken. Dasselbe Ziel dauert je nach Route 30 Sekunden oder 5 Minuten.</li>
<li><strong>Tabellen und Infoboxen prüfen</strong> — Links in Infoboxen und Tabellen sind aktiv. Auf dem Handy leicht zu übersehen — seitlich scrollen!</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Unterstützte Wikis</h2>
<p>Linky Run unterstützt die großen Wikipedia-Sprachversionen. Artikelzahl, Linkdichte und kulturelle Schwerpunkte unterscheiden sich, sodass dieselbe Schwierigkeitsstufe in jeder Sprache anders wirkt.</p>
<ul class="content-list">
<li><strong>🇰🇷 Koreanische Wikipedia</strong> — Stark bei Kultur, Geschichte und Biografien Koreas. Artikel sind kürzer als im Englischen, Links lassen sich schneller überblicken.</li>
<li><strong>🇺🇸 Englische Wikipedia</strong> — Die größte Enzyklopädie der Welt — unübertroffene Artikelzahl und Pfadvielfalt.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Sehr gute Abdeckung europäischer Geschichte und Philosophie mit sauberer, wissenschaftlicher Linkstruktur.</li>
<li><strong>🇯🇵 日本語</strong> — Außergewöhnlich dichte Abdeckung von Subkultur, Anime und Games — ideal für Popkultur-Rätsel.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Reichhaltige Themen zu Kunst, Musik und Sport aus der lateinischen Welt.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Häufige Fragen (FAQ)</h2>
<dl class="faq-list">
<dt>Darf ich die Suche oder den Zurück-Button nutzen?</dt>
<dd>Nein. Die Regeln erlauben nur <strong>Klicks auf interne Links im aktuellen Artikel</strong>. Suche, Adressleiste oder Zurück-Button machen den Lauf ungültig.</dd>
<dt>Was, wenn kein Pfad existiert?</dt>
<dd>Die Paare werden aus dem Linkgraphen generiert, ein Pfad existiert also theoretisch immer. Kategorien, Vorlagen und Bildseiten sind ausgenommen. Bei einer Sackgasse kannst du jederzeit "Aufgeben" drücken.</dd>
<dt>Wie wird die Rangliste sortiert?</dt>
<dd>Zuerst nach der verstrichenen Zeit in Millisekunden (aufsteigend), bei Gleichstand nach der Klickanzahl (aufsteigend). Am schnellsten und kürzesten gewinnt.</dd>
<dt>Funktioniert es auf dem Handy?</dt>
<dd>Ja. Linky Run ist mobil-zuerst entworfen und als PWA vom Startbildschirm installierbar. Funktioniert in iOS Safari und Android Chrome.</dd>
<dt>Wo werden meine Daten gespeichert?</dt>
<dd>Die globale Rangliste liegt in einer PostgreSQL-Datenbank auf dem Server. Persönliche Statistiken (Spielanzahl, Bestzeiten) liegen im Local Storage des Browsers. Details in der <a href="/privacy">Datenschutzerklärung</a>.</dd>
<dt>Kann ich Freunde auf derselben Route herausfordern?</dt>
<dd>Ja. Nach einem Lauf erstellt "Teilen" einen Herausforderungslink mit identischem Start und Ziel. Wer den Link öffnet, startet sofort dasselbe Spiel.</dd>
</dl>`,
    },

    fr: {
        subtitle:         'Suis les liens pour atteindre la page objectif',
        howToPlay:        'Comment jouer',
        rule1:            'Choisissez la difficulté → <strong>pages de départ et objectif</strong> assignées<br>ou entrez les pages manuellement',
        rule2:            'Cliquez uniquement les <strong>liens internes</strong> pour naviguer',
        rule3:            'Gagnez en atteignant l\'objectif le plus vite avec le moins de clics !',
        rule4:            'Pas de retour arrière, de recherche ni de liens externes',
        btnStart:         'Commencer',
        btnRankingFull:   '🏆 Classement',
        btnBack:          '← Retour',
        screenDiffTitle:  'Commencer',
        btnRanking:       '🏆 Classement',
        randomGameTitle:  'Jeu aléatoire',
        randomGameDesc:   'Choisissez la difficulté — départ aléatoire, objectif adapté.',
        diffEasy:         'Facile',
        diffEasyDetail:   'Pages populaires',
        diffMedium:       'Normal',
        diffMediumDetail: 'Pages intermédiaires',
        diffHard:         'Difficile',
        diffHardDetail:   'Pour les initiés',
        diffVeryHard:     'Très difficile',
        diffVeryHardDetail: 'Défi expert',
        customTitle:      'Paramètres personnalisés',
        labelStart:       'Départ',
        labelGoal:        'Objectif',
        placeholderPage:  'Nom de la page',
        btnCustomStart:   'Démarrer',
        modalRankingTitle: '🏆 Classement',
        tabEasy:          '🟢 Facile',
        tabMedium:        '🟡 Normal',
        tabHard:          '🟠 Difficile',
        tabVeryHard:      '🔴 Très difficile',
        lbRank:           'Rang',
        lbNick:           'Pseudo',
        lbRoute:          'Parcours',
        lbHops:           'Clics',
        lbTime:           'Temps',
        lbDifficulty:     'Difficulté',
        lbEmpty:          'Pas encore de records.<br>Soyez le premier ! 🏆',
        lbLoading:        'Chargement…',
        lbFail:           'Échec du chargement',
        lbSelect:         'Sélectionnez un onglet pour voir le classement',
        alertSamePage:    'Les pages de départ et d\'objectif sont identiques.',
        alertLoadFail:    'Impossible de charger le jeu. Réessayez.',
        alertNoStart:     'Veuillez entrer une page de départ.',
        alertNoGoal:      'Veuillez entrer une page objectif.',
        loadingText:      'Chargement de la page…',
        loadingSearching: 'Recherche de pages correspondantes…',
        hudGoalLabel:     'Objectif',
        btnPath:          'Chemin',
        btnGiveUp:        'Abandonner',
        pathEmpty:        'Pas encore de chemin',
        errorTitle:       'Page introuvable',
        errorDesc:        'Cette page n\'existe pas ou n\'est pas accessible.',
        emptyLinks:       'Cette page n\'a pas de liens internes.',
        victoryTitle:     'Objectif atteint !',
        statTime:         'Temps',
        statHops:         'Clics',
        pathLabel:        'Chemin',
        rankingFormTitle: '🏆 Soumettre au classement',
        nicknamePlaceholder: 'Pseudo (max 20 caractères)',
        btnSubmitRank:    'Soumettre',
        btnPlayAgain:     'Rejouer',
        btnShare:         'Partager 📤',
        confirmGiveUp:    'Abandonner cette partie ?',
        alertNoNick:      'Veuillez entrer un pseudo.',
        submitting:       'Envoi…',
        rankFail:         'Échec de la soumission.',
        rankOk:           '✅ Soumis !',
        shareTitle:       'Linky Run',
        copied:           'Résultat copié ! 📋',
        hopsUnit:         ' clics',
        countUnit:        ' liens',
        linkSearchPlaceholder: 'Rechercher… (raccourci : /)',
        wikiSelectTitle:  'Choisir un wiki',
        wikiExtLabel:     'Wikipédia ↗',
        wikiExtTitle:     'Voir sur Wikipédia',
        giveUpTitle:      'Abandonner cette partie ?',
        giveUpHome:       'Accueil',
        giveUpCancel:     'Annuler',
        closeBtn:         'Fermer',
        giveUpGoalBtn:    (goal) => goal ? `Aller à l'objectif (${goal})` : 'Aller à l\'objectif',
        loadingPreparing: (p)    => `Préparation de ${p}`,
        rankResult:       (rank) => `🏆 Classé ${rank}e !`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clics\nChemin : ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Quotidien',
        dailyBadge:            "Défi du jour",
        dailyDay:              (n) => `Jour ${n}`,
        btnDailyStart:         "Commencer le défi du jour",
        btnChallenge:          'Envoyer le défi 📨',
        challengeCopied:       'Défi copié ! Partage-le avec un ami 🔗',
        challengeBannerTitle:  '🔥 Défi reçu !',
        challengeBannerDesc:   (s, g) => `Réussis le parcours : ${s} → ${g} !`,
        challengeAccept:       'Accepter ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Défi Linky Run !\n${gs.start} → ${gs.goal}\nMon record : ⏱ ${time}  🔗 ${gs.hops} clics\nTu peux faire mieux ?\n🌐 ${url}`,
        btnStats:              'Mes stats 📊',
        statsTitle:            'Mes statistiques',
        statsEmpty:            'Pas encore de stats. Joue !',
        statsTotalGames:       'Parties jouées',
        statsWins:             'Victoires',
        statsWinRate:          'Taux de victoire',
        statsStreak:           'Série en cours',
        statsBestStreak:       'Meilleure série',
        statsOverallBest:      'Meilleur absolu',
        statsBestTime:         'Meilleur temps',
        statsBestHops:         'Moins de clics',
        statsByDiff:           'Par difficulté',
        statsResetConfirm:     'Réinitialiser les stats ?',
        btnStatsReset:         'Réinitialiser',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Jour ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clics\nChemin : ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── Contenu SEO / AdSense ── */
        seoAbout: `<h2 class="section-title">Qu'est-ce que Linky Run ?</h2>
<p>Linky Run est un jeu de speedrun en ligne où vous devez aller d'une page de départ à une page objectif sur Wikipédia, en suivant uniquement les <strong>liens internes bleus</strong> à l'intérieur de l'article. Au lieu de taper la cible dans la barre de recherche, vous devez trouver une chaîne de sujets liés qui relie deux pages.</p>
<p>Par exemple, pour aller de <em>« Chat »</em> à <em>« Trou noir »</em>, vous pourriez cliquer Chat → Mammifère → Biologie → Physique → Astrophysique → Trou noir. Plus votre chaîne est courte, meilleur est votre score. Après quelques parties, vous découvrirez à quel point des sujets apparemment éloignés sont en fait proches.</p>`,
        seoHowToPlay: `<h2 class="section-title">Comment jouer — étape par étape</h2>
<ol class="content-list">
<li><strong>Choisissez un wiki</strong> — coréen, anglais, allemand, français, japonais, espagnol, portugais ou italien. Chaque langue a un nombre d'articles et une densité de liens différents.</li>
<li><strong>Aléatoire ou personnalisé</strong> — En mode aléatoire, le départ et l'objectif sont choisis selon la difficulté (Facile, Moyen, Difficile, Très difficile). En mode personnalisé, vous entrez les deux pages de votre choix.</li>
<li><strong>Liens uniquement</strong> — Ne cliquez que sur les liens internes bleus dans le corps de l'article. Le bouton retour, la barre d'adresse, la recherche et les liens externes sont interdits. Cette règle est au cœur du jeu.</li>
<li><strong>Atteindre l'objectif & soumettre</strong> — Arrivé sur la page cible, votre temps et votre nombre de sauts sont enregistrés automatiquement. Entrez un pseudo pour rejoindre le classement mondial, ou partagez un lien de défi à vos amis.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Guide des difficultés</h2>
<ul class="content-list">
<li><strong>Facile (Easy)</strong> — Les pages de départ et d'arrivée proviennent de catégories proches. 2 à 4 clics suffisent généralement. Idéal pour découvrir les règles.</li>
<li><strong>Moyen (Medium)</strong> — Il faut relier deux domaines différents : personne ↔ lieu, événement ↔ concept. Pas de lien direct, mais un ou deux détours suffisent.</li>
<li><strong>Difficile (Hard)</strong> — Deux sujets qui semblent sans rapport. Les « pages-hub » (pays, siècles, grands domaines scientifiques) deviennent vos meilleures alliées.</li>
<li><strong>Très difficile (Very Hard)</strong> — Des sujets si éloignés qu'aucun chemin n'est évident. Les joueurs expérimentés devinent un hub commun, les autres devront expérimenter.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Astuces & stratégie</h2>
<ul class="content-list">
<li><strong>Chassez les hubs</strong> — Pays, siècles (ex. XXᵉ siècle), grandes disciplines contiennent des centaines voire des milliers de liens. Quand l'objectif paraît inaccessible, passez d'abord par un hub.</li>
<li><strong>Remontez avant de redescendre</strong> — Bloqué ? Montez vers une catégorie plus générale (un insecte précis → Insecte → Arthropode) puis redescendez par une autre branche.</li>
<li><strong>Lisez l'introduction</strong> — Les premiers paragraphes concentrent les liens qui définissent le sujet. Parcourez-les avant d'aller voir « Articles connexes » ou les liens externes.</li>
<li><strong>La direction prime sur la vitesse</strong> — Pour les débutants, choisir la bonne direction est plus important que cliquer vite. La même cible peut prendre 30 s ou 5 min selon la route.</li>
<li><strong>Regardez les tableaux et infoboxes</strong> — Les liens qu'ils contiennent sont actifs. Faciles à manquer sur mobile : défilez latéralement.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Wikis pris en charge</h2>
<p>Linky Run prend en charge les grandes Wikipédia mondiales. Nombre d'articles, densité de liens et centres culturels varient, et la même difficulté se ressent différemment selon la langue.</p>
<ul class="content-list">
<li><strong>🇰🇷 Wikipédia coréenne</strong> — Riche en culture, histoire et biographies coréennes. Articles plus courts qu'en anglais : les listes de liens se lisent vite.</li>
<li><strong>🇺🇸 Wikipédia anglaise</strong> — La plus grande encyclopédie du monde, nombre d'articles et diversité des chemins inégalés.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Excellente couverture de l'histoire et de la philosophie européennes, structure de liens soignée.</li>
<li><strong>🇯🇵 日本語</strong> — Couverture exceptionnelle de la sous-culture, de l'anime et du jeu vidéo — paradis des énigmes pop.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Sujets riches en art, musique et sport du monde latin pour un parfum différent.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Questions fréquentes (FAQ)</h2>
<dl class="faq-list">
<dt>Puis-je utiliser la recherche ou le bouton retour ?</dt>
<dd>Non. Les règles n'autorisent que <strong>les clics sur les liens internes de l'article en cours</strong>. Recherche, barre d'adresse ou bouton retour invalident la partie.</dd>
<dt>Et si aucun chemin n'existe ?</dt>
<dd>Les paires sont générées à partir du graphe de liens : un chemin existe donc toujours en théorie. Certaines pages (catégories, modèles, images) sont exclues. En cas d'impasse, utilisez « Abandonner ».</dd>
<dt>Comment le classement est-il trié ?</dt>
<dd>D'abord par temps écoulé (ms) croissant, puis par nombre de clics croissant en cas d'égalité. Le plus rapide et le plus court gagne.</dd>
<dt>Ça marche sur mobile ?</dt>
<dd>Oui. Linky Run est conçu mobile-first et installable en PWA depuis l'écran d'accueil. Il fonctionne sur iOS Safari et Android Chrome.</dd>
<dt>Où sont stockées mes données ?</dt>
<dd>Le classement mondial est stocké dans une base PostgreSQL sur le serveur. Les statistiques personnelles (nombre de parties, records) vivent dans le stockage local du navigateur. Voir la <a href="/privacy">politique de confidentialité</a>.</dd>
<dt>Puis-je défier un ami sur la même route ?</dt>
<dd>Oui. Après une partie, « Partager » génère un lien de défi qui lance la même partie (mêmes départ et objectif).</dd>
</dl>`,
    },

    ja: {
        subtitle:         'リンクをたどってゴールページへ',
        howToPlay:        '遊び方',
        rule1:            '難易度を選択 → <strong>スタート・ゴールページ</strong>が自動設定<br>または手動で入力',
        rule2:            '<strong>内部リンクのみ</strong>クリックしてゴールページへ移動',
        rule3:            '最短時間・最少クリックで到達すれば勝利！',
        rule4:            '戻るボタン・検索・外部リンク使用禁止',
        btnStart:         'ゲームスタート',
        btnRankingFull:   '🏆 ランキング',
        btnBack:          '← 戻る',
        screenDiffTitle:  'ゲームスタート',
        btnRanking:       '🏆 ランキング',
        randomGameTitle:  'ランダムゲーム',
        randomGameDesc:   '難易度を選ぶとスタートはランダム、ゴールは難易度に合わせて決まります。',
        diffEasy:         'かんたん',
        diffEasyDetail:   '人気ページ',
        diffMedium:       'ふつう',
        diffMediumDetail: '中級ページ',
        diffHard:         'むずかしい',
        diffHardDetail:   'マニア向け',
        diffVeryHard:     'とてもむずかしい',
        diffVeryHardDetail: '上級者向け',
        customTitle:      'カスタム設定',
        labelStart:       'スタート',
        labelGoal:        'ゴール',
        placeholderPage:  'ページ名',
        btnCustomStart:   'スタート',
        modalRankingTitle: '🏆 ランキング',
        tabEasy:          '🟢 かんたん',
        tabMedium:        '🟡 ふつう',
        tabHard:          '🟠 むずかしい',
        tabVeryHard:      '🔴 とてもむずかしい',
        lbRank:           '順位',
        lbNick:           'ニックネーム',
        lbRoute:          'ルート',
        lbHops:           'ホップ',
        lbTime:           'タイム',
        lbDifficulty:     '難易度',
        lbEmpty:          'まだ記録がありません。<br>最初の挑戦者になろう！🏆',
        lbLoading:        '読み込み中…',
        lbFail:           '読み込み失敗',
        lbSelect:         'タブを選んでランキングを確認',
        alertSamePage:    'スタートとゴールのページが同じです。',
        alertLoadFail:    'ゲームを読み込めませんでした。もう一度お試しください。',
        alertNoStart:     'スタートページを入力してください。',
        alertNoGoal:      'ゴールページを入力してください。',
        loadingText:      'ページ読み込み中…',
        loadingSearching: '条件に合うページを探しています…',
        hudGoalLabel:     'ゴール',
        btnPath:          'ルート',
        btnGiveUp:        'ギブアップ',
        pathEmpty:        'まだ移動なし',
        errorTitle:       'ページが見つかりません',
        errorDesc:        'このページは存在しないか、アクセスできません。',
        emptyLinks:       'このページには内部リンクがありません。',
        victoryTitle:     'ゴール達成！',
        statTime:         'タイム',
        statHops:         'ホップ数',
        pathLabel:        '移動ルート',
        rankingFormTitle: '🏆 ランキングに登録',
        nicknamePlaceholder: 'ニックネーム（最大20文字）',
        btnSubmitRank:    '登録',
        btnPlayAgain:     'もう一度',
        btnShare:         'シェア 📤',
        confirmGiveUp:    'このゲームをギブアップしますか？',
        alertNoNick:      'ニックネームを入力してください。',
        submitting:       '登録中…',
        rankFail:         '登録に失敗しました。',
        rankOk:           '✅ 登録完了！',
        shareTitle:       'Linky Run',
        copied:           '結果をコピーしました！ 📋',
        hopsUnit:         '回',
        countUnit:        '個',
        linkSearchPlaceholder: 'リンク検索… (ショートカット: /)',
        wikiSelectTitle:  'ウィキ選択',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'Wikipediaで見る',
        giveUpTitle:      'このゲームをギブアップしますか？',
        giveUpHome:       'ホームへ',
        giveUpCancel:     'キャンセル',
        closeBtn:         '閉じる',
        giveUpGoalBtn:    (goal) => goal ? `ゴールページへ移動 (${goal})` : 'ゴールページへ移動',
        loadingPreparing: (p)    => `${p} の準備中`,
        rankResult:       (rank) => `🏆 ${rank}位登録完了！`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops}回\nルート: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 デイリー',
        dailyBadge:            '今日のチャレンジ',
        dailyDay:              (n) => `Day ${n}`,
        btnDailyStart:         '今日のチャレンジを始める',
        btnChallenge:          '挑戦状を送る 📨',
        challengeCopied:       '挑戦状をコピーしました！友達にシェアしよう 🔗',
        challengeBannerTitle:  '🔥 挑戦状が届きました！',
        challengeBannerDesc:   (s, g) => `このルートをクリアせよ：${s} → ${g}`,
        challengeAccept:       '挑戦を受ける ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Linky Run 挑戦状！\n${gs.start} → ${gs.goal}\n自分の記録：⏱ ${time}  🔗 ${gs.hops}回\nこの記録を超えられる？\n🌐 ${url}`,
        btnStats:              'マイ記録 📊',
        statsTitle:            'マイゲーム記録',
        statsEmpty:            'まだ記録がありません。プレイしよう！',
        statsTotalGames:       '総ゲーム数',
        statsWins:             '勝利',
        statsWinRate:          '勝率',
        statsStreak:           '現在の連勝',
        statsBestStreak:       '最高連勝',
        statsOverallBest:      '総合ベスト',
        statsBestTime:         '最速タイム',
        statsBestHops:         '最少ホップ',
        statsByDiff:           '難易度別記録',
        statsResetConfirm:     '記録をリセットしますか？',
        btnStatsReset:         'リセット',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Day ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops}回\nルート: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── SEO / AdSense コンテンツ ── */
        seoAbout: `<h2 class="section-title">Linky Run とは?</h2>
<p>Linky Run は、Wikipedia の記事本文にある<strong>青い内部リンク</strong>だけをたどって、スタートページからゴールページへ最短で到達するオンラインスピードランゲームです。検索バーに目的地を入力するのではなく、2つのページをつなぐ関連トピックの連鎖を自分で見つけるのが醍醐味です。</p>
<p>例えば <em>「ネコ」</em>から <em>「ブラックホール」</em>へ向かう場合、ネコ → 哺乳類 → 生物学 → 物理学 → 天体物理学 → ブラックホール、といった経路が考えられます。いかに短い経路でつなげるかがスコアを決めます。数回プレイすれば、遠く見える話題どうしが意外なほど近くで繋がっていることに気づくでしょう。</p>`,
        seoHowToPlay: `<h2 class="section-title">詳しい遊び方</h2>
<ol class="content-list">
<li><strong>Wiki を選ぶ</strong> — 韓国語・英語・ドイツ語・フランス語・日本語・スペイン語・ポルトガル語・イタリア語の Wikipedia から選択できます。言語ごとに記事数とリンク密度が異なります。</li>
<li><strong>ランダム or カスタム</strong> — ランダムモードでは難易度(かんたん・ふつう・むずかしい・激むず)に応じてスタートとゴールが自動で割り当てられます。カスタムモードでは好きな2ページを指定できます。</li>
<li><strong>リンクのみで移動</strong> — 記事本文中の青い内部リンクのクリックのみが許可されます。ブラウザの戻る、アドレスバー入力、検索、外部リンクは禁止。この1つのルールこそがゲームの核です。</li>
<li><strong>ゴール到達 & 記録登録</strong> — ゴールページに着くと所要時間とホップ数が自動で記録されます。ニックネームを入力して世界ランキングに登録したり、同じ勝負を友達にシェアしたりできます。</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">難易度ガイド</h2>
<ul class="content-list">
<li><strong>かんたん(Easy)</strong> — スタートとゴールが近いカテゴリから選ばれます。2〜4クリックで到達可能。ルールに慣れるのに最適です。</li>
<li><strong>ふつう(Medium)</strong> — 人物 ↔ 地域、出来事 ↔ 概念など、異なる分野をつなぐ必要があります。1〜2ステップの迂回でたどり着けるペアが中心。</li>
<li><strong>むずかしい(Hard)</strong> — 一見無関係な2つの話題。「ハブページ」(国、世紀、大きな学問分野など)を経由する戦略が重要になります。</li>
<li><strong>激むず(Very Hard)</strong> — 経路がまったく見えない遠いペア。熟練者は共通ハブを直感で当てますが、一般的には試行錯誤が必要な挑戦的モード。</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">攻略のコツと戦略</h2>
<ul class="content-list">
<li><strong>ハブページを狙え</strong> — 国、世紀(例: 20世紀)、大きな学問分野は何百〜何千ものリンクを持ちます。遠い目標はまずハブ経由で近づけましょう。</li>
<li><strong>上位概念へ登る</strong> — 具体的な項目で詰まったら、上位カテゴリ(特定の昆虫 → 昆虫 → 節足動物)へ登って別の枝から降ります。</li>
<li><strong>冒頭を先に読む</strong> — 記事の冒頭には、その話題を定義する最重要リンクが集まります。「関連項目」や外部リンクより先に本文冒頭をスキャンしましょう。</li>
<li><strong>速さより方向</strong> — 初心者ほど、速くクリックするより「このページからどの分野に飛べるか」の判断が大事。同じゴールでもルート次第で30秒と5分の差が出ます。</li>
<li><strong>モバイルは横スクロール注意</strong> — 表や情報ボックスのリンクも有効です。見落としやすいので横にもスクロールを。</li>
</ul>`,
        seoWikis: `<h2 class="section-title">対応している Wiki</h2>
<p>Linky Run は世界の主要な Wikipedia に対応しています。言語ごとに記事数・リンク密度・文化的テーマが異なり、同じ難易度でも体感が違います。</p>
<ul class="content-list">
<li><strong>🇰🇷 韓国語 Wikipedia</strong> — 韓国文化・歴史・人物のテーマが豊富。英語版より記事が短く、リンクを一気に読める入門向き。</li>
<li><strong>🇺🇸 英語 Wikipedia</strong> — 世界最大の百科事典。記事数と経路の多様性が圧倒的。英語に慣れた上級者向け。</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — ヨーロッパの歴史・哲学テーマが充実。学術的でリンク構造が整っています。</li>
<li><strong>🇯🇵 日本語</strong> — サブカル・アニメ・ゲーム関連の記事密度が極めて高く、ポップカルチャー系パズルに最適。</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — 芸術・音楽・スポーツが豊かなラテン圏で、ひと味違うスピードランを。</li>
</ul>`,
        seoFaq: `<h2 class="section-title">よくある質問 (FAQ)</h2>
<dl class="faq-list">
<dt>検索バーや戻るボタンは使えますか?</dt>
<dd>いいえ。ルール上、<strong>現在の記事本文内の内部リンククリック</strong>のみが許可されます。検索・アドレスバー入力・戻るボタンを使うと記録は無効になります。</dd>
<dt>経路が存在しない場合は?</dt>
<dd>ペアはリンクグラフから生成されるため、理論上は常に経路が存在します。カテゴリ・テンプレート・画像ページなどは除外対象。行き止まりなら「ギブアップ」でゴールを閲覧したりホームに戻れます。</dd>
<dt>ランキングはどう並びますか?</dt>
<dd>所要時間(ms)の昇順が基本で、同タイムならホップ数の昇順。速く・短くゴールした記録が上位です。</dd>
<dt>モバイルでも動きますか?</dt>
<dd>はい。Linky Run はモバイル優先で設計されており、ホーム画面から PWA としてインストールも可能。iOS Safari と Android Chrome で動作します。</dd>
<dt>データはどこに保存されますか?</dt>
<dd>グローバルランキングはサーバーの PostgreSQL に、個人統計(プレイ回数、自己ベストなど)はブラウザの localStorage に保存されます。詳しくは<a href="/privacy">プライバシーポリシー</a>を参照。</dd>
<dt>同じ経路で友達と対戦できますか?</dt>
<dd>はい。クリア後の「シェア」ボタンで、同じスタート・ゴールが設定された挑戦状リンクが作成されます。リンクを開けば即座に同条件でゲームが始まります。</dd>
</dl>`,
    },

    es: {
        subtitle:         'Haz clic en los enlaces para llegar a la página objetivo',
        howToPlay:        'Cómo jugar',
        rule1:            'Elige la dificultad → <strong>páginas de inicio y objetivo</strong> asignadas automáticamente<br>o introduce las páginas manualmente',
        rule2:            'Haz clic solo en <strong>enlaces internos</strong> para navegar hacia el objetivo',
        rule3:            '¡Gana llegando en el menor tiempo y con menos clics!',
        rule4:            'Sin botón atrás, búsqueda ni enlaces externos',
        btnStart:         'Empezar',
        btnRankingFull:   '🏆 Clasificación',
        btnBack:          '← Atrás',
        screenDiffTitle:  'Empezar',
        btnRanking:       '🏆 Clasificación',
        randomGameTitle:  'Juego aleatorio',
        randomGameDesc:   'Elige la dificultad — el inicio es aleatorio, el objetivo se ajusta a la dificultad.',
        diffEasy:         'Fácil',
        diffEasyDetail:   'Páginas populares',
        diffMedium:       'Normal',
        diffMediumDetail: 'Páginas intermedias',
        diffHard:         'Difícil',
        diffHardDetail:   'Para entusiastas',
        diffVeryHard:     'Muy difícil',
        diffVeryHardDetail: 'Desafío experto',
        customTitle:      'Configuración personalizada',
        labelStart:       'Inicio',
        labelGoal:        'Objetivo',
        placeholderPage:  'Nombre de la página',
        btnCustomStart:   'Iniciar',
        modalRankingTitle: '🏆 Clasificación',
        tabEasy:          '🟢 Fácil',
        tabMedium:        '🟡 Normal',
        tabHard:          '🟠 Difícil',
        tabVeryHard:      '🔴 Muy difícil',
        lbRank:           'Puesto',
        lbNick:           'Apodo',
        lbRoute:          'Ruta',
        lbHops:           'Clics',
        lbTime:           'Tiempo',
        lbDifficulty:     'Dificultad',
        lbEmpty:          'Aún no hay registros.<br>¡Sé el primero! 🏆',
        lbLoading:        'Cargando…',
        lbFail:           'Error al cargar',
        lbSelect:         'Selecciona una pestaña para ver la clasificación',
        alertSamePage:    'Las páginas de inicio y objetivo son iguales.',
        alertLoadFail:    'No se pudo cargar el juego. Inténtalo de nuevo.',
        alertNoStart:     'Introduce una página de inicio.',
        alertNoGoal:      'Introduce una página objetivo.',
        loadingText:      'Cargando página…',
        loadingSearching: 'Buscando páginas adecuadas…',
        hudGoalLabel:     'Objetivo',
        btnPath:          'Ruta',
        btnGiveUp:        'Rendirse',
        pathEmpty:        'Sin ruta aún',
        errorTitle:       'Página no encontrada',
        errorDesc:        'Esta página no existe o no se puede acceder.',
        emptyLinks:       'Esta página no tiene enlaces internos.',
        victoryTitle:     '¡Objetivo alcanzado!',
        statTime:         'Tiempo',
        statHops:         'Clics',
        pathLabel:        'Ruta',
        rankingFormTitle: '🏆 Enviar puntuación',
        nicknamePlaceholder: 'Apodo (máx. 20 caracteres)',
        btnSubmitRank:    'Enviar',
        btnPlayAgain:     'Jugar de nuevo',
        btnShare:         'Compartir 📤',
        confirmGiveUp:    '¿Rendirse en esta partida?',
        alertNoNick:      'Introduce un apodo.',
        submitting:       'Enviando…',
        rankFail:         'Error al enviar.',
        rankOk:           '✅ ¡Enviado!',
        shareTitle:       'Linky Run',
        copied:           '¡Resultado copiado al portapapeles! 📋',
        hopsUnit:         ' clics',
        countUnit:        ' enlaces',
        linkSearchPlaceholder: 'Buscar enlaces… (atajo: /)',
        wikiSelectTitle:  'Elegir wiki',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'Ver en Wikipedia',
        giveUpTitle:      '¿Rendirse en esta partida?',
        giveUpHome:       'Ir al inicio',
        giveUpCancel:     'Cancelar',
        closeBtn:         'Cerrar',
        giveUpGoalBtn:    (goal) => goal ? `Ir a la página objetivo (${goal})` : 'Ir a la página objetivo',
        loadingPreparing: (p)    => `Preparando ${p}`,
        rankResult:       (rank) => `🏆 ¡Puesto ${rank} registrado!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clics\nRuta: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Diario',
        dailyBadge:            'Desafío del día',
        dailyDay:              (n) => `Día ${n}`,
        btnDailyStart:         'Comenzar el desafío del día',
        btnChallenge:          'Enviar desafío 📨',
        challengeCopied:       '¡Desafío copiado! Compártelo con un amigo 🔗',
        challengeBannerTitle:  '🔥 ¡Desafío recibido!',
        challengeBannerDesc:   (s, g) => `¡Completa la ruta: ${s} → ${g}!`,
        challengeAccept:       'Aceptar ▶',
        challengeText:         (gs, time, url) =>
            `🔥 ¡Desafío Linky Run!\n${gs.start} → ${gs.goal}\nMi récord: ⏱ ${time}  🔗 ${gs.hops} clics\n¿Puedes superarlo?\n🌐 ${url}`,
        btnStats:              'Mis estadísticas 📊',
        statsTitle:            'Mis estadísticas',
        statsEmpty:            'Aún no hay estadísticas. ¡A jugar!',
        statsTotalGames:       'Partidas totales',
        statsWins:             'Victorias',
        statsWinRate:          'Tasa de victorias',
        statsStreak:           'Racha actual',
        statsBestStreak:       'Mejor racha',
        statsOverallBest:      'Mejor global',
        statsBestTime:         'Mejor tiempo',
        statsBestHops:         'Menos clics',
        statsByDiff:           'Por dificultad',
        statsResetConfirm:     '¿Restablecer estadísticas?',
        btnStatsReset:         'Restablecer',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Día ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clics\nRuta: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── Contenido SEO / AdSense ── */
        seoAbout: `<h2 class="section-title">¿Qué es Linky Run?</h2>
<p>Linky Run es un juego de speedrun en línea en el que debes ir desde una página inicial hasta una página objetivo en Wikipedia usando únicamente los <strong>enlaces internos azules</strong> del artículo. En lugar de escribir el destino en la barra de búsqueda, tienes que descubrir una cadena de temas relacionados que conecte ambas páginas.</p>
<p>Por ejemplo, para ir de <em>«Gato»</em> a <em>«Agujero negro»</em>, podrías hacer clic: Gato → Mamífero → Biología → Física → Astrofísica → Agujero negro. Cuanto más corta sea tu ruta, mejor tu puntuación. Tras unas cuantas partidas descubrirás lo cerca que están temas que parecían muy lejanos.</p>`,
        seoHowToPlay: `<h2 class="section-title">Cómo jugar paso a paso</h2>
<ol class="content-list">
<li><strong>Elige una wiki</strong> — coreano, inglés, alemán, francés, japonés, español, portugués o italiano. Cada idioma tiene un número de artículos y densidad de enlaces diferentes.</li>
<li><strong>Aleatorio o personalizado</strong> — En modo aleatorio el inicio y el objetivo se asignan según la dificultad (Fácil, Medio, Difícil, Muy difícil). En modo personalizado escribes las dos páginas que quieras.</li>
<li><strong>Solo enlaces</strong> — Haz clic únicamente en los enlaces internos azules del cuerpo del artículo. El botón atrás, la barra de direcciones, la búsqueda y los enlaces externos están prohibidos. Esa regla es el corazón del juego.</li>
<li><strong>Llega al objetivo y envía</strong> — Al entrar en la página objetivo, tu tiempo y número de saltos se guardan automáticamente. Añade un apodo para subir al ranking global o comparte un enlace de reto con amigos.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Guía de dificultad</h2>
<ul class="content-list">
<li><strong>Fácil (Easy)</strong> — Inicio y objetivo provienen de categorías muy próximas. Normalmente se resuelve en 2–4 clics. Perfecto para aprender las reglas.</li>
<li><strong>Medio (Medium)</strong> — Hay que unir dos campos distintos: persona ↔ lugar, evento ↔ concepto. Sin enlace directo, pero uno o dos rodeos bastan.</li>
<li><strong>Difícil (Hard)</strong> — Dos temas que parecen sin relación. Las "páginas hub" (países, siglos, grandes campos académicos) se vuelven tu mejor aliada.</li>
<li><strong>Muy difícil (Very Hard)</strong> — Temas tan lejanos que ningún camino es obvio. Los expertos intuyen un hub común; el resto necesitará prueba y error.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Consejos y estrategia</h2>
<ul class="content-list">
<li><strong>Busca las páginas hub</strong> — Países, siglos (p. ej. siglo XX) y grandes campos científicos contienen cientos o miles de enlaces. Si el objetivo parece lejano, pasa primero por un hub.</li>
<li><strong>Sube antes de bajar</strong> — ¿Atascado? Sube a una categoría más general (un insecto → Insecto → Artrópodo) y baja por otra rama.</li>
<li><strong>Lee la introducción</strong> — Los primeros párrafos concentran los enlaces que definen el tema. Revísalos antes de ir a «Véase también» o enlaces externos.</li>
<li><strong>La dirección gana a la velocidad</strong> — Para principiantes, elegir la dirección correcta importa más que hacer clic rápido. La misma meta puede tardar 30 s o 5 min según la ruta.</li>
<li><strong>Revisa tablas e infoboxes</strong> — Los enlaces dentro de ellas funcionan. Son fáciles de perder en móvil: desplázate horizontalmente.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Wikis admitidas</h2>
<p>Linky Run admite las grandes Wikipedia del mundo. El número de artículos, la densidad de enlaces y los focos culturales varían, así que la misma dificultad se siente diferente según el idioma.</p>
<ul class="content-list">
<li><strong>🇰🇷 Wikipedia en coreano</strong> — Rica en cultura, historia y biografías de Corea. Artículos más cortos que en inglés: listas de enlaces fáciles de escanear.</li>
<li><strong>🇺🇸 Wikipedia en inglés</strong> — La enciclopedia más grande del mundo — cantidad de artículos y variedad de rutas inigualables.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Excelente cobertura de la historia y filosofía europeas con estructura de enlaces ordenada.</li>
<li><strong>🇯🇵 日本語</strong> — Densidad excepcional en subcultura, anime y videojuegos — paraíso para acertijos pop.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Ricos temas de arte, música y deporte del mundo latino para un sabor distinto.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Preguntas frecuentes (FAQ)</h2>
<dl class="faq-list">
<dt>¿Puedo usar la búsqueda o el botón atrás?</dt>
<dd>No. Las reglas solo permiten <strong>clics en enlaces internos del artículo actual</strong>. La búsqueda, la barra de direcciones o el botón atrás invalidan la partida.</dd>
<dt>¿Y si no existe un camino?</dt>
<dd>Los pares se generan del grafo de enlaces, así que en teoría siempre hay ruta. Categorías, plantillas e imágenes están excluidas. Si llegas a un callejón sin salida, usa «Rendirse».</dd>
<dt>¿Cómo se ordena el ranking?</dt>
<dd>Primero por tiempo transcurrido (ms) ascendente; en caso de empate, por número de clics ascendente. Gana el más rápido y corto.</dd>
<dt>¿Funciona en móvil?</dt>
<dd>Sí. Linky Run está diseñado mobile-first y se puede instalar como PWA desde la pantalla de inicio. Funciona en iOS Safari y Android Chrome.</dd>
<dt>¿Dónde se guardan mis datos?</dt>
<dd>El ranking global se guarda en una base PostgreSQL del servidor. Las estadísticas personales (partidas, mejores tiempos) viven en el almacenamiento local del navegador. Detalles en la <a href="/privacy">política de privacidad</a>.</dd>
<dt>¿Puedo retar a un amigo en la misma ruta?</dt>
<dd>Sí. Al acabar una partida, «Compartir» genera un enlace de reto que lanza el mismo juego (igual inicio y objetivo).</dd>
</dl>`,
    },

    pt: {
        subtitle:         'Clique nos links para chegar à página alvo',
        howToPlay:        'Como jogar',
        rule1:            'Escolha a dificuldade → <strong>páginas de início e alvo</strong> definidas automaticamente<br>ou insira as páginas manualmente',
        rule2:            'Clique apenas em <strong>links internos</strong> para navegar até o alvo',
        rule3:            'Vença chegando mais rápido e com menos cliques!',
        rule4:            'Sem botão voltar, busca ou links externos',
        btnStart:         'Começar',
        btnRankingFull:   '🏆 Ranking',
        btnBack:          '← Voltar',
        screenDiffTitle:  'Começar',
        btnRanking:       '🏆 Ranking',
        randomGameTitle:  'Jogo aleatório',
        randomGameDesc:   'Escolha a dificuldade — o início é aleatório, o alvo é ajustado à dificuldade.',
        diffEasy:         'Fácil',
        diffEasyDetail:   'Páginas populares',
        diffMedium:       'Normal',
        diffMediumDetail: 'Páginas intermediárias',
        diffHard:         'Difícil',
        diffHardDetail:   'Para entusiastas',
        diffVeryHard:     'Muito difícil',
        diffVeryHardDetail: 'Desafio expert',
        customTitle:      'Configuração personalizada',
        labelStart:       'Início',
        labelGoal:        'Alvo',
        placeholderPage:  'Nome da página',
        btnCustomStart:   'Iniciar',
        modalRankingTitle: '🏆 Ranking',
        tabEasy:          '🟢 Fácil',
        tabMedium:        '🟡 Normal',
        tabHard:          '🟠 Difícil',
        tabVeryHard:      '🔴 Muito difícil',
        lbRank:           'Posição',
        lbNick:           'Apelido',
        lbRoute:          'Rota',
        lbHops:           'Cliques',
        lbTime:           'Tempo',
        lbDifficulty:     'Dificuldade',
        lbEmpty:          'Ainda sem registros.<br>Seja o primeiro! 🏆',
        lbLoading:        'Carregando…',
        lbFail:           'Falha ao carregar',
        lbSelect:         'Selecione uma aba para ver o ranking',
        alertSamePage:    'As páginas de início e alvo são iguais.',
        alertLoadFail:    'Não foi possível carregar o jogo. Tente novamente.',
        alertNoStart:     'Insira uma página de início.',
        alertNoGoal:      'Insira uma página alvo.',
        loadingText:      'Carregando página…',
        loadingSearching: 'Buscando páginas adequadas…',
        hudGoalLabel:     'Alvo',
        btnPath:          'Rota',
        btnGiveUp:        'Desistir',
        pathEmpty:        'Sem rota ainda',
        errorTitle:       'Página não encontrada',
        errorDesc:        'Esta página não existe ou não pode ser acessada.',
        emptyLinks:       'Esta página não tem links internos.',
        victoryTitle:     'Alvo alcançado!',
        statTime:         'Tempo',
        statHops:         'Cliques',
        pathLabel:        'Rota',
        rankingFormTitle: '🏆 Enviar pontuação',
        nicknamePlaceholder: 'Apelido (máx. 20 caracteres)',
        btnSubmitRank:    'Enviar',
        btnPlayAgain:     'Jogar novamente',
        btnShare:         'Compartilhar 📤',
        confirmGiveUp:    'Desistir desta partida?',
        alertNoNick:      'Insira um apelido.',
        submitting:       'Enviando…',
        rankFail:         'Falha ao enviar.',
        rankOk:           '✅ Enviado!',
        shareTitle:       'Linky Run',
        copied:           'Resultado copiado! 📋',
        hopsUnit:         ' cliques',
        countUnit:        ' links',
        linkSearchPlaceholder: 'Buscar links… (atalho: /)',
        wikiSelectTitle:  'Escolher wiki',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'Ver na Wikipedia',
        giveUpTitle:      'Desistir desta partida?',
        giveUpHome:       'Ir para o início',
        giveUpCancel:     'Cancelar',
        closeBtn:         'Fechar',
        giveUpGoalBtn:    (goal) => goal ? `Ir para a página alvo (${goal})` : 'Ir para a página alvo',
        loadingPreparing: (p)    => `Preparando ${p}`,
        rankResult:       (rank) => `🏆 Posição ${rank} registrada!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} cliques\nRota: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Diário',
        dailyBadge:            'Desafio do dia',
        dailyDay:              (n) => `Dia ${n}`,
        btnDailyStart:         'Começar o desafio do dia',
        btnChallenge:          'Enviar desafio 📨',
        challengeCopied:       'Desafio copiado! Compartilhe com um amigo 🔗',
        challengeBannerTitle:  '🔥 Desafio recebido!',
        challengeBannerDesc:   (s, g) => `Complete a rota: ${s} → ${g}!`,
        challengeAccept:       'Aceitar ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Desafio Linky Run!\n${gs.start} → ${gs.goal}\nMeu recorde: ⏱ ${time}  🔗 ${gs.hops} cliques\nConsegue superar?\n🌐 ${url}`,
        btnStats:              'Minhas estatísticas 📊',
        statsTitle:            'Minhas estatísticas',
        statsEmpty:            'Ainda sem estatísticas. Jogue!',
        statsTotalGames:       'Total de partidas',
        statsWins:             'Vitórias',
        statsWinRate:          'Taxa de vitórias',
        statsStreak:           'Sequência atual',
        statsBestStreak:       'Melhor sequência',
        statsOverallBest:      'Melhor geral',
        statsBestTime:         'Melhor tempo',
        statsBestHops:         'Menos cliques',
        statsByDiff:           'Por dificuldade',
        statsResetConfirm:     'Redefinir estatísticas?',
        btnStatsReset:         'Redefinir',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Dia ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} cliques\nRota: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── Conteúdo SEO / AdSense ── */
        seoAbout: `<h2 class="section-title">O que é o Linky Run?</h2>
<p>O Linky Run é um jogo de speedrun online em que você deve ir de uma página inicial até uma página objetivo na Wikipédia usando apenas os <strong>links internos azuis</strong> dentro do artigo. Em vez de digitar o destino na barra de busca, você precisa descobrir uma cadeia de tópicos relacionados que conecta duas páginas.</p>
<p>Por exemplo, para ir de <em>"Gato"</em> a <em>"Buraco negro"</em>, você pode clicar: Gato → Mamífero → Biologia → Física → Astrofísica → Buraco negro. Quanto mais curta sua rota, melhor a pontuação. Depois de algumas partidas, você vai perceber o quanto tópicos aparentemente distantes estão, na verdade, próximos.</p>`,
        seoHowToPlay: `<h2 class="section-title">Como jogar passo a passo</h2>
<ol class="content-list">
<li><strong>Escolha uma wiki</strong> — coreano, inglês, alemão, francês, japonês, espanhol, português ou italiano. Cada idioma tem um número de artigos e densidade de links diferentes.</li>
<li><strong>Aleatório ou personalizado</strong> — No modo aleatório o início e o objetivo são atribuídos conforme a dificuldade (Fácil, Médio, Difícil, Muito difícil). No modo personalizado você digita as duas páginas.</li>
<li><strong>Apenas links</strong> — Clique somente nos links internos azuis no corpo do artigo. Botão voltar, barra de endereços, busca e links externos são proibidos. Essa regra única é o coração do jogo.</li>
<li><strong>Chegue ao objetivo e envie</strong> — Ao alcançar a página objetivo, seu tempo e número de saltos são registrados automaticamente. Digite um apelido para entrar no ranking global, ou compartilhe um link de desafio com amigos.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Guia de dificuldade</h2>
<ul class="content-list">
<li><strong>Fácil (Easy)</strong> — Início e objetivo vêm de categorias próximas. Em geral, 2 a 4 cliques bastam. Perfeito para aprender as regras.</li>
<li><strong>Médio (Medium)</strong> — É preciso ligar dois campos diferentes: pessoa ↔ lugar, evento ↔ conceito. Sem link direto, mas um ou dois desvios são suficientes.</li>
<li><strong>Difícil (Hard)</strong> — Dois tópicos aparentemente sem relação. As "páginas-hub" (países, séculos, grandes áreas acadêmicas) tornam-se sua melhor aliada.</li>
<li><strong>Muito difícil (Very Hard)</strong> — Tópicos tão distantes que nenhum caminho é óbvio. Jogadores experientes intuem um hub comum; os demais precisarão de tentativa e erro.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Dicas e estratégia</h2>
<ul class="content-list">
<li><strong>Procure páginas-hub</strong> — Países, séculos (ex.: século XX) e grandes áreas científicas têm centenas ou milhares de links. Quando o objetivo parecer longe, passe primeiro por um hub.</li>
<li><strong>Suba antes de descer</strong> — Travado? Suba para uma categoria mais ampla (um inseto específico → Inseto → Artrópode) e desça por outro ramo.</li>
<li><strong>Leia a introdução primeiro</strong> — Os primeiros parágrafos concentram os links que definem o tema. Passe os olhos antes de ir a "Ver também" ou links externos.</li>
<li><strong>Direção vence velocidade</strong> — Para iniciantes, escolher a direção certa importa mais do que clicar rápido. O mesmo alvo pode levar 30 s ou 5 min, dependendo da rota.</li>
<li><strong>Confira tabelas e infoboxes</strong> — Os links dentro delas são ativos. Fáceis de perder no celular: role lateralmente também.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Wikis suportadas</h2>
<p>O Linky Run suporta as grandes Wikipédias do mundo. Número de artigos, densidade de links e focos culturais variam, e a mesma dificuldade "sente" diferente conforme o idioma.</p>
<ul class="content-list">
<li><strong>🇰🇷 Wikipédia coreana</strong> — Forte em cultura, história e biografias coreanas. Artigos mais curtos que a inglesa: listas de links fáceis de escanear.</li>
<li><strong>🇺🇸 Wikipédia inglesa</strong> — A maior enciclopédia do mundo — número de artigos e variedade de rotas incomparáveis.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Excelente cobertura de história e filosofia europeias, com estrutura de links organizada.</li>
<li><strong>🇯🇵 日本語</strong> — Densidade excepcional de subcultura, anime e games — paraíso para enigmas pop.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Temas ricos de arte, música e esportes do mundo latino para um sabor diferente.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Perguntas frequentes (FAQ)</h2>
<dl class="faq-list">
<dt>Posso usar a busca ou o botão voltar?</dt>
<dd>Não. As regras só permitem <strong>cliques em links internos do artigo atual</strong>. Busca, barra de endereços ou botão voltar invalidam a partida.</dd>
<dt>E se não existir caminho?</dt>
<dd>Os pares são gerados a partir do grafo de links, então em teoria sempre existe caminho. Categorias, predefinições e imagens são excluídas. Em caso de beco sem saída, use "Desistir".</dd>
<dt>Como o ranking é ordenado?</dt>
<dd>Primeiro pelo tempo decorrido (ms) ascendente; em empate, pelo número de cliques ascendente. Vence o mais rápido e o mais curto.</dd>
<dt>Funciona no celular?</dt>
<dd>Sim. O Linky Run é mobile-first e pode ser instalado como PWA a partir da tela inicial. Funciona em iOS Safari e Android Chrome.</dd>
<dt>Onde meus dados ficam guardados?</dt>
<dd>O ranking global fica em um banco PostgreSQL no servidor. As estatísticas pessoais (partidas, melhores tempos) ficam no armazenamento local do navegador. Veja a <a href="/privacy">política de privacidade</a>.</dd>
<dt>Posso desafiar um amigo na mesma rota?</dt>
<dd>Sim. Ao terminar uma partida, "Compartilhar" gera um link de desafio que inicia o mesmo jogo (mesmo início e objetivo).</dd>
</dl>`,
    },

    it: {
        subtitle:         'Clicca i link per raggiungere la pagina obiettivo',
        howToPlay:        'Come giocare',
        rule1:            'Scegli la difficoltà → <strong>pagine di partenza e obiettivo</strong> assegnate automaticamente<br>oppure inserisci le pagine manualmente',
        rule2:            'Clicca solo i <strong>link interni</strong> per navigare verso l\'obiettivo',
        rule3:            'Vinci arrivando nel minor tempo e con meno clic!',
        rule4:            'Niente pulsante indietro, ricerca o link esterni',
        btnStart:         'Inizia',
        btnRankingFull:   '🏆 Classifica',
        btnBack:          '← Indietro',
        screenDiffTitle:  'Inizia',
        btnRanking:       '🏆 Classifica',
        randomGameTitle:  'Gioco casuale',
        randomGameDesc:   'Scegli la difficoltà — la partenza è casuale, l\'obiettivo è adatto alla difficoltà.',
        diffEasy:         'Facile',
        diffEasyDetail:   'Pagine popolari',
        diffMedium:       'Normale',
        diffMediumDetail: 'Pagine intermedie',
        diffHard:         'Difficile',
        diffHardDetail:   'Per appassionati',
        diffVeryHard:     'Molto difficile',
        diffVeryHardDetail: 'Sfida esperta',
        customTitle:      'Impostazioni personalizzate',
        labelStart:       'Partenza',
        labelGoal:        'Obiettivo',
        placeholderPage:  'Nome della pagina',
        btnCustomStart:   'Avvia',
        modalRankingTitle: '🏆 Classifica',
        tabEasy:          '🟢 Facile',
        tabMedium:        '🟡 Normale',
        tabHard:          '🟠 Difficile',
        tabVeryHard:      '🔴 Molto difficile',
        lbRank:           'Posizione',
        lbNick:           'Soprannome',
        lbRoute:          'Percorso',
        lbHops:           'Clic',
        lbTime:           'Tempo',
        lbDifficulty:     'Difficoltà',
        lbEmpty:          'Nessun record ancora.<br>Sii il primo! 🏆',
        lbLoading:        'Caricamento…',
        lbFail:           'Caricamento fallito',
        lbSelect:         'Seleziona una scheda per vedere la classifica',
        alertSamePage:    'Le pagine di partenza e obiettivo sono uguali.',
        alertLoadFail:    'Impossibile caricare il gioco. Riprova.',
        alertNoStart:     'Inserisci una pagina di partenza.',
        alertNoGoal:      'Inserisci una pagina obiettivo.',
        loadingText:      'Caricamento pagina…',
        loadingSearching: 'Ricerca di pagine adatte…',
        hudGoalLabel:     'Obiettivo',
        btnPath:          'Percorso',
        btnGiveUp:        'Arrendersi',
        pathEmpty:        'Nessun percorso ancora',
        errorTitle:       'Pagina non trovata',
        errorDesc:        'Questa pagina non esiste o non è accessibile.',
        emptyLinks:       'Questa pagina non ha link interni.',
        victoryTitle:     'Obiettivo raggiunto!',
        statTime:         'Tempo',
        statHops:         'Clic',
        pathLabel:        'Percorso',
        rankingFormTitle: '🏆 Invia punteggio',
        nicknamePlaceholder: 'Soprannome (max 20 caratteri)',
        btnSubmitRank:    'Invia',
        btnPlayAgain:     'Gioca ancora',
        btnShare:         'Condividi 📤',
        confirmGiveUp:    'Arrendersi in questa partita?',
        alertNoNick:      'Inserisci un soprannome.',
        submitting:       'Invio…',
        rankFail:         'Invio fallito.',
        rankOk:           '✅ Inviato!',
        shareTitle:       'Linky Run',
        copied:           'Risultato copiato! 📋',
        hopsUnit:         ' clic',
        countUnit:        ' link',
        linkSearchPlaceholder: 'Cerca link… (scorciatoia: /)',
        wikiSelectTitle:  'Scegli wiki',
        wikiExtLabel:     'Wikipedia ↗',
        wikiExtTitle:     'Vedi su Wikipedia',
        giveUpTitle:      'Arrendersi in questa partita?',
        giveUpHome:       'Vai alla home',
        giveUpCancel:     'Annulla',
        closeBtn:         'Chiudi',
        giveUpGoalBtn:    (goal) => goal ? `Vai alla pagina obiettivo (${goal})` : 'Vai alla pagina obiettivo',
        loadingPreparing: (p)    => `Preparazione di ${p}`,
        rankResult:       (rank) => `🏆 Posizione ${rank} registrata!`,
        shareText: (gs, time) =>
            `🔗 Linky Run\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clic\nPercorso: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        tabDaily:              '📅 Giornaliero',
        dailyBadge:            'Sfida del giorno',
        dailyDay:              (n) => `Giorno ${n}`,
        btnDailyStart:         'Inizia la sfida del giorno',
        btnChallenge:          'Invia sfida 📨',
        challengeCopied:       'Sfida copiata! Condividila con un amico 🔗',
        challengeBannerTitle:  '🔥 Sfida ricevuta!',
        challengeBannerDesc:   (s, g) => `Completa il percorso: ${s} → ${g}!`,
        challengeAccept:       'Accetta ▶',
        challengeText:         (gs, time, url) =>
            `🔥 Sfida Linky Run!\n${gs.start} → ${gs.goal}\nIl mio record: ⏱ ${time}  🔗 ${gs.hops} clic\nRiesci a batterlo?\n🌐 ${url}`,
        btnStats:              'Le mie statistiche 📊',
        statsTitle:            'Le mie statistiche',
        statsEmpty:            'Nessuna statistica ancora. Gioca!',
        statsTotalGames:       'Partite totali',
        statsWins:             'Vittorie',
        statsWinRate:          'Tasso di vittorie',
        statsStreak:           'Serie attuale',
        statsBestStreak:       'Miglior serie',
        statsOverallBest:      'Miglior risultato',
        statsBestTime:         'Miglior tempo',
        statsBestHops:         'Meno clic',
        statsByDiff:           'Per difficoltà',
        statsResetConfirm:     'Reimpostare le statistiche?',
        btnStatsReset:         'Reimposta',
        dailyShareText:        (gs, day, time) =>
            `📅 Linky Run — Giorno ${day}\n${gs.start} → ${gs.goal}\n⏱ ${time}  🔗 ${gs.hops} clic\nPercorso: ${(gs.path||[]).join(' → ')}\n🌐 ${window.location.origin}`,
        /* ── Contenuti SEO / AdSense ── */
        seoAbout: `<h2 class="section-title">Cos'è Linky Run?</h2>
<p>Linky Run è un gioco di speedrun online in cui devi andare da una pagina di partenza a una pagina obiettivo di Wikipedia usando soltanto i <strong>link interni blu</strong> presenti nell'articolo. Invece di digitare l'obiettivo nella barra di ricerca, devi scoprire una catena di argomenti correlati che collega le due pagine.</p>
<p>Per esempio, per andare da <em>«Gatto»</em> a <em>«Buco nero»</em>, potresti cliccare: Gatto → Mammifero → Biologia → Fisica → Astrofisica → Buco nero. Più corta è la tua catena, migliore è il punteggio. Dopo qualche partita scoprirai quanto siano vicini argomenti che sembravano lontanissimi.</p>`,
        seoHowToPlay: `<h2 class="section-title">Come si gioca — passo per passo</h2>
<ol class="content-list">
<li><strong>Scegli una wiki</strong> — coreano, inglese, tedesco, francese, giapponese, spagnolo, portoghese o italiano. Ogni lingua ha un numero di articoli e una densità di link diversi.</li>
<li><strong>Casuale o personalizzato</strong> — In modalità casuale la partenza e l'obiettivo vengono assegnati in base alla difficoltà (Facile, Medio, Difficile, Molto difficile). In modalità personalizzata inserisci tu le due pagine.</li>
<li><strong>Solo link</strong> — Naviga esclusivamente sui link interni blu nel corpo dell'articolo. Pulsante Indietro, barra degli indirizzi, ricerca e link esterni sono vietati. Questa unica regola è il cuore del gioco.</li>
<li><strong>Raggiungi l'obiettivo e invia</strong> — Appena atterri sulla pagina obiettivo, tempo e numero di salti vengono registrati automaticamente. Inserisci un nickname per entrare nella classifica globale, o condividi un link di sfida con gli amici.</li>
</ol>`,
        seoDifficulty: `<h2 class="section-title">Guida alle difficoltà</h2>
<ul class="content-list">
<li><strong>Facile (Easy)</strong> — Partenza e obiettivo provengono da categorie vicine. Di solito bastano 2–4 clic. Perfetto per imparare le regole.</li>
<li><strong>Medio (Medium)</strong> — Bisogna collegare due campi diversi: persona ↔ luogo, evento ↔ concetto. Nessun link diretto, ma uno o due passaggi bastano.</li>
<li><strong>Difficile (Hard)</strong> — Due argomenti apparentemente senza legame. Le "pagine hub" (paesi, secoli, grandi discipline) diventano la tua arma migliore.</li>
<li><strong>Molto difficile (Very Hard)</strong> — Argomenti così distanti che nessun percorso è ovvio. I veterani intuiscono un hub comune, agli altri servirà tentativo ed errore.</li>
</ul>`,
        seoStrategy: `<h2 class="section-title">Consigli e strategia</h2>
<ul class="content-list">
<li><strong>Caccia agli hub</strong> — Paesi, secoli (es. XX secolo), grandi discipline contengono centinaia o migliaia di link. Se l'obiettivo sembra lontano, passa prima da un hub.</li>
<li><strong>Sali prima di scendere</strong> — Bloccato? Sali a una categoria più ampia (un insetto specifico → Insetto → Artropode) e poi scendi per un altro ramo.</li>
<li><strong>Leggi prima l'introduzione</strong> — I primi paragrafi concentrano i link che definiscono l'argomento. Scorrili prima di "Voci correlate" o link esterni.</li>
<li><strong>La direzione batte la velocità</strong> — Per i principianti, scegliere la direzione giusta conta più che cliccare velocemente. Lo stesso obiettivo può richiedere 30 s o 5 min a seconda del percorso.</li>
<li><strong>Controlla tabelle e infobox</strong> — I link al loro interno sono attivi. Su mobile si perdono facilmente: scorri anche lateralmente.</li>
</ul>`,
        seoWikis: `<h2 class="section-title">Wiki supportate</h2>
<p>Linky Run supporta le principali Wikipedia del mondo. Numero di articoli, densità di link e focus culturali variano, quindi la stessa difficoltà si percepisce diversa a seconda della lingua.</p>
<ul class="content-list">
<li><strong>🇰🇷 Wikipedia coreana</strong> — Ricca di cultura, storia e biografie coreane. Articoli più corti rispetto all'inglese: liste di link veloci da scorrere.</li>
<li><strong>🇺🇸 Wikipedia inglese</strong> — La più grande enciclopedia al mondo — numero di articoli e varietà di percorsi impareggiabili.</li>
<li><strong>🇩🇪 Deutsch / 🇫🇷 Français</strong> — Ottima copertura di storia e filosofia europee, con struttura dei link ordinata.</li>
<li><strong>🇯🇵 日本語</strong> — Densità eccezionale di sottocultura, anime e videogiochi — paradiso per enigmi pop.</li>
<li><strong>🇪🇸 Español / 🇵🇹 Português / 🇮🇹 Italiano</strong> — Temi ricchi di arte, musica e sport del mondo latino per un sapore diverso.</li>
</ul>`,
        seoFaq: `<h2 class="section-title">Domande frequenti (FAQ)</h2>
<dl class="faq-list">
<dt>Posso usare la ricerca o il pulsante Indietro?</dt>
<dd>No. Le regole permettono solo <strong>clic sui link interni dell'articolo corrente</strong>. Ricerca, barra degli indirizzi o pulsante Indietro invalidano la partita.</dd>
<dt>E se non esiste alcun percorso?</dt>
<dd>Le coppie sono generate dal grafo dei link, quindi un percorso esiste sempre in teoria. Categorie, template e pagine di immagini sono escluse. In caso di vicolo cieco, usa "Arrenditi".</dd>
<dt>Come è ordinata la classifica?</dt>
<dd>Prima per tempo trascorso (ms) crescente; in caso di parità, per numero di clic crescente. Vince chi è più veloce e più corto.</dd>
<dt>Funziona da mobile?</dt>
<dd>Sì. Linky Run è pensato mobile-first e si installa come PWA dalla schermata Home. Funziona su iOS Safari e Android Chrome.</dd>
<dt>Dove vengono salvati i miei dati?</dt>
<dd>La classifica globale è in un database PostgreSQL sul server. Le statistiche personali (partite, miglior tempo) vivono nel localStorage del browser. Vedi la <a href="/privacy">privacy policy</a>.</dd>
<dt>Posso sfidare un amico sullo stesso percorso?</dt>
<dd>Sì. A partita finita, "Condividi" genera un link di sfida che avvia lo stesso gioco (stessa partenza e stesso obiettivo).</dd>
</dl>`,
    },
};

/* ── Current wiki (set by each page) ─────────────────────── */
window._WIKI = 'ko';

/** Translate key for the current wiki (falls back to ko). */
window.t = function (key) {
    const d = window.I18N[window._WIKI] || window.I18N['ko'] || window.I18N['namu'];
    if (key in d) return d[key];
    return (window.I18N['ko'] || window.I18N['namu'])[key] ?? key;
};

/** Apply data-i18n* attributes throughout the document. */
window.applyI18n = function () {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.dataset.i18n);
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
        el.innerHTML = t(el.dataset.i18nHtml);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        el.placeholder = t(el.dataset.i18nPlaceholder);
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        el.title = t(el.dataset.i18nTitle);
    });
};
