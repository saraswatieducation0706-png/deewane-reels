import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from beamsolve import solve
F=sys.argv[1] if len(sys.argv)>1 else "fig/"
S=0.7
def fin(fig,ax,x0,x1,name,y0=-1.3,y1=1.7): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def ss_defl(L,loads,a=0,b=None,n=4001):
    b=L if b is None else b; x,V,M,_=solve(L,(a,b),loads,n=n)
    th=np.concatenate([[0],np.cumsum((M[1:]+M[:-1])/2*np.diff(x))]); y=np.concatenate([[0],np.cumsum((th[1:]+th[:-1])/2*np.diff(x))])
    ya=np.interp(a,x,y); yb=np.interp(b,x,y); return x,y-(ya+(yb-ya)*(x-a)/(b-a))
# P4 cantilever 3 m, UDL 2 kN/m + 5 kN end load
xe=3*S*1.3; fig,ax=new(3.0,1.8); beam(ax,0,xe); fixed(ax,0,left=True)
udl(ax,0,xe,"2 kN/m",lx=xe*0.4); pload(ax,xe,"5 kN",y0=0.62,L=0.6)
label(ax,0.25,-0.3,"A",fs=9); label(ax,xe+0.25,-0.05,"B",fs=9)
dim(ax,0,-0.6,xe,-0.6,"3 m"); fin(fig,ax,-0.5,xe+0.5,"d10p_q4.png",y0=-1.0,y1=1.7)
# P6 SS 6 m, 20 kN at 2 m and 4 m
fig,ax=new(3.4,1.8); beam(ax,0,6*S); pin(ax,0,-0.1,0.4); roller(ax,6*S,-0.1,0.4)
pload(ax,2*S,"20 kN"); pload(ax,4*S,"20 kN"); label(ax,-0.3,0,"A",fs=9); label(ax,6*S+0.3,0,"B",fs=9)
dim(ax,0,-0.85,2*S,-0.85,"2 m"); dim(ax,2*S,-0.85,4*S,-0.85,"2 m"); dim(ax,4*S,-0.85,6*S,-0.85,"2 m")
fin(fig,ax,-0.6,6*S+0.6,"d10p_q6.png")
x,y=ss_defl(6,[('P',2,20),('P',4,20)]); k=0.6/abs(y.min())
fig,ax=new(3.4,1.4); ax.plot([0,6*S],[0,0],color=K,lw=0.8,ls="--"); ax.plot(x*S,y*k,color=K,lw=1.8)
pin(ax,0,-0.02,0.3); roller(ax,6*S,-0.02,0.3)
arrow(ax,3*S,0.02,3*S,y.min()*k,lw=0.9,both=True); label(ax,3*S,y.min()*k-0.15,"δ = 5.11 mm",fs=8,va="top")
label(ax,3*S,0.25,"elastic curve (exaggerated)",fs=7)
fin(fig,ax,-0.4,6*S+0.4,"d10p_s6.png",y0=-1.05,y1=0.45)
# P10 overhang: AB 4 m, BC 1 m, 10 kN at C
fig,ax=new(3.2,1.8); beam(ax,0,5*S); pin(ax,0,-0.1,0.4); roller(ax,4*S,-0.1,0.4)
pload(ax,5*S,"10 kN"); label(ax,-0.3,0,"A",fs=9); label(ax,4*S+0.45,-0.3,"B",fs=9); label(ax,5*S+0.3,0,"C",fs=9)
dim(ax,0,-0.85,4*S,-0.85,"4 m"); dim(ax,4*S,-0.85,5*S,-0.85,"1 m"); fin(fig,ax,-0.6,5*S+0.6,"d10p_q10.png")
x,y=ss_defl(5,[('P',5,10)],0,4); k=0.5/abs(y.min())
fig,ax=new(3.2,1.4); ax.plot([0,5*S],[0,0],color=K,lw=0.8,ls="--"); ax.plot(x*S,y*k,color=K,lw=1.8)
pin(ax,0,-0.02,0.3); roller(ax,4*S,-0.02,0.3)
arrow(ax,5*S,0.0,5*S,y[-1]*k,lw=0.9,both=True); label(ax,5*S-0.1,y[-1]*k-0.15,"1.67 mm ↓",fs=8,ha="center",va="top")
im=np.argmax(y); label(ax,x[im]*S,y[im]*k+0.15,"span lifts up (max 1.03 mm)",fs=7)
fin(fig,ax,-0.4,5*S+0.5,"d10p_s10.png",y0=-0.95,y1=0.55)
print("ok")
