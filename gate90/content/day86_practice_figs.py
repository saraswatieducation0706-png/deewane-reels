"""Day 86 (Formula Sprint: Maths & GA) practice figures. Usage: python3 day86_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
import numpy as np
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q6 contour |z - 2i| = 1.5 in the complex plane, poles at 0, 2i, -2i
fig,ax=new(2.9,3.3)
ax.set_aspect("equal")
arrow(ax,-2.6,0,2.7,0,lw=1.0); arrow(ax,0,-2.8,0,4.2,lw=1.0)
label(ax,2.75,-0.25,"Re z",fs=8,ha="right"); label(ax,0.15,4.15,"Im z",fs=8,ha="left")
th=np.linspace(0,2*np.pi,300); R=1.5
ax.plot(R*np.cos(th),2+R*np.sin(th),color=K,lw=1.5)
# anticlockwise direction arrow on the circle (at angle 0 going up)
a=np.radians(-10); b=np.radians(12)
ax.annotate("",xy=(R*np.cos(b),2+R*np.sin(b)),xytext=(R*np.cos(a),2+R*np.sin(a)),
            arrowprops=dict(arrowstyle="-|>",color=K,lw=1.4,mutation_scale=12))
label(ax,1.85,2.0,"C",fs=10,ha="left")
for (px,py,t,dx) in [(0,0,"0",-0.2),(0,2,"2i",0.2),(0,-2,"−2i",0.2)]:
    ax.plot(px,py,marker="x",color=K,ms=7,mew=1.6,zorder=5)
    label(ax,px+dx,py-0.28 if py!=2 else py+0.25,t,fs=8.5,ha="right" if dx<0 else "left")
# radius
ax.plot([0,-R*np.cos(np.radians(45))],[2,2+R*np.sin(np.radians(45))],color=K,lw=0.7,ls="--")
label(ax,-0.95,2.55,"1.5",fs=8)
fin(fig,ax,-2.7,2.9,-2.9,4.4,"d86p_q6.png")
print("ok")
