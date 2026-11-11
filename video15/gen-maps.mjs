import fs from "fs";
import { geoNaturalEarth1, geoMercator, geoPath, geoCentroid } from "d3-geo";
import { feature } from "topojson-client";
const load = (r) => { const t = JSON.parse(fs.readFileSync(`node_modules/world-atlas/countries-${r}.json`)); return feature(t, t.objects.countries).features; };
const LL = ["Bolivia","Paraguay","Mali","Burkina Faso","Niger","Chad","Central African Rep.","S. Sudan","Ethiopia","Uganda","Rwanda","Burundi","Zambia","Malawi","Zimbabwe","Botswana","eSwatini","Lesotho","Switzerland","Austria","Czechia","Slovakia","Hungary","Serbia","North Macedonia","Macedonia","Kosovo","Luxembourg","Belarus","Moldova","Armenia","Azerbaijan","Kazakhstan","Uzbekistan","Turkmenistan","Kyrgyzstan","Tajikistan","Afghanistan","Mongolia","Nepal","Bhutan","Laos","Andorra","Liechtenstein","San Marino","Vatican"];
const rnd = (d, p) => d.replace(/-?\d+\.\d+/g, (m) => (+m).toFixed(p));
const out = {};
// world
{ const f = load("110m").filter((x) => x.properties.name !== "Antarctica"); const pr = geoNaturalEarth1().fitWidth(2000, { type: "FeatureCollection", features: f }); const p = geoPath(pr);
  const b = p.bounds({ type: "FeatureCollection", features: f });
  out.world = { w: 2000, h: Math.ceil(b[1][1]), items: f.map((x) => ({ n: x.properties.name, d: rnd(p(x) || "", 1), ll: LL.includes(x.properties.name), c: p.centroid(x).map((v) => +v.toFixed(1)) })).filter((x) => x.d) };
  out.world.pt = { uz: pr([64.5, 41.5]).map((v) => +v.toFixed(1)), li: pr([9.55, 47.15]).map((v) => +v.toFixed(1)) };
  console.log("world", out.world.h, "landlocked on map:", out.world.items.filter((x) => x.ll).length, "missing:", LL.filter((n) => !f.some((x) => x.properties.name === n)).join(", ")); }
function region(key, res, ext, W, H, keep) {
  const f = load(res); const pr = geoMercator().fitExtent([[0, 0], [W, H]], { type: "Polygon", coordinates: [[[ext[0], ext[1]], [ext[0], ext[3]], [ext[2], ext[3]], [ext[2], ext[1]], [ext[0], ext[1]]]] }).clipExtent([[-40, -40], [W + 40, H + 40]]);
  const p = geoPath(pr); const big = 0.8 * (W + 80) * (H + 80);
  out[key] = { w: W, h: H, items: f.filter((x) => p.area(x) < big).map((x) => ({ n: x.properties.name, d: rnd(p(x) || "", 1), ll: LL.includes(x.properties.name), c: p.centroid(x).map((v) => +(v || 0).toFixed(1)) })).filter((x) => x.d && x.d.length > 20), pr: (ll) => pr(ll).map((v) => +v.toFixed(1)) };
  console.log(key, out[key].items.map((x) => x.n).join(", "));
}
region("ca", "50m", [44, 33, 84, 56.5], 1000, 900);
out.ca.pts = { uz: out.ca.pr([63.5, 41.6]), kz: out.ca.pr([67, 48.5]), kg: out.ca.pr([74.8, 41.4]), tj: out.ca.pr([71, 38.6]), af: out.ca.pr([66, 34.3]), tm: out.ca.pr([59, 39.2]), caspian: out.ca.pr([50.8, 41.5]) };
region("alps", "10m", [4.5, 43.2, 17.5, 49.3], 1040, 760);
out.alps.pts = { li: out.alps.pr([9.55, 47.16]), ch: out.alps.pr([8.0, 46.75]), at: out.alps.pr([14.2, 47.55]), it: out.alps.pr([10.8, 45.3]), de: out.alps.pr([10.5, 48.7]), fr: out.alps.pr([5.6, 46.6]), border1: out.alps.pr([9.45, 47.06]), border2: out.alps.pr([9.3, 46.3]), sea: out.alps.pr([8.95, 44.3]), genoa: out.alps.pr([8.93, 44.41]) };
delete out.ca.pr; delete out.alps.pr;
fs.writeFileSync("maps.json", JSON.stringify(out));
console.log("bytes", fs.statSync("maps.json").size, JSON.stringify(out.world.pt), JSON.stringify(out.ca.pts), JSON.stringify(out.alps.pts));
