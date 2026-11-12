/* Beamer Home · Version 2 "Kino": Karussell mit Regalen, Umgebungslicht */
(() => {
  'use strict';

  const A = window.Android;
  const $ = (s, r = document) => r.querySelector(s);
  const h = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const store = {
    get(k, d) { try { const v = localStorage.getItem('bh.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('bh.' + k, JSON.stringify(v)); } catch (e) { /* egal */ } },
  };
  const call = (fn, ...args) => { try { return A && A[fn] ? A[fn](...args) : null; } catch (e) { return null; } };
  const json = (s, d) => { try { return s ? JSON.parse(s) : d; } catch (e) { return d; } };
  const iconUrl = (pkg) => window.__mockIcon ? window.__mockIcon(pkg) : '/icon/' + encodeURIComponent(pkg);
  const rem = () => parseFloat(getComputedStyle(document.documentElement).fontSize);

  const S = {
    apps: [], byPkg: {},
    favs: store.get('favs', null), hidden: store.get('hidden', []),
    name: store.get('name', ''), city: store.get('city', null), saver: store.get('saver', 10),
    shelf: 0, idx: store.get('v2idx', [0, 0, 0]), moving: null,
  };

  const I = {
    wifi: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 8.8a15 15 0 0 1 20 0"/><path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><circle cx="12" cy="19.6" r=".9" fill="currentColor"/></svg>',
    wifiOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 3l18 18"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><path d="M5 12.5a10 10 0 0 1 4.2-2.6M19 12.5a10 10 0 0 0-2.6-1.8"/><path d="M2 8.8a15 15 0 0 1 6.3-3.4M22 8.8A15 15 0 0 0 12 5"/></svg>',
    bt: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7l10 10-5 5V2l5 5L7 17"/></svg>',
    display: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    sound: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>',
    gear: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/></svg>',
    sliders: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
    input: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 14h12"/></svg>',
    cast: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 16.1A5 5 0 0 1 5.9 20M2 12.05A9 9 0 0 1 9.95 20M2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-6"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg>',
    move: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9l-3 3 3 3M19 9l3 3-3 3M2 12h20"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3.2 3.9M6.6 6.6C3.9 8.4 2 12 2 12s4 7 10 7a9.5 9.5 0 0 0 5.4-1.6"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-5M12 8h0"/></svg>',
    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>',
    swap: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h14l-3-3M20 17H6l3 3"/></svg>',
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
  };

  const el = {
    time: $('#time'), date: $('#date'), weather: $('#weather'), net: $('#net'),
    label: $('#hero-label'), name: $('#hero-name'), sub: $('#hero-sub'),
    shelves: $('#shelves'), rail: $('#rail'), empty: $('#empty'),
    ambA: $('#amb-a'), ambB: $('#amb-b'),
    panel: $('#panel'), panelTitle: $('#panel-title'), panelBody: $('#panel-body'), toast: $('#toast'),
  };

  let toastTimer;
  function toast(msg) { el.toast.textContent = msg; el.toast.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.toast.classList.remove('show'), 2600); }

  // ---------- Apps ----------
  const DEFAULT_FAVS = ['com.google.android.youtube.tv', 'com.google.android.youtube', 'com.netflix.ninja', 'com.netflix.mediaclient',
    'com.amazon.amazonvideo.livingroom', 'com.amazon.avod.thirdpartyclient', 'com.disney.disneyplus', 'com.spotify.tv.android',
    'com.spotify.music', 'org.jellyfin.androidtv', 'com.plexapp.android', 'org.xbmc.kodi', 'org.videolan.vlc'];
  const SOURCE_RE = /hdmi|signal ?source|signalquelle|quelle|eingang|input ?source|^source$/i;
  const CAST_RE = /miracast|screen ?mirror|bildschirm ?spiegel|airplay|eshare|airscreen|cast/i;

  function loadApps() {
    const list = json(call('getApps'), []);
    list.sort((a, b) => a.label.localeCompare(b.label, 'de', { sensitivity: 'base' }));
    S.apps = list; S.byPkg = {}; list.forEach((a) => { S.byPkg[a.pkg] = a; });
    if (!Array.isArray(S.favs)) {
      const seen = new Set();
      S.favs = DEFAULT_FAVS.filter((p) => S.byPkg[p]).filter((p) => { const k = p.split('.').slice(0, 3).join('.'); if (seen.has(k)) return false; seen.add(k); return true; });
      if (S.favs.length < 3) list.filter((a) => !a.system).slice(0, 6 - S.favs.length).forEach((a) => S.favs.push(a.pkg));
      store.set('favs', S.favs);
    }
  }

  // Farbiges Bild für Aktionen ohne App-Icon
  const swatch = (c1, c2) => 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/></linearGradient></defs><rect width="10" height="10" fill="url(#g)"/></svg>`);

  function buildShelves() {
    const appItem = (a) => ({ kind: 'app', key: a.pkg, label: a.label, img: iconUrl(a.pkg), app: a });
    const act = (key, label, icon, c1, c2, run, sub) => ({ kind: 'act', key, label, icon, img: swatch(c1, c2), run, sub });
    const quick = [];
    const src = S.apps.find((a) => SOURCE_RE.test(a.label));
    if (src) quick.push(act('src', 'HDMI-Eingang', I.input, '#0ea5e9', '#1e3a8a', () => launch(src.pkg), 'Zu einem angeschlossenen Gerät wechseln'));
    const cast = S.apps.find((a) => CAST_RE.test(a.label) && a !== src);
    if (cast) quick.push(act('cast', 'Bildschirm spiegeln', I.cast, '#a855f7', '#4c1d95', () => launch(cast.pkg), 'Handy oder Laptop auf die Leinwand bringen'));
    quick.push(act('wifi', 'WLAN', I.wifi, '#22d3ee', '#0e7490', () => call('openSettings', 'wifi'), 'Netzwerk wählen'));
    quick.push(act('bt', 'Bluetooth', I.bt, '#3b82f6', '#1e3a8a', () => call('openSettings', 'bluetooth'), 'Lautsprecher, Kopfhörer, Controller'));
    quick.push(act('display', 'Bild', I.display, '#f59e0b', '#9a3412', () => call('openSettings', 'display'), 'Helligkeit, Format, Schärfe'));
    quick.push(act('sound', 'Ton', I.sound, '#f43f5e', '#831843', () => call('openSettings', 'sound'), 'Lautstärke und Tonausgabe'));
    quick.push(act('prefs', 'Startbildschirm', I.sliders, '#e5e7eb', '#52525b', () => openSettings(), 'Name, Wetter, Ruhemodus, Version 1'));
    quick.push(act('sys', 'Android-Einstellungen', I.gear, '#94a3b8', '#1e293b', () => call('openSettings', 'all'), 'Alle Systemeinstellungen'));
    return [
      { title: 'Favoriten', items: S.favs.map((p) => S.byPkg[p]).filter(Boolean).map(appItem),
        empty: 'Noch keine Favoriten. Geh zu <b>Alle Apps</b> und halte <b>OK</b> gedrückt.' },
      { title: 'Alle Apps', items: S.apps.filter((a) => !S.hidden.includes(a.pkg)).map(appItem), empty: 'Keine Apps gefunden.' },
      { title: 'Steuerung', items: quick, empty: '' },
    ];
  }

  let SH = [];
  const cur = () => SH[S.shelf].items[S.idx[S.shelf]];

  // ---------- Darstellung ----------
  function renderShelves() {
    el.shelves.innerHTML = '';
    SH.forEach((s, i) => {
      const b = h('button', 'shelf' + (i === S.shelf ? ' on' : ''), `<span>${s.title}</span><i></i>`);
      b.addEventListener('click', () => setShelf(i));
      el.shelves.appendChild(b);
    });
  }

  function buildRail(enter) {
    const shelf = SH[S.shelf];
    S.idx[S.shelf] = Math.max(0, Math.min(S.idx[S.shelf], shelf.items.length - 1));
    el.rail.innerHTML = '';
    shelf.items.forEach((it, i) => {
      const c = h('div', 'card' + (it.kind === 'app' && S.shelf !== 0 && S.favs.includes(it.key) ? ' isfav' : ''));
      const f = h('div', 'face');
      if (it.kind === 'app') { const img = new Image(); img.alt = ''; img.src = it.img; f.appendChild(img); }
      else { f.style.background = `url("${it.img}") center / cover`; f.innerHTML = it.icon; }
      c.appendChild(f);
      c.addEventListener('click', () => { if (i === S.idx[S.shelf]) activate(); else { S.idx[S.shelf] = i; update(); } });
      c.addEventListener('contextmenu', (e) => { e.preventDefault(); S.idx[S.shelf] = i; update(); openMenu(); });
      el.rail.appendChild(c);
    });
    el.empty.classList.toggle('hidden', shelf.items.length > 0);
    el.empty.innerHTML = shelf.empty;
    if (enter) { el.rail.classList.remove('enter-up', 'enter-down'); void el.rail.offsetWidth; el.rail.classList.add(enter); }
    renderShelves();
    update(true);
  }

  function update(skipSwap) {
    const shelf = SH[S.shelf], i0 = S.idx[S.shelf], r = rem();
    [...el.rail.children].forEach((c, i) => {
      const d = i - i0, a = Math.abs(d), sg = Math.sign(d);
      const x = d === 0 ? 0 : sg * (11.5 * r + (a - 1) * 7.6 * r);
      const z = d === 0 ? 0 : -(160 + a * 40);
      const ry = d === 0 ? 0 : -sg * 32;
      const s = d === 0 ? 1.18 : 1;
      c.style.transform = `translateX(${x}px) translateZ(${z}px) rotateY(${ry}deg) scale(${s})`;
      c.style.opacity = a > 6 ? 0 : 1;
      c.style.zIndex = 100 - a;
      c.style.visibility = a > 7 ? 'hidden' : '';
      c.classList.toggle('cur', d === 0);
      c.classList.toggle('side', d !== 0);
      c.classList.toggle('moving', d === 0 && !!S.moving);
    });
    const it = cur();
    el.label.innerHTML = `${shelf.title}${shelf.items.length ? `<span>${i0 + 1} / ${shelf.items.length}</span>` : ''}`;
    const nm = it ? it.label : shelf.title;
    if (el.name.textContent !== nm) {
      el.name.textContent = nm;
      if (!skipSwap) { el.name.classList.remove('swap'); void el.name.offsetWidth; el.name.classList.add('swap'); }
    }
    if (S.moving) el.sub.innerHTML = 'Mit <b>◀ ▶</b> verschieben, <b>OK</b> zum Ablegen';
    else if (!it) el.sub.innerHTML = '';
    else if (it.kind === 'act') el.sub.textContent = it.sub || '';
    else el.sub.innerHTML = '<b>OK</b> öffnen · <b>OK lang</b> Optionen';
    setAmbient(it ? it.img : null);
    store.set('v2idx', S.idx);
  }

  // Umgebungslicht: zwei Ebenen, die sich überblenden (verzögert, damit schnelles Scrollen flüssig bleibt)
  let ambTimer, ambFront = el.ambA, ambSrc = null;
  function setAmbient(src) {
    clearTimeout(ambTimer);
    ambTimer = setTimeout(() => {
      if (src === ambSrc) return;
      ambSrc = src;
      const back = ambFront === el.ambA ? el.ambB : el.ambA;
      back.style.backgroundImage = src ? `url("${src}")` : 'none';
      back.classList.add('on'); ambFront.classList.remove('on');
      ambFront = back;
    }, 160);
  }

  function step(delta) {
    const shelf = SH[S.shelf], n = shelf.items.length;
    if (S.moving && S.shelf === 0) {
      const i = S.favs.indexOf(S.moving), j = i + delta;
      if (j < 0 || j >= S.favs.length) return bump(delta);
      [S.favs[i], S.favs[j]] = [S.favs[j], S.favs[i]];
      SH = buildShelves(); S.idx[0] = j; buildRail(); return;
    }
    const j = S.idx[S.shelf] + delta;
    if (j < 0 || j >= n) return bump(delta);
    S.idx[S.shelf] = j; update();
  }
  function bump(delta) { const c = delta < 0 ? 'bump-l' : 'bump-r'; el.rail.classList.remove('bump-l', 'bump-r', 'enter-up', 'enter-down'); void el.rail.offsetWidth; el.rail.classList.add(c); }
  function setShelf(i) {
    if (S.moving || i < 0 || i >= SH.length || i === S.shelf) return;
    const dir = i > S.shelf ? 'enter-down' : 'enter-up';
    S.shelf = i; buildRail(dir);
  }

  function activate() {
    const it = cur(); if (!it) return;
    if (S.moving) { S.moving = null; store.set('favs', S.favs); update(); return; }
    const c = el.rail.children[S.idx[S.shelf]];
    if (c) { c.classList.remove('launch'); void c.offsetWidth; c.classList.add('launch'); }
    if (it.kind === 'app') launch(it.key); else it.run();
  }
  function launch(pkg) { if (call('launch', pkg) === false) toast('App lässt sich nicht starten'); }

  // ---------- Menüs (App-Optionen und Einstellungen) ----------
  let panelMode = null, kbOpen = false;
  function rows() { return [...el.panelBody.querySelectorAll('.row')]; }
  function showPanel(mode, title, html) {
    panelMode = mode; el.panelTitle.innerHTML = title; el.panelBody.innerHTML = html;
    el.panel.classList.remove('hidden');
    const first = rows()[0]; if (first) first.focus();
  }
  function closePanel() { if (document.activeElement) document.activeElement.blur(); el.panel.classList.add('hidden'); panelMode = null; kbOpen = false; }
  function rowMove(d) {
    const r = rows(), a = document.activeElement, i = r.indexOf(a.closest ? a.closest('.row') : a);
    const n = r[Math.max(0, Math.min(r.length - 1, i + d))];
    if (n) { n.focus(); n.scrollIntoView({ block: 'nearest' }); }
  }

  function openMenu() {
    const it = cur(); if (!it || it.kind !== 'app') return;
    const a = it.app, isFav = S.favs.includes(a.pkg);
    const items = [['open', I.play, 'Öffnen']];
    items.push(isFav ? ['unfav', I.star, 'Aus Favoriten entfernen'] : ['fav', I.star, 'Zu Favoriten hinzufügen']);
    if (isFav && S.shelf === 0 && S.favs.length > 1) items.push(['move', I.move, 'Verschieben']);
    items.push(['hide', I.eye, 'In „Alle Apps“ ausblenden'], ['info', I.info, 'App-Info']);
    if (!a.system) items.push(['del', I.trash, 'Deinstallieren', 'danger']);
    showPanel('menu', `<img src="${it.img}" alt="">${a.label.replace(/</g, '&lt;')}`,
      items.map(([k, ic, t, cls]) => `<button class="row${cls ? ' ' + cls : ''}" data-act="${k}">${ic}<span>${t}</span></button>`).join(''));
    el.panelBody.onclick = (e) => {
      const b = e.target.closest('[data-act]'); if (!b) return;
      const k = b.dataset.act; closePanel();
      if (k === 'open') launch(a.pkg);
      if (k === 'fav') { S.favs.push(a.pkg); store.set('favs', S.favs); refresh(); toast(a.label + ' ist jetzt Favorit'); }
      if (k === 'unfav') { S.favs = S.favs.filter((p) => p !== a.pkg); store.set('favs', S.favs); refresh(); }
      if (k === 'move') { S.moving = a.pkg; update(); }
      if (k === 'hide') { S.hidden.push(a.pkg); store.set('hidden', S.hidden); refresh(); toast('Ausgeblendet. Zurückholen unter Steuerung → Startbildschirm'); }
      if (k === 'info') call('appInfo', a.pkg);
      if (k === 'del') call('uninstall', a.pkg);
    };
  }

  const SAVER_STEPS = [0, 5, 10, 30, 60];
  function openSettings() {
    const info = json(call('deviceInfo'), {});
    const val = () => ({ saver: S.saver ? `nach ${S.saver} Min.` : 'aus', hidden: S.hidden.length || 'keine' });
    const v = val();
    showPanel('settings', 'Startbildschirm', `
      <div class="row" tabindex="-1" data-input="name">${I.user}<label for="v2-name">Name</label><input id="v2-name" maxlength="24" placeholder="optional"></div>
      <div class="row" tabindex="-1" data-input="city">${I.pin}<label for="v2-city">Ort fürs Wetter</label><input id="v2-city" placeholder="z. B. Hamburg"></div>
      <button class="row" data-act="saver">${I.moon}<span>Ruhemodus</span><span class="val" id="v-saver">${v.saver}</span></button>
      <button class="row" data-act="unhide">${I.eye}<span>Ausgeblendete Apps zeigen</span><span class="val" id="v-hidden">${v.hidden}</span></button>
      <div class="sep"></div>
      <button class="row" data-act="v1">${I.swap}<span>Zu Version 1 (Glas) wechseln</span></button>
      <button class="row" data-act="home">${I.home}<span>Standard-Startbildschirm wählen</span></button>
      <p class="note">Beamer Home ${info.version || ''} · Version 2 „Kino“${info.model ? '<br>' + info.model : ''}</p>`);
    const nameIn = $('#v2-name'), cityIn = $('#v2-city');
    nameIn.value = S.name; cityIn.value = S.city ? S.city.name : '';
    cityIn.addEventListener('change', () => saveCity(cityIn.value.trim()));
    nameIn.addEventListener('input', () => { S.name = nameIn.value.trim(); store.set('name', S.name); tick(); });
    el.panelBody.onclick = (e) => {
      const r = e.target.closest('[data-input]'); if (r) { r.querySelector('input').focus(); return; }
      const b = e.target.closest('[data-act]'); if (!b) return;
      const k = b.dataset.act;
      if (k === 'saver') { S.saver = SAVER_STEPS[(SAVER_STEPS.indexOf(S.saver) + 1) % SAVER_STEPS.length]; store.set('saver', S.saver); $('#v-saver').textContent = val().saver; }
      if (k === 'unhide') { const n = S.hidden.length; S.hidden = []; store.set('hidden', []); refresh(); $('#v-hidden').textContent = 'keine'; toast(n ? n + ' App(s) wieder sichtbar' : 'Keine Apps ausgeblendet'); }
      if (k === 'v1') { store.set('ui', 'v1'); location.href = '../index.html'; }
      if (k === 'home') call('openSettings', 'home');
    };
  }
  async function saveCity(q) {
    if (!q) { S.city = null; store.set('city', null); loadWeather(); return; }
    toast('Suche …');
    try {
      const d = await getJSON(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(q)}&count=1&language=de&format=json`);
      if (!d.results || !d.results.length) return toast('Ort nicht gefunden');
      const r = d.results[0];
      S.city = { name: r.name, lat: +r.latitude.toFixed(3), lon: +r.longitude.toFixed(3) };
      store.set('city', S.city); loadWeather(); toast('Wetter für ' + r.name);
    } catch (e) { toast('Keine Internetverbindung'); }
  }

  function refresh() { loadApps(); SH = buildShelves(); buildRail(); }

  // ---------- Uhr, Wetter, Netz ----------
  // Uhr mit rollenden Ziffern: nur die Stelle, die sich ändert, wird animiert
  const digits = [];
  (function buildClock() {
    el.time.innerHTML = '';
    for (let i = 0; i < 4; i++) {
      if (i === 2) el.time.appendChild(h('span', 'colon', ':'));
      const d = h('span', 'd'); d.appendChild(h('i', '', '')); el.time.appendChild(d); digits.push(d);
    }
  })();
  function setDigit(d, ch) {
    const curI = d.lastElementChild;
    if (curI.textContent === ch) return;
    if (!curI.textContent) { curI.textContent = ch; return; }
    curI.classList.remove('in'); curI.classList.add('out');
    setTimeout(() => curI.remove(), 750);
    const n = h('i', 'in'); n.textContent = ch; d.appendChild(n);
  }
  function tick() {
    const d = new Date();
    const hm = String(d.getHours()).padStart(2, '0') + String(d.getMinutes()).padStart(2, '0');
    [...hm].forEach((ch, i) => setDigit(digits[i], ch));
    el.time.setAttribute('aria-label', hm.slice(0, 2) + ':' + hm.slice(2));
    const hh = d.getHours();
    const g = hh >= 5 && hh < 11 ? 'Guten Morgen' : hh < 17 && hh >= 11 ? 'Guten Tag' : hh < 22 && hh >= 17 ? 'Guten Abend' : 'Gute Nacht';
    el.date.innerHTML = `<b>${d.toLocaleDateString('de-DE', { weekday: 'long' })}</b>${d.toLocaleDateString('de-DE', { day: 'numeric', month: 'long' })}`;
    $('#greet').textContent = g + (S.name ? ', ' + S.name : '');
  }
  async function getJSON(url) {
    const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 8000);
    try { const r = await fetch(url, { signal: ctl.signal }); if (!r.ok) throw new Error(r.status); return await r.json(); } finally { clearTimeout(to); }
  }
  const WX = (c) => c === 0 ? 'klar' : c <= 2 ? 'heiter' : c === 3 ? 'bewölkt' : c === 45 || c === 48 ? 'Nebel' : (c >= 71 && c <= 77) || c === 85 || c === 86 ? 'Schnee' : c >= 95 ? 'Gewitter' : c >= 51 ? 'Regen' : '';
  async function loadWeather() {
    if (!S.city) { el.weather.innerHTML = ''; return; }
    try {
      const d = await getJSON(`https://api.open-meteo.com/v1/forecast?latitude=${S.city.lat}&longitude=${S.city.lon}&current=temperature_2m,weather_code&timezone=auto`);
      el.weather.innerHTML = `<b>${Math.round(d.current.temperature_2m)}°</b> ${WX(d.current.weather_code)} · ${S.city.name}`;
    } catch (e) { el.weather.textContent = S.city.name; }
  }
  function updateNet() {
    const n = json(call('getNetwork'), { connected: navigator.onLine });
    el.net.classList.toggle('off', !n.connected);
    el.net.innerHTML = n.connected ? I.wifi : I.wifiOff;
  }

  // ---------- Ruhemodus ----------
  let lastInput = Date.now();
  const isIdle = () => document.body.classList.contains('idle');
  function wake() { lastInput = Date.now(); document.body.classList.remove('idle'); }
  setInterval(() => {
    if (!S.saver || isIdle() || panelMode || S.moving || document.hidden) return;
    if (Date.now() - lastInput > S.saver * 60000) document.body.classList.add('idle');
  }, 15000);

  // ---------- Fernbedienung ----------
  const DIRS = { ArrowLeft: 'l', ArrowRight: 'r', ArrowUp: 'u', ArrowDown: 'd', 37: 'l', 39: 'r', 38: 'u', 40: 'd', 21: 'l', 22: 'r', 19: 'u', 20: 'd' };
  let pressTimer, longFired = false, okDown = false, swallow = false;
  const isOk = (e) => e.key === 'Enter' || e.keyCode === 13 || e.keyCode === 23;

  document.addEventListener('keydown', (e) => {
    if (isIdle()) { wake(); swallow = true; e.preventDefault(); return; }
    lastInput = Date.now();
    if (swallow) { e.preventDefault(); return; }
    const a = document.activeElement, inInput = a && a.tagName === 'INPUT';
    const dir = DIRS[e.key] || DIRS[e.keyCode];

    if (panelMode) {
      if (dir === 'u' || dir === 'd') { e.preventDefault(); if (inInput) a.blur(); rowMove(dir === 'u' ? -1 : 1); return; }
      if (dir) { if (!inInput) e.preventDefault(); return; }
      if (isOk(e)) {
        e.preventDefault(); if (e.repeat) return;
        if (inInput) {
          if (kbOpen) { kbOpen = false; call('hideKeyboard'); a.closest('.row').focus(); }
          else { kbOpen = true; call('showKeyboard'); }
          return;
        }
        const row = a && a.closest && a.closest('.row');
        if (row && row.dataset.input) { row.querySelector('input').focus(); kbOpen = true; call('showKeyboard'); return; }
        if (row) row.click();
        return;
      }
      if (e.key === 'Escape' || (e.key === 'Backspace' && !inInput)) { e.preventDefault(); closePanel(); }
      return;
    }

    if (dir) {
      e.preventDefault();
      if (dir === 'l' || dir === 'r') step(dir === 'l' ? -1 : 1);
      else setShelf(S.shelf + (dir === 'u' ? -1 : 1));
      return;
    }
    if (isOk(e)) {
      e.preventDefault(); if (e.repeat || okDown) return;
      okDown = true; longFired = false; clearTimeout(pressTimer);
      pressTimer = setTimeout(() => { const it = cur(); if (it && it.kind === 'app' && !S.moving) { longFired = true; openMenu(); } }, 650);
      return;
    }
    if (e.key === 'Escape' || e.key === 'Backspace') { e.preventDefault(); onBack(); return; }
    if (e.key === 'ContextMenu' || e.key === 'm') { e.preventDefault(); onMenu(); }
  }, true);

  document.addEventListener('keyup', (e) => {
    if (swallow) { swallow = false; okDown = false; clearTimeout(pressTimer); return; }
    if (isOk(e) && okDown) { okDown = false; clearTimeout(pressTimer); if (!longFired) activate(); e.preventDefault(); }
  }, true);

  let wheelLock = 0;
  document.addEventListener('wheel', (e) => {
    wake(); if (panelMode) return;
    const now = Date.now(); if (now - wheelLock < 120) return; wheelLock = now;
    const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    step(d > 0 ? 1 : -1);
  }, { passive: true });
  document.addEventListener('pointerdown', wake, true);
  el.panel.addEventListener('click', (e) => { if (e.target === el.panel) closePanel(); });

  function onBack() {
    if (isIdle()) return wake();
    if (panelMode) return closePanel();
    if (S.moving) { S.moving = null; store.set('favs', S.favs); return update(); }
    if (S.idx[S.shelf] > 0) { S.idx[S.shelf] = 0; return update(); }
    if (S.shelf !== 0) setShelf(0);
  }
  function onMenu() {
    if (panelMode) return closePanel();
    const it = cur();
    if (it && it.kind === 'app') openMenu(); else openSettings();
  }

  window.BH = {
    onBack, onMenu, toast,
    onSettingsKey: () => (panelMode ? closePanel() : openSettings()),
    onHome: () => { wake(); closePanel(); S.moving = null; if (S.shelf !== 0) setShelf(0); S.idx[0] = 0; update(); },
    onResume: () => { wake(); updateNet(); tick(); },
    onAppsChanged: () => refresh(),
  };

  // ---------- Start ----------
  loadApps();
  SH = buildShelves();
  buildRail();
  tick(); setInterval(tick, 1000);
  updateNet(); setInterval(updateNet, 15000);
  loadWeather(); setInterval(loadWeather, 30 * 60000);
  window.addEventListener('resize', () => update(true));
})();
