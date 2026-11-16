"""A 64 állapot számításának ellenőrzései: ütközésvizsgáló kontrollja, egybevágóság, tükörpárok, csavarások."""
import numpy as np, itertools
from spidron_allapotok import build, collisions, seg_tri
# 2) különbözőek-e az állapotok (egybevágóság tükrözéssel együtt)
def sig(V):
    D=np.linalg.norm(V[:,None]-V[None],axis=2);return np.round(np.sort(D.ravel()),7)
for a0 in (0.10,0.22):
    S=[];
    for bits in itertools.product([0,1],repeat=6):
        V,_=build(a0,bits);S.append(sig(V).tobytes())
    print(f'a0={a0}: különböző alakok (forgatás és tükrözés erejéig):',len(set(S)))
# 3) a profil (|a_n| és |csavarás|) független-e a bitektől
def prof(bits,a0=0.22):
    V,_=build(a0,bits);return np.round(np.abs(V[0::6,2]),9)
P={tuple(prof(b)) for b in itertools.product([0,1],repeat=6)}
print('különböző |amplitúdó|-profilok:',len(P))
V,_=build(0.22,[1]*6);print('|a_n| szintenként (R0=1):',np.round(np.abs(V[0::6,2]),4))
from spidron_allapotok import build, collisions, step
# pozitív kontroll: két egymásba metsző háromszög
V=np.array([[0,0,0],[1,0,0],[0,1,0],[.2,.2,-.5],[.3,.3,.5],[1,1,.5.__class__(0.5)]],float)
print('pozitív kontroll (metsző pár):',collisions(V,[(0,1,2),(3,4,5)]),'| nem metsző pár:',collisions(V+np.array([[0,0,0]]*3+[[5,5,0]]*3),[(0,1,2),(3,4,5)]))
def sig(V):
    D=np.linalg.norm(V[:,None]-V[None],axis=2);return np.round(np.sort(D.ravel()),7).tobytes()
def twist(bits,a0=0.22):
    R,a,th=1.0,a0,0.0;out=[]
    for n in range(6):
        x,d=step(R,a,1 if bits[n] else -1);out.append(np.degrees(d));a,th,R=x,th+d,R/np.sqrt(3)
    return np.round(out,3)
pairs=all(sig(build(0.22,b)[0])==sig(build(0.22,tuple(1-x for x in b))[0]) for b in itertools.product([0,1],repeat=6))
print('minden állapot a bitkomplementerének tükörképe:',pairs)
print('övenkénti többletcsavarás (fok), 111111, a0=0.22:',twist((1,)*6))
print('övenkénti többletcsavarás (fok), 101010, a0=0.22:',twist((1,0,1,0,1,0)))
