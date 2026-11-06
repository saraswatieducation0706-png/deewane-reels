"""Day 69 (EM & SOM Revision) practice figures. Usage: python3 day69_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from beamsolve import solve
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def hatch_line(ax,p,q,side=-1,size=0.12,lw=1.3):
    """surface from p to q with hatching on one side (-1 = right of the direction p->q)"""
    p,q=np.array(p,float),np.array(q,float); d=q-p; L=np.hypot(*d); u=d/L; n=np.array([-u[1],u[0]])*side
    ax.plot(*np.c_[p,q],color=K,lw=lw)
    for s in np.linspace(0.05*L,0.97*L,max(4,int(L/size))):
        a=p+s*u; b=a+size*(n*0.8-u*0.55); ax.plot(*np.c_[a,b],color=K,lw=0.7)

# Q1 sphere in a V-groove (faces at 60 deg and 30 deg to the horizontal)
fig,ax=new(3.4,2.6)
r=0.8; L=2.4
pl=(-L*np.cos(np.radians(60)),L*np.sin(np.radians(60))); pr=(L*np.cos(np.radians(30)),L*np.sin(np.radians(30)))
hatch_line(ax,pl,(0,0),side=-1,size=0.14); hatch_line(ax,(0,0),pr,side=-1,size=0.14)
c=r*np.array([0.36603,1.36603])
ax.add_patch(Circle(tuple(c),r,fc="#dddddd",ec=K,lw=1.3,zorder=4)); ax.add_patch(Circle(tuple(c),0.03,fc=K,zorder=5))
arrow(ax,c[0],c[1],c[0],c[1]-0.55,lw=1.2); label(ax,c[0]+0.2,c[1]-0.42,"W",fs=9,zorder=6)
ax.plot([0,-1.3],[0,0],color=K,lw=0.6,ls=":"); ax.plot([0,1.6],[0,0],color=K,lw=0.6,ls=":")
angarc(ax,0,0,0.55,120,180,"60°",fs=8,lr=0.85); angarc(ax,0,0,0.75,0,30,"30°",fs=8,lr=1.05)
fin(fig,ax,-1.6,2.3,-0.35,2.3,"d69p_q1.png")
# S1 free-body diagram of the sphere
fig,ax=new(2.6,2.4)
ax.add_patch(Circle((0,0),0.6,fc="#eeeeee",ec=K,lw=1.2)); ax.add_patch(Circle((0,0),0.03,fc=K))
arrow(ax,0,0,0,-1.0,lw=1.3); label(ax,0.35,-0.95,"W = 100 N",fs=7.5,ha="left")
# reaction on the 30-deg face acts along its normal, i.e. 30 deg from the vertical, pointing up-left
u1=np.array([-np.sin(np.radians(30)),np.cos(np.radians(30))]); u2=np.array([np.sin(np.radians(60)),np.cos(np.radians(60))])
arrow(ax,*(u1*0.6),*(u1*1.4),lw=1.3); label(ax,*(u1*1.4+np.array([-0.05,0.18])),"R₁ (30° face)",fs=7)
arrow(ax,*(u2*0.6),*(u2*1.4),lw=1.3); label(ax,*(u2*1.4+np.array([0.1,0.18])),"R₂ (60° face)",fs=7)
ax.plot([0,0],[0,1.2],color=K,lw=0.6,ls=":")
angarc(ax,0,0,0.85,90,120,"30°",fs=7,lr=1.02); angarc(ax,0,0,1.0,30,90,"60°",fs=7,lr=1.17)
fin(fig,ax,-1.6,1.9,-1.2,1.75,"d69p_s1.png")

# Q2 triangular truss
fig,ax=new(3.6,2.4)
A,B,C=(0,0),(6,0),(2,3)
for p,q in ((A,B),(A,C),(B,C)): member(ax,p,q,lw=2)
for p in (A,B,C): joint(ax,*p,0.12)
pin(ax,0,-0.12,0.8); roller(ax,6,-0.12,0.8)
label(ax,-0.45,0.25,"A",fs=9); label(ax,6.45,0.25,"B",fs=9); label(ax,2.4,3.25,"C",fs=9)
arrow(ax,2,4.3,2,3.15); label(ax,2,4.55,"24 kN",fs=8)
for x in (0,2,6): ext(ax,x,-0.9,x,-1.75)
hdim(ax,0,2,-1.55,"2 m",above=True,fs=7.5); hdim(ax,2,6,-1.55,"4 m",above=True,fs=7.5)
ext(ax,2.2,3,7.2,3); ext(ax,6.5,0,7.2,0); vdim(ax,7.0,0,3,"3 m",side="right",fs=7.5)
fin(fig,ax,-1.0,8.0,-1.9,4.8,"d69p_q2.png")

# Q9 simply supported beam, point load + partial UDL
fig,ax=new(4.4,2.0)
beam(ax,0,8,0.25); pin(ax,0,-0.125,0.55); roller(ax,8,-0.125,0.55)
pload(ax,2,"40 kN",y0=0.125,L=1.0,fs=8); udl(ax,4,8,"10 kN/m",y=0.125,h=0.5,fs=8)
label(ax,-0.4,0.35,"A",fs=9); label(ax,8.4,0.35,"B",fs=9)
for x in (0,2,4,8): ext(ax,x,-0.65,x,-1.2)
hdim(ax,0,2,-1.05,"2 m",above=False,fs=7.5); hdim(ax,2,4,-1.05,"2 m",above=False,fs=7.5); hdim(ax,4,8,-1.05,"4 m",above=False,fs=7.5)
fin(fig,ax,-0.8,8.8,-1.5,1.6,"d69p_q9.png")
x,V,M,R=solve(8,[0,8],[('P',2,40),('U',4,8,10)])
diagrams(F+"d69p_s9.png",8,x,V,M,vmarks=[(1,40,"+40"),(6,-20,""),(7.7,-40,"−40")],mmarks=[(2,80,"80"),(4,80,"80")],w=3.8,h=2.6)

# Q11 cantilever with a load at mid-length
fig,ax=new(3.8,1.9)
beam(ax,0,3,0.22); fixed(ax,0,left=True,h=0.9)
pload(ax,1.5,"12 kN",y0=0.11,L=0.9,fs=8)
label(ax,-0.35,0.62,"A",fs=9); label(ax,1.75,-0.3,"C",fs=9); label(ax,3.25,0,"B",fs=9)
for x in (0,1.5,3): ext(ax,x,-0.2 if x else -0.5,x,-0.95)
hdim(ax,0,1.5,-0.8,"1.5 m",above=False,fs=7.5); hdim(ax,1.5,3,-0.8,"1.5 m",above=False,fs=7.5)
label(ax,2.3,0.65,"EI = 6000 kN·m²",fs=7.5)
fin(fig,ax,-0.5,3.6,-1.25,1.35,"d69p_q11.png")
