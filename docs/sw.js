/* Service worker de Universo Makina: l'app s'obre sense cobertura.
   build.py canvia VERSION a cada build → el mòbil baixa la nova versió la propera vegada que té xarxa. */
const VERSION = '20261103-133723-c7d268c1';
const CACHE = 'um-' + VERSION;
const FONTS = 'um-fonts';   // la lletra (Google Fonts) es guarda a part: no cal tornar-la a baixar a cada versió
const FILES = ['./', 'manifest.webmanifest', 'assets/icons/icon-192.png', 'assets/icons/icon-512.png', 'assets/icons/apple-touch-icon.png'];
const FONT_CSS = 'https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap';
const isFont = u => u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com';

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(FILES.map(f => new Request(f, { cache: 'reload' })));   // ha d'anar bé, si no, no s'instal·la
    // Lletra: si falla (sense xarxa), l'app tira de Helvetica Neue igualment
    try {
      const fc = await caches.open(FONTS);
      if (!(await fc.match(FONT_CSS))) {
        const r = await fetch(FONT_CSS, { mode: 'cors' });
        if (r.ok) {
          const css = await r.clone().text();
          await fc.put(FONT_CSS, r);
          const urls = [...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map(m => m[1]);
          await Promise.all(urls.map(u => fetch(u, { mode: 'cors' }).then(x => x.ok && fc.put(u, x)).catch(() => {})));
        }
      }
    } catch {}
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE && k !== FONTS) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (isFont(u)) {   // lletra: primer la guardada; si no hi és, xarxa i es guarda
    e.respondWith(caches.open(FONTS).then(async c => (await c.match(req)) || fetch(req).then(r => { if (r.ok || r.type === 'opaque') c.put(req, r.clone()); return r; })));
    return;
  }
  if (u.origin !== location.origin) return;
  // Pàgina i fitxers propis: primer la memòria (obre a l'instant i sense cobertura); si no hi és, xarxa
  e.respondWith((async () => {
    const c = await caches.open(CACHE);
    const hit = req.mode === 'navigate'
      ? (await c.match(req, { ignoreSearch: true })) || (await c.match('./'))
      : await c.match(req, { ignoreSearch: true });
    return hit || fetch(req);
  })());
});
