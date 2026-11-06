"""Day 61 (Machine Tools, NTM & Additive) practice figures. Usage: python3 day61_practice_figs.py <outdir>
The milling cutter is drawn at first contact, so it passes exactly through the corner of the work and the
approach A = sqrt(d(D - d)) is to scale."""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# Q12 slab milling: cutter D = 80 mm at first contact with a work piece 250 mm long, depth of cut d = 5 mm
D,d=80.0,5.0; A=np.sqrt(d*(D-d)); top=0.0
cx,cy=-A,top+D/2-d
assert abs(np.hypot(cx,cy-top)-D/2)<1e-9           # the cutter passes through the corner (0, top)
fig,ax=new(4.4,2.6)
ax.add_patch(Rectangle((0,-30),130,30,fc="#e4e4e4",ec=K,lw=1.2))
ax.plot([0,130],[-d,-d],color=K,lw=0.8,ls="--")
ax.text(68,-18,"work (250 mm long)",fontsize=7.5,ha="center",va="center")
ax.add_patch(Circle((cx,cy),D/2,fc="white",ec=K,lw=1.4)); ax.plot(cx,cy,"+",color=K,ms=7)
ax.plot([cx,cx],[cy,top-34],color=K,lw=0.6,ls="-.")
ax.text(cx,cy+6,"cutter\nD = 80 mm",fontsize=7.5,ha="center",va="bottom")
omega(ax,cx,cy,D/2+5,"",ccw=False,a0=100,a1=150)
hdim(ax,cx,0,top-36,"A",above=False,fs=8); ext(ax,0,0,0,-38)
ext(ax,130,-d,146,-d); ext(ax,130,0,146,0); arrow(ax,142,14,142,0,lw=0.8); arrow(ax,142,-19,142,-d,lw=0.8)
ax.text(147,9,"d = 5 mm",fontsize=7.5,ha="left",va="center")
arrow(ax,60,12,85,12,lw=1.1); ax.text(72,15,"cutter travel",fontsize=7.5,ha="center",va="bottom")
ax.set_xlim(-90,195); ax.set_ylim(-46,82); save(fig,F+"d61p_q12.png")
