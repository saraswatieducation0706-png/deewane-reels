import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
# P8 overhung disc on a cantilever shaft fixed in a rigid housing
fig,ax=new(3.0,1.9)
ax.add_patch(Rectangle((-0.6,-0.7),0.6,1.4,fc="white",ec=K,lw=1.2,hatch="////"))
shaft(ax,0,2.4,0,lw=3.0); ax.add_patch(Rectangle((2.32,-0.6),0.16,1.2,fc="#bbbbbb",ec=K,lw=1.2,zorder=4))
label(ax,2.68,0.35,"disc 8 kg",fs=8,ha="left")
hdim(ax,0,2.4,-0.95,"L = 300 mm",above=False,fs=8); ext(ax,0,-0.72,0,-1.05); ext(ax,2.4,-0.62,2.4,-1.05)
label(ax,1.2,0.25,"d = 25 mm",fs=8,va="bottom")
fin(fig,ax,-0.8,3.9,-1.45,0.9,"d22p_q8.png")
# P11 spring-mass-damper with harmonic force
fig,ax=new(2.4,2.6)
hatch_ground(ax,-0.9,0.9,-1.6,down=True,size=0.15)
spring(ax,(-0.4,-1.6),(-0.4,-0.35),n=4,w=0.12); damper(ax,(0.4,-1.6),(0.4,-0.35),w=0.17)
block(ax,0,0,1.2,0.7,"m = 20 kg",fs=8)
label(ax,-0.6,-1.0,"k",fs=9,ha="right"); label(ax,0.62,-1.0,"c",fs=9,ha="left")
arrow(ax,0,1.25,0,0.37); label(ax,0.1,1.3,"F₀ sin ωt",fs=8,ha="left")
fin(fig,ax,-1.3,1.6,-1.95,1.55,"d22p_q11.png")
