import numpy as np
from spidron_allapotok import build
def creases(bits,a0=0.18):
    """Belső élek: +1 völgy (felülről nézve felfelé hajlik), -1 gerinc (hegy), 0 sík."""
    V,T=build(a0,bits);E={}
    for ti,t in enumerate(T):
        for p,q in ((t[0],t[1]),(t[1],t[2]),(t[0],t[2])): E.setdefault((min(p,q),max(p,q)),[]).append(ti)
    out={}
    for (p,q),ts in E.items():
        if len(ts)!=2: continue
        t1,t2=T[ts[0]],T[ts[1]]
        r1=[v for v in t1 if v not in(p,q)][0]; r2=[v for v in t2 if v not in(p,q)][0]
        n=np.cross(V[q]-V[p],V[r1]-V[p]); n=n if n[2]>0 else -n
        h=(V[r2]-V[p])@n/np.linalg.norm(n)
        out[(p,q)]=0 if abs(h)<1e-9 else (1 if h>0 else -1)
    return V,T,out
if __name__=='__main__':
    _,_,base=creases((1,)*6)
    for b in [(1,)*6,(0,)*6,(1,0,1,0,1,0),(1,1,1,0,0,0),(0,1,1,1,1,1)]:
        _,_,c=creases(b);d=sum(c[k]!=base[k] for k in c)
        print(''.join(map(str,b)),'hegy:',sum(v<0 for v in c.values()),'völgy:',sum(v>0 for v in c.values()),'sík:',sum(v==0 for v in c.values()),'| eltér a 111111-től:',d,'él')
    # melyik élek függenek az adott öv bitjétől?
    _,_,c0=creases((1,)*6);_,_,c1=creases((0,1,1,1,1,1))
    print('az 1. öv bitje ennyi gyűrődés irányát változtatja:',sum(c0[k]!=c1[k] for k in c0))
