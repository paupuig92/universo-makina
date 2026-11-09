/* Service worker de Universo Makina: l'app s'obre sense cobertura.
   build.py posa a VERSION una empremta del contingut → si canvia res, el mòbil baixa la versió nova la propera vegada que té xarxa. */
const VERSION = '6b348383';
const CACHE = 'um-' + VERSION;
const FILES = ['./', 'manifest.webmanifest', 'assets/icons/icon-192.png', 'assets/icons/icon-512.png', 'assets/icons/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await c.addAll(FILES.map(f => new Request(f, { cache: 'reload' })));   // ha d'anar bé, si no, no s'instal·la
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);   // també l'antiga «um-fonts»
    await self.clients.claim();
  })());
});

// Si una versió s'ha quedat esperant, l'app la pot fer passar (botó «Actualizar»)
self.addEventListener('message', e => { if (e.data === 'skip') self.skipWaiting(); });

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
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
