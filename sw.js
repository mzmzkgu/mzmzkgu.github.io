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

// ── 공포매매 단계 도달 알림 ──
// 서버(push_fear.py)는 시장 조건만 보고 모든 구독자에게 같은 푸시(d.fear)를 보낸다. 사용자가 끝낸 단계·평단·보유수량은
// 서버에 없고 이 기기의 IndexedDB('fearbuy'/'kv'/'alert')에만 있다. 여기서 그 값을 읽어 끝난 단계는 숨기고,
// 매도는 수익률 조건까지 확인한 뒤 팝업을 띄운다. 규칙 숫자는 서버가 payload 로 내려준다. (앱 app.js, 서버 push_fear.py 와 같은 규칙)
function fearLocalState() {
  return new Promise(res => {
    try {
      const rq = indexedDB.open("fearbuy", 1);
      rq.onupgradeneeded = () => rq.result.createObjectStore("kv");
      rq.onerror = () => res(null);
      rq.onsuccess = () => {
        const db = rq.result;
        const g = db.transaction("kv").objectStore("kv").get("alert");
        g.onsuccess = () => { db.close(); res(g.result || null); };
        g.onerror = () => { db.close(); res(null); };
      };
    } catch (_) { res(null); }
  });
}

async function fearPush(d) {
  const f = d.fear, st = await fearLocalState();
  const opt = { icon: "/assets/images/icon-192.png", renotify: true, data: { url: d.url || "/buytheDip/" } };
  if (!st) {   // 기기에 상태가 없으면(앱을 아직 안 열었거나 지워진 경우) 거르지 않고 서버가 준 문구를 그대로 보여준다
    return self.registration.showNotification(d.title || "공포매매 알림", { ...opt, body: d.body || "", tag: d.tag || "fear" });
  }
  const done = new Set(st.done || []), avg = Number(st.avg) || 0, held = Number(st.held) || 0;
  const profit = held > 0 && avg > 0 && f.price ? (f.price / avg - 1) * 100 : null;
  const buys = (f.buy || []).filter(x => !done.has(x.label));
  const sells = (f.sell || []).filter(x => !done.has(x.label) && profit !== null && profit >= x.profit);
  const jobs = [];
  if (buys.length) {
    jobs.push(self.registration.showNotification("공포매매 · " + buys.map(x => x.label).join("·") + " 매수 조건 도달", {
      ...opt, tag: "fear-buy",
      body: "F&G " + Number(f.fg).toFixed(1) + " · VIX " + Number(f.vix).toFixed(1) + " → " + buys.map(x => x.label + " 시드의 " + x.ratio + "%").join(", ") + " 매수 타이밍",
    }));
  }
  if (sells.length) {
    jobs.push(self.registration.showNotification("공포매매 · " + sells.map(x => x.label).join("·") + " 매도 조건 도달", {
      ...opt, tag: "fear-sell",
      body: "F&G " + Number(f.fg).toFixed(1) + " · 수익률 " + (profit >= 0 ? "+" : "") + profit.toFixed(1) + "% → " + sells.map(x => x.label + " 평가액의 " + x.ratio + "%").join(", ") + " 매도 타이밍",
    }));
  }
  if (jobs.length) return Promise.all(jobs);
  // 전부 끝낸 단계라 보여줄 게 없다: 브라우저는 푸시를 받으면 알림을 하나 보여야 하므로(안 그러면 "사이트가 백그라운드에서
  // 업데이트되었습니다" 기본 알림이 뜬다) 소리 없는 알림을 띄우자마자 닫는다.
  await self.registration.showNotification("공포매매", { tag: "fear-hidden", silent: true, body: "" });
  (await self.registration.getNotifications({ tag: "fear-hidden" })).forEach(n => n.close());
}

self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { body: e.data ? e.data.text() : "" }; }
  if (d.fear) { e.waitUntil(fearPush(d)); return; }
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
