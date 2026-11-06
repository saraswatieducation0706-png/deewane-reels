"""Day 70 (TOM, Vibrations & MD Revision) practice figures. Usage: python3 day70_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q5 reverted compound gear train (schematic side view)
fig,ax=new(3.8,2.9)
shaft(ax,-0.3,1.05,0); shaft(ax,0.45,2.65,1.6); shaft(ax,1.55,3.3,0)
shaft_gear(ax,0.8,0,0.4,"",w=0.18); shaft_gear(ax,0.8,1.6,1.2,"",w=0.18)
shaft_gear(ax,2.3,1.6,0.45,"",w=0.18); shaft_gear(ax,2.3,0,1.15,"",w=0.18)
label(ax,0.8,-0.62,"A (20)",fs=8); label(ax,0.55,2.55,"B (60)",fs=8,ha="right")
label(ax,2.55,2.25,"C",fs=8,ha="left"); label(ax,2.55,-0.95,"D",fs=8,ha="left")
bearing(ax,0.1,0); bearing(ax,1.5,1.6); bearing(ax,3.0,0)
arrow(ax,-0.9,0,-0.35,0,lw=1.1); label(ax,-0.95,0.25,"input",fs=7.5,ha="left")
arrow(ax,3.35,0,3.9,0,lw=1.1); label(ax,3.35,0.25,"output",fs=7.5,ha="left")
fin(fig,ax,-1.0,4.0,-1.35,3.05,"d70p_q5.png")

# Q9 compound pendulum: uniform rod pivoted 0.25 m from its top end
fig,ax=new(2.2,3.0)
hatch_ground(ax,-0.6,0.6,0.45,down=False,size=0.12)
ax.plot([0,0],[0.45,0.0],color=K,lw=1.4)
ax.add_patch(Rectangle((-0.06,-1.0+0.25),0.12,1.0,fc="#dddddd",ec=K,lw=1.2,zorder=3))
ax.add_patch(Circle((0,0),0.05,fc="white",ec=K,lw=1.2,zorder=5)); label(ax,-0.2,0.05,"O",fs=9)
ext(ax,0.08,0.25,0.5,0.25); ext(ax,0.08,0,0.5,0); ext(ax,0.08,-0.75,0.5,-0.75)
vdim(ax,0.42,0,0.25,"",side="right"); label(ax,0.52,0.125,"0.25 m",fs=7.5,ha="left")
vdim(ax,0.42,-0.75,0,"0.75 m",side="right",fs=7.5)
ax.plot([0,-0.25],[0,-0.68],color=K,lw=0.8,ls="--"); angarc(ax,0,0,0.45,-90,-110,"θ",fs=8,lr=0.58)
fin(fig,ax,-0.75,1.2,-0.9,0.65,"d70p_q9.png")
