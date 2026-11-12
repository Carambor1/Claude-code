// "First try" film — one glossy metaball blob on a transparent canvas. Lumpy and restless at first, a clean sphere at the end.
import * as THREE from "three";
import { MarchingCubes } from "three/examples/jsm/objects/MarchingCubes.js";
const ss = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * x * (x * (x * 6 - 15) + 10); };
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
export async function init(canvas, K) {
  const W = canvas.width, H = canvas.height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.setClearColor(0x000000, 0);
  const cam = new THREE.PerspectiveCamera(30, W / H, 0.1, 100); cam.position.set(0, 0, 9); cam.lookAt(0, 0, 0);
  const scene = new THREE.Scene();
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const k = new THREE.DirectionalLight(0xffffff, 2.4); k.position.set(-3, 5, 6); scene.add(k);
  const r = new THREE.DirectionalLight(0xffd0b0, 1.6); r.position.set(5, -2, 3); scene.add(r);
  const b = new THREE.PointLight(0xffffff, 40, 30); b.position.set(2, 3, 5); scene.add(b);
  const mat = new THREE.MeshPhongMaterial({ color: 0xff4a12, specular: 0xffffff, shininess: 90, emissive: 0x5a1200 });
  const mc = new MarchingCubes(56, mat, false, false, 90000); mc.isolation = 80; mc.scale.setScalar(2.1); scene.add(mc);
  const NB = 9;
  function blob(u, smooth) {
    mc.reset();
    const rough = 1 - smooth;
    for (let i = 0; i < NB; i++) {
      const a = u * (0.9 + hash(i) * 1.3) + i * 2.1, c = u * (0.7 + hash(i * 3) * 1.1) + i * 1.3;
      const rad = (0.06 + 0.11 * hash(i * 7)) * rough;
      const x = 0.5 + Math.sin(a) * Math.cos(c * 0.7) * rad, y = 0.5 + Math.cos(a * 0.8 + i) * rad * 1.1, z = 0.5 + Math.sin(c) * rad;
      mc.addBall(x, y, z, lerp(0.34 + 0.24 * hash(i * 11), 0.42, smooth), 12);
    }
    mc.update();
  }
  function render(t) {
    const T = K.at; let vis = 0, smooth = 0, sc = 1, yy = 0;
    if (t < T.a1) { vis = 1; smooth = 0; sc = lerp(0.2, 1, ss(0, 0.7, t)) * (1 - ss(T.a1 - 0.3, T.a1, t) * 0.8); yy = -0.75; }
    else if (t >= T.b0) { vis = 1; smooth = ss(K.today - 0.25, K.today + 0.55, t); sc = lerp(0.2, 1.05, ss(T.b0, T.b0 + 0.6, t)) + smooth * 0.08 * Math.sin((t - K.today) * 5) * Math.exp(-(t - K.today) * 2.5); yy = -0.7; }
    if (!vis) { renderer.clear(); return; }
    blob(t * 1.5, smooth); mc.scale.setScalar(2.3 * sc); mc.position.y = yy; mc.rotation.y = t * 0.5; mc.rotation.x = Math.sin(t * 0.7) * 0.2 * (1 - smooth);
    mat.color.setHex(0xff4a12); renderer.render(scene, cam);
  }
  return { render };
}
