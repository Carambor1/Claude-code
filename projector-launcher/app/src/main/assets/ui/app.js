/* Beamer Home: Oberfläche und Fernbedienungs-Steuerung */
(() => {
  'use strict';

  const A = window.Android;
  const $ = (s, r = document) => r.querySelector(s);
  const h = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

  // ---------- Speicher ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem('bh.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('bh.' + k, JSON.stringify(v)); } catch (e) { /* egal */ } },
  };

  const state = {
    apps: [],
    byPkg: {},
    favs: store.get('favs', null),
    hidden: store.get('hidden', []),
    name: store.get('name', ''),
    city: store.get('city', null),        // { name, lat, lon }
    theme: store.get('theme', 'aurora'),
    saver: store.get('saver', 10),          // Minuten, 0 = aus
    calm: store.get('calm', false),         // Hintergrund-Animation aus
    moving: null,                           // Paket, das gerade verschoben wird
  };

  // ---------- Symbole ----------
  const I = {
    gear: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h0a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h0a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v0a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    wifi: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 8.8a15 15 0 0 1 20 0"/><path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><circle cx="12" cy="19.6" r=".9" fill="currentColor"/></svg>',
    wifiOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 3l18 18"/><path d="M8.5 16.1a5 5 0 0 1 7 0"/><path d="M5 12.5a10 10 0 0 1 4.2-2.6M19 12.5a10 10 0 0 0-2.6-1.8"/><path d="M2 8.8a15 15 0 0 1 6.3-3.4M22 8.8A15 15 0 0 0 12 5"/><circle cx="12" cy="19.6" r=".9" fill="currentColor"/></svg>',
    lan: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-5h14v5"/></svg>',
    bt: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7l10 10-5 5V2l5 5L7 17"/></svg>',
    display: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    sound: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>',
    input: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 11h1M10 11h1M14 11h1M18 11h0"/><path d="M6 14h12"/></svg>',
    cast: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 16.1A5 5 0 0 1 5.9 20M2 12.05A9 9 0 0 1 9.95 20M2 8V6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-6"/><circle cx="2" cy="20" r=".6" fill="currentColor"/></svg>',
    store: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/></svg>',
    plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg>',
    starOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M9.1 8.5L12 2.5l2.9 6 6.6.9-3.6 3.5M17.6 17.6l.5 2.9L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l3.8-.5"/></svg>',
    move: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 9l-3 3 3 3M19 9l3 3-3 3M2 12h20"/></svg>',
    eyeOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3l18 18"/><path d="M10.6 5.1A10 10 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3.2 3.9M6.6 6.6C3.9 8.4 2 12 2 12s4 7 10 7a9.5 9.5 0 0 0 5.4-1.6"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-5M12 8h0"/></svg>',
    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>',
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    wave: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M2 12c2-3 4-3 6 0s4 3 6 0 4-3 6 0"/></svg>',
    // Wetter
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    partly: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3v1.5M3.6 4.8l1 1M2 9.5h1.5M13 6.3A4 4 0 0 0 5 9a4 4 0 0 0 .4 1.7"/><path d="M17.5 20H8a4.5 4.5 0 1 1 .9-8.9A5.5 5.5 0 0 1 19.6 13a3.5 3.5 0 0 1-2.1 7z"/></svg>',
    cloud: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H8a5 5 0 1 1 1-9.9A6 6 0 0 1 20.6 11 4 4 0 0 1 17.5 19z"/></svg>',
    fog: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 9h16M2 13h20M5 17h14"/></svg>',
    rain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 15H8a5 5 0 1 1 1-9.9A6 6 0 0 1 20.6 7 4 4 0 0 1 17.5 15z"/><path d="M8 18l-1 3M12 18l-1 3M16 18l-1 3"/></svg>',
    snow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 14H8a5 5 0 1 1 1-9.9A6 6 0 0 1 20.6 6 4 4 0 0 1 17.5 14z"/><path d="M8 18h0M12 20h0M16 18h0M10 22h0M14 22h0" stroke-width="2.6"/></svg>',
    storm: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 15H8a5 5 0 1 1 1-9.9A6 6 0 0 1 20.6 7 4 4 0 0 1 17.5 15z"/><path d="M13 13l-3 4.5h4L11 22"/></svg>',
  };

  // ---------- Elemente ----------
  const el = {
    time: $('#time'), date: $('#date'), greeting: $('#greeting'),
    weather: $('#weather'), net: $('#net'), settingsBtn: $('#btn-settings'),
    main: $('#main'), favs: $('#favs'), quick: $('#quick'), apps: $('#apps'), count: $('#appcount'),
    menu: $('#menu'), menuItems: $('#menu-items'), menuTitle: $('#menu-title'), menuIco: $('#menu-ico'),
    settings: $('#settings'), settingsBody: $('#settings-body'),
    saver: $('#saver'), saverClock: $('#saver-clock'), sTime: $('#s-time'), sDate: $('#s-date'),
    toast: $('#toast'), hint: $('#hint'),
  };
  el.settingsBtn.innerHTML = I.gear;

  // ---------- Hilfen ----------
  const iconUrl = (pkg) => window.__mockIcon ? window.__mockIcon(pkg) : '/icon/' + encodeURIComponent(pkg);
  const bannerUrl = (pkg) => '/banner/' + encodeURIComponent(pkg);
  const call = (fn, ...args) => { try { return A && A[fn] ? A[fn](...args) : null; } catch (e) { return null; } };
  const json = (s, d) => { try { return s ? JSON.parse(s) : d; } catch (e) { return d; } };

  let toastTimer;
  function toast(msg) {
    el.toast.textContent = msg;
    el.toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.toast.classList.remove('show'), 2600);
  }

  // Grundfarbe eines Icons bestimmen, damit die Favoriten-Karte dazu passt
  const tintCache = {};
  function tintFrom(img, done) {
    const key = img.dataset.pkg;
    if (tintCache[key]) return done(tintCache[key]);
    try {
      const c = document.createElement('canvas'); c.width = c.height = 16;
      const g = c.getContext('2d', { willReadFrequently: true });
      g.drawImage(img, 0, 0, 16, 16);
      const d = g.getImageData(0, 0, 16, 16).data;
      let r = 0, gg = 0, b = 0, w = 0;
      for (let i = 0; i < d.length; i += 4) {
        const a = d[i + 3] / 255; if (a < .5) continue;
        const mx = Math.max(d[i], d[i + 1], d[i + 2]), mn = Math.min(d[i], d[i + 1], d[i + 2]);
        const sat = mx ? (mx - mn) / mx : 0;
        const wt = .15 + sat * sat * 3 * (mx > 30 ? 1 : .2);
        r += d[i] * wt; gg += d[i + 1] * wt; b += d[i + 2] * wt; w += wt;
      }
      if (!w) return;
      r /= w; gg /= w; b /= w;
      // Für dunklen Hintergrund abdunkeln, aber Farbigkeit behalten
      const k = Math.min(1, 150 / Math.max(r, gg, b, 1));
      const col = `rgb(${Math.round(r * k)}, ${Math.round(gg * k)}, ${Math.round(b * k)})`;
      tintCache[key] = col; done(col);
    } catch (e) { /* ignorieren */ }
  }

  // ---------- Apps ----------
  const DEFAULT_FAVS = [
    'com.google.android.youtube.tv', 'com.google.android.youtube', 'com.netflix.ninja', 'com.netflix.mediaclient',
    'com.amazon.amazonvideo.livingroom', 'com.amazon.avod.thirdpartyclient', 'com.disney.disneyplus',
    'com.spotify.tv.android', 'com.spotify.music', 'org.jellyfin.androidtv', 'com.plexapp.android',
    'org.xbmc.kodi', 'org.videolan.vlc', 'tv.twitch.android.app', 'com.android.chrome',
  ];
  const SOURCE_RE = /hdmi|signal ?source|signalquelle|quelle|eingang|input ?source|^source$/i;
  const CAST_RE = /miracast|screen ?mirror|bildschirm ?spiegel|airplay|eshare|airscreen|cast/i;
  const STORE_PKGS = ['com.android.vending', 'com.amazon.venezia', 'com.aptoide.pt'];

  function loadApps() {
    const list = json(call('getApps'), []);
    list.sort((a, b) => a.label.localeCompare(b.label, 'de', { sensitivity: 'base' }));
    state.apps = list;
    state.byPkg = {};
    list.forEach((a) => { state.byPkg[a.pkg] = a; });

    if (!Array.isArray(state.favs)) {
      state.favs = DEFAULT_FAVS.filter((p) => state.byPkg[p]);
      // Pro Dienst nur eine Variante (TV- oder Handy-App)
      const seen = new Set();
      state.favs = state.favs.filter((p) => { const k = p.split('.').slice(0, 3).join('.').replace(/\.tv$/, ''); if (seen.has(k)) return false; seen.add(k); return true; });
      if (state.favs.length < 3) list.filter((a) => !a.system).slice(0, 6 - state.favs.length).forEach((a) => state.favs.push(a.pkg));
      store.set('favs', state.favs);
    }
  }

  const visibleApps = () => state.apps.filter((a) => !state.hidden.includes(a.pkg));
  const favApps = () => state.favs.map((p) => state.byPkg[p]).filter(Boolean);

  // ---------- Darstellung ----------
  function render() {
    const keep = document.activeElement && document.activeElement.dataset.key;

    // Favoriten
    el.favs.innerHTML = '';
    favApps().forEach((a) => {
      const t = h('button', 'tile fav' + (state.moving === a.pkg ? ' moving' : ''));
      t.dataset.nav = ''; t.dataset.key = 'fav:' + a.pkg; t.dataset.pkg = a.pkg;
      const art = h('div', 'art');
      const ico = new Image(); ico.className = 'ico'; ico.dataset.pkg = a.pkg; ico.alt = '';
      ico.onload = () => tintFrom(ico, (c) => art.style.setProperty('--tint', c));
      ico.src = iconUrl(a.pkg);
      art.appendChild(ico);
      if (a.banner && !window.__mockIcon) {
        const bn = new Image(); bn.className = 'banner'; bn.alt = '';
        bn.onload = () => { ico.remove(); };
        bn.onerror = () => bn.remove();
        bn.src = bannerUrl(a.pkg);
        art.appendChild(bn);
      }
      t.appendChild(art);
      t.appendChild(h('div', 'label')).textContent = a.label;
      t.addEventListener('click', () => onTile(t));
      el.favs.appendChild(t);
    });
    const add = h('button', 'tile fav add', `<div class="art">${I.plus}</div><div class="label">Favorit hinzufügen</div>`);
    add.dataset.nav = ''; add.dataset.key = 'fav:+';
    add.addEventListener('click', () => {
      const first = el.apps.querySelector('.app:not(.isfav)') || el.apps.querySelector('.app');
      if (first) focusEl(first);
      toast('App auswählen und OK lang drücken');
    });
    el.favs.appendChild(add);

    // Schnellzugriff
    el.quick.innerHTML = '';
    const qa = [];
    const src = state.apps.find((a) => SOURCE_RE.test(a.label));
    if (src) qa.push({ key: 'src', label: 'Eingang', icon: I.input, run: () => launch(src.pkg) });
    const cast = state.apps.find((a) => CAST_RE.test(a.label) && a !== src);
    if (cast) qa.push({ key: 'cast', label: 'Spiegeln', icon: I.cast, run: () => launch(cast.pkg) });
    qa.push({ key: 'wifi', label: 'WLAN', icon: I.wifi, run: () => call('openSettings', 'wifi') });
    qa.push({ key: 'bt', label: 'Bluetooth', icon: I.bt, run: () => call('openSettings', 'bluetooth') });
    qa.push({ key: 'display', label: 'Bild', icon: I.display, run: () => call('openSettings', 'display') });
    qa.push({ key: 'sound', label: 'Ton', icon: I.sound, run: () => call('openSettings', 'sound') });
    const st = STORE_PKGS.map((p) => state.byPkg[p]).find(Boolean);
    if (st) qa.push({ key: 'store', label: 'Apps laden', icon: I.store, run: () => launch(st.pkg) });
    qa.push({ key: 'sys', label: 'System', icon: I.gear, run: () => call('openSettings', 'all') });
    qa.forEach((q) => {
      const b = h('button', 'qa', `${q.icon}<span>${q.label}</span>`);
      b.dataset.nav = ''; b.dataset.key = 'qa:' + q.key;
      b.addEventListener('click', q.run);
      el.quick.appendChild(b);
    });

    // Alle Apps
    el.apps.innerHTML = '';
    const vis = visibleApps();
    el.count.textContent = vis.length;
    if (!vis.length) el.apps.appendChild(h('div', 'empty', 'Keine Apps gefunden.'));
    vis.forEach((a) => {
      const t = h('button', 'tile app' + (state.favs.includes(a.pkg) ? ' isfav' : ''));
      t.dataset.nav = ''; t.dataset.key = 'app:' + a.pkg; t.dataset.pkg = a.pkg;
      const img = new Image(); img.alt = ''; img.loading = 'lazy'; img.src = iconUrl(a.pkg);
      t.appendChild(img);
      t.appendChild(h('span')).textContent = a.label;
      t.addEventListener('click', () => onTile(t));
      el.apps.appendChild(t);
    });

    if (keep) {
      const again = document.querySelector(`[data-key="${CSS.escape(keep)}"]`);
      if (again) focusEl(again, true);
      else if (layer() === document.body) focusEl(defaultFocus(), true);
    }
  }

  function onTile(t) {
    const pkg = t.dataset.pkg;
    if (state.moving) { stopMoving(); return; }
    t.classList.remove('launch'); void t.offsetWidth; t.classList.add('launch');
    launch(pkg);
  }

  function launch(pkg) {
    const ok = call('launch', pkg);
    if (ok === false) toast('App lässt sich nicht starten');
  }

  // ---------- Uhr, Datum, Begrüßung ----------
  function greet(hh) {
    if (hh >= 5 && hh < 11) return 'Guten Morgen';
    if (hh >= 11 && hh < 17) return 'Guten Tag';
    if (hh >= 17 && hh < 22) return 'Guten Abend';
    return 'Gute Nacht';
  }
  function tick() {
    const d = new Date();
    const t = d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
    const ds = d.toLocaleDateString('de-DE', { weekday: 'long', day: 'numeric', month: 'long' });
    el.time.textContent = t; el.date.textContent = ds;
    el.greeting.textContent = greet(d.getHours()) + (state.name ? ', ' + state.name : '');
    el.sTime.textContent = t; el.sDate.textContent = ds;
  }

  // ---------- Netzwerk ----------
  let online = true;
  function updateNet() {
    const n = json(call('getNetwork'), { connected: navigator.onLine, type: 'wifi' });
    const wasOnline = online;
    online = !!n.connected;
    el.net.classList.toggle('off', !online);
    el.net.innerHTML = !online ? I.wifiOff : (n.type === 'ethernet' ? I.lan : I.wifi);
    el.net.title = online ? 'Verbunden' : 'Keine Verbindung';
    if (online && !wasOnline) loadWeather();
  }

  // ---------- Wetter (Open-Meteo, ohne API-Schlüssel) ----------
  const WX = (code) => {
    if (code === 0) return [I.sun, 'Klar'];
    if (code <= 2) return [I.partly, 'Heiter'];
    if (code === 3) return [I.cloud, 'Bewölkt'];
    if (code === 45 || code === 48) return [I.fog, 'Nebel'];
    if ((code >= 71 && code <= 77) || code === 85 || code === 86) return [I.snow, 'Schnee'];
    if (code >= 95) return [I.storm, 'Gewitter'];
    if (code >= 51) return [I.rain, 'Regen'];
    return [I.cloud, ''];
  };
  function renderWeatherPrompt() {
    el.weather.innerHTML = `${I.pin}<span class="city">Ort für Wetter festlegen</span>`;
  }
  async function getJSON(url) {
    const ctl = new AbortController();
    const to = setTimeout(() => ctl.abort(), 8000);
    try { const r = await fetch(url, { signal: ctl.signal }); if (!r.ok) throw new Error(r.status); return await r.json(); }
    finally { clearTimeout(to); }
  }
  async function loadWeather() {
    if (!state.city) return renderWeatherPrompt();
    const c = state.city;
    try {
      const d = await getJSON(`https://api.open-meteo.com/v1/forecast?latitude=${c.lat}&longitude=${c.lon}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&forecast_days=1&timezone=auto`);
      const [ico, txt] = WX(d.current.weather_code);
      const t = Math.round(d.current.temperature_2m);
      const hi = Math.round(d.daily.temperature_2m_max[0]), lo = Math.round(d.daily.temperature_2m_min[0]);
      el.weather.innerHTML = `${ico}<span class="temp">${t}°</span><span class="city">${c.name} · ${hi}°/${lo}°</span>`;
      el.weather.title = txt;
    } catch (e) {
      el.weather.innerHTML = `${I.cloud}<span class="city">${c.name} · offline</span>`;
    }
  }
  async function findCity(name) {
    const d = await getJSON(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(name)}&count=1&language=de&format=json`);
    if (!d.results || !d.results.length) return null;
    const r = d.results[0];
    return { name: r.name, lat: +r.latitude.toFixed(3), lon: +r.longitude.toFixed(3) };
  }

  // ---------- Fokus & Fernbedienung ----------
  function layer() {
    if (!el.menu.classList.contains('hidden')) return el.menu;
    if (!el.settings.classList.contains('hidden')) return el.settings;
    return document.body;
  }
  function focusables() {
    return [...layer().querySelectorAll('[data-nav]')].filter((e) => e.offsetParent !== null && !e.disabled && !e.closest('.overlay.hidden'));
  }
  function inLayer(e) { return e && layer().contains(e) && e.hasAttribute('data-nav'); }

  function focusEl(e, instant) {
    if (!e) return;
    e.focus({ preventScroll: true });
    reveal(e, instant);
  }
  function reveal(e, instant) {
    const behavior = instant ? 'auto' : 'smooth';
    if (el.main.contains(e)) {
      const sec = e.closest('.sec');
      if (sec === el.main.firstElementChild) el.main.scrollTo({ top: 0, behavior });
      else {
        const r = e.getBoundingClientRect(), m = el.main.getBoundingClientRect();
        const pad = m.height * 0.12;
        if (r.top < m.top + pad) el.main.scrollBy({ top: r.top - m.top - pad, behavior });
        else if (r.bottom > m.bottom - pad) el.main.scrollBy({ top: r.bottom - m.bottom + pad, behavior });
      }
      const row = e.closest('.row');
      if (row) {
        const r = e.getBoundingClientRect(), w = row.getBoundingClientRect();
        if (r.left < w.left + 30) row.scrollBy({ left: r.left - w.left - 30, behavior });
        else if (r.right > w.right - 30) row.scrollBy({ left: r.right - w.right + 30, behavior });
      }
    } else if (layer() === el.settings) {
      e.scrollIntoView({ block: 'nearest', behavior });
    }
  }

  function move(dir) {
    const cur = document.activeElement;
    const items = focusables();
    if (!inLayer(cur)) { focusEl(defaultFocus()); return; }
    const r = cur.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    let best = null, bestScore = Infinity;
    for (const e of items) {
      if (e === cur) continue;
      const b = e.getBoundingClientRect();
      const bx = b.left + b.width / 2, by = b.top + b.height / 2;
      let gap, cross, overlap;
      if (dir === 'left' || dir === 'right') {
        if (dir === 'left' ? bx >= cx - 1 : bx <= cx + 1) continue;
        overlap = b.top < r.bottom - 2 && b.bottom > r.top + 2;
        if (!overlap) continue; // links/rechts nie in eine andere Zeile springen
        gap = dir === 'left' ? r.left - b.right : b.left - r.right;
        cross = Math.abs(by - cy);
      } else {
        if (dir === 'up' ? by >= cy - 1 : by <= cy + 1) continue;
        gap = dir === 'up' ? r.top - b.bottom : b.top - r.bottom;
        overlap = b.left < r.right && b.right > r.left;
        cross = Math.abs(bx - cx);
      }
      const score = Math.max(gap, 0) * 1 + cross * (overlap ? 0.3 : 1.2);
      if (score < bestScore) { bestScore = score; best = e; }
    }
    if (best) focusEl(best);
  }

  function defaultFocus() {
    const L = layer();
    if (L !== document.body) return L.querySelector('[data-nav]');
    return el.favs.querySelector('[data-nav]') || el.apps.querySelector('[data-nav]');
  }

  // Verschieben eines Favoriten
  function startMoving(pkg) {
    state.moving = pkg; render();
    focusEl($(`[data-key="${CSS.escape('fav:' + pkg)}"]`), true);
    toast('Mit ◀ ▶ verschieben, OK zum Ablegen');
  }
  function stopMoving() {
    const pkg = state.moving; state.moving = null; store.set('favs', state.favs); render();
    focusEl($(`[data-key="${CSS.escape('fav:' + pkg)}"]`), true);
  }
  function shiftFav(delta) {
    const i = state.favs.indexOf(state.moving), j = i + delta;
    if (i < 0 || j < 0 || j >= state.favs.length) return;
    [state.favs[i], state.favs[j]] = [state.favs[j], state.favs[i]];
    render();
    focusEl($(`[data-key="${CSS.escape('fav:' + state.moving)}"]`));
  }

  const DIRS = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down', 37: 'left', 39: 'right', 38: 'up', 40: 'down', 21: 'left', 22: 'right', 19: 'up', 20: 'down' };
  let pressTimer = null, longFired = false, swallow = false, okDown = false, kbOpen = false;
  document.addEventListener('focusout', (e) => { if (e.target.tagName === 'INPUT') kbOpen = false; });

  document.addEventListener('keydown', (e) => {
    activity();
    if (!el.saver.classList.contains('hidden')) { hideSaver(); swallow = true; e.preventDefault(); return; }
    if (swallow) { e.preventDefault(); return; }
    const a = document.activeElement;
    const inInput = a && a.tagName === 'INPUT';
    const dir = DIRS[e.key] || DIRS[e.keyCode];

    if (dir) {
      if (inInput && (dir === 'left' || dir === 'right')) return;
      e.preventDefault();
      if (state.moving && (dir === 'left' || dir === 'right')) { shiftFav(dir === 'left' ? -1 : 1); return; }
      if (state.moving) return;
      move(dir);
      return;
    }
    if (e.key === 'Enter' || e.keyCode === 13 || e.keyCode === 23) {
      if (inInput) {
        e.preventDefault();
        if (e.repeat) return;
        if (kbOpen) { kbOpen = false; call('hideKeyboard'); if (a.dataset.submit) $(a.dataset.submit).click(); }
        else { kbOpen = true; call('showKeyboard'); }
        return;
      }
      e.preventDefault();
      if (e.repeat || okDown) return;
      okDown = true; longFired = false;
      clearTimeout(pressTimer);
      pressTimer = setTimeout(() => {
        const t = document.activeElement;
        if (t && t.dataset.pkg && !state.moving) { longFired = true; openMenuFor(t); }
      }, 650);
      return;
    }
    if (e.key === 'Escape' || e.key === 'GoBack' || e.key === 'BrowserBack' || (e.key === 'Backspace' && !inInput)) {
      e.preventDefault(); onBack(); return;
    }
    if (e.key === 'ContextMenu' || e.key === 'm') { e.preventDefault(); onMenu(); }
  }, true);

  document.addEventListener('keyup', (e) => {
    if (swallow) { swallow = false; okDown = false; clearTimeout(pressTimer); e.preventDefault(); return; }
    if (e.key === 'Enter' || e.keyCode === 13 || e.keyCode === 23) {
      if (!okDown) return;
      okDown = false;
      clearTimeout(pressTimer);
      if (!longFired) {
        const a = document.activeElement;
        if (inLayer(a)) a.click(); else focusEl(defaultFocus());
      }
      e.preventDefault();
    }
  }, true);

  // Maus/Touch (z. B. Air-Mouse-Fernbedienung)
  document.addEventListener('mouseover', (e) => {
    const t = e.target.closest('[data-nav]');
    if (t && inLayer(t) && document.activeElement !== t) t.focus({ preventScroll: true });
  });
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    const t = e.target.closest('[data-pkg]');
    if (t) openMenuFor(t);
  });
  document.addEventListener('pointerdown', activity, true);
  document.addEventListener('wheel', activity, { passive: true, capture: true });

  // ---------- Kontextmenü ----------
  let menuReturn = null;
  function openMenuFor(t) {
    if (!t || !t.dataset.pkg) return;
    const a = state.byPkg[t.dataset.pkg]; if (!a) return;
    menuReturn = t.dataset.key;
    const isFav = state.favs.includes(a.pkg);
    const items = [];
    items.push({ icon: I.home, label: 'Öffnen', run: () => launch(a.pkg) });
    if (isFav) {
      items.push({ icon: I.starOff, label: 'Aus Favoriten entfernen', run: () => { state.favs = state.favs.filter((p) => p !== a.pkg); store.set('favs', state.favs); render(); } });
      if (state.favs.length > 1) items.push({ icon: I.move, label: 'Verschieben', run: () => startMoving(a.pkg), keepFocus: true });
    } else {
      items.push({ icon: I.star, label: 'Zu Favoriten hinzufügen', run: () => { state.favs.push(a.pkg); store.set('favs', state.favs); render(); toast(a.label + ' ist jetzt Favorit'); } });
    }
    items.push({ icon: I.eyeOff, label: 'In „Alle Apps“ ausblenden', run: () => {
      state.hidden.push(a.pkg); store.set('hidden', state.hidden); render(); toast('Ausgeblendet. Zurückholen in den Einstellungen');
    } });
    items.push({ icon: I.info, label: 'App-Info', run: () => call('appInfo', a.pkg) });
    if (!a.system) items.push({ icon: I.trash, label: 'Deinstallieren', cls: 'danger', run: () => call('uninstall', a.pkg) });

    el.menuTitle.textContent = a.label;
    el.menuIco.src = iconUrl(a.pkg);
    el.menuItems.innerHTML = '';
    items.forEach((it) => {
      const b = h('button', 'mi' + (it.cls ? ' ' + it.cls : ''), `${it.icon}<span>${it.label}</span>`);
      b.dataset.nav = '';
      b.addEventListener('click', () => { closeMenu(!it.keepFocus); it.run(); });
      el.menuItems.appendChild(b);
    });
    el.menu.classList.remove('hidden');
    focusEl(el.menuItems.firstElementChild, true);
  }
  function closeMenu(restore = true) {
    el.menu.classList.add('hidden');
    if (restore) {
      const t = menuReturn && document.querySelector(`[data-key="${CSS.escape(menuReturn)}"]`);
      focusEl(t || defaultFocus(), true);
    }
  }

  // ---------- Einstellungen ----------
  const THEMES = [
    ['aurora', 'Aurora', 'linear-gradient(135deg,#14b8a6,#7c3aed)'],
    ['sunset', 'Abendrot', 'linear-gradient(135deg,#f97316,#db2777)'],
    ['ocean', 'Ozean', 'linear-gradient(135deg,#2563eb,#0891b2)'],
    ['forest', 'Wald', 'linear-gradient(135deg,#16a34a,#0d9488)'],
    ['mono', 'Graphit', 'linear-gradient(135deg,#52525b,#18181b)'],
  ];
  const SAVER_STEPS = [0, 5, 10, 30, 60];

  function openSettings(focusKey) {
    const info = json(call('deviceInfo'), {});
    el.settingsBody.innerHTML = `
      <div class="set"><label>Dein Name (für die Begrüßung)</label>
        <div class="line"><input id="in-name" data-nav data-key="s:name" maxlength="24" placeholder="optional"></div></div>
      <div class="set"><label>Ort für das Wetter</label>
        <div class="line"><input id="in-city" data-nav data-key="s:city" data-submit="#btn-city" placeholder="z. B. Hamburg">
        <button id="btn-city" class="btn" data-nav data-key="s:citybtn">Übernehmen</button></div></div>
      <div class="set"><label>Design</label><div class="swatches" id="sw"></div></div>
      <div class="set stack">
        <button class="btn wide" data-nav data-key="s:saver" id="btn-saver">${I.moon}<span>Bildschirmschoner</span><span class="val"></span></button>
        <button class="btn wide" data-nav data-key="s:calm" id="btn-calm">${I.wave}<span>Bewegter Hintergrund</span><span class="val"></span></button>
        <button class="btn wide" data-nav data-key="s:unhide" id="btn-unhide">${I.eye}<span>Ausgeblendete Apps zeigen</span><span class="val"></span></button>
      </div>
      <div class="set stack">
        <button class="btn wide" data-nav data-key="s:home" id="btn-home">${I.home}<span>Standard-Startbildschirm wählen</span></button>
        <button class="btn wide" data-nav data-key="s:sys" id="btn-sys">${I.gear}<span>Android-Einstellungen</span></button>
        <button class="btn wide" data-nav data-key="s:date" id="btn-date">${I.info}<span>Datum &amp; Uhrzeit</span></button>
      </div>
      <div class="about">Beamer Home ${info.version || ''}<br>${info.model || ''}${info.android ? ' · Android ' + info.android : ''}</div>`;

    const nameIn = $('#in-name'), cityIn = $('#in-city');
    nameIn.value = state.name;
    cityIn.value = state.city ? state.city.name : '';
    nameIn.addEventListener('input', () => { state.name = nameIn.value.trim(); store.set('name', state.name); tick(); });

    $('#btn-city').addEventListener('click', async () => {
      const q = cityIn.value.trim();
      if (!q) { state.city = null; store.set('city', null); loadWeather(); toast('Wetter ausgeschaltet'); return; }
      toast('Suche …');
      try {
        const c = await findCity(q);
        if (!c) { toast('Ort nicht gefunden'); return; }
        state.city = c; store.set('city', c); cityIn.value = c.name; loadWeather(); toast('Wetter für ' + c.name);
      } catch (e) { toast('Keine Internetverbindung'); }
    });

    const sw = $('#sw');
    THEMES.forEach(([id, name, grad]) => {
      const b = h('button', 'sw' + (state.theme === id ? ' on' : ''));
      b.dataset.nav = ''; b.dataset.key = 's:t:' + id; b.title = name; b.style.background = grad;
      b.addEventListener('click', () => { setTheme(id); sw.querySelectorAll('.sw').forEach((x) => x.classList.toggle('on', x === b)); });
      sw.appendChild(b);
    });

    const saverBtn = $('#btn-saver'), calmBtn = $('#btn-calm'), unhideBtn = $('#btn-unhide');
    const paint = () => {
      saverBtn.querySelector('.val').textContent = state.saver ? `nach ${state.saver} Min.` : 'aus';
      calmBtn.querySelector('.val').textContent = state.calm ? 'aus' : 'an';
      unhideBtn.querySelector('.val').textContent = state.hidden.length || 'keine';
    };
    paint();
    saverBtn.addEventListener('click', () => { state.saver = SAVER_STEPS[(SAVER_STEPS.indexOf(state.saver) + 1) % SAVER_STEPS.length]; store.set('saver', state.saver); paint(); });
    calmBtn.addEventListener('click', () => { state.calm = !state.calm; store.set('calm', state.calm); document.body.classList.toggle('calm', state.calm); paint(); });
    unhideBtn.addEventListener('click', () => { const n = state.hidden.length; state.hidden = []; store.set('hidden', []); render(); paint(); toast(n ? n + ' App(s) wieder sichtbar' : 'Keine Apps ausgeblendet'); });
    $('#btn-home').addEventListener('click', () => call('openSettings', 'home'));
    $('#btn-sys').addEventListener('click', () => call('openSettings', 'all'));
    $('#btn-date').addEventListener('click', () => call('openSettings', 'date'));

    el.settings.classList.remove('hidden');
    const f = focusKey && $(`[data-key="${CSS.escape(focusKey)}"]`, el.settings);
    focusEl(f || $('#sw .sw.on') || defaultFocus(), true);
  }
  function closeSettings() {
    if (document.activeElement) document.activeElement.blur();
    el.settings.classList.add('hidden');
    focusEl(el.settingsBtn, true);
  }
  function setTheme(id) { state.theme = id; store.set('theme', id); document.body.dataset.theme = id; }

  el.settingsBtn.addEventListener('click', () => openSettings());
  el.weather.addEventListener('click', () => openSettings('s:city'));
  el.menu.addEventListener('click', (e) => { if (e.target === el.menu) closeMenu(); });
  el.settings.addEventListener('click', (e) => { if (e.target === el.settings) closeSettings(); });

  // ---------- Bildschirmschoner ----------
  let lastInput = Date.now(), saverMove;
  function activity() {
    lastInput = Date.now();
    el.hint.classList.add('gone');
  }
  function showSaver() {
    el.saver.classList.remove('hidden');
    const place = () => {
      el.saverClock.style.opacity = 0;
      setTimeout(() => {
        const W = innerWidth, H = innerHeight, cw = el.saverClock.offsetWidth, ch = el.saverClock.offsetHeight;
        el.saverClock.style.left = Math.random() * Math.max(0, W - cw) + 'px';
        el.saverClock.style.top = Math.random() * Math.max(0, H - ch) + 'px';
        el.saverClock.style.opacity = 1;
      }, 1500);
    };
    place();
    saverMove = setInterval(place, 30000);
  }
  function hideSaver() { el.saver.classList.add('hidden'); clearInterval(saverMove); lastInput = Date.now(); }
  setInterval(() => {
    if (!state.saver || !el.saver.classList.contains('hidden') || document.hidden) return;
    if (layer() !== document.body || state.moving) return;
    if (Date.now() - lastInput > state.saver * 60000) showSaver();
  }, 15000);

  // ---------- Systemereignisse (aus MainActivity) ----------
  function onBack() {
    if (!el.saver.classList.contains('hidden')) return hideSaver();
    if (state.moving) return stopMoving();
    if (!el.menu.classList.contains('hidden')) return closeMenu();
    if (!el.settings.classList.contains('hidden')) return closeSettings();
    el.main.scrollTo({ top: 0, behavior: 'smooth' });
    el.favs.scrollTo({ left: 0, behavior: 'smooth' });
    focusEl(defaultFocus());
  }
  function onMenu() {
    if (!el.menu.classList.contains('hidden')) return closeMenu();
    const a = document.activeElement;
    if (a && a.dataset.pkg && layer() === document.body) openMenuFor(a);
    else if (layer() === document.body) openSettings();
    else if (layer() === el.settings) closeSettings();
  }
  function onHome() {
    hideSaver();
    if (state.moving) stopMoving();
    el.menu.classList.add('hidden');
    el.settings.classList.add('hidden');
    el.main.scrollTo({ top: 0 });
    el.favs.scrollTo({ left: 0 });
    focusEl(defaultFocus(), true);
  }

  window.BH = {
    onBack, onMenu, onHome, toast,
    onSettingsKey: () => (layer() === el.settings ? closeSettings() : openSettings()),
    onResume: () => { activity(); hideSaver(); updateNet(); tick(); if (!inLayer(document.activeElement)) focusEl(defaultFocus(), true); },
    onAppsChanged: () => { loadApps(); render(); },
  };

  // ---------- Start ----------
  document.body.dataset.theme = state.theme;
  document.body.classList.toggle('calm', state.calm);
  loadApps();
  render();
  tick();
  setInterval(tick, 1000);
  updateNet();
  setInterval(updateNet, 15000);
  loadWeather();
  setInterval(loadWeather, 30 * 60000);
  focusEl(defaultFocus(), true);
  setTimeout(() => el.hint.classList.add('gone'), 12000);
})();
