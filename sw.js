// 소소한 재테크 작업실 서비스워커 (사이트 전체 범위 "/"): 오프라인 캐시 + 웹 푸시
// 주의: ipotracker 등 같은 도메인의 다른 도구 페이지도 이 서비스워커가 관리한다.
const VER = "v1";
const PAGES = "sosojae-pages-" + VER;
const STATIC = "sosojae-static-" + VER;
const MAX_PAGES = 40;

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(PAGES).then(c => c.add("/")).catch(() => {}).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k.startsWith("sosojae-") && k !== PAGES && k !== STATIC).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function trim(name, max) {
  const c = await caches.open(name), ks = await c.keys();
  for (let i = 0; i < ks.length - max; i++) await c.delete(ks[i]);
}

const CDN = /(^|\.)jsdelivr\.net$|(^|\.)gstatic\.com$|^fonts\.googleapis\.com$/;

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const same = url.origin === location.origin;
  // 광고·분석·시트 데이터 등 외부 요청은 건드리지 않는다 (서비스워커를 거치지 않고 그대로 네트워크)
  if (!same && !CDN.test(url.hostname)) return;
  // 서비스워커 파일 자체와 실시간 데이터(마켓시그널)는 항상 네트워크
  if (same && (url.pathname === "/sw.js" || url.pathname.startsWith("/marketTraffic/"))) return;

  // 페이지 이동: 네트워크 우선(새 글/새 배포 즉시 반영) -> 실패하면 캐시, 없으면 홈
  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req)
        .then(r => {
          if (r && r.ok) { const copy = r.clone(); caches.open(PAGES).then(c => c.put(req, copy)).then(() => trim(PAGES, MAX_PAGES)); }
          return r;
        })
        .catch(() => caches.match(req).then(hit => hit || caches.match("/")))
    );
    return;
  }
  // 이미지/CSS/JS/폰트/CDN 라이브러리: 캐시 우선 + 백그라운드 갱신
  e.respondWith(
    caches.match(req).then(hit => {
      const net = fetch(req)
        .then(r => { if (r && (r.ok || r.type === "opaque")) { const copy = r.clone(); caches.open(STATIC).then(c => c.put(req, copy)); } return r; })
        .catch(() => hit);
      return hit || net;
    })
  );
});

self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "소소한 재테크 알림", {
    body: d.body || "",
    icon: "/assets/images/icon-192.png",
    tag: d.tag || "sosojae",
    renotify: true,
    data: { url: d.url || "/ipotracker/" },
  }));
});

self.addEventListener("notificationclick", e => {
  e.notification.close();
  const target = new URL((e.notification.data && e.notification.data.url) || "/", self.location.origin).href;
  e.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then(cs => {
      for (const c of cs) {
        if (new URL(c.url).origin === self.location.origin && "focus" in c) {
          return c.focus().then(w => (w && "navigate" in w && w.url !== target ? w.navigate(target).catch(() => w) : w));
        }
      }
      return clients.openWindow(target);
    })
  );
});
