// GPS film — two 3D sets on a transparent canvas: a dotted globe with the GPS constellation (to scale), and a cube wave.
// render(t) is a pure function of time (seek-safe).
import * as THREE from "three";

const D2R = Math.PI / 180;
const ss = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * x * (x * (x * 6 - 15) + 10); };
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const ORANGE = new THREE.Color("#ff5a1f"), WHITE = new THREE.Color("#f3efe8");

export async function init(canvas, K) {
  const W = canvas.width, H = canvas.height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.setClearColor(0x000000, 0);
  const cam = new THREE.PerspectiveCamera(36, W / H, 0.1, 500);
  const img = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = "assets/tex/water.jpg"; });
  const mc = document.createElement("canvas"); mc.width = 512; mc.height = 256; const mg = mc.getContext("2d"); mg.drawImage(img, 0, 0, 512, 256); const mask = mg.getImageData(0, 0, 512, 256).data;
  const isLand = (lat, lon) => { const x = Math.floor(((lon + 180) / 360) * 511), y = Math.floor(((90 - lat) / 180) * 255); return mask[(y * 512 + x) * 4] < 110; };

  // ---------- set G: dotted globe + constellation
  const sG = new THREE.Scene(); sG.add(new THREE.AmbientLight(0xffffff, 1.4)); const dl = new THREE.DirectionalLight(0xffffff, 2.2); dl.position.set(3, 4, 6); sG.add(dl);
  const globe = new THREE.Group(); sG.add(globe);
  const pts = []; const N = 9000;
  for (let i = 0; i < N; i++) { const y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = i * 2.399963; const lat = Math.asin(y) / D2R, lon = (((th / D2R) % 360) + 540) % 360 - 180; if (isLand(lat, lon)) pts.push(new THREE.Vector3(Math.cos(th) * r, y, Math.sin(th) * r)); }
  const dots = new THREE.InstancedMesh(new THREE.BoxGeometry(0.017, 0.017, 0.017), new THREE.MeshBasicMaterial({ color: WHITE }), pts.length);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S3 = new THREE.Vector3(1, 1, 1), ZP = new THREE.Vector3(0, 0, 1);
  pts.forEach((p, i) => { Q.setFromUnitVectors(ZP, p); M.compose(p, Q, S3); dots.setMatrixAt(i, M); }); globe.add(dots);
  globe.add(new THREE.Mesh(new THREE.SphereGeometry(0.985, 48, 32), new THREE.MeshBasicMaterial({ color: 0x1b1917 })));
  globe.add(new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(0.99, 18, 12)), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.07 })));
  const RS = 4.17, SATS = [], rings = [];
  for (let p = 0; p < 6; p++) {
    const plane = new THREE.Group(); plane.rotation.y = (p / 6) * Math.PI * 2; const tilt = new THREE.Group(); tilt.rotation.x = 55 * D2R; plane.add(tilt); sG.add(plane);
    const ring = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 160 }, (_, i) => new THREE.Vector3(Math.cos((i / 160) * 6.283) * RS, 0, Math.sin((i / 160) * 6.283) * RS))), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 })); tilt.add(ring); rings.push(ring);
    for (let k = 0; k < 5; k++) { const g = new THREE.Group(); const body = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.12), new THREE.MeshStandardMaterial({ color: ORANGE, roughness: 0.4, emissive: ORANGE, emissiveIntensity: 0.55 }));
      const pan = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.02, 0.1), new THREE.MeshStandardMaterial({ color: WHITE, roughness: 0.5 })); g.add(body, pan);
      const pulse = new THREE.Mesh(new THREE.RingGeometry(0.95, 1, 48), new THREE.MeshBasicMaterial({ color: ORANGE, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false })); g.add(pulse);
      tilt.add(g); SATS.push({ g, pulse, a0: (k / 5) * 6.283 + p * 0.63, i: p * 5 + k }); }
  }
  // ---------- set V: cube wave
  const sV = new THREE.Scene(); sV.add(new THREE.AmbientLight(0xffffff, 0.75)); const dv = new THREE.DirectionalLight(0xffffff, 1.7); dv.position.set(-4, 9, 5); sV.add(dv); const dv2 = new THREE.DirectionalLight(0xff8a4a, 0.5); dv2.position.set(6, 3, -4); sV.add(dv2);
  const GN = 30, cubes = new THREE.InstancedMesh(new THREE.BoxGeometry(0.9, 1, 0.9), new THREE.MeshStandardMaterial({ roughness: 0.55 }), GN * GN); sV.add(cubes); const col = new THREE.Color();
  const pin = new THREE.Group(); pin.scale.setScalar(1.6); const pb = new THREE.Mesh(new THREE.SphereGeometry(1.0, 32, 24), new THREE.MeshStandardMaterial({ color: WHITE, roughness: 0.3, emissive: WHITE, emissiveIntensity: 0.35 })); pb.position.y = 2.6; const ps = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 2.6, 12), new THREE.MeshStandardMaterial({ color: WHITE })); ps.position.y = 1.3; pin.add(pb, ps); sV.add(pin);
  const tgt = new THREE.Mesh(new THREE.TorusGeometry(1.8, 0.12, 12, 64), new THREE.MeshBasicMaterial({ color: WHITE })); tgt.rotation.x = Math.PI / 2; sV.add(tgt);
  const hgt = (x, z, u) => 2.6 + 2.2 * Math.sin(x * 0.42 + u * 2.2) * Math.cos(z * 0.36 - u * 1.6) + 1.1 * Math.sin((x + z) * 0.3 + u * 1.1);

  function render(t) {
    const T = K.at;
    if (t >= T.gA && t < T.gB) {
      const u = t - T.gA, d = T.gB - T.gA; globe.rotation.y = -1.9 + u * 0.22;
      const rev = ss(0.2, 2.2, u);
      rings.forEach((r, i) => { r.material.opacity = 0.22 * ss(0.5 + i * 0.12, 1.6 + i * 0.12, u); });
      SATS.forEach((s) => { const a = s.a0 + u * 0.16; s.g.position.set(Math.cos(a) * RS, 0, Math.sin(a) * RS); s.g.rotation.y = -a; const pop = ss(0.7 + s.i * 0.045, 1.0 + s.i * 0.045, u); s.g.scale.setScalar(0.001 + pop * (1 + 0.5 * Math.sin(Math.min(1, (u - 0.7 - s.i * 0.045) / 0.5) * Math.PI) * (pop < 1 ? 1 : 0)));
        const ph = ((u - K.shout + s.i * 0.21) % 1.1 + 1.1) % 1.1 / 1.1; const on = u > K.shout - 0.1; s.pulse.scale.setScalar(0.15 + ph * 0.75); s.pulse.material.opacity = on ? (1 - ph) * 0.7 : 0; s.pulse.lookAt(cam.position); });
      const dist = lerp(3.4, 24, rev) - ss(d - 0.5, d, u) * 6, el = lerp(0.1, 0.42, rev), az = 0.3 + u * 0.1;
      cam.position.set(Math.sin(az) * Math.cos(el) * dist, Math.sin(el) * dist, Math.cos(az) * Math.cos(el) * dist); cam.up.set(0, 1, 0); cam.lookAt(0, lerp(0, -0.6, rev), 0); cam.fov = 36; cam.updateProjectionMatrix();
      renderer.render(sG, cam);
    } else if (t >= T.vA && t < T.vB) {
      const u = t - T.vA, d = T.vB - T.vA; const miss = ss(K.miss, K.miss + 0.55, t);
      for (let i = 0; i < GN; i++) for (let j = 0; j < GN; j++) { const x = i - GN / 2 + 0.5, z = j - GN / 2 + 0.5; const edge = Math.max(0, 1 - Math.hypot(x, z) / (GN * 0.52)); const h = Math.max(0.12, hgt(x, z, u) * Math.min(1, edge * 2.4) * ss(0, 0.9, u - Math.hypot(x, z) * 0.03)); V.set(x, h / 2, z); S3.set(1, h, 1); Q.identity(); M.compose(V, Q, S3); cubes.setMatrixAt(i * GN + j, M); col.copy(WHITE).lerp(ORANGE, Math.min(1, Math.max(0, (h - 2.2) / 2.4))); cubes.setColorAt(i * GN + j, col); }
      cubes.instanceMatrix.needsUpdate = true; cubes.instanceColor.needsUpdate = true; S3.set(1, 1, 1);
      const tx = 0, tz = 0, mx = lerp(0, 8.5, miss), mz = lerp(0, -5.5, miss);
      tgt.position.set(tx, hgt(tx, tz, u) + 0.25, tz); pin.position.set(mx, hgt(mx, mz, u) + Math.sin(miss * Math.PI) * 5, mz); pb.material.color.copy(WHITE).lerp(ORANGE, miss); pb.material.emissive.copy(pb.material.color);
      const az = 0.7 + u * 0.12, dist = lerp(150, 128, ss(0, d, u));
      cam.position.set(Math.sin(az) * dist * 0.72, dist * 0.62, Math.cos(az) * dist * 0.72); cam.up.set(0, 1, 0); cam.lookAt(1.5, -1.5, -1); cam.fov = 30; cam.updateProjectionMatrix();
      renderer.render(sV, cam);
    } else { renderer.clear(); }
  }
  return { render };
}
