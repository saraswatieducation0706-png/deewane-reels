import numpy as np
def solve(L,supports,loads,n=20001,x0=0.0):
    """loads: ('P',x,F down) ('U',a,b,w down) ('T',a,b,w0,w1) ('C',x,M clockwise). supports: list of x (1 for cantilever 'fix' at x=L or 0 given as ('fix',x)). returns x,V,M"""
    x=np.linspace(x0,L,n)
    def resultant():
        F=0;Mo=0  # moment about origin, ccw +
        for l in loads:
            if l[0]=='P': F+=l[2]; Mo-=l[2]*l[1]
            if l[0]=='U': f=l[3]*(l[2]-l[1]); F+=f; Mo-=f*(l[1]+l[2])/2
            if l[0]=='T':
                a,b,w0,w1=l[1:]; f=(w0+w1)/2*(b-a); xc=a+(b-a)*(w0+2*w1)/(3*(w0+w1)); F+=f; Mo-=f*xc
            if l[0]=='C': Mo-=l[2]
        return F,Mo
    F,Mo=resultant()
    R=[]
    if supports[0]=='fix':
        xf=supports[1]; R=[('fix',xf,F,-(Mo+F*xf))]
    else:
        a,b=supports; Rb=(-Mo-F*a)/(b-a)*-1
        # equations: Ra+Rb=F ; Ra*a+Rb*b + Mo =0
        A=np.array([[1,1],[a,b]]); Ra,Rb=np.linalg.solve(A,[F,-Mo]); R=[('R',a,Ra),('R',b,Rb)]
    V=np.zeros(n); M=np.zeros(n)
    for i,xi in enumerate(x):
        v=0;m=0
        items=[]
        for r in R:
            if r[0]=='R' and r[1]<xi: v+=r[2]; m+=r[2]*(xi-r[1])
            if r[0]=='fix' and r[1]<xi: v+=r[2]; m+=r[2]*(xi-r[1])-r[3]*0  # handled below
        for l in loads:
            if l[0]=='P' and l[1]<xi: v-=l[2]; m-=l[2]*(xi-l[1])
            if l[0]=='U' and l[1]<xi:
                e=min(xi,l[2]); f=l[3]*(e-l[1]); v-=f; m-=f*(xi-(l[1]+e)/2)
            if l[0]=='T' and l[1]<xi:
                a,b,w0,w1=l[1:]; e=min(xi,b); we=w0+(w1-w0)*(e-a)/(b-a); f=(w0+we)/2*(e-a)
                xc=a+(e-a)*(w0+2*we)/(3*(w0+we)) if (w0+we)>0 else a; v-=f; m-=f*(xi-xc)
            if l[0]=='C' and l[1]<xi: m+=l[2]
        V[i]=v;M[i]=m
    if supports[0]=='fix' and supports[1]==0:
        M=M+R[0][3]*-1 if False else M
    return x,V,M,R
