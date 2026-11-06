import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P6 symmetric I-section carrying a vertical shear force V
fig,ax=new(2.8,2.4)
B,tf,H,tw=1.6,0.22,2.0,0.18
section(ax,[(-B/2,H/2-tf,B,tf),(-B/2,-H/2,B,tf),(-tw/2,-H/2+tf,tw,H-2*tf)])
na_line(ax,-B/2-0.2,B/2+0.2,0,"N.A.",fs=8)
arrow(ax,B/2+0.75,0.55,B/2+0.75,-0.55,lw=1.5); label(ax,B/2+0.92,0.0,"V",fs=10,ha="left")
label(ax,0,H/2+0.2,"flange",fs=8); label(ax,0.35,-0.45,"web",fs=8,ha="left")
fin(fig,ax,-B/2-0.35,B/2+1.25,-H/2-0.2,H/2+0.42,"d83p_q6.png")
print("ok")
