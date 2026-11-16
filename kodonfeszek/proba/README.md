# A spidronfészek 64 állapota: számítás és fizikai próba

Kérdés: igaz-e, hogy egy hat övből álló spidronfészeknek 64 jól elkülöníthető, stabil hajtásállapota van (övenként egy bit, Erdély Dániel 0/1 jele szerint)? Ez a „geometriai memória” ötlet alapja.

## Számítás

Modell: ideális, vastagság nélküli, merev lapok; a hatszögek csúcsai felváltva emelkednek és süllyednek (3-szoros forgásszimmetrikus alakok). Más hajtásmódokat a modell nem vizsgál. Szkript: [`../scripts/spidron_allapotok.py`](../scripts/spidron_allapotok.py), ellenőrzések: [`../scripts/ellenorzes_allapotok.py`](../scripts/ellenorzes_allapotok.py), nyers eredmény: [`allapotok_utkozes.json`](allapotok_utkozes.json).

| Eredmény | Érték |
|---|---|
| Merev folytatás övenként | pontosan 2 (a belső hatszög azonos vagy ellentétes ritmusban emelkedik; az öv ennek megfelelően egyik vagy másik irányba fordul) |
| Állapotok száma 6 övvel | 2⁶ = 64 |
| Ütközésmentes állapotok | 64 / 64, a külső csúcsok teljes vizsgált emelkedési tartományában (a csúcssugár 3–24,5%-a) |
| Élhossz-eltérés | < 10⁻⁹ (a hajtás merev) |
| Különböző alakok | 64 forgatás erejéig; 32 tükrözéssel együtt: egy állapot és bitjei ellentettje egymás tükörképe |
| Emelkedések nagysága | minden állapotban azonos, csak az irány különbözik (külső 0,22 R esetén szintenként 0,22; 0,12; 0,066; 0,036; 0,020; 0,011) |
| Váltás két állapot között | csak a sík lapon át: kisimítás, majd újrahajtás |
| Stabilitás a merev modellben | nincs: a szerkezet erő nélkül mozog, egyik állapotot sem tartja meg semmi |

Következmény: a 64 állapot geometriailag létezik. Hogy melyik marad meg magától, azt csak az anyag (a hajtásvonalak és a lapok merevsége) döntheti el.

## Fizikai próba

Csomag: [`spidron_fesek_proba.pdf`](spidron_fesek_proba.pdf) (sablon A4-re, 100%-os méretben; hegy- és völgyhajtások két állapotra; a próba menete; jegyzőkönyv mind a 64 állapothoz). Előállítása: [`../scripts/proba_pdf.py`](../scripts/proba_pdf.py) (reportlab, DejaVu betűtípus).

### Eredmények

| Dátum | Anyag, méret | Állapotok | Hajtható | Megmaradt magától | Hány öv | Megjegyzés |
|---|---|---|---|---|---|---|
| 2026-11-16 | papír, A4-es sablon | nincs rögzítve | igen | részben | nincs rögzítve | első próba; a részletek pótlandók |

A jegyzőkönyv kitöltött oldalai és a fotók ide kerülhetnek, a fájlnévben az állapot bitjeivel.
