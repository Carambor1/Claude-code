// "Every Second on Earth" — the 3D film. One renderer, five sets; render(t) is a pure function of time (seek-safe).
import * as THREE from "three";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/examples/jsm/postprocessing/OutputPass.js";

const D2R = Math.PI / 180;
const ss = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * x * (x * (x * 6 - 15) + 10); };
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const ll = (lat, lon, r = 1) => { const phi = (90 - lat) * D2R, th = (lon + 180) * D2R; return new THREE.Vector3(-r * Math.sin(phi) * Math.cos(th), r * Math.cos(phi), r * Math.sin(phi) * Math.sin(th)); };
const glowTex = (inner = "rgba(255,255,255,1)", mid = "rgba(255,255,255,0.35)") => { const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d"); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, inner); gr.addColorStop(0.25, mid); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };

export async function init(canvas, K) {
  const W = canvas.width, H = canvas.height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const cam = new THREE.PerspectiveCamera(38, W / H, 0.05, 4000);
  const loader = new THREE.TextureLoader();
  const load = (u, srgb = true) => new Promise((res, rej) => loader.load(u, (t) => { if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; res(t); }, undefined, rej));
  const [tDay, tNight, tCloud, tSky] = await Promise.all([load("assets/tex/day.jpg"), load("assets/tex/night.jpg"), load("assets/tex/clouds.png"), load("assets/tex/sky.jpg")]);
  const GLOW = glowTex();

  // ================= SET A: Earth =================
  const sA = new THREE.Scene();
  const sky = new THREE.Mesh(new THREE.SphereGeometry(1500, 32, 16), new THREE.MeshBasicMaterial({ map: tSky, side: THREE.BackSide, color: 0x9aa4c0 })); sA.add(sky);
  const sunDir = new THREE.Vector3(1, 0, 0);
  const earthMat = new THREE.ShaderMaterial({
    uniforms: { day: { value: tDay }, night: { value: tNight }, sun: { value: sunDir } },
    vertexShader: "varying vec2 vUv; varying vec3 vN; varying vec3 vP; void main(){ vUv=uv; vN=normalize(mat3(modelMatrix)*normal); vec4 wp=modelMatrix*vec4(position,1.0); vP=wp.xyz; gl_Position=projectionMatrix*viewMatrix*wp; }",
    fragmentShader: `uniform sampler2D day; uniform sampler2D night; uniform vec3 sun; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main(){ vec3 N=normalize(vN); vec3 V=normalize(cameraPosition-vP); float d=dot(N,sun); float lit=smoothstep(-0.12,0.28,d);
        vec3 dc=texture2D(day,vUv).rgb; vec3 nc=texture2D(night,vUv).rgb;
        vec3 col=dc*(0.06+1.25*max(d,0.0))*lit + nc*2.6*(1.0-lit);
        vec3 Hh=normalize(sun+V); float sp=pow(max(dot(N,Hh),0.0),60.0)*smoothstep(0.0,0.2,d)*(dc.b>dc.r*1.25?0.55:0.0); col+=vec3(1.0,0.95,0.85)*sp;
        float fr=pow(1.0-max(dot(N,V),0.0),3.0); col+=vec3(0.25,0.55,1.0)*fr*(0.25+0.9*smoothstep(-0.25,0.4,d));
        gl_FragColor=vec4(col,1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  });
  const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), earthMat); sA.add(earth);
  const cloudMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, uniforms: { map: { value: tCloud }, sun: { value: sunDir } },
    vertexShader: "varying vec2 vUv; varying vec3 vN; void main(){ vUv=uv; vN=normalize(mat3(modelMatrix)*normal); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }",
    fragmentShader: "uniform sampler2D map; uniform vec3 sun; varying vec2 vUv; varying vec3 vN; void main(){ vec4 c=texture2D(map,vUv); float a=max(c.a*c.r,0.0); float d=dot(normalize(vN),sun); float l=0.04+1.1*smoothstep(-0.1,0.5,d); gl_FragColor=vec4(vec3(l),a*0.9);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}",
  });
  const clouds = new THREE.Mesh(new THREE.SphereGeometry(1.012, 96, 64), cloudMat); sA.add(clouds);
  const atmo = new THREE.Mesh(new THREE.SphereGeometry(1.16, 64, 48), new THREE.ShaderMaterial({
    transparent: true, side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false, uniforms: { sun: { value: sunDir } },
    vertexShader: "varying vec3 vN; varying vec3 vP; void main(){ vN=normalize(mat3(modelMatrix)*normal); vec4 wp=modelMatrix*vec4(position,1.0); vP=wp.xyz; gl_Position=projectionMatrix*viewMatrix*wp; }",
    fragmentShader: "uniform vec3 sun; varying vec3 vN; varying vec3 vP; void main(){ vec3 N=normalize(vN); vec3 V=normalize(cameraPosition-vP); float g=clamp(-dot(N,V),0.0,1.0); float edge=pow(clamp(g/0.52,0.0,1.0),3.0)*1.25; float d=dot(N,sun); gl_FragColor=vec4(vec3(0.3,0.6,1.0)*edge*(0.15+0.95*smoothstep(-0.5,0.4,d)),1.0); }",
  })); sA.add(atmo);
  const sunSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex("rgba(255,250,235,1)", "rgba(255,210,140,0.5)"), blending: THREE.AdditiveBlending, depthWrite: false, depthTest: true })); sunSprite.scale.setScalar(160); sA.add(sunSprite);
  // births: ring + beam + glow at four places
  const BIRTHS = [[6.5, 3.4], [30, 31.2], [-1.3, 36.8], [19, 72.8]].map(([la, lo], i) => {
    const g = new THREE.Group(); const p = ll(la, lo, 1.014); g.position.copy(p); g.lookAt(p.clone().multiplyScalar(2));
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.8, 1, 64), new THREE.MeshBasicMaterial({ color: 0xffd27a, transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false }));
    const ring2 = ring.clone(); ring2.material = ring.material.clone();
    const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.012, 1, 12, 1, true), new THREE.MeshBasicMaterial({ color: 0xffe2a8, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); beam.rotation.x = Math.PI / 2;
    const dot = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0xffd9a0, blending: THREE.AdditiveBlending, depthWrite: false }));
    g.add(ring, ring2, beam, dot); sA.add(g); return { g, ring, ring2, beam, dot, t: K.births[i] };
  });
  // lightning flashes on the night side
  const FLT = glowTex("rgba(255,255,255,1)", "rgba(190,215,255,0.22)"); const FL = []; for (let i = 0; i < 64; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: FLT, color: 0xd6e6ff, blending: THREE.AdditiveBlending, depthWrite: false })); s.position.copy(ll(lerp(-32, 44, hash(i * 3 + 1)), lerp(-128, -56, hash(i * 7 + 2)), 1.02)); sA.add(s); FL.push({ s, t: K.strike + hash(i * 11 + 5) * 2.9, d: 0.2 + hash(i * 13) * 0.22, sz: 0.09 + hash(i * 17) * 0.13 }); }
  // orbit path + speed streaks (r5), light trail (r6)
  const orbit = new THREE.Line(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 400 }, (_, i) => { const a = (i / 399 - 0.5) * 0.5; return new THREE.Vector3(Math.sin(a) * 900, 0, 900 - Math.cos(a) * 900); })), new THREE.LineBasicMaterial({ color: 0x6fb6ff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending })); sA.add(orbit);
  const NS = 900, sp = new Float32Array(NS * 6); const streakGeo = new THREE.BufferGeometry(); streakGeo.setAttribute("position", new THREE.BufferAttribute(sp, 3));
  const streaks = new THREE.LineSegments(streakGeo, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending })); streaks.frustumCulled = false; sA.add(streaks);
  const LN = 7 * 160, lp = []; for (let i = 0; i <= LN; i++) { const a = (i / 160) * Math.PI * 2 + 0.6, r = 1.5 + (i / LN) * 0.35; const pr = (i / LN) * 1.5 - 0.75; const x = Math.cos(a) * r, y = Math.sin(a) * r * 0.82, z = Math.sin(a) * r * 0.57; lp.push(new THREE.Vector3(x * Math.cos(pr) + z * Math.sin(pr), y, -x * Math.sin(pr) + z * Math.cos(pr))); }
  const trail = new THREE.Line(new THREE.BufferGeometry().setFromPoints(lp), new THREE.LineBasicMaterial({ color: 0xffe9a0, transparent: true, blending: THREE.AdditiveBlending })); trail.material.color.setRGB(1.9, 1.5, 0.7); trail.frustumCulled = false; sA.add(trail);
  const photon = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: 0xfff1c0, blending: THREE.AdditiveBlending, depthWrite: false })); photon.scale.setScalar(0.42); photon.material.color.setRGB(1.6, 1.4, 1.0); sA.add(photon);

  // ================= SET B: the bee =================
  const sB = new THREE.Scene();
  { const c = document.createElement("canvas"); c.width = 16; c.height = 256; const g = c.getContext("2d"); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "#5aa7e8"); gr.addColorStop(0.55, "#bfe3f5"); gr.addColorStop(0.75, "#f4e9b8"); gr.addColorStop(1, "#7fae4e"); g.fillStyle = gr; g.fillRect(0, 0, 16, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; sB.add(new THREE.Mesh(new THREE.SphereGeometry(400, 24, 16), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide }))); }
  sB.add(new THREE.HemisphereLight(0xfff6e0, 0xc4d6a0, 1.9)); const kB = new THREE.DirectionalLight(0xfff0d0, 3.2); kB.position.set(4, 6, 5); sB.add(kB); const rB = new THREE.DirectionalLight(0x9fd0ff, 2.2); rB.position.set(-5, 2, -6); sB.add(rB);
  for (let i = 0; i < 46; i++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex("rgba(255,255,255,0.9)", "rgba(255,255,255,0.75)"), color: [0xfff3b0, 0x9fd070, 0xffffff, 0xffd98a, 0x7fbf5a][i % 5], transparent: true, opacity: 0.3 + hash(i) * 0.3, depthWrite: false })); s.position.set((hash(i * 3) - 0.5) * 40, (hash(i * 5) - 0.55) * 46, -10 - hash(i * 7) * 24); s.scale.setScalar(4 + hash(i * 9) * 8); sB.add(s); }
  const bee = new THREE.Group(); sB.add(bee);
  { const fl = new THREE.Group(); fl.position.set(-0.6, -3.1, -0.4); fl.rotation.set(-0.5, 0, 0.12); sB.add(fl);
    const pm = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
    for (let i = 0; i < 16; i++) { const p = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 12), pm); const a = (i / 16) * 6.283; p.scale.set(1.25, 0.09, 0.42); p.position.set(Math.cos(a) * 1.75, 0.05 * (i % 2), Math.sin(a) * 1.75); p.rotation.y = -a; fl.add(p); }
    const cc = new THREE.Mesh(new THREE.SphereGeometry(0.95, 32, 20), new THREE.MeshStandardMaterial({ color: 0xf5b90f, roughness: 0.9 })); cc.scale.y = 0.45; fl.add(cc);
    const stm = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 14, 12), new THREE.MeshStandardMaterial({ color: 0x4f8f3a, roughness: 0.8 })); stm.position.y = -7.1; fl.add(stm); }
  { const c = document.createElement("canvas"); c.width = 256; c.height = 64; const g = c.getContext("2d"); g.fillStyle = "#f2b01e"; g.fillRect(0, 0, 256, 64); g.fillStyle = "#17120c"; [28, 84, 140, 196].forEach((x) => g.fillRect(x, 0, 30, 64)); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const ab = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), new THREE.MeshStandardMaterial({ map: t, roughness: 0.55 })); ab.rotation.z = Math.PI / 2; ab.scale.set(0.78, 1.25, 0.78); ab.position.x = -1.05; bee.add(ab);
    const fur = new THREE.MeshStandardMaterial({ color: 0xd99a1c, roughness: 0.95 }), dark = new THREE.MeshStandardMaterial({ color: 0x15110c, roughness: 0.35, metalness: 0.1 });
    const th = new THREE.Mesh(new THREE.SphereGeometry(0.72, 40, 28), fur); th.position.x = 0.35; bee.add(th);
    const hd = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 24), dark); hd.position.set(1.15, -0.05, 0); bee.add(hd);
    [-1, 1].forEach((sd) => { const ey = new THREE.Mesh(new THREE.SphereGeometry(0.24, 24, 16), new THREE.MeshStandardMaterial({ color: 0x050505, roughness: 0.08, metalness: 0.6 })); ey.position.set(1.36, 0.08, sd * 0.3); ey.scale.set(0.8, 1.15, 0.8); bee.add(ey);
      const an = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 0.7, 8), dark); an.position.set(1.55, 0.42, sd * 0.2); an.rotation.z = -0.9; an.rotation.y = sd * 0.3; bee.add(an);
      for (let j = 0; j < 3; j++) { const lg = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.025, 0.8, 8), dark); lg.position.set(0.7 - j * 0.42, -0.75, sd * 0.45); lg.rotation.x = sd * 0.5; lg.rotation.z = 0.25 - j * 0.3; bee.add(lg); } });
    const st = new THREE.Mesh(new THREE.ConeGeometry(0.09, 0.4, 12), dark); st.rotation.z = Math.PI / 2; st.position.x = -2.42; bee.add(st); }
  const wingGeo = new THREE.CircleGeometry(1, 40); wingGeo.scale(0.5, 1.25, 1); wingGeo.translate(0, 1.25, 0);
  const WG = []; [-1, 1].forEach((sd) => { for (let k = 0; k < 7; k++) { const m = new THREE.Mesh(wingGeo, new THREE.MeshBasicMaterial({ color: 0x7fa6cc, transparent: true, opacity: 0.2, side: THREE.DoubleSide, depthWrite: false })); m.position.set(0.3, 0.45, sd * 0.3); bee.add(m); WG.push({ m, sd, k }); } });

  // ================= SET C: blood =================
  const sC = new THREE.Scene(); sC.background = new THREE.Color(0x2a0306); sC.fog = new THREE.Fog(0x4a060b, 8, 70);
  sC.add(new THREE.AmbientLight(0xff8080, 0.55)); const pC = new THREE.PointLight(0xffe2d0, 260, 80, 1.6); sC.add(pC); const dC = new THREE.DirectionalLight(0xff9a8a, 1.6); dC.position.set(2, 5, 4); sC.add(dC);
  { const c = document.createElement("canvas"); c.width = c.height = 256; const g = c.getContext("2d"); g.fillStyle = "#8a1016"; g.fillRect(0, 0, 256, 256); for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(${40 + Math.floor(hash(i) * 120)},0,0,${0.12 + hash(i * 3) * 0.2})`; g.beginPath(); g.arc(hash(i * 5) * 256, hash(i * 7) * 256, 4 + hash(i * 9) * 16, 0, 7); g.fill(); } const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 14); t.colorSpace = THREE.SRGBColorSpace;
    const tun = new THREE.Mesh(new THREE.CylinderGeometry(6.2, 6.2, 260, 48, 1, true), new THREE.MeshStandardMaterial({ map: t, side: THREE.BackSide, roughness: 0.7 })); tun.rotation.x = Math.PI / 2; tun.position.z = -90; sC.add(tun); sC.userData.tunTex = t; }
  const prof = []; for (let i = 0; i <= 28; i++) { const a = (i / 28) * Math.PI, r = Math.sin(a), y = Math.cos(a) * (0.13 + 0.22 * r * r * r); prof.push(new THREE.Vector2(r, y)); }
  const NC = 340, cells = new THREE.InstancedMesh(new THREE.LatheGeometry(prof, 40), new THREE.MeshPhongMaterial({ color: 0xc81a22, specular: 0xffb0a0, shininess: 55 }), NC); cells.frustumCulled = false; sC.add(cells);
  const CD = Array.from({ length: NC }, (_, i) => { const a = hash(i * 3) * 6.283, r = 1.0 + Math.sqrt(hash(i * 5)) * 4.4; return { x: Math.cos(a) * r, y: Math.sin(a) * r, z: hash(i * 7) * 110, s: 0.55 + hash(i * 9) * 0.5, rx: hash(i * 11) * 6, ry: hash(i * 13) * 6, w: 0.4 + hash(i * 15) * 1.4, born: hash(i * 17) }; });
  const M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), V3 = new THREE.Vector3(), SC3 = new THREE.Vector3();

  // ================= SET E: the Sun =================
  const sE = new THREE.Scene(); sE.background = new THREE.Color(0x030102);
  const NOISE = `vec3 mod289(vec3 x){return x-floor(x*(1.0/289.0))*289.0;} vec4 mod289(vec4 x){return x-floor(x*(1.0/289.0))*289.0;} vec4 permute(vec4 x){return mod289(((x*34.0)+1.0)*x);} vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}
    float snoise(vec3 v){ const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0); vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx); vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy); vec3 x1=x0-i1+C.xxx; vec3 x2=x0-i2+C.yyy; vec3 x3=x0-D.yyy; i=mod289(i);
      vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0)); float n_=0.142857142857; vec3 ns=n_*D.wyz-D.xzx; vec4 j=p-49.0*floor(p*ns.z*ns.z); vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_); vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y); vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw); vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0)); vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww; vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w); vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3))); p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w; vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m; return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3))); }
    float fbm(vec3 p){ float f=0.0, a=0.5; for(int i=0;i<5;i++){ f+=a*snoise(p); p*=2.02; a*=0.5; } return f; }`;
  const sunMat = new THREE.ShaderMaterial({ uniforms: { time: { value: 0 } },
    vertexShader: "varying vec3 vP; varying vec3 vN; varying vec3 vW; void main(){ vP=position; vN=normalize(mat3(modelMatrix)*normal); vec4 wp=modelMatrix*vec4(position,1.0); vW=wp.xyz; gl_Position=projectionMatrix*viewMatrix*wp; }",
    fragmentShader: NOISE + "uniform float time; varying vec3 vP; varying vec3 vN; varying vec3 vW; void main(){ vec3 p=normalize(vP); float n=fbm(p*2.6+vec3(0.0,time*0.12,time*0.07)); float c=fbm(p*7.0+vec3(time*0.2,0.0,n)); float v=0.5+0.5*n+0.28*c; vec3 col=mix(vec3(0.75,0.12,0.0),vec3(1.0,0.55,0.05),smoothstep(0.2,0.6,v)); col=mix(col,vec3(1.0,0.95,0.6),smoothstep(0.6,0.95,v)); float mu=max(dot(normalize(vN),normalize(cameraPosition-vW)),0.0); col*=0.55+0.75*pow(mu,0.5); col+=vec3(1.0,0.5,0.1)*pow(1.0-mu,3.0)*1.2; gl_FragColor=vec4(col*0.82,1.0); }" });
  const sun = new THREE.Mesh(new THREE.SphereGeometry(3, 96, 64), sunMat); sE.add(sun);
  const corona = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex("rgba(255,200,90,1)", "rgba(255,120,20,0.45)"), blending: THREE.AdditiveBlending, depthWrite: false })); corona.scale.setScalar(12); corona.material.opacity = 0.55; sE.add(corona);
  const NP = 2600, pp = new Float32Array(NP * 3), pcol = new Float32Array(NP * 3); const pGeo = new THREE.BufferGeometry(); pGeo.setAttribute("position", new THREE.BufferAttribute(pp, 3)); pGeo.setAttribute("color", new THREE.BufferAttribute(pcol, 3));
  const parts = new THREE.Points(pGeo, new THREE.PointsMaterial({ size: 0.22, map: GLOW, vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true })); parts.frustumCulled = false; sE.add(parts);
  const PD = Array.from({ length: NP }, (_, i) => { const u = hash(i * 3) * 2 - 1, a = hash(i * 5) * 6.283, s = Math.sqrt(1 - u * u); return { d: new THREE.Vector3(s * Math.cos(a), u, s * Math.sin(a)), ph: hash(i * 7), sp: 0.25 + hash(i * 9) * 0.5 }; });
  { const st = new Float32Array(1500 * 3); for (let i = 0; i < 1500; i++) { const u = hash(i * 21) * 2 - 1, a = hash(i * 23) * 6.283, s = Math.sqrt(1 - u * u); st[i * 3] = s * Math.cos(a) * 300; st[i * 3 + 1] = u * 300; st[i * 3 + 2] = s * Math.sin(a) * 300; } const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.BufferAttribute(st, 3)); sE.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.1, sizeAttenuation: true, transparent: true, opacity: 0.7 }))); }

  // ================= post =================
  const composer = new EffectComposer(renderer); composer.setSize(W, H);
  const rp = new RenderPass(sA, cam); composer.addPass(rp);
  const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.7, 0.55, 0.8); composer.addPass(bloom);
  composer.addPass(new OutputPass());
  await renderer.compileAsync(sA, cam); await renderer.compileAsync(sB, cam); await renderer.compileAsync(sC, cam); await renderer.compileAsync(sE, cam);

  const T = K.at; const up = new THREE.Vector3(0, 1, 0);
  function earthCam(lat, lon, dist, tgtLat, tgtLon, tgtR, roll = 0) { cam.position.copy(ll(lat, lon, dist)); cam.up.set(0, 1, 0); cam.lookAt(tgtR ? ll(tgtLat, tgtLon, tgtR) : new THREE.Vector3()); cam.rotateZ(roll); }
  function setSun(lat, lon) { sunDir.copy(ll(lat, lon, 1)); sunSprite.position.copy(sunDir).multiplyScalar(900); }

  function render(t) {
    let scene = sA; cam.fov = 38; bloom.strength = 0.7; bloom.threshold = 0.8; renderer.toneMappingExposure = 1.05;
    if (t < T.bee || (t >= T.fly && t < T.sun) || t >= T.end) {
      // ---------- Earth set
      clouds.rotation.y = t * 0.006; orbit.material.opacity = 0; streaks.material.opacity = 0; trail.visible = false; photon.visible = false; sunSprite.visible = true; sunSprite.scale.setScalar(160);
      BIRTHS.forEach((b) => { const u = (t - b.t) / 1.5; const on = u > 0 && u < 1 && t < T.bee; b.g.visible = on; if (on) { const e = 1 - Math.pow(1 - u, 3); b.ring.scale.setScalar(0.02 + e * 0.16); b.ring.material.opacity = (1 - u) * 1.0; const u2 = Math.max(0, u - 0.18) / 0.82, e2 = 1 - Math.pow(1 - u2, 3); b.ring2.scale.setScalar(0.02 + e2 * 0.1); b.ring2.material.opacity = u2 > 0 ? (1 - u2) * 0.8 : 0; const bh = Math.min(1, u * 5) * 0.34; b.beam.scale.set(1, bh, 1); b.beam.position.z = bh / 2; b.beam.material.opacity = Math.min(1, u * 6) * (1 - u * u); b.dot.scale.setScalar(0.1 + 0.12 * Math.sin(Math.min(1, u * 3) * Math.PI)); b.dot.material.opacity = 1 - u * u; } });
      FL.forEach((f) => { const u = (t - f.t) / f.d; const on = u > 0 && u < 1 && t < T.bee; f.s.visible = on; if (on) { const fl = (u < 0.25 ? u / 0.25 : 1 - (u - 0.25) / 0.75) * (0.6 + 0.4 * Math.sin(u * 40)); f.s.scale.setScalar(f.sz * (1.0 + fl * 2.2)); f.s.material.opacity = Math.min(1, fl * 1.8); } });
      if (t < T.bee) {
        // r1: sunrise close over the terminator, pull back; r2: glide to the night side
        const a = ss(0, T.strikeCam, t), b = ss(T.strikeCam - 0.6, T.strikeCam + 2.6, t);
        setSun(8, 62 - t * 0.6);
        const lon = lerp(-34, 36, 1 - Math.pow(1 - Math.min(1, t / T.strikeCam), 2.2)) + b * -128, lat = lerp(22, 12, a) + b * 8;
        const dist = lerp(1.5, 5.6, ss(0.0, 3.4, t)) - b * 0.7 + ss(T.bee - 0.9, T.bee, t) * -2.6;
        earthCam(lat, lon, dist, lerp(14, 6, a), lon + lerp(16, 0, ss(0, 2.6, t)), lerp(0.9, 0, ss(0.4, 2.8, t)), lerp(0.25, 0, ss(0, 3, t)));
      } else if (t < T.sun) {
        const u = t - T.fly, k = ss(T.light - 0.9, T.light + 0.5, t);
        sunDir.set(-0.45, 0.45, 0.78).normalize(); sunSprite.position.copy(sunDir).multiplyScalar(900); sunSprite.visible = false;
        // Earth races along its orbit: path + streaks fly past (-x), camera chases
        orbit.material.opacity = 0.55 * (1 - k); streaks.material.opacity = 1.0 * (1 - k) * ss(T.fly, T.fly + 0.5, t);
        const spd = 26;
        for (let i = 0; i < NS; i++) { const x0 = hash(i * 3) * 60 - 30, y = (hash(i * 5) - 0.5) * 16, z = (hash(i * 7) - 0.5) * 20 - 1; let x = ((x0 - u * spd * (0.6 + hash(i * 9))) % 60 + 90) % 60 - 30; const len = 1.2 + hash(i * 11) * 3.2; sp[i * 6] = x; sp[i * 6 + 1] = y; sp[i * 6 + 2] = z; sp[i * 6 + 3] = x + len; sp[i * 6 + 4] = y; sp[i * 6 + 5] = z; if (Math.abs(y) < 1.3 && Math.abs(z) < 1.3) { sp[i * 6 + 1] = sp[i * 6 + 4] = y + 2.2; } }
        streakGeo.attributes.position.needsUpdate = true;
        earth.rotation.y = 0; const p0 = new THREE.Vector3(-4.6 + u * 0.35, 1.25 - u * 0.1, 3.4), p1 = new THREE.Vector3(0.8, 1.6, 11.6);
        cam.position.lerpVectors(p0, p1, k); cam.up.set(0, 1, 0); cam.lookAt(new THREE.Vector3(lerp(1.1, 0, k), 0, 0)); cam.rotateZ(lerp(-0.12, 0, k));
        // light laps the planet seven times
        const lu = Math.min(1, Math.max(0, (t - K.lapStart) / (K.lap * 7)));
        trail.visible = lu > 0; photon.visible = lu > 0 && lu < 1; trail.geometry.setDrawRange(0, Math.floor(lu * LN) + 1); trail.material.opacity = 0.95; if (lu > 0) { bloom.strength = 0.75; bloom.threshold = 0.78; } if (lu > 0) photon.position.copy(lp[Math.floor(lu * LN)]);
        cam.position.multiplyScalar(1 + ss(T.sun - 0.7, T.sun, t) * -0.5);
      } else {
        // finale: sunrise over the limb, then a slow pull back
        const u = t - T.end; setSun(4, 196 - u * 3.4);
        const lon = 96 - u * 1.2, dist = lerp(1.9, 6.0, ss(0, 7.5, u));
        earthCam(16 - u * 0.6, lon, dist, 10, lon + lerp(34, 0, ss(0, 6, u)), lerp(1.0, 0, ss(0.5, 6.5, u)), lerp(0.18, 0, ss(0, 5, u)));
        sunSprite.scale.setScalar(240); bloom.strength = 0.95;
      }
      earthMat.uniforms.sun.value = sunDir; cam.updateProjectionMatrix();
    } else if (t < T.blood) {
      // ---------- bee
      scene = sB; const u = t - T.bee, d = T.blood - T.bee; bloom.strength = 0.25; bloom.threshold = 0.95; renderer.toneMappingExposure = 1.0;
      bee.position.set(Math.sin(u * 1.3) * 0.25, Math.sin(u * 2.1) * 0.22, 0); bee.rotation.set(Math.sin(u * 1.7) * 0.06, 0.35 + Math.sin(u * 0.9) * 0.12, -0.12 + Math.sin(u * 2.3) * 0.05);
      WG.forEach(({ m, sd, k }) => { const ph = u * 200 * 0.21 + k * 0.42; const sw = Math.sin(ph) * 0.95; m.rotation.set(sd * (0.75 + sw * 0.6), 0, -0.3);  });
      const a = lerp(0.25, 1.05, ss(0, d, u)), r = lerp(15.5, 11, ss(0, d * 0.8, u)) + ss(d - 0.6, d, u) * -6;
      cam.position.set(Math.sin(a) * r + 0.3, 0.9 - u * 0.12, Math.cos(a) * r); cam.up.set(0, 1, 0); cam.lookAt(-0.3, 0.1, 0); cam.fov = 34; cam.updateProjectionMatrix();
    } else if (t < T.fly) {
      // ---------- blood
      scene = sC; const u = t - T.blood, d = T.fly - T.blood; bloom.strength = 0.35; bloom.threshold = 0.85;
      const flow = u * 13;
      for (let i = 0; i < NC; i++) { const c = CD[i]; const z = ((c.z + flow * (0.8 + c.w * 0.25)) % 110) - 104; const grow = ss(c.born * 1.8, c.born * 1.8 + 0.35, u); E.set(c.rx + u * c.w, c.ry + u * c.w * 0.7, 0); Q.setFromEuler(E); V3.set(c.x + Math.sin(u + i) * 0.15, c.y + Math.cos(u * 0.8 + i) * 0.15, z); SC3.setScalar(c.s * grow + 0.0001); M4.compose(V3, Q, SC3); cells.setMatrixAt(i, M4); }
      cells.instanceMatrix.needsUpdate = true; sC.userData.tunTex.offset.y = -u * 0.5;
      cam.position.set(Math.sin(u * 0.7) * 0.5, Math.cos(u * 0.5) * 0.35, 4 - u * 0.4); cam.up.set(Math.sin(u * 0.35) * 0.18, 1, 0); cam.lookAt(Math.sin(u * 0.4) * 0.6, 0, -30); pC.position.copy(cam.position); cam.fov = 58 - ss(0, 1.2, u) * 8 + ss(d - 0.5, d, u) * 30; cam.updateProjectionMatrix();
    } else {
      // ---------- sun
      scene = sE; const u = t - T.sun, d = T.end - T.sun; bloom.strength = 0.55; bloom.threshold = 0.82; renderer.toneMappingExposure = 0.9; sunMat.uniforms.time.value = 20 + u * 2.2;
      for (let i = 0; i < NP; i++) { const p = PD[i]; const f = (p.ph + u * p.sp * 0.6) % 1; const r = 3.02 + f * f * 9; pp[i * 3] = p.d.x * r; pp[i * 3 + 1] = p.d.y * r; pp[i * 3 + 2] = p.d.z * r; const b = (1 - f) * (f < 0.06 ? f / 0.06 : 1); pcol[i * 3] = b; pcol[i * 3 + 1] = b * (0.55 - f * 0.3); pcol[i * 3 + 2] = b * 0.12; }
      pGeo.attributes.position.needsUpdate = true; pGeo.attributes.color.needsUpdate = true;
      const a = -0.5 + u * 0.09, r = lerp(22, 10.5, ss(0, d * 0.85, u)) + ss(d - 0.6, d, u) * 9;
      cam.position.set(Math.sin(a) * r, 1.2 - u * 0.2, Math.cos(a) * r); cam.up.set(0.12, 1, 0); cam.lookAt(0, 0.4, 0); cam.fov = 40; cam.updateProjectionMatrix();
    }
    rp.scene = scene; composer.render();
  }
  return { render };
}
