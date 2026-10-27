import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P1 rigid insulated tank with paddle wheel
fig,ax=new(3.0,2.3)
ax.add_patch(Rectangle((-0.12,-0.12),2.24,1.54,fc="#e0e0e0",ec=K,lw=1.0,hatch="////"))
ax.add_patch(Rectangle((0,0),2.0,1.3,fc="#dbe9f6",ec=K,lw=1.4))
ax.plot([1.0,1.0],[0.45,1.75],color=K,lw=2)
for dx in (-0.3,0.3): ax.add_patch(Rectangle((1.0+min(dx,0),0.3),abs(dx),0.3,fc="#999999",ec=K,lw=1))
ax.add_patch(Rectangle((0.94,0.3),0.12,0.3,fc="#999999",ec=K,lw=1))
omega(ax,1.0,1.75,0.18,"",ccw=True)
label(ax,1.35,1.85,"W = 40 kJ (in)",fs=7.5,ha="left")
label(ax,0.45,1.0,"air\n0.8 kg",fs=8)
label(ax,1.0,-0.38,"rigid, insulated",fs=7.5)
fin(fig,ax,-0.3,2.9,-0.55,2.1,"d42p_q1.png")

# P5 heat engine driving a heat pump
fig,ax=new(3.8,2.6)
reservoir(ax,0,1.6,"source 900 K",w=1.4)
reservoir(ax,1.2,-0.7,"atmosphere 300 K",w=3.4,fc="#dbe9f6")
reservoir(ax,2.4,1.6,"building 350 K",w=1.4)
device(ax,0,0.45,"HE"); device(ax,2.4,0.45,"HP")
flow(ax,0,1.39,0,0.75,"Q₁",side="right"); flow(ax,0,0.15,0,-0.49,"",side="right")
flow(ax,2.4,-0.49,2.4,0.15,"",side="right"); flow(ax,2.4,0.75,2.4,1.39,"Q (to building)",side="right")
flow(ax,0.3,0.45,2.1,0.45,"",side="right"); label(ax,1.2,0.62,"W",fs=9)
fin(fig,ax,-0.9,3.9,-1.05,1.95,"d42p_q5.png")
