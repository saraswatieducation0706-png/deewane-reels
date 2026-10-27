import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# S3 lumped cooling curve of the copper sphere
fig,ax=new(3.6,2.3)
sx=0.0022; sy=0.008; tau=685.3
arrow(ax,0,-0.15,3.3,-0.15,lw=1.0); arrow(ax,0,-0.15,0,1.85,lw=1.0)
label(ax,3.35,-0.27,"t (s)",fs=8,ha="left"); label(ax,-0.08,1.85,"T (°C)",fs=8,ha="right")
ts=np.linspace(0,1400,200); T=25+175*np.exp(-ts/tau)
ax.plot(ts*sx,(T-25)*sy+0.2,color="#D7191F",lw=2)
y0=0.2; ax.plot([0,3.1],[y0,y0],color=K,lw=0.8,ls="--"); label(ax,3.1,y0-0.1,"T∞ = 25 °C",fs=7,ha="right")
y80=(80-25)*sy+0.2; x=793*sx
ax.plot([0,x],[y80,y80],color=K,lw=0.6,ls=":"); ax.plot([x,x],[-0.15,y80],color=K,lw=0.6,ls=":")
ax.plot(x,y80,"o",color="#D7191F",ms=4)
label(ax,-0.08,y80,"80",fs=7.5,ha="right"); label(ax,-0.08,175*sy+0.2,"200",fs=7.5,ha="right")
label(ax,x,-0.28,"793 s",fs=7.5)
label(ax,2.1,1.45,"θ/θᵢ = e^(−t/τ),  τ = 685 s",fs=7.5)
fin(fig,ax,-0.5,3.7,-0.45,2.0,"d43p_s3.png")

# P5 long rod from furnace wall
fig,ax=new(3.4,1.6)
ax.add_patch(Rectangle((-0.6,-0.6),0.6,1.2,fc="#f3d9d9",ec=K,lw=1.2,hatch="//"))
label(ax,-0.3,0.8,"furnace wall",fs=7)
ax.add_patch(Rectangle((0,-0.08),2.6,0.16,fc="#e3c770",ec=K,lw=1.1))
ax.plot([2.6,2.9],[0,0],color=K,lw=1,ls=(0,(2,2))); label(ax,3.0,0,"very long",fs=7,ha="left")
label(ax,1.6,0.35,"brass rod, D = 8 mm, k = 110 W/m·K",fs=7)
label(ax,1.3,-0.38,"air, h = 15 W/m²·K",fs=7)
label(ax,0.15,-0.7,"base 60 K above air",fs=7,ha="left")
fin(fig,ax,-0.7,3.8,-0.9,1.0,"d43p_q5.png")

# P12 semi-infinite slab
fig,ax=new(3.0,2.3)
ax.add_patch(Rectangle((0,0),2.4,1.6,fc="#e8e8e8",ec="none"))
ax.plot([0,2.4],[1.6,1.6],color="#D7191F",lw=3)
label(ax,1.2,1.82,"surface held at 80 °C",fs=7.5,color="#D7191F")
label(ax,1.75,0.35,"initially 30 °C",fs=7.5)
ax.plot([0.7],[0.95],"o",color=K,ms=4); label(ax,0.82,0.95,"T = ?",fs=8,ha="left")
vdim(ax,0.4,0.95,1.6,"60 mm",side="left",fs=7.5)
label(ax,1.2,-0.15,"x ↓ (semi-infinite)",fs=7)
fin(fig,ax,-0.6,2.6,-0.35,2.0,"d43p_q12.png")

# P14 pin fin with insulated tip
fig,ax=new(3.4,1.7)
hatch_wall(ax,0,-0.6,0.6,left=True,size=0.15)
ax.add_patch(Rectangle((0,-0.1),2.4,0.2,fc="#cccccc",ec=K,lw=1.2))
ax.add_patch(Rectangle((2.4,-0.16),0.08,0.32,fc="#888888",ec=K,lw=1))
label(ax,2.55,0.32,"insulated tip",fs=7,ha="left")
hdim(ax,0,2.4,-0.4,"L = 60 mm",above=False,fs=7.5)
label(ax,-0.12,0.75,"base 100 °C",fs=7,ha="left")
label(ax,1.2,0.38,"D = 4 mm, k = 100 W/m·K",fs=7)
label(ax,1.2,-0.95,"air 25 °C, h = 25 W/m²·K",fs=7)
fin(fig,ax,-0.4,3.6,-1.1,0.95,"d43p_q14.png")
