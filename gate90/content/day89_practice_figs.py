"""Day 89 (Final Formula Revision) practice figures. Usage: python3 day89_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# S5 Mohr's circle for sx = 50, sy = -10, txy = 40 MPa (scaled 1 unit = 10 MPa)
fig,ax=new(3.4,2.8)
c,R=mohr(ax,5.0,-1.0,4.0)
label(ax,5.0+0.15,-4.0-0.3,"X (50, 40)",fs=7.5,ha="left"); label(ax,-1.0-0.15,4.0+0.3,"Y (−10, −40)",fs=7.5,ha="right")
label(ax,c+R+0.1,-0.75,"σ₁ = 70",fs=7.5,ha="left"); label(ax,c-R-0.1,-0.75,"σ₂ = −30",fs=7.5,ha="right")
ax.add_patch(Circle((c,0),0.08,fc=K)); label(ax,c+0.25,0.5,"C (20, 0)",fs=7.5,ha="left")
ax.plot([c,c],[0,-R],color=K,lw=0.8); label(ax,c+0.15,-R+0.9,"R = 50",fs=7.5,ha="left")
label(ax,7.6,-5.6,"stresses in MPa",fs=7,ha="right")
fin(fig,ax,-4.6,8.4,-6.7,6.6,"d89p_s5.png")

# S9 fillet weld section: leg s and throat t = s cos 45° = 0.707 s
fig,ax=new(3.0,2.2)
ax.add_patch(Rectangle((0,0),3.0,0.5,fc="#dddddd",ec=K,lw=1.2))      # lower plate
ax.add_patch(Rectangle((1.2,0.5),1.8,0.5,fc="#dddddd",ec=K,lw=1.2))  # upper plate (lapped)
s=0.5
ax.add_patch(Polygon([[1.2,0.5],[1.2-s,0.5],[1.2,0.5+s]],closed=True,fc="#777777",ec=K,lw=1.2))
# throat: from root (1.2,0.5) perpendicular to the weld face
fx,fy=1.2-s/2,0.5+s/2
ax.plot([1.2,fx],[0.5,fy],color="white",lw=1.2,ls="--")
ext(ax,1.2-s,0.5,1.2-s,-0.32); ext(ax,1.2,0.5,1.2,-0.32); hdim(ax,1.2-s,1.2,-0.25,"s",above=False,fs=8); vdim(ax,1.32,0.5,0.5+s,"s",side="right",fs=8)
label(ax,-0.05,1.2,"throat t = 0.707 s",fs=7.5,ha="left"); arrow(ax,0.45,1.1,fx-0.05,fy-0.03,lw=0.7)
fin(fig,ax,-0.1,3.1,-0.55,1.35,"d89p_s9.png")
print("ok")
