import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P12 spring-mass on a smooth floor
fig,ax=new(3.4,1.6)
hatch_wall(ax,0,0,0.9,left=True); hatch_ground(ax,0,3.2,0)
spring(ax,(0,0.35),(1.6,0.35)); block(ax,1.95,0.35,0.7,0.6,"2 kg")
label(ax,0.8,0.72,"k = 800 N/m",fs=8)
ax.plot([1.95,1.95],[0.75,1.05],color=K,lw=0.6,ls="--"); arrow(ax,1.95,0.95,2.55,0.95,lw=1.1); label(ax,2.62,0.95,"x",fs=9,ha="left")
label(ax,2.9,0.35,"smooth",fs=7.5)
fin(fig,ax,-0.4,3.4,-0.25,1.2,"d39p_q12.png")

# P14 rod, ends at zero, initial sine profile
fig,ax=new(3.6,1.9)
ax.add_patch(Rectangle((0,0),3,0.3,fc="#f3d9d9",ec=K,lw=1.4))
hatch_wall(ax,0,-0.25,0.55,left=True); hatch_wall(ax,3,-0.25,0.55,left=False)
xs=np.linspace(0,3,60); ax.plot(xs,0.45+0.5*np.sin(np.pi*xs/3),color=K,lw=1.2,ls="--")
label(ax,1.5,1.12,"u(x, 0) = sin πx",fs=8)
label(ax,-0.1,0.75,"u = 0",fs=8,ha="right"); label(ax,3.1,0.75,"u = 0",fs=8,ha="left")
arrow(ax,0,-0.45,3,-0.45,lw=0.9,both=True); label(ax,1.5,-0.62,"L = 1",fs=9)
fin(fig,ax,-0.8,3.8,-0.8,1.3,"d39p_q14.png")
