import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WB=dict(fc="white",ec="none",pad=0.8)

# P3 double-glazed window (section)
fig,ax=new(3.6,2.4)
G=1.0
ax.add_patch(Rectangle((0,0),0.25,1.8,fc="#cfe3f3",ec=K,lw=1.2))
ax.add_patch(Rectangle((0.25,0),G,1.8,fc="white",ec=K,lw=0.8,ls="--"))
ax.add_patch(Rectangle((0.25+G,0),0.25,1.8,fc="#cfe3f3",ec=K,lw=1.2))
R=0.5+G
label(ax,0.125,2.0,"glass",fs=7.5); label(ax,R-0.125,2.0,"glass",fs=7.5)
label(ax,0.25+G/2,0.9,"air gap\n10 mm\nk = 0.026",fs=7)
hdim(ax,0,0.25,-0.25,"4 mm",above=False,fs=7); hdim(ax,R-0.25,R,-0.25,"4 mm",above=False,fs=7)
label(ax,R/2,-0.7,"glass k = 0.78 W/m·K",fs=7)
label(ax,-0.75,1.15,"room\n22 °C",fs=8); label(ax,-0.75,0.55,"h = 10",fs=7.5)
label(ax,R+0.75,1.15,"outside\n−8 °C",fs=8); label(ax,R+0.75,0.55,"h = 40",fs=7.5)
arrow(ax,-0.45,1.55,-0.05,1.55,lw=1.0); arrow(ax,R+0.1,1.55,R+0.5,1.55,lw=1.0)
fin(fig,ax,-1.2,R+1.2,-0.9,2.2,"d41p_q3.png")

# S3 thermal circuit
def res(ax,x0,x1,y,txt):
    n=6; xs=np.linspace(x0+0.08,x1-0.08,2*n+1); ys=[y]+[y+(0.09 if i%2 else -0.09) for i in range(1,2*n)]+[y]
    ax.plot([x0,x0+0.08],[y,y],color=K,lw=1); ax.plot(xs,ys,color=K,lw=1); ax.plot([x1-0.08,x1],[y,y],color=K,lw=1)
    label(ax,(x0+x1)/2,y+0.3,txt,fs=7)
fig,ax=new(4.4,1.1)
names=["1/hᵢ","L/k glass","L/k air","L/k glass","1/hₒ"]
for i,t in enumerate(names): res(ax,i*0.9,i*0.9+0.9,0,t)
for x in [0,0.9,1.8,2.7,3.6,4.5]: ax.add_patch(Circle((x,0),0.04,fc=K))
label(ax,0,-0.3,"22 °C",fs=7.5); label(ax,4.5,-0.3,"−8 °C",fs=7.5)
fin(fig,ax,-0.3,4.8,-0.5,0.55,"d41p_s3.png")

# P10 two slabs side by side
fig,ax=new(3.0,2.4)
ax.add_patch(Rectangle((0,0.9),1.2,0.9,fc="#f3d9d9",ec=K,lw=1.3)); label(ax,0.6,1.35,"k",fs=10)
ax.add_patch(Rectangle((0,0),1.2,0.9,fc="#dbe9f6",ec=K,lw=1.3)); label(ax,0.6,0.45,"3k",fs=10)
ax.plot([0,0],[0,1.8],color=K,lw=3); ax.plot([1.2,1.2],[0,1.8],color=K,lw=3)
label(ax,-0.12,0.9,"T₁",fs=9,ha="right"); label(ax,1.32,0.9,"T₂",fs=9,ha="left")
hdim(ax,0,1.2,-0.25,"L",above=False)
label(ax,1.7,1.35,"A/2",fs=8,ha="left"); label(ax,1.7,0.45,"A/2",fs=8,ha="left")
label(ax,0.6,2.05,"T₁ > T₂",fs=8)
fin(fig,ax,-0.5,2.2,-0.6,2.25,"d41p_q10.png")

# P11 pipe with two insulation layers (cross-section)
import math
fig,ax=new(3.0,2.7)
ax.add_patch(Circle((0,0),1.0,fc="#dbe9f6",ec=K,lw=1.3))
ax.add_patch(Circle((0,0),0.75,fc="#f3d9d9",ec=K,lw=1.3))
ax.add_patch(Circle((0,0),0.5,fc="#bbbbbb",ec=K,lw=1.3))
ax.add_patch(Circle((0,0),0.03,fc=K))
label(ax,0,0.25,"pipe",fs=7)
for r,a in [(0.5,200),(0.75,250),(1.0,300)]:
    arrow(ax,0,0,r*math.cos(math.radians(a)),r*math.sin(math.radians(a)),lw=0.8)
label(ax,-0.68,-0.2,"50",fs=6.5,bbox=WB); label(ax,-0.3,-0.92,"75",fs=6.5,bbox=WB); label(ax,0.62,-1.02,"100",fs=6.5,bbox=WB)
label(ax,1.15,0.75,"k = 0.05",fs=7,ha="left"); ax.plot([0.45,1.12],[0.42,0.75],color=K,lw=0.6)
label(ax,1.15,1.05,"k = 0.1",fs=7,ha="left"); ax.plot([0.62,1.12],[0.72,1.05],color=K,lw=0.6)
label(ax,-1.1,1.1,"pipe surface 200 °C",fs=7,ha="left")
label(ax,1.15,-0.55,"outer surface\n40 °C",fs=7,ha="left")
label(ax,0,-1.3,"radii in mm",fs=7)
fin(fig,ax,-1.2,2.2,-1.45,1.3,"d41p_q11.png")

# P15 truncated cone, insulated side
fig,ax=new(3.4,1.9)
ax.add_patch(Polygon([[0,-0.7],[2.2,-0.3],[2.2,0.3],[0,0.7]],closed=True,fc="#e8e8e8",ec=K,lw=1.4))
for x in np.linspace(0.1,2.1,12):
    yt=0.7-0.4*x/2.2
    ax.plot([x,x+0.1],[yt,yt+0.12],color=K,lw=0.7); ax.plot([x,x+0.1],[-yt,-yt-0.12],color=K,lw=0.7)
label(ax,1.1,0.95,"insulated",fs=7.5)
arrow(ax,0.4,0,1.8,0,lw=1.2); label(ax,1.1,0.15,"Q",fs=8.5)
label(ax,-0.1,0,"T₁",fs=9,ha="right"); label(ax,2.3,0,"T₂",fs=9,ha="left")
label(ax,0,-0.95,"large end",fs=7); label(ax,2.2,-0.6,"small end",fs=7)
fin(fig,ax,-0.5,2.8,-1.1,1.1,"d41p_q15.png")
