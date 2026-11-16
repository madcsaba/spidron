# Kodonfészek

Böngészőben futó, mozgó modell, amely a genetikai kód 64 kodonját három nyelven mutatja egyszerre: **DNS/RNS** (bázisok, kodonok, párosodás), **I Ching** (vonalak, trigramok, hexagramok) és **spidron** (Erdély Dániel formája: övek, karok, önhasonló nagyítás). Mellé hang tartozik, amely ugyanezt hallhatóvá teszi.

Megnyitás: [`index.html`](index.html). Élőben, ha a GitHub Pages be van kapcsolva: https://madcsaba.github.io/spidron/kodonfeszek/

A modell **jelölési rendszer, nem felfedezés.** Az I Ching nem tud a DNS-ről, a hexagramok jelentése nem írja le az aminosavakat, a hang pedig nem hat a DNS-re. Amit a modell ad: egy olyan jelölés, amelyben a genetikai kód valódi rendje láthatóvá és hallhatóvá válik. Hogy melyik állítás mennyire erős, azt a három szint jelzi.

## A három igazságszint

| Szint | Mit jelent | Példa |
|---|---|---|
| 1. szerkezeti | A szabályból következik, mindhárom rendszerben igaz. | A szemközti szál minden vonalat megfordít (錯卦). |
| 2. helyzeti | A genetikai kód valódi, kiszámolt tulajdonsága, olyan helyen, amelyet a mi elrendezésünk jelöl ki. A tény igaz, a hely megállapodás. | A 6. vonal 64 kodonból 60-nál néma. |
| 3. költői | Szép egybeesés, amely egy másik kiosztásban eltűnik. Nem bizonyíték. | A CCC (prolin) a 12. hexagram, a „Pangás”, és a prolin tényleg megtöri a fehérjék α-hélixét. |

Az oldalon a „Szintek” kapcsolóval elrejthető a 3. szint.

## A leképezés

Minden bázisnak két kétértékű tulajdonsága van:

| Bázis | Gyűrű | Amino / keto | Hidrogénkötés |
|---|---|---|---|
| A | purin (jang) | amino (jang) | 2, gyenge |
| G | purin (jang) | keto (jin) | 3, erős |
| C | pirimidin (jin) | amino (jang) | 3, erős |
| U / T | pirimidin (jin) | keto (jin) | 2, gyenge |

- **Alsó trigram** (1–3. vonal): a kodon három bázisának gyűrűbitje.
- **Felső trigram** (4–6. vonal): ugyanezek amino/keto bitje.
- **Egy bázis = egy 應-pár:** az 1–4., 2–5. és 3–6. vonal. A trigramhatár így nem vág át bázist.
- **Kötés-trigram:** bázisonként a két bit „kizáró vagy”-a, vagyis az erős/gyenge kötés. A párosodás nem változtat rajta, ezért a két szálon közös.

**Eltérés a repó többi oldalától.** Az [`iching.html`](../iching.html) más, szintén érvényes kiosztást használ: ott egy bázis két *egymás utáni* vonal (1–2, 3–4, 5–6). A szemközti szál mindkettőben a 錯, de ugyanannak a kodonnak a két oldalon más hexagram felel meg. A Kodonfészek a 應-páros változatot használja, mert ebben a hagyományos vonalhelyek (két közép, a 6. vonal mint „helyzeten túli”) egybeesnek a kód kiszámolt tulajdonságaival. Az oldal fejlécében a nyolc érvényes, 應-páros kiosztás között lehet váltani.

## Az oldal használata

- **Vezetett út:** tíz lépés a bázistól a szintekig. Utána szabad felfedezés.
- **Lejátszás és léptetés:** a fészek kodononként befelé áramlik. Szóköz: lejátszás, nyilak: léptetés, C: szemközti szál, F: teljes képernyő.
- **Kártya (jobb oldal):** az olvasott kodon, aminosav, hexagram (írásjeggyel, névvel, hagyományos jelentéssel), a kötés-trigram és az érvényes szintek. Egy bázisra kattintva átírod a kodont (visszavonható).
- **Inzulinváltozatok:** négy ismert pontmutáció az emberi inzulin génjében. A hatásukat az oldal a szekvenciából számolja.
- **Összehasonlítás:** egy második szekvencia kodononként, vagy egy szinonim átirat (ugyanaz a fehérje, más kodonokkal).
- **64-es tábla:** oszlop az alsó, sor a felső trigram, Fu Xi-sorrendben. Kattintásra beírja a kodont.
- **Rétegek:** Remegés, Gerinc (2–5. tengely), 應-párok, Kötés, Lágy fény. A **Dombormű** csúszka a sík fészket térbe hajlítja.

## A hang: mire jó, és hogyan használd

A hang a kodon szerkezetét teszi hallhatóvá, hogy fül alapján is követni lehessen. Jelölés, nem fizikai kapcsolat.

**Indítás:** a fejlécben a Hang gomb, majd léptetés. Minden kodon három hangként szól. Végig halkan szól egy mély D: ez a tükörtengely.

| Amit hallasz | Amit jelent |
|---|---|
| A hang a tengely fölött vagy alatt | purin (A, G) vagy pirimidin (C, U) |
| A hang közel vagy messze a tengelytől | erős (G, C) vagy gyenge (A, U) kötés |
| Két hosszú, egy rövid hang | az első két bázis cseréje szinte mindig más aminosavat ad (95,6% és 100%), a harmadiké ritkán (31,1%) |
| Remegő harmadik hang | a lazább, wobble-párosodás helye |
| A középső hang a legmélyebb (U) | az aminosav mindig víztaszító, 16 kodonból 16-szor |

A hangok: A = +7, G = +2, C = −2, U = −7 félhang a D-től (vagyis A, E, C, G). A tengellyel együtt pentaton skála. A ±2 és ±7 választás, más szimmetrikus hangközzel is működne.

**Három kísérlet:**

1. **„Mindkettő” mód:** a két szál egyszerre szól, balra és jobbra. Szűk hangköz (nagy terc) erős párt, tág hangköz (nagy nóna) gyenge párt jelez. A három hangköz a kötés-trigram, és a két szálon azonos.
2. **Mutáció:** kattints a harmadik bázisra. Ha a hang a tengely ugyanazon oldalán marad (U↔C, A↔G), az aminosav 64 kodonból 60-nál ugyanaz. Ha átugrik (U↔G, C↔A), 30-nál megváltozik.
3. **Szemközti szál:** a dallam rák-tükörben szól, tükrözve és visszafelé, ahogy a másik szál a saját irányában olvasódik.

Lejátszás közben √3 arányú Shepard-hang szól: a fészek nagyításának hangja, amely mindig emelkedik, mégis önmagába tér vissza.

## Fájlok

| Fájl | Tartalom |
|---|---|
| `index.html` | Az oldal. Egyetlen fájl, build nélkül; a three.js r128-at a repó közös `../vendor/three.min.js` másolatából tölti, CDN nélkül. |
| `data/kodonok.csv` | A 64 kodon: aminosav, hexagram, trigramok, szemközti szál, kötés-trigram, szintek |
| `data/hexagramok.csv` | A 64 hexagram: jel, írásjegy, pinyin, magyar név, rövid hagyományos jelentés, kodon |
| `data/trigramok.csv`, `data/bazisok.csv`, `data/vonalhelyek.csv` | A nyolc trigram, a négy bázis, a hat vonalhely |
| `data/fogalmak.csv`, `data/szintek.csv` | Fogalomtár a három rendszerből, szintjelöléssel |
| `data/proba_kiosztasok.csv`, `data/proba_veletlen_kodok.csv` | A véletlen elleni próba eredménye |
| `data/inzulin_cds_rns.txt` | Az emberi inzulin (preproinzulin) kódoló szakasza, RNS-betűkkel |
| `versciklus.md` | Tizenkét vers a három szint szerint |
| `scripts/build_data.py` | Előállítja a `data/*.csv` táblákat, és ellenőrzi az inzulinszekvenciát |
| `scripts/check_relief.js` | Ellenőrzi, hogy a dombormű hajtása merev és önhasonló |
| `proba/` | A spidronfészek 64 hajtásállapotának számítása és fizikai próbája: eredmények, nyomtatható sablon és jegyzőkönyv ([leírás](proba/README.md)) |
| `scripts/spidron_allapotok.py`, `scripts/hajtasiranyok.py`, `scripts/ellenorzes_allapotok.py`, `scripts/proba_pdf.py` | A 64 állapot merev megoldása és ütközésvizsgálata, a hegy- és völgyhajtások, az ellenőrzések és a próba-PDF (numpy, reportlab) |

Futtatás:

```bash
python3 -m http.server          # a repó gyökeréből, majd: http://localhost:8000/kodonfeszek/
python3 scripts/build_data.py   # a kodonfeszek mappából; csak standard könyvtár
node scripts/check_relief.js    # a kodonfeszek mappából
```

## A véletlen elleni próba röviden

- A 24 lehetséges bázis–vonal kiosztásból 8-ban teljesül, hogy a szemközti szál a teljes ellentét, és hogy a harmadik bázis egyik vonala 60 kodonnál néma. Mindhárom vizsgált állítás egyszerre csak egyben teljesül, a mostaniban, amelyet éppen ezért választottunk.
- A genetikai kódot 20 000-szer véletlenszerűen összekeverve a 6. vonal átlagosan 2,9 kodonnál néma (legfeljebb 16-nál), és a „középső U mindig víztaszító” egyszer sem teljesül.
- A mintázat tehát a genetikai kód tulajdonsága. Az I Ching nem tesz hozzá információt, csak egy olyan jelölést ad, amelyben ez a rend látszik.

## Források

- Emberi inzulin gén, kódoló szakasz: GenBank AH002844.2, a [DNAvisualization.org példafájlja](https://github.com/Benjamin-Lee/DNAvisualization.org/blob/master/example_seqs/insulin.fasta) alapján. A fordítás betűre egyezik a preproinzulin ismert sorrendjével.
- Inzulinváltozatok (jelölés: NM_000207.3): [Rat Genome Database, INS](https://rgd.mcw.edu/rgdweb/report/gene/main.html?id=731056).
- Spidron: Erdély Dániel, [Some Surprising New Properties of the Spidrons](https://archive.bridgesmathart.org/2005/bridges2005-179.pdf) (Bridges 2005) és [The SpHidron Conjecture](https://static1.bridgesmathart.org/2011/cdrom/proceedings/70/index.html) (Bridges 2011); [Spidron – Wikipedia](https://en.wikipedia.org/wiki/Spidron).
- Hexagramnevek: a Wilhelm–Baynes-féle elterjedt címeket követik ([YellowBridge](https://mail.yellowbridge.com/onlinelit/yijing-notes.php), [List of hexagrams of the I Ching](https://en.wikipedia.com/wiki/Qian_(hexagram))). A magyar nevek és a rövid jelentések saját megfogalmazások, nem egy kiadott fordításból valók.
- Wobble-párosodás: F. H. C. Crick, 1966.

## Licenc

A repó gyökerében lévő [`LICENSE`](../LICENSE) szerint: a kód MIT, a magyar szövegek (magyarázatok, versek, adattáblák szövegei) CC BY 4.0. A three.js saját MIT-licence alatt áll (`../vendor/three.LICENSE`).
