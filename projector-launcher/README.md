# Beamer Home: eigener Startbildschirm für den Magcubic HY300 Pro+

Ein Launcher, der die Oberfläche des Beamers ersetzt. Android läuft darunter weiter,
aber nach der Home-Taste siehst du nur noch diese Oberfläche.

- Große Uhr, Datum, Begrüßung, Wetter (Open-Meteo, ohne Konto)
- **Favoriten** als große Kacheln (TV-Banner oder Icon mit passender Farbe)
- **Schnellzugriff**: HDMI-Eingang & Bildschirm-Spiegeln (wenn eine passende App da ist), WLAN, Bluetooth, Bild, Ton, Play Store, System
- **Alle Apps** im Raster, Apps ausblenden, App-Info, Deinstallieren
- Komplett mit dem Steuerkreuz bedienbar, Air-Mouse und Touch gehen auch
- 5 Designs, Bildschirmschoner mit wandernder Uhr, Hintergrund-Animation abschaltbar

## Bedienung

| Taste | Funktion |
|---|---|
| Steuerkreuz | Fokus bewegen |
| **OK** | App öffnen bzw. Knopf drücken |
| **OK lang** oder **Menü** | Optionen zur App: Favorit, Verschieben, Ausblenden, Info, Deinstallieren |
| **Zurück** | Menü schließen bzw. nach oben springen |
| **Home** | immer zurück zum Startbildschirm |

Bei Eingabefeldern (Name, Ort) öffnet **OK** die Bildschirmtastatur. Ein zweites **OK** übernimmt die Eingabe.

## Installieren

1. APK laden: <https://github.com/Carambor1/Claude-code/releases/download/beamer-home-latest/BeamerHome.apk>
   - **Direkt am Beamer**: die App *Downloader* (Play Store) installieren und dort die Adresse oben eingeben.
   - **Oder** am Handy oder PC laden, auf einen USB-Stick kopieren und am Beamer mit dem Dateimanager öffnen.
2. Falls Android fragt: „Installation aus unbekannten Quellen“ für diese App erlauben.
3. **Home-Taste** drücken, dann **Beamer Home** und **Immer** wählen.
   Kommt keine Abfrage: in Beamer Home unter *Einstellungen → Standard-Startbildschirm wählen*
   oder in Android unter *Einstellungen → Apps → Standard-Apps → Startbildschirm-App*.

### Falls die Firmware keinen anderen Startbildschirm zulässt

Manche Beamer-Firmwares haben keinen Auswahl-Dialog. Dann geht es per ADB
(Entwickleroptionen → USB- bzw. Netzwerk-Debugging an):

```sh
adb connect <IP-des-Beamers>:5555
adb shell cmd package set-home-activity de.beamerhome.launcher/.MainActivity
```

Zurück zum Original-Launcher: in den Android-Einstellungen wieder umstellen oder Beamer Home deinstallieren.

## Aufbau

```
projector-launcher/
├── app/src/main/java/.../MainActivity.java   Android-Hülle: Vollbild-WebView, Home-Taste, Brücke (window.Android)
├── app/src/main/assets/ui/                   Die Oberfläche (HTML/CSS/JS)
│   ├── index.html, style.css, app.js
│   └── mock.js                               simuliert Android im normalen Browser
└── keystore/beamerhome.jks                   fester Signaturschlüssel (nur privat), damit Updates sich drüber installieren
```

Die Brücke stellt bereit: `getApps`, `launch`, `openSettings`, `appInfo`, `uninstall`,
`getNetwork`, `deviceInfo`, `showKeyboard`/`hideKeyboard`. App-Icons und TV-Banner liefert sie unter `/icon/<paket>` bzw. `/banner/<paket>`.

**Oberfläche am PC testen:** `cd app/src/main/assets/ui && python3 -m http.server`, dann
<http://localhost:8000> öffnen und mit den Pfeiltasten, Enter (lang drücken für Optionen) und Esc bedienen.

**Bauen:** passiert automatisch per GitHub Actions bei jedem Push (`.github/workflows/beamer-home.yml`).
Lokal mit Android SDK: `gradle assembleRelease` in diesem Ordner.
