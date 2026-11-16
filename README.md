# Spidron–Ji King–DNS

Interaktív, böngészőben futó prototípusok egy közös, 6 bites állapottérről, amely három nézetből olvasható: **hexagram** (Ji csing), **kodon** (genetikai kód) és **spidron** (Erdély Dániel formája).

Élő változat (GitHub Pages): https://madcsaba.github.io/spidron/

## Oldalak

| Fájl | Tartalom |
|---|---|
| `index.html` | Nyitóoldal |
| `iching.html` | **A változások tere:** a 64 hexagram 3D térben (4×4×4 kocka, 6D vetület, Fu Hszi négyzet és kör, Wen király sorrend); párok, 錯, 綜, 互, szomszédok, azonos aminosav; változó vonalak és a fő szöveg Csu Hszi szabálya szerint; szövegrétegek (原文, magyar, Legge, 彖/象); jelenet, spidron (2D / 3D), hajtogatási minta (SVG), jelenet-leírás (JSON), idővonal, 64 szín, opcionális képgenerálás saját API-kulccsal |
| `chroma.html` | **SJK-Chroma Engine v1.3** (three.js): 3D spidron-fészek (6 öv = 6 vonal), RGB-színkocka a 錯 komplementer tengellyel, spidronhedron (8 trigram-csúcs); színtani panel, 五音 hangrezonancia (Web Audio), Hamming-szomszédsági paletta CSS-exporttal, 8×8 King Wen mátrix |
| `spidron-cube.html` | **Spidron-kocka** (three.js): a 64 hexagram spidron-fészkekből kirakva egy 4×4×4-es kockában; a fészek hajtásai a vonalak, színe a vonalpárok (R, G, B), a kiválasztott hexagram 錯 ellentéte a középponton át és 6 szomszédja kiemelve; szétnyitás, hajtásmélység, emeletenkénti szűrés |
| `harmonia.html` | **Spidron Harmónia Labor** (three.js): a spidron felépítése 4 lépésben (2D kiterítve és 3D hajtogatva: egy kar, hatszögű fészek, kupola); a szintek mérete hangfrekvenciára (négy leképezés, köztük a mérettel fordított arányú f₀·(√3)^k) és a 2⁴⁰-es oktáv-transzponálással fényhullámhosszra képezve, Web Audio hangokkal |
| `spidron-lab.html` | **Spidron-labor:** SJK-mozaik (hatszögű LBP vs. gradiens-szabály), SJK-UI demó (spidron-gomb, mutáció + időgörbe, spirális menü), színek (spidron-színkör HSL/OKLCH-ban, harmóniák, hexagram mint paletta, 64 szín) |
| `kodonfeszek/` | **Kodonfészek:** mozgó 3D spidronfészek, amelyben minden öv egy kodon és minden kar egy hexagramvonal (應-páros kiosztás); szemközti szál mint tükör, kötés-trigram, inzulingén és ismert változatai, szinonim átirat, hangrend magyarázattal, három igazságszint, véletlen elleni próba, adattáblák CSV-ben, versciklus. Részletek: [`kodonfeszek/README.md`](kodonfeszek/README.md) |

A `chroma.html` saját hozzárendelést használ: a színt a két trigramból számolja (az R csatornát az 1. és 4. vonal adja, azaz ⅔ alsó + ⅓ felső trigram), a kodont pedig Krakowski kódolásával. A 錯 itt is a kiegészítő szín. A többi oldal a vonalpáros (1–2 = R, 3–4 = G, 5–6 = B) hozzárendelést használja.

A `harmonia.html` 2⁴⁰-es oktáv-transzponálása (hang → fény) és a hajtás–felhang kapcsolata szemléltető leképezés, nem fizikai törvény; az oldal ezt jelzi is.

## Futtatás

Nincs build lépés és nincs függőség. Helyben:

```bash
python3 -m http.server
```

Utána: `http://localhost:8000/`

## Felépítés

- Nincs külső betűtípus, CDN vagy követőkód. Az `index.html`, `iching.html` és `spidron-lab.html` minden CSS-t és JS-t az oldalon belül tartalmaz; a `spidron-cube.html` minden CSS-t az oldalon belül tartalmaz, a three.js-t a helyi `vendor/three.min.js`-ből tölti; a `chroma.html` és a `harmonia.html` a saját helyi CSS-ét (`chroma.css`, `harmonia.css`: Tailwind CSS 3.4-gyel előre fordítva, csak a használt osztályok) és a helyi `vendor/three.min.js`-t (three.js r128) tölti be. A `kodonfeszek/` oldal a közös `vendor/three.min.js` másolatot használja.
- A hat fő oldal kétnyelvű (HU/EN): a szövegek `<span class="hu">` / `<span class="en">` párokban; a választott nyelv a `localStorage["sjk-lang"]` kulcsban, a nyelvváltáskor `sjk:lang` esemény fut. Kivétel: a `kodonfeszek/` csak magyarul érhető el.
- Böngészőben tárolva (csak az adott gépen): nyelv, idővonal (`iching-log`), képgenerálási beállítások (`iching-img`; a kulcs csak kifejezett kérésre).
- A képgenerálás az egyetlen hely, ahol az oldal külső szolgáltatást hív: csak kattintásra, a felhasználó saját kulcsával, közvetlenül a böngészőből.

## Megfeleltetések (röviden)

- **Hexagram → kocka:** a három vonalpár (1–2, 3–4, 5–6) a három tengely, Gray-sorrendben.
- **Hexagram → kodon:** vonalpár (alsó, felső) → bázis: jang-jang = A, jin-jang = G, jang-jin = C, jin-jin = U. 1. bit = amino/keto, 2. bit = purin/pirimidin; a 錯 a komplementer szál.
- **Hexagram → spidron:** a hat kar a hat vonal; jang = hegyhajtás, jin = völgyhajtás. A 64 állapot virtuális (a papír-spidron hajtogatása egyetlen szabadságfokú).
- **Hexagram → szín:** vonalpár → R, G, B csatorna, 4 fokozat (0, 85, 170, 255); a 錯 a kiegészítő szín. Palettaként: a jang vonalak a hat alapszín közül a palettában lévők.

- **Kodonfészek:** itt egy bázis nem két egymás utáni vonal, hanem egy 應-pár (1–4, 2–5, 3–6): az alsó trigram a gyűrűbitek, a felső az amino-bitek. A 錯 itt is a komplementer szál, de ugyanannak a kodonnak más hexagram felel meg, mint az `iching.html`-ben. Indoklás és próba: [`kodonfeszek/README.md`](kodonfeszek/README.md).

Ezek választott megfeleltetések, nem felfedezések.

## Források

- 周易 eredeti szöveg (közkincs), digitális kiadás: [freizl/yijing](https://github.com/freizl/yijing); néhány hagyományos/egyszerűsített írásjegy-csere és két adathiba javítva.
- James Legge: *The Yî King*, Sacred Books of the East XVI, 1882 (közkincs); átirat: [opencosmos-ai/iching](https://github.com/opencosmos-ai/iching) (Wikisource alapján).
- A magyar fordítás (ítéletek, képek, vonalak, 彖/象) saját munka a kínai eredetiből, Legge-t segédletként használva; lektorálásra vár.
- A 4×4×4-es kocka-szemlélet S. H. Cullinane finitegeometry.org oldalaiból ihletődik; a koordináta-hozzárendelés saját.
- Oklab / OKLCH: Björn Ottosson.
- [three.js](https://threejs.org/) r128 (MIT), helyi másolat: `vendor/three.min.js`, licenc: `vendor/three.LICENSE`.

## Licenc

- **Kód** (HTML, CSS, JavaScript): MIT, lásd [`LICENSE`](LICENSE).
- **Magyar fordítások és magyarázó szövegek:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) – szabadon felhasználható a forrás (`madcsaba/spidron`) megnevezésével.
- **A 周易 kínai szövege és Legge fordítása:** közkincs.

## Eredet

A prototípusok a [madcsaba/ai-awareness-wireframe](https://github.com/madcsaba/ai-awareness-wireframe) repóban készültek (`iching.html`, `spidron-lab.html`), onnan kerültek át önálló repóba.
