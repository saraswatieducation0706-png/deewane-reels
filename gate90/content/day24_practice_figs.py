import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
# P4 k1 and k2 side by side to a light plate, k3 from the plate to the mass
fig,ax=new(2.3,3.2)
hatch_ground(ax,-0.9,0.9,1.6,down=False,size=0.15)
spring(ax,(-0.4,1.6),(-0.4,0.55),n=4,w=0.11); spring(ax,(0.4,1.6),(0.4,0.55),n=4,w=0.11)
ax.plot([-0.7,0.7],[0.55,0.55],color=K,lw=2.4)
spring(ax,(0,0.55),(0,-0.55),n=4,w=0.11)
block(ax,0,-0.9,1.0,0.7,"10 kg",fs=8)
label(ax,-0.6,1.08,"k₁",fs=9,ha="right"); label(ax,0.6,1.08,"k₂",fs=9,ha="left"); label(ax,0.2,0.0,"k₃",fs=9,ha="left")
label(ax,0.8,0.55,"light plate",fs=7,ha="left")
fin(fig,ax,-1.2,1.9,-1.4,1.95,"d24p_q4.png")
# P6 solid cylinder rolling without slip, spring at the centre
fig,ax=new(3.0,1.7)
hatch_ground(ax,-0.3,3.2,0,down=True,size=0.15)
hatch_wall(ax,0,0,1.3,left=True,size=0.15)
ax.add_patch(Circle((2.2,0.6),0.6,fc="#dddddd",ec=K,lw=1.3)); joint(ax,2.2,0.6,0.05)
spring(ax,(0,0.6),(2.15,0.6),n=6,w=0.1)
label(ax,0.8,0.9,"k = 900 N/m",fs=8); label(ax,2.2,0.2,"6 kg",fs=8)
omega(ax,2.2,0.6,0.85,"",ccw=False,a0=40,a1=100); label(ax,3.05,1.35,"rolls, no slip",fs=7,ha="left")
fin(fig,ax,-0.5,4.3,-0.35,1.6,"d24p_q6.png")
