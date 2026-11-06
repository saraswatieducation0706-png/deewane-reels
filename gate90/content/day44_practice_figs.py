import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
RED="#D7191F"; BLUE="#2B6CB0"

# P3 flat plate seen from above, flow along the 0.6 m side
fig,ax=new(3.4,2.0)
ax.add_patch(Rectangle((0,0),1.8,1.5,fc="#e3c770",ec=K,lw=1.2))
label(ax,0.9,0.75,"plate, 60 K\nhotter than air",fs=7)
for y in (0.3,0.75,1.2): arrow(ax,-0.75,y,-0.15,y,lw=1.1)
label(ax,-0.45,1.5,"air 4 m/s",fs=7.5)
hdim(ax,0,1.8,-0.25,"0.6 m (along flow)",above=False,fs=7)
vdim(ax,2.05,0,1.5,"0.5 m",side="right",fs=7)
fin(fig,ax,-0.9,2.8,-0.55,1.75,"d44p_q3.png")

# P7 tube with uniform heat flux
fig,ax=new(3.8,1.6)
ax.add_patch(Rectangle((0,-0.15),3.0,0.3,fc="#d6e6f5",ec=K,lw=1.2))
for x in np.linspace(0.3,2.7,7):
    arrow(ax,x,0.55,x,0.17,lw=0.9,color=RED); arrow(ax,x,-0.55,x,-0.17,lw=0.9,color=RED)
label(ax,1.5,0.7,"q″ = 20 kW/m² (uniform)",fs=7,color=RED)
arrow(ax,-0.6,0,-0.05,0,lw=1.3); label(ax,-0.35,0.18,"20 °C",fs=7.5); label(ax,-0.35,-0.2,"0.1 kg/s",fs=7)
arrow(ax,3.05,0,3.6,0,lw=1.3); label(ax,3.33,0.18,"60 °C",fs=7.5)
label(ax,1.5,0,"water, D = 30 mm",fs=7)
label(ax,1.5,-0.72,"L = ?",fs=7.5)
fin(fig,ax,-0.7,3.7,-0.85,0.85,"d44p_q7.png")

# S7 temperature along the tube (uniform heat flux): Ts and Tm parallel lines
fig,ax=new(3.4,2.2)
arrow(ax,0,0,3.0,0,lw=1.0); arrow(ax,0,0,0,2.0,lw=1.0)
label(ax,3.05,-0.12,"x",fs=8,ha="left"); label(ax,-0.08,2.0,"T",fs=8,ha="right")
ax.plot([0,2.6],[0.35,1.25],color=BLUE,lw=1.8); ax.plot([0.5,2.6],[0.95,1.75],color=RED,lw=1.8)
ax.plot([0,0.5],[0.65,0.95],color=RED,lw=1.4,ls="--")
label(ax,1.05,0.42,"Tₘ (water)",fs=7.5,color=BLUE); label(ax,1.05,1.37,"Tₛ (wall)",fs=7.5,color=RED)
label(ax,-0.08,0.35,"20",fs=7,ha="right"); label(ax,2.68,1.25,"60",fs=7,ha="left")
ax.plot([2.6,2.6],[0,1.25],color=K,lw=0.6,ls=":"); label(ax,2.6,-0.13,"L = 8.87 m",fs=7)
arrow(ax,2.2,1.12,2.2,1.6,lw=0.8,both=True); label(ax,2.28,1.36,"q″/h",fs=7,ha="left")
fin(fig,ax,-0.4,3.4,-0.3,2.15,"d44p_s7.png")

# P14 cylinder in cross-flow
fig,ax=new(3.2,1.9)
ax.add_patch(Circle((0,0),0.45,fc="#cccccc",ec=K,lw=1.3))
label(ax,0,0,"120 °C",fs=7.5)
for y in (-0.6,-0.2,0.2,0.6): arrow(ax,-1.6,y,-1.0,y,lw=1.1)
label(ax,-1.3,0.9,"air 20 °C, 8 m/s",fs=7.5)
arrow(ax,-0.45,-0.75,0.45,-0.75,lw=0.9,both=True); label(ax,0,-0.93,"D = 25 mm",fs=7.5)
ax.plot([-0.45,-0.45],[-0.05,-0.82],color=K,lw=0.5); ax.plot([0.45,0.45],[-0.05,-0.82],color=K,lw=0.5)
label(ax,0.95,0.55,"long cylinder\n(axis normal to page)",fs=7,ha="left")
fin(fig,ax,-1.8,1.9,-1.1,1.1,"d44p_q14.png")
