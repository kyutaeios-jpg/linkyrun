export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 토큰은 Authorization 헤더 우선, 폴백으로 쿼리 파라미터도 허용 (하위 호환)
    const token = request.headers.get('Authorization')?.replace('Bearer ', '') || url.searchParams.get('token');
    if (token !== env.SECRET_TOKEN) {
      return new Response('Unauthorized', { status: 401 });
    }

    const type = url.searchParams.get('type');

    // 랜덤 페이지 제목만 반환 (body 없음)
    if (type === 'random') {
      try {
        const response = await fetch('https://namu.wiki/random', {
          headers: {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'ko-KR,ko;q=0.9',
          },
          redirect: 'follow',
        });
        return new Response('', {
          headers: {
            'X-Namu-Url': response.url,
            'X-Namu-Status': String(response.status),
          },
        });
      } catch (e) {
        return new Response(`Error: ${e.message}`, { status: 502 });
      }
    }

    // 이미지 프록시 (나무위키 CDN 핫링크 차단 우회)
    if (type === 'image') {
      const imageUrl = url.searchParams.get('url');
      if (!imageUrl) return new Response('Missing url', { status: 400 });

      // 허용 도메인: *.namu.la 만 허용
      let parsed;
      try { parsed = new URL(imageUrl); }
      catch (_) { return new Response('Invalid url', { status: 400 }); }
      if (!parsed.hostname.endsWith('.namu.la') && parsed.hostname !== 'namu.la') {
        return new Response('Forbidden', { status: 403 });
      }

      try {
        const response = await fetch(imageUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Referer': 'https://namu.wiki/',
          },
        });
        const body = await response.arrayBuffer();
        return new Response(body, {
          status: response.status,
          headers: {
            'Content-Type': response.headers.get('Content-Type') || 'image/jpeg',
            'Cache-Control': 'public, max-age=86400',
            'Access-Control-Allow-Origin': '*',
          },
        });
      } catch (e) {
        return new Response(`Error: ${e.message}`, { status: 502 });
      }
    }

    // 역링크 수 조회 (나무위키 backlink API)
    if (type === 'backlink') {
      const title = url.searchParams.get('title');
      if (!title) return new Response('Missing title', { status: 400 });
      try {
        const blUrl = `https://namu.wiki/backlink/${encodeURIComponent(title)}`;
        const response = await fetch(blUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json',
            'Accept-Language': 'ko-KR,ko;q=0.9',
            'Referer': 'https://namu.wiki/',
          },
          redirect: 'follow',
        });
        const text = await response.text();
        return new Response(text, {
          status: response.status,
          headers: { 'Content-Type': 'text/html; charset=utf-8' },
        });
      } catch (e) {
        return new Response(`Error: ${e.message}`, { status: 502 });
      }
    }

    // 일반 페이지 fetch
    const title = url.searchParams.get('title');
    if (!title) {
      return new Response('Missing title', { status: 400 });
    }

    const namuUrl = `https://namu.wiki/w/${encodeURIComponent(title)}`;

    try {
      const response = await fetch(namuUrl, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'ko-KR,ko;q=0.9',
          'Referer': 'https://namu.wiki/',
        },
        redirect: 'follow',
      });

      const html = await response.text();

      return new Response(html, {
        status: response.status,
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'X-Namu-Status': String(response.status),
          'X-Namu-Url': response.url,
        },
      });
    } catch (e) {
      return new Response(`Fetch error: ${e.message}`, { status: 502 });
    }
  },
};
