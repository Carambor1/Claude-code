/* Nur für die Vorschau im normalen Browser: simuliert die Android-Brücke.
   Auf dem Beamer existiert window.Android bereits, dann passiert hier nichts. */
(() => {
  if (window.Android) return;
  const apps = [
    ['com.google.android.youtube.tv', 'YouTube', '#ff0033', 'YT'],
    ['com.netflix.ninja', 'Netflix', '#e50914', 'N'],
    ['com.amazon.amazonvideo.livingroom', 'Prime Video', '#1399ff', 'P'],
    ['com.disney.disneyplus', 'Disney+', '#113ccf', 'D+'],
    ['com.spotify.tv.android', 'Spotify', '#1ed760', 'S'],
    ['org.jellyfin.androidtv', 'Jellyfin', '#aa5cc3', 'J'],
    ['org.videolan.vlc', 'VLC', '#ff8800', 'V'],
    ['com.android.vending', 'Play Store', '#01875f', '▶'],
    ['com.android.chrome', 'Chrome', '#4285f4', 'C'],
    ['com.softwinner.tvdsetting', 'Einstellungen', '#64748b', '⚙', true],
    ['com.hy.hdmiinput', 'HDMI', '#0ea5e9', 'H', true],
    ['com.ecloud.eshare.server', 'Screen Mirror', '#8b5cf6', '⇪', true],
    ['com.android.music', 'Musik', '#f43f5e', '♪', true],
    ['com.android.gallery3d', 'Galerie', '#f59e0b', '▣', true],
    ['com.android.filemanager', 'Dateien', '#22c55e', 'F', true],
    ['tv.twitch.android.app', 'Twitch', '#9146ff', 'T'],
    ['com.zdf.android.mediathek', 'ZDFmediathek', '#fa7d19', 'Z'],
    ['de.swr.ard.avp.mobile.android.amazon', 'ARD Mediathek', '#0060ab', 'ARD'],
    ['com.plexapp.android', 'Plex', '#e5a00d', '›'],
    ['org.xbmc.kodi', 'Kodi', '#17b2e7', 'K'],
    ['com.android.calendar', 'Kalender', '#3b82f6', '31', true],
  ];
  const meta = {};
  apps.forEach(([pkg, label, color, glyph, system]) => { meta[pkg] = { label, color, glyph, system: !!system }; });

  window.__mockIcon = (pkg) => {
    if (window.__brandIcons && window.__brandIcons[pkg]) return window.__brandIcons[pkg];
    const m = meta[pkg] || { color: '#475569', glyph: '?' };
    const fs = m.glyph.length > 2 ? 30 : m.glyph.length > 1 ? 40 : 56;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect width="96" height="96" rx="22" fill="${m.color}"/><text x="48" y="50" dominant-baseline="central" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="${fs}" fill="#fff">${m.glyph}</text></svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  };

  const log = (...a) => console.log('[Android]', ...a);
  window.Android = {
    getApps: () => JSON.stringify(apps.map(([pkg]) => ({ pkg, label: meta[pkg].label, tv: true, banner: false, system: meta[pkg].system }))),
    launch: (pkg) => { log('launch', pkg); window.BH && BH.toast('Startet ' + meta[pkg].label + ' (Vorschau)'); return true; },
    openSettings: (w) => { log('openSettings', w); window.BH && BH.toast('Öffnet Einstellungen: ' + w + ' (Vorschau)'); },
    appInfo: (p) => log('appInfo', p),
    uninstall: (p) => log('uninstall', p),
    showKeyboard: () => {},
    hideKeyboard: () => {},
    getNetwork: () => JSON.stringify({ connected: navigator.onLine, type: 'wifi' }),
    deviceInfo: () => JSON.stringify({ model: 'Browser-Vorschau', android: '', version: 'dev' }),
  };
})();
