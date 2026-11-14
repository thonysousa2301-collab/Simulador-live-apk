const CACHE = "simulador-live-v5";
const ARQUIVOS = ["./", "./index.html", "./manifest.json", "./icon-192.png", "./icon-512.png"];
const THREE_URL = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then(async (cache) => {
      await cache.addAll(ARQUIVOS);
      try {
        const resposta = await fetch(THREE_URL, { mode: "no-cors" });
        await cache.put(THREE_URL, resposta);
      } catch (e) {
        // sem internet nessa hora: o jogo baixa a biblioteca na próxima abertura
      }
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((chaves) => Promise.all(chaves.filter((c) => c !== CACHE).map((c) => caches.delete(c))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request).then((emCache) => {
      if (emCache) return emCache;
      return fetch(event.request).then((resposta) => {
        const copia = resposta.clone();
        caches.open(CACHE).then((cache) => cache.put(event.request, copia));
        return resposta;
      }).catch(() => caches.match("./index.html"));
    })
  );
});
