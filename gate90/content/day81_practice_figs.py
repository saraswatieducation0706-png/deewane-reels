import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P5 two blocks hanging over a light frictionless pulley (Atwood machine)
fig,ax=new(2.4,2.6)
yc=2.0; R=0.35
ax.plot([-0.9,0.9],[2.75,2.75],color=K,lw=1.6); hatch_ground(ax,-0.9,0.9,2.75,down=False,size=0.12)
ax.plot([0,0],[2.75,yc],color=K,lw=1.4)                       # hanger
ax.add_patch(Circle((0,yc),R,fc="#eeeeee",ec=K,lw=1.3)); ax.add_patch(Circle((0,yc),0.05,fc=K,ec=K))
yA=0.55; yB=1.05
ax.plot([-R,-R],[yc,yA+0.45],color=K,lw=1.0); ax.plot([R,R],[yc,yB+0.35],color=K,lw=1.0)
ax.add_patch(Rectangle((-R-0.28,yA-0.1),0.56,0.55,fc="#bbbbbb",ec=K,lw=1.2)); label(ax,-R,yA+0.17,"5 kg",fs=8)
ax.add_patch(Rectangle((R-0.22,yB),0.44,0.35,fc="#dddddd",ec=K,lw=1.2)); label(ax,R,yB+0.175,"3 kg",fs=8)
fin(fig,ax,-1.0,1.0,0.2,2.95,"d81p_q5.png")

# P6 compound bar: steel rod joined to a thicker brass rod, fixed at the left, pulled at the right
fig,ax=new(3.8,1.6)
L1,L2=2.0,1.0; h1,h2=0.22,0.44
hatch_wall(ax,0,-0.5,0.5,left=True,size=0.14); ax.plot([0,0],[-0.5,0.5],color=K,lw=1.6)
ax.add_patch(Rectangle((0,-h1/2),L1,h1,fc="#cccccc",ec=K,lw=1.2)); label(ax,L1/2,0.27,"steel",fs=8)
ax.add_patch(Rectangle((L1,-h2/2),L2,h2,fc="#eeeeee",ec=K,lw=1.2)); label(ax,L1+L2/2,0,"brass",fs=8)
arrow(ax,L1+L2,0,L1+L2+0.55,0,lw=1.5); label(ax,L1+L2+0.62,0.18,"20 kN",fs=8,ha="left")
y=-0.55
hdim(ax,0,L1,y,"1 m, 200 mm²",above=False,fs=7.5); hdim(ax,L1,L1+L2,y,"0.5 m, 400 mm²",above=False,fs=7.5)
ext(ax,L1,-h2/2-0.04,L1,y-0.06); ext(ax,L1+L2,-h2/2-0.04,L1+L2,y-0.06)
fin(fig,ax,-0.35,L1+L2+1.25,-1.0,0.65,"d81p_q6.png")
print("ok")
