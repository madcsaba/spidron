import numpy as np, itertools, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from hajtasiranyok import creases
from spidron_allapotok import build
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
W,H=A4; s3=np.sqrt(3)
def P(n,k,R0): r=R0/s3**n; a=np.radians(60-30*n-60*k); return r*np.cos(a),r*np.sin(a)
def para(c,x,y,text,size=10,lead=14,width=17*cm,font='DV'):
    c.setFont(font,size)
    for line in text.split('\n'):
        words=line.split(' ');cur=''
        for w in words:
            t=(cur+' '+w).strip()
            if pdfmetrics.stringWidth(t,font,size)>width: c.drawString(x,y,cur);y-=lead;cur=w
            else: cur=t
        c.drawString(x,y,cur);y-=lead
    return y
c=canvas.Canvas(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','proba','spidron_fesek_proba.pdf'),pagesize=A4)
c.setTitle('Spidronfészek – 64 állapot fizikai próbája')
# ---------- 1. oldal: sablon
R0=9*cm; cx,cy=W/2,H/2-1.2*cm
c.setFont('DVB',15);c.drawString(2*cm,H-2*cm,'Spidronfészek-sablon, 6 öv')
para(c,2*cm,H-2.7*cm,'Nyomtasd 100%-os méretben (méretezés nélkül). Ellenőrzés: a lenti 5 cm-es vonal pontosan 5 cm legyen. A külső kontúr mentén vágd ki, a belső kis hatszöget hagyd meg vagy vágd ki. Minden belső vonal hajtásvonal: karcold be tompa hegyű eszközzel. A pöttyös csúcsok a hatszögek „páratlan” csúcsai, a 3. oldal szerint ezek emelkednek vagy süllyednek.',9,12)
for n in range(6):
    for k in range(6):
        a,b,p,q=P(n,k,R0),P(n,k+1,R0),P(n+1,k,R0),P(n+1,k+1,R0)
        c.setStrokeColorRGB(.35,.35,.35);c.setLineWidth(.5);c.setDash(3,2)
        for u,v in((a,p),(b,p),(p,q)): c.line(cx+u[0],cy+u[1],cx+v[0],cy+v[1])
c.setDash();c.setLineWidth(1.4);c.setStrokeColorRGB(0,0,0)
for k in range(6):
    a,b=P(0,k,R0),P(0,k+1,R0);c.line(cx+a[0],cy+a[1],cx+b[0],cy+b[1])
for n in range(7):
    for k in range(0,6,2):
        x,y=P(n,k,R0);rad=max(1.3,3.2/ (s3**n))
        c.setFillColorRGB(.1,.1,.1);c.circle(cx+x,cy+y,rad,fill=1,stroke=0)
c.setFillColorRGB(0,0,0)
for n in range(4):
    x,y=(np.array(P(n,1,R0))+np.array(P(n,2,R0))+np.array(P(n+1,1,R0)))/3
    c.setFont('DVB',max(6,11-2*n));c.drawCentredString(cx+x*1.0,cy+y*1.0-3,f'{n+1}')
c.setLineWidth(1);c.line(2*cm,1.8*cm,7*cm,1.8*cm);c.line(2*cm,1.6*cm,2*cm,2.0*cm);c.line(7*cm,1.6*cm,7*cm,2.0*cm)
c.setFont('DV',8);c.drawString(2*cm,1.15*cm,'5 cm  ·  külső hatszög csúcssugara 9 cm, minden öv √3-szor kisebb az előzőnél.');c.drawString(2*cm,0.75*cm,'Az 5–6. öv papíron csak A3-as (141%-os) nyomtatással hajtható.')
c.showPage()
# ---------- 2. oldal: két minta-állapot hegy/völgy jelöléssel
c.setFont('DVB',15);c.drawString(2*cm,H-2*cm,'Hegy- és völgyhajtások két állapotra')
para(c,2*cm,H-2.7*cm,'Felülről, a nyomtatott oldal felől nézve. Piros pont-vonal: hegyhajtás (a gyűrődés feléd domborodik). Kék szaggatott: völgyhajtás (tőled elfelé). A számítás ideális, vastagság nélküli, merev lapokkal készült; papíron a hajtások csak közelítik ezt.',9,12)
def draw_state(bits,ox,oy,R):
    V,T,cr=creases(bits)
    Vf,_=build(0.0,bits)
    for (p,q),s in cr.items():
        u,v=Vf[p]*R,Vf[q]*R
        if s<0: c.setStrokeColorRGB(.8,.1,.1);c.setDash([4,1.5,1,1.5])
        else: c.setStrokeColorRGB(.1,.3,.85);c.setDash(3,2)
        c.setLineWidth(.8);c.line(ox+u[0],oy+u[1],ox+v[0],oy+v[1])
    c.setDash();c.setStrokeColorRGB(0,0,0);c.setLineWidth(1.2)
    for k in range(6):
        a,b=Vf[k]*R,Vf[(k+1)%6]*R;c.line(ox+a[0],oy+a[1],ox+b[0],oy+b[1])
    c.setFont('DVB',11);c.drawCentredString(ox,oy-R-0.8*cm,'Állapot '+''.join(map(str,bits)))
draw_state((1,)*6,W/2,H-10.2*cm,5.6*cm)
draw_state((1,0,1,0,1,0),W/2,H-22.6*cm,5.6*cm)
c.showPage()
# ---------- 3. oldal: a bitek jelentése és a próba menete
c.setFont('DVB',15);c.drawString(2*cm,H-2*cm,'A 64 állapot: mit jelentenek a bitek, és mit kell kipróbálni')
txt=('Mit mond a számítás (ideális, vastagság nélküli, merev lapok; a hatszögek csúcsai felváltva fel-le mozognak):\n'
'• Minden övnek pontosan két merev folytatása van: a belső hatszög csúcsai ugyanabban vagy ellentétes ritmusban emelkednek, mint a külsőé. Ettől az öv az egyik vagy a másik irányba fordul el (Erdély 0/1 jele). Hat öv: 2⁶ = 64 állapot.\n'
'• Mind a 64 állapot hajtható ütközés nélkül, a teljes vizsgált tartományban (a külső csúcsok emelkedése a csúcssugár 3–24,5%-a).\n'
'• A 64 állapot 32 tükörpár: egy állapot és a bitjei ellentettje egymás tükörképe.\n'
'• Az emelkedések nagysága minden állapotban ugyanaz, csak az irányuk különbözik. Ezért két állapot között csak a sík lapon át lehet váltani: kisimítás, majd újrahajtás.\n'
'• A merev modellben egyik állapotot sem tartja meg semmi: a szerkezet erőmentesen mozog. Hogy egy állapot magától megmarad-e, azt csak a valódi anyag (a hajtásvonalak és lapok merevsége) döntheti el. Ezt kell kipróbálni.\n\n'
'A bitek leolvasása, kívülről befelé:\n'
'1. A külső hatszög pöttyös csúcsait emeld meg (a pöttyteleneket süllyeszd).\n'
'2. Ha az 1. bit 1, a következő hatszög pöttyös csúcsai is emelkednek; ha 0, azok süllyednek, a pötytelenek emelkednek.\n'
'3. Így tovább: minden bit a következő hatszögnek a közvetlenül kívüle lévőhöz viszonyított ritmusát adja meg.\n\n'
'A próba menete minden állapotra:\n'
'1. Hajtsd a fészket a bitek szerint, óvatosan, a külső peremtől befelé.\n'
'2. Hajtható? Igen, ha a lapok gyűrődés és szakadás nélkül felveszik az alakot.\n'
'3. Megmarad? Engedd el a lapot 10 másodpercre, sík asztalon. Igen, ha nem ugrik át más alakba és nem simul ki.\n'
'4. Hány öv hajtható ténylegesen? A belső övek kicsik: írd fel, hányadik övig sikerült.\n'
'5. Fotózd le felülről és oldalról, a fájlnévben az állapot bitjeivel.\n\n'
'Ha egy állapot sem marad meg magától, a 64 állapotú „geometriai memória” csak külső rögzítéssel működhet. Ha többféle megmarad, az anyag kétállapotú (bistabil) viselkedése adja a memóriát, és ezt érdemes pontosan mérni.')
y=para(c,2*cm,H-2.9*cm,txt,9.5,13)
c.setFont('DV',8);c.drawString(2*cm,1.2*cm,'Számítás: kodonfeszek/scripts/spidron_allapotok.py – merev hajtás, 3-szoros forgásszimmetrikus alakok; más hajtásmódokat a modell nem vizsgál.')
c.showPage()
# ---------- 4–5. oldal: jegyzőkönyv
states=[''.join(map(str,b)) for b in itertools.product([1,0],repeat=6)]
for page in range(2):
    c.setFont('DVB',14);c.drawString(2*cm,H-2*cm,f'Jegyzőkönyv ({page+1}/2)')
    cols=['Állapot','Tükörpárja','Hajtható?','Megmarad?','Hány öv?','Megjegyzés']
    xs=[2*cm,4.2*cm,6.6*cm,8.7*cm,11.0*cm,13.0*cm,19*cm]
    y=H-3.1*cm;c.setFont('DVB',8.5)
    for i,t in enumerate(cols): c.drawString(xs[i]+2,y,t)
    c.setLineWidth(.4)
    for r,s in enumerate(states[page*32:(page+1)*32]):
        y-=0.74*cm;c.setFont('DV',9.5)
        c.drawString(xs[0]+2,y+3,s);c.drawString(xs[1]+2,y+3,''.join('1' if ch=='0' else '0' for ch in s))
        c.line(xs[0],y,xs[-1],y)
    for x in xs: c.line(x,H-2.85*cm,x,y)
    c.line(xs[0],H-2.85*cm,xs[-1],H-2.85*cm)
    c.showPage()
c.save()
print('ok')
