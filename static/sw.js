const CACHE_NAME = 'linkyrun-v4';
const STATIC_ASSETS = [
    '/',
    '/static/manifest.json',
    '/static/icon.svg',
];
// CSS/JS는 ?v= 쿼리스트링으로 캐시 무효화되므로 SW precache에서 제외.
// 대신 아래 fetch 핸들러의 cache-first 전략으로 자동 캐싱됨.

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys()
            .then(keys => Promise.all(
                keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
            ))
            .then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // Always go network-first for dynamic routes
    if (url.pathname.startsWith('/page/') ||
        url.pathname.startsWith('/api/'))  {
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // Cache-first for static assets
    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            return fetch(event.request).then(response => {
                if (response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put(event.request, clone));
                }
                return response;
            });
        })
    );
});
