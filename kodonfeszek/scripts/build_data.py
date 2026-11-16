#!/usr/bin/env python3
"""A Kodonfészek adattábláinak előállítása (data/*.csv).

Futtatás a kodonfeszek mappából:  python3 scripts/build_data.py

A kodonokból számolt oszlopokat (hexagram, trigramok, komplementer,
kötés-trigram, néma vonalak, próba) a szkript számolja ki; a szöveges
táblák (fogalmak, vonalhelyek, szintek) adatként szerepelnek benne.
Csak a Python standard könyvtárát használja.
"""
import csv
import itertools
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# --- A genetikai kód (standard), UCAG-sorrendben -------------------------
B = "UCAG"
AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODE = {a + b + c: AAS[i * 16 + j * 4 + k]
        for i, a in enumerate(B) for j, b in enumerate(B) for k, c in enumerate(B)}
A3 = {"F": ("Phe", "fenilalanin"), "L": ("Leu", "leucin"), "S": ("Ser", "szerin"),
      "Y": ("Tyr", "tirozin"), "*": ("Stop", "stopjel"), "C": ("Cys", "cisztein"),
      "W": ("Trp", "triptofán"), "P": ("Pro", "prolin"), "H": ("His", "hisztidin"),
      "Q": ("Gln", "glutamin"), "R": ("Arg", "arginin"), "I": ("Ile", "izoleucin"),
      "M": ("Met", "metionin"), "T": ("Thr", "treonin"), "N": ("Asn", "aszparagin"),
      "K": ("Lys", "lizin"), "V": ("Val", "valin"), "A": ("Ala", "alanin"),
      "D": ("Asp", "aszparaginsav"), "E": ("Glu", "glutaminsav"), "G": ("Gly", "glicin")}
HYD = set("FLIMV")


def group(a):
    if a in "AVLIPFMWG":
        return "apoláris"
    if a in "STCYNQ":
        return "poláris"
    if a in "KRH":
        return "bázikus (+)"
    if a in "DE":
        return "savas (−)"
    return "stop"


# --- I Ching ----------------------------------------------------------------
# Trigram kódja: alsó vonal a legnagyobb helyiérték (1. vonal * 4 + 2. * 2 + 3.)
TRI = {7: ("☰", "Ég", "Qian"), 6: ("☱", "Tó", "Dui"), 5: ("☲", "Tűz", "Li"),
       4: ("☳", "Mennydörgés", "Zhen"), 3: ("☴", "Szél", "Xun"), 2: ("☵", "Víz", "Kan"),
       1: ("☶", "Hegy", "Gen"), 0: ("☷", "Föld", "Kun")}
ORD = [7, 4, 2, 1, 0, 3, 5, 6]  # Wen király-tábla sor/oszlop sorrendje
KW = [[1, 25, 6, 33, 12, 44, 13, 10], [34, 51, 40, 62, 16, 32, 55, 54],
      [5, 3, 29, 39, 8, 48, 63, 60], [26, 27, 4, 52, 23, 18, 22, 41],
      [11, 24, 7, 15, 2, 46, 36, 19], [9, 42, 59, 53, 20, 57, 37, 61],
      [14, 21, 64, 56, 35, 50, 30, 38], [43, 17, 47, 31, 45, 28, 49, 58]]
PY = ["Qian", "Kun", "Zhun", "Meng", "Xu", "Song", "Shi", "Bi", "Xiao Chu", "Lü", "Tai", "Pi",
      "Tong Ren", "Da You", "Qian", "Yu", "Sui", "Gu", "Lin", "Guan", "Shi He", "Bi", "Bo", "Fu",
      "Wu Wang", "Da Chu", "Yi", "Da Guo", "Kan", "Li", "Xian", "Heng", "Dun", "Da Zhuang", "Jin",
      "Ming Yi", "Jia Ren", "Kui", "Jian", "Xie", "Sun", "Yi", "Guai", "Gou", "Cui", "Sheng", "Kun",
      "Jing", "Ge", "Ding", "Zhen", "Gen", "Jian", "Gui Mei", "Feng", "Lü", "Xun", "Dui", "Huan",
      "Jie", "Zhong Fu", "Xiao Guo", "Ji Ji", "Wei Ji"]
ZH = ("乾 坤 屯 蒙 需 訟 師 比 小畜 履 泰 否 同人 大有 謙 豫 隨 蠱 臨 觀 噬嗑 賁 剝 復 無妄 大畜 頤 大過 "
      "坎 離 咸 恆 遯 大壯 晉 明夷 家人 睽 蹇 解 損 益 夬 姤 萃 升 困 井 革 鼎 震 艮 漸 歸妹 豐 旅 巽 兌 "
      "渙 節 中孚 小過 既濟 未濟").split()
HU = ["A teremtő", "A befogadó", "Kezdeti nehézség", "Ifjúi balgaság", "Várakozás", "Viszály",
      "A sereg", "Összetartás", "A kicsi szelídítő ereje", "Fellépés", "Béke", "Pangás",
      "Közösség az emberekkel", "Nagy birtoklás", "Szerénység", "Lelkesedés", "Követés",
      "A megromlott helyrehozása", "Közeledés", "Szemlélődés", "Átharapás", "Kecsesség",
      "Szétesés", "Visszatérés", "Ártatlanság", "A nagy szelídítő ereje", "Táplálás",
      "A nagy túlsúlya", "A mélység", "A tapadó", "Hatás", "Tartósság", "Visszavonulás",
      "A nagy ereje", "Haladás", "A fény elsötétülése", "A család", "Ellentét", "Akadály",
      "Felszabadulás", "Csökkenés", "Gyarapodás", "Áttörés", "Találkozás", "Gyülekezés",
      "Felemelkedés", "Szorongattatás", "A kút", "Forradalom", "Az üst", "A felrázó",
      "A nyugalom", "Fokozatos fejlődés", "A férjhez menő leány", "Bőség", "A vándor",
      "A szelíd", "A derűs", "Szétoszlás", "Korlátozás", "Belső igazság", "A kicsi túlsúlya",
      "Beteljesülés után", "Beteljesülés előtt"]
GL = ["teremtő erő, kitartó cselekvés", "befogadás, odaadó követés", "nehéz kezdet, csírázás",
      "tapasztalatlanság, tanulás", "türelmes várakozás", "vita, peres ügy",
      "fegyelem, szervezett sokaság", "összefogás, szövetség",
      "a kis erő visszatart, finom fékezés", "óvatos lépés, helyes viselkedés",
      "béke, ég és föld összhangja", "megrekedés, elzáródás", "közösség, egyetértés",
      "bőséges birtoklás", "szerénység", "lelkesedés, készenlét", "követés, alkalmazkodás",
      "a megromlott helyrehozása", "közeledés, felügyelet", "szemlélődés, rálátás",
      "átharapás, az akadály eltávolítása", "díszítés, kecsesség", "lehámlás, szétesés",
      "visszatérés, fordulópont", "ártatlanság, a váratlan", "a nagy erő felhalmozása",
      "táplálás, gondoskodás", "túlterhelés, a nagy túlsúlya", "mélység, ismétlődő veszély",
      "tapadó fény, világosság", "kölcsönös hatás, vonzás", "tartósság, állandóság",
      "visszavonulás", "a nagy ereje", "haladás, felkelő nap", "a fény elsötétülése",
      "család, háznép", "ellentét, eltávolodás", "akadály, nehéz út",
      "feloldás, megkönnyebbülés", "csökkenés, lemondás", "gyarapodás",
      "áttörés, határozott döntés", "váratlan találkozás", "gyülekezés", "felemelkedés",
      "szorongatottság, kimerülés", "kút, közös forrás", "gyökeres változás",
      "üst, átalakítás és táplálás", "megrázkódtatás, mennydörgés", "nyugalom, megállás",
      "fokozatos fejlődés", "a férjhez menő leány, alárendelt helyzet", "bőség, tetőpont",
      "vándor, úton lét", "szelíd behatolás, szél", "derű, öröm", "szétoszlás, feloldódás",
      "korlátozás, mérték", "belső igazság, bizalom", "a kicsi túlsúlya, apró lépések",
      "beteljesülés után, rend", "beteljesülés előtt, átmenet"]
POET = {"UUU": "Az elsőként megfejtett kodon (1961, poli-U → fenilalanin); csupa jin: A befogadó.",
        "AAA": "Csupa jang: A teremtő. A poli-A a korai kísérletekben lizint adott.",
        "CCC": "12. Pangás: a prolin megtöri a fehérjék α-hélixét.",
        "GGG": "11. Béke, a CCC (12. Pangás) teljes ellentéte: Tai–Pi pár."}

# --- A modell kiosztása: bázis -> (gyűrű, amino) -------------------------------
# Alsó trigram = a három bázis gyűrűbitje (purin 1, pirimidin 0),
# felső trigram = az amino-bitjük (amino 1, keto 0); az i. bázis az (i, i+3) vonalpár.
BIT = {"A": (1, 1), "G": (1, 0), "C": (0, 1), "U": (0, 0)}
CP = {"A": "U", "U": "A", "G": "C", "C": "G"}


def lines(c, bit=BIT):
    r = [bit[b] for b in c]
    return [r[0][0], r[1][0], r[2][0], r[0][1], r[1][1], r[2][1]]


def tri(l):
    return l[0] * 4 + l[1] * 2 + l[2], l[3] * 4 + l[4] * 2 + l[5]


def hexnum(l):
    lo, up = tri(l)
    return KW[ORD.index(up)][ORD.index(lo)]


def bond(c):
    return [1 if b in "GC" else 0 for b in c]


def kep(lo, up):
    if lo == up:
        return "Kettőzött " + TRI[up][1].lower()
    nev = TRI[lo][1].lower()
    return f"{TRI[up][1]} {'az' if nev[0] in 'aáeéiíoóöőuúüű' else 'a'} {nev} fölött"


def write(name, header, rows):
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def kodonok():
    rows = []
    for c in CODE:
        a = CODE[c]
        l = lines(c)
        lo, up = tri(l)
        n = hexnum(l)
        inv = hexnum([1 - x for x in l])
        rc = "".join(CP[b] for b in reversed(c))
        c6 = c[:2] + {"U": "C", "C": "U", "A": "G", "G": "A"}[c[2]]
        bb = bond(c)
        bt = bb[0] * 4 + bb[1] * 2 + bb[2]
        rows.append([
            c, A3[a][0], n, PY[n - 1], HU[n - 1], kep(lo, up),
            f"{TRI[lo][0]} {TRI[lo][1]}", f"{TRI[up][0]} {TRI[up][1]}", group(a),
            "start" if c == "AUG" else ("stop" if a == "*" else ""), A3[a][1], c.replace("U", "T"),
            "".join(map(str, l)), f"{inv}. {PY[inv - 1]} – {HU[inv - 1]}",
            f"{rc} ({A3[CODE[rc]][0]}) → {hexnum(lines(rc))}. {PY[hexnum(lines(rc)) - 1]}",
            "igen" if c[1] == "U" else "nem",
            "néma" if CODE[c6] == a else f"számít ({c6} → {A3[CODE[c6]][0]})",
            POET.get(c, ""), f"{TRI[bt][0]} {TRI[bt][1]}", 6 + sum(bb)])
    write("kodonok.csv",
          ["Kodon (RNS)", "Aminosav", "Hexagram", "Pinyin", "Magyar név", "Kép",
           "Alsó trigram (gyűrűszál)", "Felső trigram (amino-szál)", "Csoport", "Jel",
           "Aminosav neve", "Kodon (DNS)", "Vonalak 1→6", "Szemközti szál (錯, 1. szint)",
           "Másik szál saját irányban", "Középső bázis U (2. szint: víztaszító)",
           "6. vonal (2. szint)", "Költői megjegyzés (3. szint)",
           "Kötés-trigram (két szálon közös, 1. szint)", "Hidrogénkötések"], rows)


def hexagramok():
    by = {hexnum(lines(c)): c for c in CODE}
    rows = [[n, chr(0x4DC0 + n - 1), ZH[n - 1], PY[n - 1], HU[n - 1], GL[n - 1], by[n],
             A3[CODE[by[n]]][0]] for n in range(1, 65)]
    write("hexagramok.csv", ["Szám", "Jel", "Írásjegy", "Pinyin", "Magyar név",
                             "Hagyományos jelentés röviden", "Kodon (alapkiosztás)", "Aminosav"], rows)


def trigramok():
    tul = {7: "erős, teremtő", 6: "derűs, örvendező", 5: "tapadó, világos", 4: "felrázó, mozgató",
           3: "szelíd, behatoló", 2: "mély, veszélyes", 1: "nyugvó, megálló", 0: "befogadó, odaadó"}
    rows = []
    for v in [7, 6, 5, 4, 3, 2, 1, 0]:
        bits = [(v >> 2) & 1, (v >> 1) & 1, v & 1]
        rows.append([TRI[v][0], TRI[v][1], TRI[v][2], "".join(map(str, bits)), tul[v],
                     "–".join("purin" if x else "pirimidin" for x in bits),
                     "–".join("amino" if x else "keto" for x in bits),
                     f"{TRI[7 - v][0]} {TRI[7 - v][1]}"])
    write("trigramok.csv", ["Jel", "Név", "Pinyin", "Vonalak alulról", "Hagyományos tulajdonság",
                            "Alsó trigramként: gyűrűminta", "Felső trigramként: amino-minta",
                            "Fu Xi-ellenpár (inverz)"], rows)


def bazisok():
    write("bazisok.csv", ["Bázis", "Típus", "Gyűrűk", "Amino / keto", "Alsó vonal (gyűrű)",
                          "Felső vonal (amino)", "Párja", "Hidrogénkötések"],
          [["A (adenin)", "purin", 2, "amino", "jang", "jang", "T (DNS) / U (RNS)", 2],
           ["G (guanin)", "purin", 2, "keto", "jang", "jin", "C", 3],
           ["C (citozin)", "pirimidin", 1, "amino", "jin", "jang", "G", 3],
           ["T (timin, DNS) / U (uracil, RNS)", "pirimidin", 1, "keto", "jin", "jin", "A", 2]])


def sensitivity():
    """Pozíciónként: a pontmutációk hány százaléka cserél aminosavat (stop nélküli kodonokon)."""
    out = []
    for p in range(3):
        s = n = 0
        for c, a in CODE.items():
            if a == "*":
                continue
            for x in B:
                if x != c[p]:
                    n += 1
                    s += CODE[c[:p] + x + c[p + 1:]] == a
        out.append(round(100 * (1 - s / n), 1))
    return out


def vonalhelyek():
    s1, s2, s3 = sensitivity()
    write("vonalhelyek.csv",
          ["Vonal", "Hagyományos helyérték", "Trigram", "Bázis és tulajdonság",
           "Mutációs érzékenység (%)", "Spidron (mozgó modell)", "Szint", "Mi tény, mi megállapodás"],
          [[1, "Kezdet, rejtett alap", "alsó", "1. bázis: gyűrű (purin jang, pirimidin jin)", s1,
            "1. kar; szemben a 4. kar (egy bázis)", "2. helyzeti",
            "Tény: az érzékenység a kódból számolt. Megállapodás: hogy az 1. bázis az 1. és 4. vonal."],
           [2, "Alsó közép, helyénvaló (中)", "alsó",
            "2. bázis: gyűrű. Ha a középső bázis U (2. és 5. vonal jin), az aminosav víztaszító", s2,
            "2. kar, a 2–5. tengelyen: átforduláskor mozdulatlan", "2. helyzeti",
            "Tény: középső U esetén 16-ból 16 kodon víztaszító. Megállapodás: hogy a középső bázis "
            "a 2. és 5. vonal; a hagyomány „közép” fogalmával való egyezés ebből adódik."],
           [3, "Átmenet, bizonytalan hely", "alsó", "3. bázis: gyűrű; lötyögő (wobble) párosodás", s3,
            "3. kar: gyengén remeg", "2. helyzeti",
            "Tény: a 3. vonal átfordítása 34 kodonnál néma. Megállapodás: a vonal helye."],
           [4, "Átlépés a külsőbe", "felső", "1. bázis: amino (jang) / keto (jin)", s1,
            "4. kar; szemben az 1. kar", "2. helyzeti", "Ugyanaz, mint az 1. vonalnál."],
           [5, "Felső közép, uralkodó (中)", "felső", "2. bázis: amino / keto", s2,
            "5. kar, a 2–5. tengelyen: mozdulatlan", "2. helyzeti", "Ugyanaz, mint a 2. vonalnál."],
           [6, "Túl a helyzeten, a bölcs", "felső", "3. bázis: amino / keto; 64-ből 60 esetben néma", s3,
            "6. kar: erősen remeg", "2. helyzeti",
            "Tény: a 6. vonal átfordítása 60 kodonnál néma. Megállapodás: a vonal helye; "
            "négy rokon kiosztásban ugyanez a 3. vonalra esik."]])


def proba():
    """A 24 lehetséges bázis–(gyűrű, amino) kiosztás próbája, és a véletlen kódok próbája."""
    cods = list(CODE)
    order = [(1, 1), (1, 0), (0, 1), (0, 0)]

    def props(m, cd=CODE):
        inv = {v: k for k, v in m.items()}
        s1 = all(m[CP[b]] == (1 - m[b][0], 1 - m[b][1]) for b in B)
        f6 = {b: inv[(m[b][0], 1 - m[b][1])] for b in B}
        f3 = {b: inv[(1 - m[b][0], m[b][1])] for b in B}
        n6 = sum(cd[c] == cd[c[:2] + f6[c[2]]] for c in cods)
        n3 = sum(cd[c] == cd[c[:2] + f3[c[2]]] for c in cods)
        mid = inv[(0, 0)]
        s3 = all(cd[c] in HYD for c in cods if c[1] == mid)
        return s1, n6, n3, mid, s3

    rows = []
    for perm in itertools.permutations(order):
        m = dict(zip("AGCU", perm))
        s1, n6, n3, mid, s3 = props(m)
        label = " ".join(f"{b}={m[b][0]}{m[b][1]}" for b in "AGCU")
        rows.append([label, "igen" if s1 else "nem", n6, n3, mid, "igen" if s3 else "nem",
                     int(s1) + int(n6 == 60) + int(s3), "a modell kiosztása" if m == BIT else ""])
    rows.sort(key=lambda r: (-r[6], r[7] == ""))
    write("proba_kiosztasok.csv",
          ["Kiosztás (alsó, felső vonal)", "Komplementer = teljes ellentét", "6. vonal néma (64-ből)",
           "3. vonal néma (64-ből)", "A „00” bázis", "Közép 00 → mindig víztaszító",
           "Teljesülő állítás (3-ból)", "Megjegyzés"], rows)

    random.seed(1)
    vals = list(CODE.values())
    N = 20000
    n6s, mh = [], 0
    for _ in range(N):
        random.shuffle(vals)
        cd = dict(zip(cods, vals))
        _, n6, _, _, s3 = props(BIT, cd)
        n6s.append(n6)
        mh += s3
    write("proba_veletlen_kodok.csv", ["Mérőszám", "Érték"],
          [["Keverések száma", N], ["6. vonal néma, átlag", round(sum(n6s) / N, 2)],
           ["6. vonal néma, legnagyobb", max(n6s)], ["6. vonal néma ≥ 60", sum(x >= 60 for x in n6s)],
           ["„Középső U mindig víztaszító” teljesült", mh],
           ["Valódi kód: 6. vonal néma", props(BIT)[1]], ["Valódi kód: középső U víztaszító", "16/16"]])


def inzulin_ellenorzes():
    """Az inzulin kódoló szakasza lefordítva egyezik-e a preproinzulin ismert sorrendjével."""
    seq = open(os.path.join(DATA, "inzulin_cds_rns.txt")).read().strip()
    prot = "".join(CODE[seq[i:i + 3]] for i in range(0, len(seq), 3))
    known = ("MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPL"
             "ALEGSLQKRGIVEQCCTSICSLYQLENYCN*")
    assert prot == known, "az inzulinszekvencia nem a várt fehérjét adja"
    return len(seq) // 3


if __name__ == "__main__":
    kodonok()
    hexagramok()
    trigramok()
    bazisok()
    vonalhelyek()
    proba()
    print("Mutációs érzékenység (1., 2., 3. pozíció, %):", sensitivity())
    print("Inzulin: kodonok száma a stoppal együtt:", inzulin_ellenorzes())
    print("Kész: data/*.csv")
