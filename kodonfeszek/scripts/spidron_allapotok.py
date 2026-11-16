"""A spidronfészek 64 övenkénti hajtásállapota: merev megoldás és ütközésvizsgálat.

Modell: a hatszögek csúcsai felváltva +a_n és -a_n magasságban (3-szoros forgásszimmetria),
övenként két merev megoldás: a belső hatszög ugyanolyan vagy ellentétes előjelű váltakozással,
ami az öv +delta vagy -delta irányú elfordulásának felel meg (Erdély 0/1 jele).
"""
import itertools, json, os, numpy as np
s3=np.sqrt(3)

def step(R,a,sgn):
    """Belső amplitúdó és többletcsavarás a választott irányban (sgn=+1/-1)."""
    r=R/s3
    if abs(a)<1e-15: return 0.0,0.0
    rho=np.sqrt(R*R-4*a*a)
    def F(x):
        rp=np.sqrt(r*r-4*x*x); d=np.pi/6+np.arcsin(np.clip(2*a*x/(rho*rp),-1,1))
        return rho*rho+rp*rp-2*rho*rp*np.cos(d)+(a-x)**2-r*r
    # gyök keresése felezéssel a választott előjelű félben (x*a előjele = sgn)
    lo,hi=(1e-12,r/2-1e-12)
    s=np.sign(a)*sgn
    f=lambda t:F(s*t)
    xs=np.linspace(lo,hi,400); v=[f(t) for t in xs]
    for i in range(len(xs)-1):
        if np.sign(v[i])!=np.sign(v[i+1]):
            A,B=xs[i],xs[i+1]
            for _ in range(80):
                M=(A+B)/2
                if np.sign(f(A))==np.sign(f(M)): A=M
                else: B=M
            x=s*(A+B)/2
            rp=np.sqrt(r*r-4*x*x)
            return x,np.arcsin(np.clip(2*a*x/(rho*rp),-1,1))
    return None,None

def build(a0,bits,R0=1.0):
    """Csúcsok szintenként (0..6) és háromszögek (öv, kar, típus)."""
    R,a,th=R0,a0,0.0; lev=[]
    for n in range(7):
        rho=np.sqrt(max(R*R-4*a*a,0))
        lev.append([np.array([rho*np.cos(np.radians(60-30*n-60*k)-th),rho*np.sin(np.radians(60-30*n-60*k)-th),(1 if k%2==0 else -1)*a]) for k in range(6)])
        if n<6:
            x,dth=step(R,a,1 if bits[n] else -1)
            if x is None: return None,None
            a,th,R=x,th+dth,R/s3
    V=[];idx={}
    for n in range(7):
        for k in range(6): idx[(n,k)]=len(V);V.append(lev[n][k])
    T=[]
    for n in range(6):
        for k in range(6):
            T.append((idx[(n,k)],idx[(n,(k+1)%6)],idx[(n+1,k)]))
            T.append((idx[(n,(k+1)%6)],idx[(n+1,k)],idx[(n+1,(k+1)%6)]))
    return np.array(V),T

def edge_lengths_ok(V,T,R0=1.0):
    worst=0
    for (i,j,k) in T:
        for p,q in ((i,j),(j,k),(k,i)):
            L=np.linalg.norm(V[p]-V[q]);worst=max(worst,L)
    return worst

def seg_tri(p,q,a,b,c,eps=1e-9):
    d=q-p;e1=b-a;e2=c-a;h=np.cross(d,e2);det=e1@h
    if abs(det)<1e-14: return False
    f=1/det;s=p-a;u=f*(s@h)
    if u<eps or u>1-eps: return False
    qv=np.cross(s,e1);v=f*(d@qv)
    if v<eps or u+v>1-eps: return False
    t=f*(e2@qv)
    return eps<t<1-eps

def collisions(V,T):
    n=0
    E=set()
    for t in T:
        for p,q in ((t[0],t[1]),(t[1],t[2]),(t[0],t[2])): E.add((min(p,q),max(p,q)))
    for (p,q) in E:
        for t in T:
            if p in t or q in t: continue
            if seg_tri(V[p],V[q],V[t[0]],V[t[1]],V[t[2]]): n+=1
    return n

def rigidity(V,T,R0=1.0):
    # minden élhossz egyezik-e a sík fészek élhosszával
    err=0
    for (i,j,k) in T:
        pass
    return err

if __name__=='__main__':
    # a sík fészek élhosszai referenciaként
    Vf,Tf=build(0.0,[1]*6)
    ref={}
    for t in Tf:
        for p,q in ((t[0],t[1]),(t[1],t[2]),(t[0],t[2])): ref[(min(p,q),max(p,q))]=np.linalg.norm(Vf[p]-Vf[q])
    A0=[0.03,0.06,0.10,0.14,0.18,0.22,0.245]
    res={}
    for bits in itertools.product([0,1],repeat=6):
        row=[]
        for a0 in A0:
            V,T=build(a0,bits)
            if V is None: row.append(None);continue
            err=max(abs(np.linalg.norm(V[p]-V[q])-L) for (p,q),L in ref.items())
            assert err<1e-9,(bits,a0,err)
            row.append(collisions(V,T))
        res[''.join(map(str,bits))]=row
    json.dump({'a0':A0,'res':res},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','proba','allapotok_utkozes.json'),'w'))
    free=[k for k,v in res.items() if all(x==0 for x in v)]
    print('a0 értékek:',A0)
    print('ütközésmentes minden a0-nál:',len(free))
    from collections import Counter
    for i,a0 in enumerate(A0):
        print(f'a0={a0}: ütközésmentes {sum(1 for v in res.values() if v[i]==0)}/64')
    print('példák:',{k:res[k] for k in ['000000','111111','101010','010101','110000','001111']})
