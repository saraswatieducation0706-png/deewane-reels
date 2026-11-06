"""Day 67 (Maths Revision) practice figures. Usage: python3 day67_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# Q7 circle x^2 + y^2 = 9 traversed anticlockwise
fig,ax=new(2.8,2.8)
th=np.linspace(0,2*np.pi,300)
ax.add_patch(Circle((0,0),3,fc="#e6eef6",ec=K,lw=1.4))
arrow(ax,-4.2,0,4.4,0,lw=0.8); arrow(ax,0,-4.2,0,4.4,lw=0.8)
ax.text(4.4,-0.25,"x",fontsize=9,ha="right",va="top"); ax.text(-0.25,4.4,"y",fontsize=9,ha="right",va="top")
for a in (45,225):
    t=np.radians(a); x,y=3*np.cos(t),3*np.sin(t)
    ax.annotate("",xy=(x-0.5*np.sin(t),y+0.5*np.cos(t)),xytext=(x,y),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.4,mutation_scale=12))
ax.plot([0,3*np.cos(np.radians(-35))],[0,3*np.sin(np.radians(-35))],color=K,lw=0.8)
ax.text(1.05,-1.35,"3",fontsize=9,ha="center",va="center")
ax.text(-2.5,2.75,"C",fontsize=9.5,ha="center",va="center")
ax.set_xlim(-4.5,4.7); ax.set_ylim(-4.5,4.7); save(fig,F+"d67p_q7.png")
