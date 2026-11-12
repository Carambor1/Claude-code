/* Beamer Home · Version 2 "Kino"
   Gerade App-Reihe, Regale als Tabs, Umgebungslicht aus der App-Farbe.
   Sparsam gebaut für Beamer mit 1 GB RAM: nur sichtbare Bilder werden geladen,
   keine Filter, Timer laufen nur, wenn der Startbildschirm sichtbar ist. */
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
  const isMock = !!window.__mockIcon;
  const rem = () => parseFloat(getComputedStyle(document.documentElement).fontSize);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  const S = {
    apps: [], byPkg: {},
    favs: store.get('favs', null), hidden: store.get('hidden', []),
    name: store.get('name', ''), city: store.get('city', null), saver: store.get('saver', 10),
    shelf: 0, idx: store.get('v2idx', [0, 0, 0]), moving: null,
  };

  // ---------- Symbole ----------
  const P = (d, extra = '') => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"${extra}>${d}</svg>`;
  const I = {
    wifi: P('<path d="M2 8.8a15 15 0 0 1 20 0"/><path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><circle cx="12" cy="19.6" r=".9" fill="currentColor"/>'),
    wifiOff: P('<path d="M3 3l18 18"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><path d="M5 12.5a10 10 0 0 1 4.2-2.6M19 12.5a10 10 0 0 0-2.6-1.8"/><path d="M2 8.8a15 15 0 0 1 6.3-3.4M22 8.8A15 15 0 0 0 12 5"/>'),
    bt: P('<path d="M7 7l10 10-5 5V2l5 5L7 17"/>'),
    display: P('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    sound: P('<path d="M11 5L6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>'),
    gear: P('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3 1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8 1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>'),
    sliders: P('<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>'),
    input: P('<rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 14h12M7 10.5h.01M10 10.5h.01M13 10.5h.01M16 10.5h.01"/>'),
    cast: P('<path d="M2 16.1A5 5 0 0 1 5.9 20M2 12.05A9 9 0 0 1 9.95 20M2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-6"/><path d="M2 20h.01"/>'),
    folder: P('<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5H9l2 2.5h8.5A1.5 1.5 0 0 1 21 9v9.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/>'),
    image: P('<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>'),
    music: P('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
    playBox: P('<rect x="2" y="4" width="20" height="16" rx="3"/><path d="M10 9l5 3-5 3z" fill="currentColor"/>'),
    globe: P('<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.6 2.8 3.9 6 3.9 9.5S14.6 18.7 12 21.5C9.4 18.7 8.1 15.5 8.1 12S9.4 5.3 12 2.5z"/>'),
    download: P('<path d="M12 3v12M7 10l5 5 5-5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>'),
    projector: P('<rect x="2" y="7" width="20" height="10" rx="2.5"/><circle cx="15.5" cy="12" r="3"/><path d="M5.5 10.5h4M5.5 13.5h2.5M5 17v2M19 17v2"/>'),
    calendar: P('<rect x="3" y="4.5" width="18" height="16.5" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>'),
    clock: P('<circle cx="12" cy="12" r="9.5"/><path d="M12 6.5V12l3.5 2"/>'),
    star: P('<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/>'),
    move: P('<path d="M5 9l-3 3 3 3M19 9l3 3-3 3M2 12h20"/>'),
    eye: P('<path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3.2 3.9M6.6 6.6C3.9 8.4 2 12 2 12s4 7 10 7a9.5 9.5 0 0 0 5.4-1.6"/>'),
    info: P('<circle cx="12" cy="12" r="10"/><path d="M12 16v-5M12 8h.01"/>'),
    trash: P('<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>'),
    play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg>',
    swap: P('<path d="M4 7h14l-3-3M20 17H6l3 3"/>'),
    home: P('<path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>'),
    moon: P('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'),
    user: P('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    pin: P('<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>'),
    down: P('<path d="M6 9l6 6 6-6"/>'),
    up: P('<path d="M6 15l6-6 6 6"/>'),
  };

  // Eigenes Icon-Bild: Farbverlauf + Symbol. Für Aktionen und hässliche Firmware-Icons.
  function tile(icon, c1, c2) {
    const inner = icon.replace('<svg ', '<svg x="27" y="27" width="42" height="42" ').replace(/currentColor/g, '#fff');
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/></linearGradient></defs><rect width="96" height="96" fill="url(#g)"/>${inner}</svg>`);
  }

  // System-Apps der Beamer-Firmware bekommen eigene Icons (die Originale sind meist schwach)
  const KEEP_ORIGINAL = /^(com\.android\.vending|com\.android\.chrome|com\.google\.|com\.netflix|com\.amazon|com\.disney|com\.spotify)/;
  const SYS_ICONS = [
    [/hdmi|signal ?source|signalquelle|quelle|eingang|input ?source|^source$/i, I.input, '#38bdf8', '#1d4ed8', 'input'],
    [/mirror|spiegel|miracast|eshare|airplay|airscreen|screen ?share|cast/i, I.cast, '#c084fc', '#6d28d9', 'cast'],
    [/trapez|keystone|projektion|projector|fokus|focus|bildkorrektur|correction/i, I.projector, '#5eead4', '#0f766e'],
    [/einstellung|setting/i, I.gear, '#cbd5e1', '#475569'],
    [/datei|file|explorer|ordner/i, I.folder, '#fcd34d', '#d97706'],
    [/galerie|gallery|foto|photo|album/i, I.image, '#f9a8d4', '#be185d'],
    [/musik|music|audio/i, I.music, '#fda4af', '#e11d48'],
    [/video|player|media|film/i, I.playBox, '#fdba74', '#ea580c'],
    [/browser|internet|web/i, I.globe, '#67e8f9', '#0e7490'],
    [/bluetooth/i, I.bt, '#93c5fd', '#2563eb'],
    [/update|ota|aktualis|upgrade/i, I.download, '#86efac', '#15803d'],
    [/kalender|calendar/i, I.calendar, '#fca5a5', '#dc2626'],
    [/uhr|clock|wecker|alarm/i, I.clock, '#e5e7eb', '#3f3f46'],
  ];
  function sysLook(a) {
    if (!a.system || KEEP_ORIGINAL.test(a.pkg)) return null;
    for (const [re, icon, c1, c2, role] of SYS_ICONS) if (re.test(a.label)) return { img: tile(icon, c1, c2), color: c2, role };
    return null;
  }

  const el = {
    time: $('#time'), date: $('#date'), weather: $('#weather'), net: $('#net'), tabs: $('#tabs'),
    label: $('#hero-label'), name: $('#hero-name'), sub: $('#hero-sub'),
    row: $('#row'), empty: $('#empty'), peek: $('#peek'), peekLabel: $('#peek-label'), peekIcons: $('#peek-icons'),
    ambA: $('#amb-a'), ambB: $('#amb-b'), art: $('#art'),
    panel: $('#panel'), panelTitle: $('#panel-title'), panelBody: $('#panel-body'), toast: $('#toast'),
  };

  let toastTimer;
  function toast(msg) { el.toast.textContent = msg; el.toast.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.toast.classList.remove('show'), 2600); }

  // ---------- Apps ----------
  const DEFAULT_FAVS = ['com.google.android.youtube.tv', 'com.google.android.youtube', 'com.netflix.ninja', 'com.netflix.mediaclient',
    'com.amazon.amazonvideo.livingroom', 'com.amazon.avod.thirdpartyclient', 'com.disney.disneyplus', 'com.spotify.tv.android',
    'com.spotify.music', 'org.jellyfin.androidtv', 'com.plexapp.android', 'org.xbmc.kodi', 'org.videolan.vlc'];

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

  function buildShelves() {
    const appItem = (a) => {
      const look = sysLook(a);
      return { kind: 'app', key: a.pkg, label: a.label, img: look ? look.img : (isMock ? window.__mockIcon(a.pkg) : '/icon/' + encodeURIComponent(a.pkg)),
        color: look ? look.color : null, app: a, role: look && look.role };
    };
    const act = (key, label, icon, c1, c2, run, sub) => ({ kind: 'act', key, label, img: tile(icon, c1, c2), color: c2, run, sub });
    const quick = [];
    const src = S.apps.find((a) => (sysLook(a) || {}).role === 'input');
    if (src) quick.push(act('src', 'HDMI-Eingang', I.input, '#38bdf8', '#1d4ed8', () => launch(src.pkg), 'Zu einem angeschlossenen Gerät wechseln'));
    const cast = S.apps.find((a) => (sysLook(a) || {}).role === 'cast');
    if (cast) quick.push(act('cast', 'Bildschirm spiegeln', I.cast, '#c084fc', '#6d28d9', () => launch(cast.pkg), 'Handy oder Laptop auf die Leinwand bringen'));
    quick.push(act('wifi', 'WLAN', I.wifi, '#67e8f9', '#0e7490', () => call('openSettings', 'wifi'), 'Netzwerk wählen'));
    quick.push(act('bt', 'Bluetooth', I.bt, '#93c5fd', '#2563eb', () => call('openSettings', 'bluetooth'), 'Lautsprecher, Kopfhörer, Controller'));
    quick.push(act('display', 'Bild', I.display, '#fcd34d', '#c2410c', () => call('openSettings', 'display'), 'Helligkeit, Format, Schärfe'));
    quick.push(act('sound', 'Ton', I.sound, '#fda4af', '#be123c', () => call('openSettings', 'sound'), 'Lautstärke und Tonausgabe'));
    quick.push(act('prefs', 'Startbildschirm', I.sliders, '#e5e7eb', '#52525b', () => openSettings(), 'Name, Wetter, Ruhemodus'));
    quick.push(act('sys', 'Android-Einstellungen', I.gear, '#cbd5e1', '#334155', () => call('openSettings', 'all'), 'Alle Systemeinstellungen'));
    return [
      { title: 'Favoriten', items: S.favs.map((p) => S.byPkg[p]).filter(Boolean).map(appItem),
        empty: 'Noch keine Favoriten.<br>Geh zu <b>Alle Apps</b> und halte <b>OK</b> gedrückt.' },
      { title: 'Alle Apps', items: S.apps.filter((a) => !S.hidden.includes(a.pkg)).map(appItem), empty: 'Keine Apps gefunden.' },
      { title: 'Steuerung', items: quick, empty: '' },
    ];
  }

  let SH = [];
  const cur = () => SH[S.shelf].items[S.idx[S.shelf]];

  // ---------- Farbe eines Icons (einmal berechnen, dann merken) ----------
  const colorCache = {};
  const probe = document.createElement('canvas'); probe.width = probe.height = 12;
  const pctx = probe.getContext('2d', { willReadFrequently: true });
  function colorOf(it, cb) {
    if (it.color) return cb(it.color);
    if (colorCache[it.key]) return cb(colorCache[it.key]);
    const img = new Image();
    img.onload = () => {
      let col = '#334155';
      try {
        pctx.clearRect(0, 0, 12, 12); pctx.drawImage(img, 0, 0, 12, 12);
        const d = pctx.getImageData(0, 0, 12, 12).data;
        let r = 0, g = 0, b = 0, w = 0;
        for (let i = 0; i < d.length; i += 4) {
          if (d[i + 3] < 128) continue;
          const mx = Math.max(d[i], d[i + 1], d[i + 2]), mn = Math.min(d[i], d[i + 1], d[i + 2]);
          const wt = .08 + ((mx - mn) / (mx || 1)) ** 2 * (mx > 40 ? 3 : .3);
          r += d[i] * wt; g += d[i + 1] * wt; b += d[i + 2] * wt; w += wt;
        }
        if (w) { const k = Math.min(1.4, 190 / Math.max(r / w, g / w, b / w, 1)); col = `rgb(${Math.round(r / w * k)},${Math.round(g / w * k)},${Math.round(b / w * k)})`; }
      } catch (e) { /* Standardfarbe */ }
      colorCache[it.key] = col; cb(col);
    };
    img.onerror = () => cb('#334155');
    img.src = it.img;
  }

  // ---------- Darstellung ----------
  function renderTabs() {
    el.tabs.innerHTML = '';
    SH.forEach((s, i) => {
      const b = h('button', 'tab' + (i === S.shelf ? ' on' : ''), s.title);
      b.addEventListener('click', () => setShelf(i));
      el.tabs.appendChild(b);
    });
  }

  function renderPeek() {
    const next = S.shelf < SH.length - 1 ? S.shelf + 1 : S.shelf - 1;
    const s = SH[next];
    if (!s || !s.items.length) { el.peek.classList.add('none'); return; }
    el.peek.classList.remove('none');
    el.peekLabel.innerHTML = (next > S.shelf ? I.down : I.up) + esc(s.title);
    el.peekIcons.innerHTML = '';
    s.items.slice(0, 14).forEach((it) => { const sp = h('span'); const img = new Image(); img.alt = ''; img.decoding = 'async'; img.src = it.img; sp.appendChild(img); el.peekIcons.appendChild(sp); });
  }

  let cards = [];
  function buildRow(enter) {
    const shelf = SH[S.shelf];
    S.idx[S.shelf] = Math.max(0, Math.min(S.idx[S.shelf], shelf.items.length - 1));
    el.row.innerHTML = ''; cards = [];
    shelf.items.forEach((it, i) => {
      const c = h('div', 'card' + (it.kind === 'app' && S.shelf !== 0 && S.favs.includes(it.key) ? ' isfav' : ''));
      c.appendChild(h('div', 'face'));
      c.addEventListener('click', () => { if (i === S.idx[S.shelf]) activate(); else { S.idx[S.shelf] = i; update(); } });
      c.addEventListener('contextmenu', (e) => { e.preventDefault(); S.idx[S.shelf] = i; update(); openMenu(); });
      el.row.appendChild(c); cards.push(c);
    });
    el.empty.classList.toggle('hidden', shelf.items.length > 0);
    el.empty.innerHTML = shelf.empty;
    if (enter) { el.row.classList.remove('enter-up', 'enter-down', 'bump-l', 'bump-r'); void el.row.offsetWidth; el.row.classList.add(enter); }
    renderTabs(); renderPeek();
    update(true);
  }

  function update(skipSwap) {
    const shelf = SH[S.shelf], i0 = S.idx[S.shelf], r = rem();
    const W = 10.5 * r, G = 1.5 * r, X0 = 4 * r, EXTRA = W * 0.12 + .6 * r;
    const visibleRight = Math.ceil((innerWidth - X0) / (W + G)) + 1;
    cards.forEach((c, i) => {
      const d = i - i0;
      const on = d >= -1 && d <= visibleRight;
      // Bilder nur für sichtbare Karten laden; weit entfernte wieder freigeben
      const face = c.firstChild;
      if (d >= -2 && d <= visibleRight + 2) {
        if (!face.firstChild) { const img = new Image(); img.alt = ''; img.decoding = 'async'; img.src = shelf.items[i].img; face.appendChild(img); }
      } else if (face.firstChild && Math.abs(d) > 30) face.textContent = '';
      c.style.visibility = on ? '' : 'hidden';
      if (!on) return;
      const x = X0 + d * (W + G) + (d > 0 ? EXTRA : 0);
      c.style.transform = `translateX(${x}px) scale(${d === 0 ? 1.12 : 1})`;
      c.classList.toggle('cur', d === 0);
      c.classList.toggle('dim', d < 0);
      c.classList.toggle('moving', d === 0 && !!S.moving);
    });
    const it = cur();
    el.label.innerHTML = esc(shelf.title) + (shelf.items.length ? `<span>${i0 + 1} / ${shelf.items.length}</span>` : '');
    const nm = it ? it.label : '';
    if (el.name.textContent !== nm) {
      el.name.textContent = nm;
      if (!skipSwap) { el.name.classList.remove('swap'); void el.name.offsetWidth; el.name.classList.add('swap'); }
    }
    if (S.moving) el.sub.innerHTML = 'Mit <b>◀ ▶</b> verschieben, <b>OK</b> zum Ablegen';
    else if (!it) el.sub.innerHTML = '';
    else if (it.kind === 'act') el.sub.textContent = it.sub || '';
    else el.sub.innerHTML = '<b>OK</b> öffnen · <b>OK lang</b> Optionen';
    setMood(it);
    store.set('v2idx', S.idx);
  }

  // Umgebungslicht + TV-Banner: verzögert, damit schnelles Durchscrollen flüssig bleibt
  let moodTimer, ambFront = el.ambA, moodKey = null;
  function setMood(it) {
    clearTimeout(moodTimer);
    moodTimer = setTimeout(() => {
      const key = it ? it.key : '';
      if (key === moodKey) return;
      moodKey = key;
      const paint = (col) => {
        if (moodKey !== key) return;
        const back = ambFront === el.ambA ? el.ambB : el.ambA;
        back.style.background = `radial-gradient(ellipse 75% 85% at 22% 78%, color-mix(in srgb, ${col} 62%, transparent), transparent 70%),
          radial-gradient(ellipse 60% 70% at 92% 8%, color-mix(in srgb, ${col} 34%, transparent), transparent 72%), var(--ink)`;
        back.classList.add('on'); ambFront.classList.remove('on'); ambFront = back;
      };
      if (it) colorOf(it, paint); else paint('#1e293b');
      // Echtes App-Bild (TV-Banner), wenn die App eins mitbringt
      el.art.classList.remove('on');
      if (it && it.kind === 'app' && it.app.banner && !isMock && !it.role) {
        el.art.onload = () => { if (moodKey === key) el.art.classList.add('on'); };
        el.art.src = '/banner/' + encodeURIComponent(it.key);
      }
    }, 140);
  }

  function step(delta) {
    const n = SH[S.shelf].items.length;
    if (S.moving && S.shelf === 0) {
      const i = S.favs.indexOf(S.moving), j = i + delta;
      if (j < 0 || j >= S.favs.length) return bump(delta);
      [S.favs[i], S.favs[j]] = [S.favs[j], S.favs[i]];
      SH = buildShelves(); S.idx[0] = j; buildRow(); return;
    }
    const j = S.idx[S.shelf] + delta;
    if (j < 0 || j >= n) return bump(delta);
    S.idx[S.shelf] = j; update();
  }
  function bump(delta) { el.row.classList.remove('bump-l', 'bump-r', 'enter-up', 'enter-down'); void el.row.offsetWidth; el.row.classList.add(delta < 0 ? 'bump-l' : 'bump-r'); }
  function setShelf(i) {
    if (S.moving || i < 0 || i >= SH.length || i === S.shelf) return;
    const dir = i > S.shelf ? 'enter-down' : 'enter-up';
    S.shelf = i; buildRow(dir);
  }

  function activate() {
    const it = cur(); if (!it) return;
    if (S.moving) { S.moving = null; store.set('favs', S.favs); update(); return; }
    const c = cards[S.idx[S.shelf]];
    if (c) { c.classList.remove('launch'); void c.offsetWidth; c.classList.add('launch'); }
    if (it.kind === 'app') launch(it.key); else it.run();
  }
  function launch(pkg) { if (call('launch', pkg) === false) toast('App lässt sich nicht starten'); }

  // ---------- Menüs ----------
  let panelMode = null, kbOpen = false;
  const rows = () => [...el.panelBody.querySelectorAll('.row')];
  function showPanel(mode, title, html) {
    panelMode = mode; el.panelTitle.innerHTML = title; el.panelBody.innerHTML = html;
    el.panel.classList.remove('hidden');
    const first = rows()[0]; if (first) first.focus();
  }
  function closePanel() { if (document.activeElement) document.activeElement.blur(); el.panel.classList.add('hidden'); panelMode = null; kbOpen = false; }
  function rowMove(d) {
    const r = rows(), a = document.activeElement, i = r.indexOf(a && a.closest ? a.closest('.row') : a);
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
    showPanel('menu', `<img src="${it.img}" alt="">${esc(a.label)}`,
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
    const saverTxt = () => (S.saver ? `nach ${S.saver} Min.` : 'aus');
    showPanel('settings', 'Startbildschirm', `
      <div class="row" tabindex="-1" data-input="name">${I.user}<label for="v2-name">Name</label><input id="v2-name" maxlength="24" placeholder="optional"></div>
      <div class="row" tabindex="-1" data-input="city">${I.pin}<label for="v2-city">Ort fürs Wetter</label><input id="v2-city" placeholder="z. B. Hamburg"></div>
      <button class="row" data-act="saver">${I.moon}<span>Ruhemodus</span><span class="val" id="v-saver">${saverTxt()}</span></button>
      <button class="row" data-act="unhide">${I.eye}<span>Ausgeblendete Apps zeigen</span><span class="val" id="v-hidden">${S.hidden.length || 'keine'}</span></button>
      <div class="sep"></div>
      <button class="row" data-act="v1">${I.swap}<span>Zu Version 1 (Glas) wechseln</span></button>
      <button class="row" data-act="home">${I.home}<span>Standard-Startbildschirm wählen</span></button>
      <p class="note">Beamer Home ${esc(info.version || '')} · Version 2 „Kino“${info.model ? '<br>' + esc(info.model) : ''}</p>`);
    const nameIn = $('#v2-name'), cityIn = $('#v2-city');
    nameIn.value = S.name; cityIn.value = S.city ? S.city.name : '';
    nameIn.addEventListener('input', () => { S.name = nameIn.value.trim(); store.set('name', S.name); });
    cityIn.addEventListener('change', () => saveCity(cityIn.value.trim()));
    el.panelBody.onclick = (e) => {
      const r = e.target.closest('[data-input]'); if (r) { r.querySelector('input').focus(); return; }
      const b = e.target.closest('[data-act]'); if (!b) return;
      const k = b.dataset.act;
      if (k === 'saver') { S.saver = SAVER_STEPS[(SAVER_STEPS.indexOf(S.saver) + 1) % SAVER_STEPS.length]; store.set('saver', S.saver); $('#v-saver').textContent = saverTxt(); }
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

  function refresh() { loadApps(); SH = buildShelves(); buildRow(); }

  // ---------- Uhr (rollende Ziffern), Wetter, Netz ----------
  const digits = [];
  (function buildClock() {
    for (let i = 0; i < 4; i++) {
      if (i === 2) el.time.appendChild(h('span', 'colon', ':'));
      const d = h('span', 'd'); d.appendChild(h('i', '', '')); el.time.appendChild(d); digits.push(d);
    }
  })();
  function setDigit(d, ch) {
    const c = d.lastElementChild;
    if (c.textContent === ch) return;
    if (!c.textContent || document.hidden) { c.textContent = ch; return; }
    c.classList.remove('in'); c.classList.add('out'); setTimeout(() => c.remove(), 750);
    const n = h('i', 'in'); n.textContent = ch; d.appendChild(n);
  }
  let lastMinute = '';
  function tick() {
    const d = new Date();
    const hm = String(d.getHours()).padStart(2, '0') + String(d.getMinutes()).padStart(2, '0');
    if (hm === lastMinute) return; // nur einmal pro Minute etwas tun
    lastMinute = hm;
    [...hm].forEach((ch, i) => setDigit(digits[i], ch));
    el.time.setAttribute('aria-label', hm.slice(0, 2) + ':' + hm.slice(2));
    el.date.innerHTML = `<b>${d.toLocaleDateString('de-DE', { weekday: 'long' })}</b>${d.toLocaleDateString('de-DE', { day: 'numeric', month: 'long' })}`;
  }
  async function getJSON(url) {
    const ctl = new AbortController(); const to = setTimeout(() => ctl.abort(), 8000);
    try { const r = await fetch(url, { signal: ctl.signal }); if (!r.ok) throw new Error(r.status); return await r.json(); } finally { clearTimeout(to); }
  }
  async function loadWeather() {
    if (!S.city) { el.weather.innerHTML = ''; return; }
    try {
      const d = await getJSON(`https://api.open-meteo.com/v1/forecast?latitude=${S.city.lat}&longitude=${S.city.lon}&current=temperature_2m&timezone=auto`);
      el.weather.innerHTML = `<b>${Math.round(d.current.temperature_2m)}°</b> ${esc(S.city.name)}`;
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

  // Ein einziger Takt für alles, alle 5 s; im Hintergrund pausiert die App ihn ganz
  let lastWeather = 0, lastNet = 0;
  setInterval(() => {
    if (document.hidden) return;
    tick();
    const now = Date.now();
    if (now - lastNet > 15000) { lastNet = now; updateNet(); }
    if (now - lastWeather > 30 * 60000) { lastWeather = now; loadWeather(); }
    if (S.saver && !isIdle() && !panelMode && !S.moving && now - lastInput > S.saver * 60000) document.body.classList.add('idle');
  }, 5000);

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
    onResume: () => { wake(); lastMinute = ''; tick(); updateNet(); },
    onAppsChanged: () => refresh(),
    // Android meldet RAM-Knappheit: Bilder außerhalb des Blickfelds freigeben
    onLowMemory: () => {
      const i0 = S.idx[S.shelf];
      cards.forEach((c, i) => { if (Math.abs(i - i0) > 10) c.firstChild.textContent = ''; });
      for (const k in colorCache) delete colorCache[k];
    },
  };

  // ---------- Start ----------
  loadApps();
  SH = buildShelves();
  buildRow();
  tick(); updateNet(); loadWeather(); lastWeather = lastNet = Date.now();
  window.addEventListener('resize', () => update(true));
})();
