package de.beamerhome.launcher;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.ComponentCallbacks2;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.util.LruCache;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Startbildschirm für den Beamer. Die eigentliche Oberfläche ist eine Web-App
 * (assets/ui), die unter https://beamerhome.local/ ausgeliefert wird. Diese Klasse
 * stellt ihr eine kleine Brücke (window.Android) zum System bereit.
 */
public class MainActivity extends Activity {

    private static final String HOST = "beamerhome.local";
    private static final String BASE = "https://" + HOST + "/";

    private WebView web;
    // Höchstens ~3 MB Icons im RAM (der Beamer hat nur 1 GB)
    private final LruCache<String, byte[]> iconCache = new LruCache<String, byte[]>(3 * 1024 * 1024) {
        @Override
        protected int sizeOf(String key, byte[] value) {
            return value == null ? 1 : value.length;
        }
    };
    private static final byte[] NONE = new byte[0];

    private final BroadcastReceiver packageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            iconCache.evictAll();
            js("BH.onAppsChanged()");
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().getDecorView().setBackgroundColor(Color.BLACK);

        web = new WebView(this);
        web.setBackgroundColor(Color.BLACK);
        web.setFocusable(true);
        web.setFocusableInTouchMode(true);
        web.setVerticalScrollBarEnabled(false);
        web.setHorizontalScrollBarEnabled(false);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(false);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        s.setTextZoom(100);

        web.addJavascriptInterface(new Bridge(), "Android");
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (!HOST.equals(uri.getHost())) return null; // Internet (z. B. Wetter) normal laden
                return serve(uri.getPath());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                // Links nie im Launcher öffnen, sondern im Browser des Systems
                if (HOST.equals(request.getUrl().getHost())) return false;
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, request.getUrl())
                            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                } catch (Exception ignored) {
                }
                return true;
            }
        });

        setContentView(web);
        hideSystemBars();
        web.loadUrl(BASE + "index.html");
        web.requestFocus();

        IntentFilter f = new IntentFilter();
        f.addAction(Intent.ACTION_PACKAGE_ADDED);
        f.addAction(Intent.ACTION_PACKAGE_REMOVED);
        f.addAction(Intent.ACTION_PACKAGE_CHANGED);
        f.addAction(Intent.ACTION_PACKAGE_REPLACED);
        f.addDataScheme("package");
        if (Build.VERSION.SDK_INT >= 33) {
            registerReceiver(packageReceiver, f, Context.RECEIVER_EXPORTED);
        } else {
            registerReceiver(packageReceiver, f);
        }
    }

    @SuppressWarnings("deprecation")
    private void hideSystemBars() {
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideSystemBars();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
        web.resumeTimers();
        hideSystemBars();
        js("BH.onResume()");
    }

    @Override
    protected void onPause() {
        // Während Netflix & Co. laufen, rechnet der Startbildschirm nichts
        web.onPause();
        web.pauseTimers();
        super.onPause();
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        if (level >= ComponentCallbacks2.TRIM_MEMORY_RUNNING_LOW) {
            iconCache.evictAll();
            if (web != null) {
                web.clearCache(false);
                js("BH.onLowMemory && BH.onLowMemory()");
            }
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        // Home-Taste gedrückt, während der Launcher schon offen ist
        js("BH.onHome()");
    }

    @Override
    protected void onDestroy() {
        try {
            unregisterReceiver(packageReceiver);
        } catch (Exception ignored) {
        }
        web.destroy();
        super.onDestroy();
    }

    @SuppressWarnings("deprecation")
    @Override
    public void onBackPressed() {
        // Ein Launcher wird nie mit "Zurück" beendet, die Web-UI entscheidet.
        js("BH.onBack()");
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        int code = event.getKeyCode();
        if (code == KeyEvent.KEYCODE_MENU || code == KeyEvent.KEYCODE_SETTINGS) {
            if (event.getAction() == KeyEvent.ACTION_UP) {
                js(code == KeyEvent.KEYCODE_MENU ? "BH.onMenu()" : "BH.onSettingsKey()");
            }
            return true;
        }
        return super.dispatchKeyEvent(event);
    }

    private void js(String code) {
        if (web == null) return;
        web.post(() -> web.evaluateJavascript("window.BH && " + code, null));
    }

    // ---------- Dateien für die Web-UI ----------

    private WebResourceResponse serve(String path) {
        try {
            if (path == null || path.equals("/")) path = "/index.html";
            if (path.startsWith("/icon/")) {
                return png(appImage(Uri.decode(path.substring(6)), false));
            }
            if (path.startsWith("/banner/")) {
                return png(appImage(Uri.decode(path.substring(8)), true));
            }
            InputStream in = getAssets().open("ui" + path);
            WebResourceResponse r = new WebResourceResponse(mime(path), "utf-8", in);
            Map<String, String> h = new HashMap<>();
            h.put("Cache-Control", "no-cache");
            r.setResponseHeaders(h);
            return r;
        } catch (Exception e) {
            return notFound();
        }
    }

    private WebResourceResponse png(byte[] data) {
        if (data == null) return notFound();
        WebResourceResponse r = new WebResourceResponse("image/png", null, new ByteArrayInputStream(data));
        Map<String, String> h = new HashMap<>();
        h.put("Cache-Control", "max-age=86400");
        r.setResponseHeaders(h);
        return r;
    }

    private WebResourceResponse notFound() {
        return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found",
                new HashMap<>(), new ByteArrayInputStream(new byte[0]));
    }

    private static String mime(String path) {
        if (path.endsWith(".html")) return "text/html";
        if (path.endsWith(".css")) return "text/css";
        if (path.endsWith(".js")) return "application/javascript";
        if (path.endsWith(".svg")) return "image/svg+xml";
        if (path.endsWith(".png")) return "image/png";
        if (path.endsWith(".jpg") || path.endsWith(".jpeg")) return "image/jpeg";
        if (path.endsWith(".webp")) return "image/webp";
        if (path.endsWith(".json")) return "application/json";
        if (path.endsWith(".woff2")) return "font/woff2";
        return "application/octet-stream";
    }

    private byte[] appImage(String pkg, boolean banner) {
        String key = (banner ? "b:" : "i:") + pkg;
        byte[] cached = iconCache.get(key);
        if (cached != null) return cached == NONE ? null : cached;
        byte[] out = null;
        try {
            PackageManager pm = getPackageManager();
            Drawable d;
            if (banner) {
                d = pm.getApplicationBanner(pkg);
                if (d == null) {
                    Intent i = pm.getLeanbackLaunchIntentForPackage(pkg);
                    if (i != null) d = pm.getActivityBanner(i);
                }
            } else {
                d = pm.getApplicationIcon(pkg);
            }
            if (d != null) out = toPng(d, banner ? 320 : 160, banner ? 180 : 160);
        } catch (Exception ignored) {
        }
        iconCache.put(key, out == null ? NONE : out);
        return out;
    }

    private static byte[] toPng(Drawable d, int w, int h) {
        Bitmap bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
        Canvas c = new Canvas(bmp);
        d.setBounds(0, 0, w, h);
        d.draw(c);
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.PNG, 90, bos);
        bmp.recycle();
        return bos.toByteArray();
    }

    // ---------- Brücke für JavaScript (window.Android) ----------

    private class Bridge {

        @JavascriptInterface
        public String getApps() {
            PackageManager pm = getPackageManager();
            Map<String, JSONObject> apps = new LinkedHashMap<>();
            addApps(pm, Intent.CATEGORY_LEANBACK_LAUNCHER, apps, true);
            addApps(pm, Intent.CATEGORY_LAUNCHER, apps, false);
            JSONArray arr = new JSONArray();
            for (JSONObject o : apps.values()) arr.put(o);
            return arr.toString();
        }

        private void addApps(PackageManager pm, String category, Map<String, JSONObject> out, boolean tv) {
            Intent i = new Intent(Intent.ACTION_MAIN).addCategory(category);
            List<ResolveInfo> list = pm.queryIntentActivities(i, 0);
            for (ResolveInfo ri : list) {
                String pkg = ri.activityInfo.packageName;
                if (pkg.equals(getPackageName()) || out.containsKey(pkg)) continue;
                try {
                    ApplicationInfo ai = ri.activityInfo.applicationInfo;
                    JSONObject o = new JSONObject();
                    o.put("pkg", pkg);
                    o.put("label", String.valueOf(ri.loadLabel(pm)));
                    o.put("tv", tv);
                    o.put("banner", tv && (ai.banner != 0 || ri.activityInfo.banner != 0));
                    o.put("system", (ai.flags & ApplicationInfo.FLAG_SYSTEM) != 0);
                    out.put(pkg, o);
                } catch (Exception ignored) {
                }
            }
        }

        @JavascriptInterface
        public boolean launch(String pkg) {
            PackageManager pm = getPackageManager();
            Intent i = pm.getLeanbackLaunchIntentForPackage(pkg);
            if (i == null) i = pm.getLaunchIntentForPackage(pkg);
            if (i == null) return false;
            final Intent start = i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            runOnUiThread(() -> {
                try {
                    startActivity(start);
                } catch (Exception e) {
                    js("BH.toast('App konnte nicht gestartet werden')");
                }
            });
            return true;
        }

        @JavascriptInterface
        public void openSettings(String which) {
            String action;
            switch (which == null ? "" : which) {
                case "wifi": action = Settings.ACTION_WIFI_SETTINGS; break;
                case "bluetooth": action = Settings.ACTION_BLUETOOTH_SETTINGS; break;
                case "display": action = Settings.ACTION_DISPLAY_SETTINGS; break;
                case "sound": action = Settings.ACTION_SOUND_SETTINGS; break;
                case "apps": action = Settings.ACTION_APPLICATION_SETTINGS; break;
                case "date": action = Settings.ACTION_DATE_SETTINGS; break;
                case "home": action = Settings.ACTION_HOME_SETTINGS; break;
                case "language": action = Settings.ACTION_LOCALE_SETTINGS; break;
                default: action = Settings.ACTION_SETTINGS;
            }
            final String a = action;
            runOnUiThread(() -> {
                try {
                    startActivity(new Intent(a).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                } catch (Exception e) {
                    try {
                        startActivity(new Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                    } catch (Exception ignored) {
                        js("BH.toast('Einstellungen nicht verfügbar')");
                    }
                }
            });
        }

        @JavascriptInterface
        public void appInfo(String pkg) {
            runOnUiThread(() -> {
                try {
                    startActivity(new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                            Uri.parse("package:" + pkg)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                } catch (Exception ignored) {
                }
            });
        }

        @JavascriptInterface
        public void uninstall(String pkg) {
            runOnUiThread(() -> {
                try {
                    startActivity(new Intent(Intent.ACTION_DELETE, Uri.parse("package:" + pkg))
                            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                } catch (Exception ignored) {
                }
            });
        }

        @JavascriptInterface
        public void showKeyboard() {
            runOnUiThread(() -> {
                InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
                web.requestFocus();
                if (imm != null) imm.showSoftInput(web, InputMethodManager.SHOW_IMPLICIT);
            });
        }

        @JavascriptInterface
        public void hideKeyboard() {
            runOnUiThread(() -> {
                InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
                if (imm != null) imm.hideSoftInputFromWindow(web.getWindowToken(), 0);
            });
        }

        @JavascriptInterface
        public String getNetwork() {
            JSONObject o = new JSONObject();
            try {
                ConnectivityManager cm = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
                Network n = cm.getActiveNetwork();
                NetworkCapabilities nc = n == null ? null : cm.getNetworkCapabilities(n);
                String type = "none";
                if (nc != null) {
                    if (nc.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) type = "wifi";
                    else if (nc.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)) type = "ethernet";
                    else type = "other";
                }
                o.put("connected", nc != null && nc.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET));
                o.put("type", type);
            } catch (Exception ignored) {
            }
            return o.toString();
        }

        @JavascriptInterface
        public String deviceInfo() {
            JSONObject o = new JSONObject();
            try {
                o.put("model", Build.MANUFACTURER + " " + Build.MODEL);
                o.put("android", Build.VERSION.RELEASE);
                PackageInfo pi = getPackageManager().getPackageInfo(getPackageName(), 0);
                o.put("version", pi.versionName);
            } catch (Exception ignored) {
            }
            return o.toString();
        }
    }
}
