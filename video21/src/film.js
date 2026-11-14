// "I Carry the King" — low-poly 3D devlog teaser. One renderer, one rig (king + sedan chair + four carriers) moved between
// small sets (meadow, dungeon wagon, rope bridge, castle mountain). render(t) is a pure function of time (seek-safe).
import * as THREE from "three";

const ss = (a, b, t) => { const x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); };
const lerp = (a, b, x) => a + (b - a) * x;
const hash = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: 0.85, ...o });
const box = (w, h, d, c) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M(c));
const ball = (r, c, d = 1) => new THREE.Mesh(new THREE.IcosahedronGeometry(r, d), M(c));
const cyl = (r1, r2, h, c, s = 8) => new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, s), M(c));
const cone = (r, h, c, s = 6) => new THREE.Mesh(new THREE.ConeGeometry(r, h, s), M(c));
const at = (m, x, y, z) => { m.position.set(x, y, z); return m; };
const SKIN = 0xf2c9a0, GOLD = 0xf2b632, COLS = [0xe2463f, 0x3f7fe2, 0x4fbf5a, 0xf2c530];

export async function init(canvas, K) {
  const W = canvas.width, H = canvas.height;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
  const scene = new THREE.Scene(); const SKY = new THREE.Color(0x9fd4ff), DUSK = new THREE.Color(0xffc98a);
  scene.background = SKY.clone(); scene.fog = new THREE.Fog(0xcfe9ff, 40, 190);
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 600);
  const hemi = new THREE.HemisphereLight(0xdff1ff, 0x8fbf6a, 1.25); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffe7bd, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 80 }); scene.add(sun, sun.target);

  // ---------- characters
  function carrier(c) {
    const g = new THREE.Group(); const body = at(cyl(0.3, 0.4, 0.75, c), 0, 0.82, 0); const head = at(ball(0.36, SKIN), 0, 1.5, 0);
    const e1 = at(ball(0.05, 0x1a1a1a, 0), -0.13, 1.55, 0.31), e2 = at(ball(0.05, 0x1a1a1a, 0), 0.13, 1.55, 0.31);
    const l1 = at(cyl(0.09, 0.09, 0.5, 0x3a2c22, 6), -0.15, 0.25, 0), l2 = at(cyl(0.09, 0.09, 0.5, 0x3a2c22, 6), 0.15, 0.25, 0);
    const a1 = at(cyl(0.07, 0.07, 0.55, c, 6), -0.36, 1.12, 0), a2 = at(cyl(0.07, 0.07, 0.55, c, 6), 0.36, 1.12, 0);
    g.add(body, head, e1, e2, l1, l2, a1, a2); g.traverse((o) => { o.castShadow = true; }); g.userData = { l1, l2, a1, a2, head }; return g;
  }
  function walk(g, ph, amt = 1, arms = true) { const u = g.userData; u.l1.rotation.x = Math.sin(ph) * 0.8 * amt; u.l2.rotation.x = -Math.sin(ph) * 0.8 * amt; if (arms) { const inner = g.userData.home[0] > 0 ? u.a1 : u.a2, outer = g.userData.home[0] > 0 ? u.a2 : u.a1, sgn = g.userData.home[0] > 0 ? 1 : -1; inner.rotation.z = sgn * 2.2; inner.position.set(-sgn * 0.42, 1.36, 0); outer.rotation.z = 0; outer.position.set(sgn * 0.36, 1.12, 0); } }
  const king = new THREE.Group();
  const robe = at(ball(0.95, 0xb3202a, 2), 0, 0.85, 0); robe.scale.set(1.08, 0.92, 1.0);
  const fur = at(new THREE.Mesh(new THREE.TorusGeometry(0.8, 0.13, 6, 14), M(0xfdf6ec)), 0, 1.38, 0); fur.rotation.x = Math.PI / 2;
  const khead = at(ball(0.46, SKIN, 2), 0, 1.95, 0.05); const face = khead.material;
  const crown = new THREE.Group(); crown.add(at(cyl(0.36, 0.33, 0.24, GOLD, 10), 0, 0, 0)); for (let i = 0; i < 6; i++) { const a = (i / 6) * 6.283; crown.add(at(cone(0.09, 0.26, GOLD, 4), Math.cos(a) * 0.3, 0.24, Math.sin(a) * 0.3)); } crown.add(at(ball(0.07, 0xe2463f, 0), 0, 0.02, 0.35)); crown.position.set(0, 2.42, 0.05); crown.scale.setScalar(1.25);
  const ke1 = at(ball(0.055, 0x1a1a1a, 0), -0.17, 2.0, 0.46), ke2 = at(ball(0.055, 0x1a1a1a, 0), 0.17, 2.0, 0.46);
  const br1 = at(box(0.2, 0.05, 0.05, 0x3a2416), -0.17, 2.13, 0.45), br2 = at(box(0.2, 0.05, 0.05, 0x3a2416), 0.17, 2.13, 0.45);
  const must = at(box(0.36, 0.07, 0.06, 0x3a2416), 0, 1.82, 0.48); const mouth = at(box(0.16, 0.05, 0.05, 0x7a1f1f), 0, 1.72, 0.47);
  const kArm = new THREE.Group(); kArm.position.set(0.82, 1.35, 0.2); kArm.add(at(cyl(0.12, 0.1, 0.7, 0xb3202a, 6), 0, -0.3, 0)); const grapes = new THREE.Group(); for (let i = 0; i < 9; i++) grapes.add(at(ball(0.09, 0x7a3fb0, 0), (hash(i) - 0.5) * 0.22, -0.72 - (i % 3) * 0.1, (hash(i * 3) - 0.5) * 0.22)); kArm.add(grapes);
  const kArm2 = new THREE.Group(); kArm2.position.set(-0.82, 1.35, 0.2); kArm2.add(at(cyl(0.12, 0.1, 0.7, 0xb3202a, 6), 0, -0.3, 0));
  king.add(robe, fur, khead, crown, ke1, ke2, br1, br2, must, mouth, kArm, kArm2); king.traverse((o) => { o.castShadow = true; });
  const steam = []; for (let i = 0; i < 6; i++) { const s = ball(0.16, 0xffffff, 0); s.material.transparent = true; king.add(s); steam.push(s); }
  const sedan = new THREE.Group(); const plat = at(box(2.3, 0.18, 1.9, GOLD), 0, 0, 0); const cush = at(box(1.9, 0.16, 1.5, 0x8e1b2a), 0, 0.17, 0);
  sedan.add(plat, cush, at(cyl(0.07, 0.07, 5.4, 0x8a5a2b, 6), -1.05, -0.05, 0), at(cyl(0.07, 0.07, 5.4, 0x8a5a2b, 6), 1.05, -0.05, 0));
  sedan.children[2].rotation.x = sedan.children[3].rotation.x = Math.PI / 2;
  for (const [x, z] of [[-1.05, -0.85], [1.05, -0.85], [-1.05, 0.85], [1.05, 0.85]]) sedan.add(at(cyl(0.05, 0.05, 2.7, GOLD, 6), x, 1.35, z));
  const roof = at(cone(1.75, 0.8, 0x8e1b2a, 4), 0, 3.1, 0); roof.rotation.y = Math.PI / 4; sedan.add(roof, at(ball(0.14, GOLD, 0), 0, 3.6, 0)); sedan.traverse((o) => { o.castShadow = true; });
  const rig = new THREE.Group(); scene.add(rig); const CAR = COLS.map((c, i) => { const g = carrier(c); g.userData.home = [i % 2 ? 1.5 : -1.5, 0, i < 2 ? 2.15 : -2.15]; rig.add(g); return g; });
  const chair = new THREE.Group(); chair.position.y = 1.5; chair.add(sedan, king); king.position.y = 0.2; rig.add(chair);

  // ---------- world
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), M(0x86c35c)); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
  const path = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 900), M(0xe2c98f)); path.rotation.x = -Math.PI / 2; path.position.y = 0.01; path.receiveShadow = true; scene.add(path);
  const trees = []; for (let i = 0; i < 26; i++) { const g = new THREE.Group(); const sc = 0.9 + hash(i) * 1.1; g.add(at(cyl(0.16, 0.2, 1.2, 0x7a5230, 5), 0, 0.6, 0), at(cone(1.0, 2.2, i % 3 ? 0x4f9a48 : 0x3f8a52, 6), 0, 2.2, 0), at(cone(0.75, 1.6, 0x5fae52, 6), 0, 3.3, 0)); g.scale.setScalar(sc); g.traverse((o) => { o.castShadow = true; }); g.userData = { x: (i % 2 ? 1 : -1) * (12 + hash(i * 3) * 16), z0: hash(i * 7) * 120 }; scene.add(g); trees.push(g); }
  for (let i = 0; i < 9; i++) { const h = cone(14 + hash(i) * 16, 9 + hash(i * 5) * 12, i % 2 ? 0x79b863 : 0x6fb06a, 5); h.position.set((i % 2 ? 1 : -1) * (55 + hash(i * 9) * 60), 3, -80 + i * 28); scene.add(h); }
  // geese
  const GEESE = []; for (let i = 0; i < 6; i++) { const g = new THREE.Group(); const b = at(ball(0.34, 0xffffff, 1), 0, 0.55, 0); b.scale.set(0.8, 0.8, 1.25); const n = at(cyl(0.07, 0.09, 0.6, 0xffffff, 6), 0, 0.95, 0.3); n.rotation.x = 0.35; const hd = at(ball(0.13, 0xffffff, 0), 0, 1.27, 0.42); const bk = at(cone(0.06, 0.22, 0xf28a1e, 4), 0, 1.25, 0.6); bk.rotation.x = Math.PI / 2; const w1 = at(box(0.5, 0.05, 0.36, 0xf3f3f3), -0.42, 0.62, 0), w2 = at(box(0.5, 0.05, 0.36, 0xf3f3f3), 0.42, 0.62, 0); const f1 = at(cyl(0.03, 0.03, 0.3, 0xf28a1e, 4), -0.1, 0.15, 0), f2 = at(cyl(0.03, 0.03, 0.3, 0xf28a1e, 4), 0.1, 0.15, 0); g.add(b, n, hd, bk, w1, w2, f1, f2); g.traverse((o) => { o.castShadow = true; }); g.userData = { w1, w2, f1, f2 }; g.visible = false; scene.add(g); GEESE.push(g); }
  // dungeon wagon set (x = 60)
  const DX = 60; const wagon = new THREE.Group(); wagon.position.set(DX + 1.5, 0, 0); wagon.add(at(box(2.6, 0.2, 2.0, 0x6b4a2b), 0, 0.75, 0), at(box(2.6, 0.2, 2.0, 0x4a3320), 0, 2.75, 0));
  for (let i = 0; i < 7; i++) { wagon.add(at(cyl(0.05, 0.05, 2.0, 0x2c2c33, 5), -1.25 + i * 0.417, 1.75, 0.95), at(cyl(0.05, 0.05, 2.0, 0x2c2c33, 5), -1.25 + i * 0.417, 1.75, -0.95)); }
  for (const [x, z] of [[-0.9, 1.05], [0.9, 1.05], [-0.9, -1.05], [0.9, -1.05]]) { const wh = at(cyl(0.5, 0.5, 0.16, 0x3a2a1c, 10), x, 0.5, z); wh.rotation.x = Math.PI / 2; wagon.add(wh); }
  const donkey = new THREE.Group(); donkey.add(at(box(1.3, 0.6, 0.5, 0x8d8378), 0, 1.0, 0), at(box(0.45, 0.5, 0.4, 0x8d8378), 0.85, 1.35, 0), at(box(0.1, 0.4, 0.08, 0x8d8378), 0.85, 1.75, 0.14), at(box(0.1, 0.4, 0.08, 0x8d8378), 0.85, 1.75, -0.14)); for (const [x, z] of [[-0.5, 0.18], [0.5, 0.18], [-0.5, -0.18], [0.5, -0.18]]) donkey.add(at(box(0.14, 0.7, 0.14, 0x756c62), x, 0.35, z)); donkey.position.set(2.7, 0, 0); wagon.add(donkey); wagon.traverse((o) => { o.castShadow = true; }); scene.add(wagon);
  const guard = () => { const g = new THREE.Group(); g.add(at(cyl(0.2, 0.26, 1.2, 0x5b6470, 6), 0, 1.0, 0), at(ball(0.26, SKIN), 0, 1.85, 0), at(cone(0.3, 0.36, 0x9aa3ad, 6), 0, 2.15, 0), at(cyl(0.07, 0.07, 0.7, 0x2c2c33, 5), -0.1, 0.3, 0), at(cyl(0.07, 0.07, 0.7, 0x2c2c33, 5), 0.1, 0.3, 0), at(cyl(0.03, 0.03, 2.6, 0x7a5230, 5), 0.34, 1.4, 0), at(cone(0.09, 0.3, 0xc9d0d8, 4), 0.34, 2.85, 0)); g.traverse((o) => { o.castShadow = true; }); scene.add(g); return g; };
  const G1 = guard(), G2 = guard(); const prisoner = carrier(COLS[1]); scene.add(prisoner);
  // rope bridge set (x = 120)
  const BX = 120; const BY = 12; scene.add(at(box(40, 30, 40, 0x9a8f80), BX - 27, BY - 15, 0), at(box(40, 30, 40, 0x9a8f80), BX + 27, BY - 15, 0), at(box(40, 0.4, 40, 0x86c35c), BX - 27, BY + 0.01, 0), at(box(40, 0.4, 40, 0x86c35c), BX + 27, BY + 0.01, 0)); const gap = at(box(14, 0.3, 60, 0x3b7fb5), BX, 0.2, 0); scene.add(gap);
  const bridge = new THREE.Group(); bridge.position.set(BX, BY, 0); for (let i = 0; i < 15; i++) bridge.add(at(box(0.8, 0.12, 3.0, i % 2 ? 0x9a6b3c : 0x855a30), -6.5 + i * 0.93, 0, 0));
  bridge.add(at(cyl(0.05, 0.05, 14, 0x5a4326, 5), 0, 1.1, 1.5), at(cyl(0.05, 0.05, 14, 0x5a4326, 5), 0, 1.1, -1.5)); bridge.children[15].rotation.z = bridge.children[16].rotation.z = Math.PI / 2; bridge.traverse((o) => { o.castShadow = true; o.receiveShadow = true; }); scene.add(bridge);
  // castle mountain set (x = 200)
  const CX = 200, CZ = -70; const mount = cone(46, 78, 0x8b8f97, 7); mount.position.set(CX, 39, CZ); scene.add(mount); scene.add(at(cone(16, 26, 0xf4f6f8, 7), CX, 67, CZ));
  for (let i = 0; i < 6; i++) { const m2 = cone(22 + hash(i) * 14, 30 + hash(i * 3) * 24, i % 2 ? 0x7d848f : 0x6f7783, 6); m2.position.set(CX + (i - 2.5) * 30, 14, CZ - 34 - hash(i * 7) * 20); scene.add(m2); }
  const castle = new THREE.Group(); castle.position.set(CX, 80, CZ); castle.add(at(box(10, 7, 8, 0xd9d2c2), 0, 2, 0), at(box(4, 11, 4, 0xcfc7b6), 0, 6, 0), at(cone(3.4, 5, 0xb3202a, 4), 0, 14, 0));
  for (const [x, z] of [[-5.5, -4.5], [5.5, -4.5], [-5.5, 4.5], [5.5, 4.5]]) castle.add(at(cyl(1.5, 1.6, 10, 0xd9d2c2, 8), x, 3.5, z), at(cone(1.9, 3.6, 0xb3202a, 8), x, 10.3, z));
  castle.add(at(cyl(0.06, 0.06, 3, 0x5a4326, 4), 0, 18, 0), at(box(1.6, 0.9, 0.05, GOLD), 0.85, 18.9, 0)); scene.add(castle);
  const fogs = []; for (let i = 0; i < 7; i++) { const f = new THREE.Mesh(new THREE.PlaneGeometry(170, 16), new THREE.MeshBasicMaterial({ color: 0xfff0d6, transparent: true, opacity: 0.34, depthWrite: false, fog: false })); f.position.set(CX + (hash(i) - 0.5) * 40, 6 + i * 6.5, CZ + 44 - i * 5); scene.add(f); fogs.push(f); }
  await renderer.compileAsync(scene, cam);

  function pose(t, o) {
    // o: {x, z, yaw, speed, wob, tilt, kingOn, anger, kingPos?}
    rig.position.set(o.x, o.y || 0, o.z); rig.rotation.y = o.yaw || 0; const ph = t * (o.speed || 0) * 2.1;
    CAR.forEach((g, i) => { const h = g.userData.home; g.visible = o.show ? o.show[i] > 0 : true; const sc = o.show ? Math.min(1, o.show[i]) : 1; g.scale.setScalar(sc * (1 + (o.show ? Math.sin(Math.min(1, o.show[i]) * Math.PI) * 0.25 : 0)));
      g.position.set(h[0], Math.abs(Math.sin(ph + i * 1.6)) * 0.09 * Math.min(1, o.speed || 0) - (o.squash || 0) * 0.14, h[2]); walk(g, ph + i * 1.6, Math.min(1, o.speed || 0)); g.rotation.y = 0; });
    const wob = o.wob || 0; chair.position.y = 1.5 + Math.sin(ph * 2) * 0.05 - (o.squash || 0) * 0.16; chair.rotation.z = Math.sin(t * 7.3) * 0.05 * wob + (o.roll || 0); chair.rotation.x = Math.sin(t * 5.1 + 1) * 0.04 * wob + (o.tilt || 0);
    const an = o.anger || 0; face.color.set(SKIN).lerp(new THREE.Color(0xe2463f), an); br1.rotation.z = -0.5 * an - 0.1; br2.rotation.z = 0.5 * an + 0.1; mouth.scale.x = 1 + an * 0.8; king.visible = o.kingOn !== false;
    king.position.set(0, 0.2, 0); king.rotation.set(0, 0, 0); king.scale.set(1, 1, 1); if (o.kingFn) o.kingFn(king);
    const eat = o.eat || 0; kArm.rotation.z = lerp(0.2, 2.2, (Math.sin(t * 4) * 0.5 + 0.5) * eat) + (o.point || 0) * 1.4; kArm.rotation.x = -(o.point || 0) * 1.3;
    steam.forEach((s, i) => { const u = ((t * 0.9 + i / 6) % 1); s.visible = an > 0.5; s.position.set((i % 2 ? 0.55 : -0.55) + Math.sin(i + u * 3) * 0.15, 2.4 + u * 1.3, 0.1); s.scale.setScalar(0.5 + u * 1.2); s.material.opacity = (1 - u) * 0.9 * an; });
  }
  function look(px, py, pz, tx, ty, tz, fov = 40) { cam.position.set(px, py, pz); cam.up.set(0, 1, 0); cam.lookAt(tx, ty, tz); cam.fov = fov; cam.updateProjectionMatrix(); sun.position.set(tx + 9, 16, tz + 7); sun.target.position.set(tx, 0, tz); sun.target.updateMatrixWorld(); }
  const T = K.at;
  function render(t) {
    scene.background.copy(SKY); scene.fog.color.set(0xcfe9ff); scene.fog.near = 40; scene.fog.far = 190; sun.color.set(0xffe7bd); sun.intensity = 2.6; hemi.intensity = 1.25;
    GEESE.forEach((g) => { g.visible = false; }); prisoner.visible = false; G1.visible = G2.visible = false; path.position.x = 0; path.rotation.z = 0;
    const scroll = (spd) => trees.forEach((g) => { g.position.set(g.userData.x, 0, ((g.userData.z0 - t * spd) % 120 + 120) % 120 - 60); });
    scroll(0);
    if (t < T.s2) {
      // 1 hook: press play, the chair tips and the king flies
      const u = Math.max(0, t - K.trip); const tip = ss(K.trip - 0.12, K.trip + 0.12, t);
      scroll(3.2 * (1 - tip));
      pose(t, { x: 0, z: 0, yaw: 0.0, speed: 1.5 * (1 - tip), wob: 1.5, tilt: tip * 0.75, eat: 1 - tip, kingFn: (k) => { if (u > 0) { k.position.set(Math.sin(u * 2) * 0.6, 0.2 + 9.5 * u - 5.2 * u * u, 4.5 * u); k.rotation.set(u * 9, u * 2, u * 3); } } });
      const d = lerp(13.5, 11.5, ss(0, K.trip, t)) + u * 1.2; look(7.5, 3.6 + u * 1.6, d, 0, 2.3 + Math.min(4.5, u * 4.2), 0.5 + u * 1.2, 40);
    } else if (t < T.s3) {
      // 2 the idea: four friends pop in, the king drops on, push in on the grumpy face
      const sh = CAR.map((_, i) => (t - (K.vier + i * 0.14)) / 0.25); const drop = (t - K.koenig) / 0.35; const landed = ss(0, 1, drop); const go = ss(K.tragen - 0.1, K.tragen + 0.4, t);
      scroll(3.2 * go);
      pose(t, { x: 0, z: 0, yaw: 0, speed: 1.4 * go, wob: go, show: sh, kingOn: drop > 0, squash: Math.sin(Math.min(1, Math.max(0, drop - 0.9) * 2.2) * Math.PI) * 1.2, eat: go, anger: 0.15, kingFn: (k) => { k.position.y = 0.2 + (1 - landed) * 9; const q = Math.sin(Math.min(1, Math.max(0, drop - 0.95) * 2.5) * Math.PI); k.scale.set(1 + q * 0.18, 1 - q * 0.2, 1 + q * 0.18); } });
      const p = ss(K.tragen + 0.2, T.s3 - 0.1, t), a = -0.55 + (t - T.s2) * 0.16; const r = lerp(14.5, 4.6, p);
      look(Math.sin(a) * r, lerp(4.4, 3.9, p), Math.cos(a) * r, 0, lerp(2.2, 3.55, p), 0.2, lerp(42, 30, p));
    } else if (t < K.kerkerCut) {
      // 3a wobble -> anger
      const an = ss(K.wackelt, K.wuetend2 + 0.3, t); scroll(3.2);
      pose(t, { x: 0, z: 0, speed: 1.7, wob: 1 + an * 5, anger: an, point: ss(K.ab - 0.25, K.ab, t) });
      look(-6.0 + Math.sin(t * 9) * 0.06 * an, 4.0, 11.8, 0, 2.7, 0.2, 38);
    } else if (t < T.s4) {
      // 3b off to the dungeon
      const u = t - K.kerkerCut, d = T.s4 - K.kerkerCut; rig.position.set(-500, 0, 0);
      prisoner.visible = G1.visible = G2.visible = true; const m = ss(0, d * 0.62, u); const inside = u > d * 0.62;
      const px = lerp(DX - 2.9, DX - 0.2, m); prisoner.position.set(inside ? DX + 1.5 : px, inside ? 0.86 : 0, 0); prisoner.rotation.y = Math.PI / 2; prisoner.rotation.z = inside ? 0 : 0.35; walk(prisoner, u * 16, inside ? 0 : 1, false); prisoner.userData.a1.rotation.z = 2.4; prisoner.userData.a2.rotation.z = -2.4;
      G1.position.set((inside ? DX - 0.6 : px + 0.8), 0, 0.75); G2.position.set((inside ? DX - 0.6 : px + 0.8), 0, -0.75); G1.rotation.y = G2.rotation.y = Math.PI / 2;
      wagon.rotation.z = inside ? Math.sin(Math.min(1, (u - d * 0.62) * 4) * Math.PI) * 0.06 : 0;
      look(DX - 0.6 + u * 0.3, 2.6, 13, DX - 0.1, 1.7, 0, 40);
    } else if (t < K.brueckeCut) {
      // 4a geese
      const u = t - T.s4; scroll(9);
      pose(t, { x: 0, z: 0, speed: 3.2, wob: 3, anger: 0.5 });
      GEESE.forEach((g, i) => { g.visible = true; g.scale.setScalar(1.7); const z = -5.6 - (i % 3) * 1.7 + u * 1.6 + Math.sin(t * 6 + i) * 0.2, x = (i - 2.5) * 1.5; g.position.set(x, Math.abs(Math.sin(t * 14 + i * 2)) * 0.25, z); g.userData.w1.rotation.z = Math.sin(t * 30 + i) * 0.9; g.userData.w2.rotation.z = -Math.sin(t * 30 + i) * 0.9; g.userData.f1.rotation.x = Math.sin(t * 22 + i) * 0.8; g.userData.f2.rotation.x = -Math.sin(t * 22 + i) * 0.8; });
      look(5.8, 2.3, 10.5 - u * 0.5, 0.2, 1.7, -2.5, 44);
    } else if (t < K.burgCut) {
      // 4b the wobbly bridge
      const u = t - K.brueckeCut; const sway = Math.sin(t * 4.2) * 0.2; bridge.rotation.x = sway; bridge.position.y = BY + Math.sin(t * 8.4) * 0.12;
      pose(t, { x: BX - 1.5 + u * 1.2, y: 0.2 + bridge.position.y, z: 0, yaw: Math.PI / 2, speed: 0.9, wob: 4, roll: 0, tilt: sway * 1.6, anger: 0.8, kingFn: (k) => { k.position.z = sway * 2.2; k.rotation.x = sway * 1.2; } });
      rig.rotation.x = sway;
      look(BX + 3 - u * 0.6, BY + 6.5, 19, BX, BY + 1.2, 0, 40);
    } else if (t < T.s5) {
      // 4c the castle on the mountain: golden hour pull-back
      const u = t - K.burgCut, d = T.s5 - K.burgCut, p = ss(0, d, u); rig.rotation.x = 0;
      scene.background.copy(DUSK); scene.fog.color.set(0xffd9a8); scene.fog.near = 60; scene.fog.far = 330; sun.color.set(0xffb066); sun.intensity = 3.2; hemi.intensity = 0.95;
      pose(t, { x: CX, z: CZ + 62, yaw: Math.PI, speed: 1.2, wob: 1 });
      fogs.forEach((f, i) => { f.position.x = CX + (hash(i) - 0.5) * 40 + Math.sin(t * 0.3 + i) * 6; f.lookAt(cam.position); });
      const cz = lerp(CZ + 34, CZ + 96, p), cy = lerp(84, 9, p); cam.position.set(CX + lerp(10, 5, p), cy, cz); cam.up.set(0, 1, 0); cam.lookAt(CX, lerp(88, 44, p), CZ); cam.fov = 46; cam.updateProjectionMatrix();
      sun.position.set(CX + 40, 50, CZ + 90); sun.target.position.set(CX, 40, CZ); sun.target.updateMatrixWorld();
    } else {
      // 5 the game running under the code window (and behind the end card)
      rig.rotation.x = 0; scroll(3.2); pose(t, { x: 0, z: 0, speed: 1.5, wob: 1.2, eat: 1, anger: 0.2 });
      const a = 0.5 + (t - T.s5) * 0.12; look(Math.sin(a) * 12, 4.4, Math.cos(a) * 12, 0, 2.1, 0, 40);
    }
    renderer.render(scene, cam);
  }
  return { render };
}
