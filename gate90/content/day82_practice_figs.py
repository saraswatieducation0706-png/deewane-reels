"""Day 82 (Formula Sprint: Thermal) practice figures. Usage: python3 day82_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WATER="#cfe3f5"

# Q1 vertical rectangular gate in the wall of a water tank (section): top edge 1 m below the surface, 2 m high
fig,ax=new(3.0,3.2)
ax.add_patch(Rectangle((0,0),2.0,3.4,fc=WATER,ec="none"))
ax.plot([0,2.0],[3.4,3.4],color=K,lw=0.9)
ax.plot([1.45,1.75,1.6,1.45],[3.47,3.47,3.4,3.47],color=K,lw=0.8)       # free-surface mark
ax.plot([2.0,2.0],[0,0.4],color=K,lw=2.2); ax.plot([2.0,2.0],[2.4,3.9],color=K,lw=2.2)
hatch_wall(ax,2.0,0,0.4,left=False); hatch_wall(ax,2.0,2.4,3.9,left=False)
ax.plot([0,2.0],[0,0],color=K,lw=2.2); hatch_ground(ax,0,2.0,0,down=True)
ax.add_patch(Rectangle((2.0,0.4),0.1,2.0,fc="#999999",ec=K,lw=1.3,zorder=4))
label(ax,2.55,1.4,"gate\n1.5 m wide",fs=7.5,ha="left")
vdim(ax,1.3,2.4,3.4,"1 m",side="left"); vdim(ax,1.3,0.4,2.4,"2 m",side="left")
ext(ax,1.15,2.4,2.0,2.4); ext(ax,1.15,0.4,2.0,0.4)
label(ax,0.5,0.55,"Water",fs=8.5)
fin(fig,ax,-0.2,3.6,-0.3,4.0,"d82p_q1.png")

# Q4 horizontal venturimeter with mercury U-tube
fig,ax=new(3.8,2.4)
yt,yb=0.55,-0.55; rt=0.27
xs=[0,0.8,1.6,1.9,3.2,4.0]; top=[yt,yt,rt,rt,yt,yt]
ax.plot(xs,top,color=K,lw=1.4); ax.plot(xs,[-v for v in top],color=K,lw=1.4)
ax.fill_between(xs,[-v for v in top],top,color=WATER)
label(ax,0.4,0,"160 mm",fs=7.5); label(ax,1.75,0,"80 mm",fs=7)
arrow(ax,-0.6,0,-0.05,0,lw=1.2)
# tappings and U-tube
x1,x2=0.4,1.75; yb1=-1.75
for x,y0 in ((x1,-yt),(x2,-rt)): ax.plot([x-0.05,x-0.05],[y0,yb1],color=K,lw=1); ax.plot([x+0.05,x+0.05],[y0,yb1+0.0],color=K,lw=1)
ax.plot([x1-0.05,x2+0.05],[yb1-0.1,yb1-0.1],color=K,lw=1); ax.plot([x1+0.05,x2-0.05],[yb1+0.0,yb1+0.0],color=K,lw=1)
ax.plot([x1-0.05,x1-0.05],[yb1,yb1-0.1],color=K,lw=1); ax.plot([x2+0.05,x2+0.05],[yb1,yb1-0.1],color=K,lw=1)
hl,hr=-1.25,-1.55   # mercury levels: lower on inlet side (higher pressure)
ax.add_patch(Rectangle((x1-0.05,yb1-0.1),0.1,hr-(yb1-0.1),fc="#888888",ec="none"))
ax.add_patch(Rectangle((x2-0.05,yb1-0.1),0.1,hl-(yb1-0.1),fc="#888888",ec="none"))
ax.add_patch(Rectangle((x1-0.05,yb1-0.1),x2-x1+0.1,0.1,fc="#888888",ec="none"))
ax.plot([x2+0.15,x2+0.35],[hl,hl],color=K,lw=0.5); ax.plot([x1+0.05,x2+0.35],[hr,hr],color=K,lw=0.5,ls=":")
vdim(ax,x2+0.3,hr,hl,"220 mm",side="right",fs=7.5)
label(ax,1.08,-2.1,"mercury (S = 13.6)",fs=7.5)
fin(fig,ax,-0.7,4.1,-2.3,0.8,"d82p_q4.png")

# Q9 composite furnace wall
fig,ax=new(3.6,2.4)
ax.add_patch(Rectangle((0,0),0.9,1.8,fc="#e8b9a0",ec=K,lw=1.2))
ax.add_patch(Rectangle((0.9,0),0.8,1.8,fc="#f3e6c8",ec=K,lw=1.2))
label(ax,0.45,1.1,"fireclay",fs=7.5); label(ax,0.45,0.8,"k = 1.15",fs=7)
label(ax,1.3,1.1,"insul.",fs=7.5); label(ax,1.3,0.8,"k = 0.23",fs=7)
hdim(ax,0,0.9,-0.22,"230 mm",above=False,fs=7.5); hdim(ax,0.9,1.7,-0.22,"115 mm",above=False,fs=7.5)
label(ax,-0.6,1.15,"gases\n900 °C",fs=8); label(ax,-0.6,0.55,"h = 50",fs=7.5)
label(ax,2.3,1.15,"air\n30 °C",fs=8); label(ax,2.3,0.55,"h = 12",fs=7.5)
arrow(ax,-0.25,1.95,1.95,1.95,lw=1.1); label(ax,0.85,2.12,"q",fs=9)
fin(fig,ax,-1.15,2.8,-0.65,2.3,"d82p_q9.png")

# Q11 solution: counter-flow temperature profiles
fig,ax=new(3.4,2.4)
ax.plot([0,0],[0,1.6],color=K,lw=1.0); ax.plot([0,3],[0,0],color=K,lw=1.0)
s=1/100.0
ax.plot([0,3],[140*s,80*s],color="#c0392b",lw=1.6); ax.plot([0,3],[65*s,25*s],color="#2471a3",lw=1.6)
arrow(ax,1.2,(140-0.4*60)*s+0.08,1.8,(140-0.6*60)*s+0.08,lw=1.0); arrow(ax,1.8,(65-0.6*40)*s-0.09,1.2,(65-0.4*40)*s-0.09,lw=1.0)
label(ax,-0.08,1.40,"140",fs=7.5,ha="right"); label(ax,3.08,0.80,"80",fs=7.5,ha="left")
label(ax,-0.08,0.65,"65",fs=7.5,ha="right"); label(ax,3.08,0.25,"25",fs=7.5,ha="left")
ax.plot([0.15,0.15],[0.65,1.40],color=K,lw=0.6,ls="--"); label(ax,0.22,1.0,"ΔT₁ = 75",fs=7,ha="left")
ax.plot([2.85,2.85],[0.25,0.80],color=K,lw=0.6,ls="--"); label(ax,2.78,0.55,"ΔT₂ = 55",fs=7,ha="right")
label(ax,1.5,1.45,"hot",fs=7.5,color="#c0392b"); label(ax,1.5,0.15,"cold",fs=7.5,color="#2471a3")
label(ax,1.5,-0.15,"length along exchanger",fs=7.5,va="top"); label(ax,-0.35,1.6,"T (°C)",fs=7.5)
fin(fig,ax,-0.6,3.5,-0.45,1.75,"d82p_s11.png")

# Q12 concentric tube and duct (cross-section)
fig,ax=new(2.6,2.6)
ax.add_patch(Circle((0,0),1.58,fc="#bbbbbb",ec=K,lw=1.2)); ax.add_patch(Circle((0,0),1.5,fc="white",ec=K,lw=1.2))
ax.add_patch(Circle((0,0),0.5,fc="#e8b9a0",ec=K,lw=1.4))
label(ax,0,0,"tube",fs=7.5)
label(ax,0,0.75,"tube: 700 K, ε = 0.6",fs=6.5); label(ax,0,1.08,"duct: 350 K, ε = 0.4",fs=6.5)
arrow(ax,-0.5,-0.0-0.95,0.5,-0.95,lw=0.8,both=True); label(ax,0,-1.08,"0.1 m",fs=7)
arrow(ax,-1.5,-1.75,1.5,-1.75,lw=0.8,both=True); label(ax,0,-1.9,"0.3 m",fs=7,va="top")
ext(ax,-0.5,0,-0.5,-1.0); ext(ax,0.5,0,0.5,-1.0); ext(ax,-1.5,0,-1.5,-1.85); ext(ax,1.5,0,1.5,-1.85)
fin(fig,ax,-1.8,1.8,-2.2,1.7,"d82p_q12.png")
