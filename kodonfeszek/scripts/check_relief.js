// A spidron-dombormű geometriájának ellenőrzése: az index.html saját függvényeit futtatja,
// és megnézi, hogy a háromszögek élhossza minden állásban változatlan-e (merev hajtás),
// valamint hogy a nagyítás egy öv után pontosan önmagába tér-e vissza.
// Futtatás a kodonfeszek mappából:  node scripts/check_relief.js
const fs = require('fs'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const js = html.match(/<script>\n([\s\S]*)<\/script>/)[1];
const a = js.indexOf('function chainStep'), b = js.indexOf('const tv=');
class V { set(x, y, z) { this.x = x; this.y = y; this.z = z; return this } }
const T = new Function('const R0=3,s3=Math.sqrt(3),D=Math.PI/180;let relief=0;' + js.slice(a, b) +
  ';return {shape,vpos,set:r=>relief=r,LV}')();
const d = (p, q) => Math.hypot(p.x - q.x, p.y - q.y, p.z - q.z);
let worst = 0, wrap = 0;
for (const rel of [0, 0.08, 0.16, 0.22]) for (const f of [0, 0.3, 0.5, 0.77, 1]) {
  T.set(rel); T.shape(f);
  for (let n = -1; n <= 8; n++) {
    const R = 3 / Math.pow(Math.sqrt(3), n), r = R / Math.sqrt(3);
    for (let k = 0; k < 6; k++) {
      const A = T.vpos(n, k, new V()), B = T.vpos(n, k + 1, new V()), C = T.vpos(n + 1, k, new V()), E = T.vpos(n + 1, k + 1, new V());
      worst = Math.max(worst, Math.abs(d(A, B) - R) / R, Math.abs(d(A, C) - r) / r, Math.abs(d(B, C) - r) / r,
        Math.abs(d(C, E) - r) / r, Math.abs(d(B, E) - r) / r);
    }
  }
}
T.set(0.16); T.shape(1); const L1 = T.LV.map(x => ({ ...x })); T.shape(0); const L0 = T.LV.map(x => ({ ...x }));
for (let j = 0; j < 10; j++) wrap = Math.max(wrap, Math.abs(L1[j].a / Math.sqrt(3) - L0[j + 1].a), Math.abs(L1[j].th - L0[j + 1].th));
console.log('legnagyobb relatív élhossz-eltérés:', worst.toExponential(2));
console.log('eltérés egy öv nagyítása után:', wrap.toExponential(2));
if (worst > 1e-9 || wrap > 1e-9) { console.error('HIBA: a hajtás nem merev vagy nem önhasonló'); process.exit(1); }
console.log('Rendben: merev és önhasonló.');
