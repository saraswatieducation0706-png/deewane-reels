import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WATER="#d6e8f7"

# P5 triangular truss: span 4 m, height 3 m, load 30 kN at apex
fig,ax=new(3.0,2.6)
s=0.6; A=(0,0); B=(4*s,0); C=(2*s,3*s)
for p,q in ((A,B),(A,C),(B,C)): member(ax,p,q)
for p in (A,B,C): joint(ax,*p)
pin(ax,*A,0.3); roller(ax,*B,0.3)
arrow(ax,C[0],C[1]+0.75,C[0],C[1]+0.08); label(ax,C[0],C[1]+0.92,"30 kN",fs=8)
label(ax,-0.2,0.12,"A",fs=9,ha="right"); label(ax,B[0]+0.15,0.3,"B",fs=9,ha="left"); label(ax,C[0]-0.2,C[1]+0.05,"C",fs=9,ha="right")
hdim(ax,0,4*s,-0.55,"4 m",above=False)
ext(ax,0,-0.3,0,-0.6); ext(ax,4*s,-0.3,4*s,-0.6)
vdim(ax,4*s+0.55,0,3*s,"3 m",side="right"); ext(ax,C[0]+0.1,C[1],4*s+0.6,C[1]); ext(ax,B[0]+0.45,0,4*s+0.6,0)
fin(fig,ax,-0.6,4*s+1.2,-0.95,3*s+1.1,"d78p_q5.png")

# P6 cantilever with UDL and tip load
fig,ax=new(3.6,1.9)
s=1.4
beam(ax,0,2*s,t=0.16); fixed(ax,0,left=True,h=0.8)
udl(ax,0,2*s,"6 kN/m",y=0.08,h=0.4)
pload(ax,2*s,"4 kN",y0=0.08,L=0.85)
hdim(ax,0,2*s,-0.5,"2 m",above=False); ext(ax,2*s,-0.1,2*s,-0.55)
# section inset
sx,sy=2*s+0.8,-0.15
section(ax,[(sx,sy-0.35,0.35,0.7)])
label(ax,sx+0.175,sy-0.52,"100",fs=7); label(ax,sx+0.47,sy,"200",fs=7,ha="left")
label(ax,sx+0.175,sy+0.5,"section (mm)",fs=7)
fin(fig,ax,-0.4,2*s+1.55,-0.85,1.35,"d78p_q6.png")

# P10 jet striking a flat plate moving away
fig,ax=new(3.4,1.6)
ax.add_patch(Polygon([[0,-0.35],[0.7,-0.12],[0.7,0.12],[0,0.35]],closed=True,fc="#dddddd",ec=K,lw=1.2))
ax.add_patch(Rectangle((0.7,-0.12),1.6,0.24,fc=WATER,ec="none"))
ax.plot([0.7,2.3],[0.12,0.12],color="#4a7fb0",lw=0.8); ax.plot([0.7,2.3],[-0.12,-0.12],color="#4a7fb0",lw=0.8)
ax.add_patch(Rectangle((2.3,-0.6),0.1,1.2,fc="#999999",ec=K,lw=1.2))
arrow(ax,0.9,0.32,1.6,0.32,lw=1.2); label(ax,1.25,0.48,"V = 25 m/s",fs=7.5)
arrow(ax,2.55,0.0,3.15,0.0,lw=1.2); label(ax,2.85,0.18,"u = 10 m/s",fs=7.5)
label(ax,1.5,-0.3,"Ø 60 mm jet",fs=7.5)
label(ax,2.35,-0.78,"flat plate",fs=7.5)
fin(fig,ax,-0.1,3.4,-0.95,0.7,"d78p_q10.png")
print("ok")
