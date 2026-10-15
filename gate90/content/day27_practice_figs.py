import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def axes(ax,x1,y1):
    arrow(ax,-0.15,0,x1,0,lw=0.9); arrow(ax,0,-0.15,0,y1,lw=0.9)
    label(ax,x1+0.06,0,"x",fs=9,ha="left"); label(ax,0,y1+0.08,"y",fs=9,va="bottom")
# P10 triangle x = 0, y = 0, x + y = 1 traversed anticlockwise
fig,ax=new(2.4,2.4)
ax.add_patch(Polygon([[0,0],[1,0],[0,1]],closed=True,fc="#e6e6e6",ec=K,lw=1.6))
axes(ax,1.4,1.4)
for p,q in (((0.3,0),(0.6,0)),((0.6,0.4),(0.35,0.65)),((0,0.7),(0,0.4))): arrow(ax,p[0],p[1],q[0],q[1],lw=1.6)
label(ax,-0.08,-0.1,"O",fs=8,ha="right"); label(ax,1.0,-0.12,"(1, 0)",fs=8,va="top"); label(ax,-0.08,1.0,"(0, 1)",fs=8,ha="right")
label(ax,0.62,0.62,"x + y = 1",fs=8,ha="left"); label(ax,0.28,0.28,"R",fs=10)
fin(fig,ax,-0.6,1.6,-0.35,1.6,"d27p_q10.png")
