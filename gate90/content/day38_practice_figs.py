import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P4 two engines in series, equal efficiencies
fig,ax=new(3.0,3.4)
reservoir(ax,0,2.4,"T₁ = 1600 K"); reservoir(ax,0,0.8,"T = ?"); reservoir(ax,0,-0.8,"T₃ = 400 K")
device(ax,0,1.6,"E₁"); device(ax,0,0,"E₂")
flow(ax,0,2.18,0,1.9,"Q₁"); flow(ax,0,1.3,0,1.02,"Q"); flow(ax,0,0.58,0,0.3,"Q"); flow(ax,0,-0.3,0,-0.58,"Q₃")
arrow(ax,0.3,1.6,0.95,1.6,lw=1.3); label(ax,0.7,1.75,"W₁",fs=8); arrow(ax,0.3,0,0.95,0,lw=1.3); label(ax,0.7,0.15,"W₂",fs=8)
fin(fig,ax,-1.0,1.5,-1.15,2.75,"d38p_q4.png")

# P8 constant-v and constant-p lines on T-s
fig,ax=new(3.2,2.6)
ts_axes(ax,2.6,2.2)
s=np.linspace(0.3,2.3,50)
ax.plot(s,0.35*np.exp((s-0.3)/1.45),color=K,lw=1.5); ax.plot(s,0.35*np.exp((s-0.3)/2.1),color=K,lw=1.5,ls="--")
label(ax,2.35,1.42,"curve A",fs=8,ha="left"); label(ax,2.35,0.88,"curve B",fs=8,ha="left")
ax.add_patch(Circle((0.3,0.35),0.035,fc=K,zorder=6)); label(ax,0.25,0.5,"1",fs=9)
fin(fig,ax,-0.3,3.2,-0.2,2.45,"d38p_q8.png")

# P10 Carnot rectangle on T-s
fig,ax=new(3.4,2.6)
sx,sy=0.75,0.0024
ts_axes(ax,2.8,2.3,"S (kJ/K)","T (K)")
P=[(1,800),(3,800),(3,300),(1,300)]; Q=[(a*sx,b*sy) for a,b in P]
cycle(ax,Q,["1","2","3","4"],[(-0.1,0.12),(0.1,0.12),(0.12,-0.1),(-0.12,-0.1)])
for (a,b),(x,y) in zip(P,Q): ax.plot([x,x],[0,y],color=K,lw=0.5,ls=":")
ax.plot([0,sx],[800*sy]*2,color=K,lw=0.5,ls=":"); ax.plot([0,sx],[300*sy]*2,color=K,lw=0.5,ls=":")
label(ax,-0.05,800*sy,"800",fs=7.5,ha="right"); label(ax,-0.05,300*sy,"300",fs=7.5,ha="right")
label(ax,sx,-0.12,"1",fs=7.5); label(ax,3*sx,-0.12,"3",fs=7.5)
fin(fig,ax,-0.6,3.9,-0.3,2.55,"d38p_q10.png")

# P11 engine driving refrigerator
fig,ax=new(3.8,2.8)
reservoir(ax,-1.1,1.4,"1000 K",w=1.2); reservoir(ax,0.0,-1.0,"300 K (atmosphere)",w=3.6); reservoir(ax,1.1,1.4,"250 K",w=1.2)
device(ax,-1.1,0.2,"HE"); device(ax,1.1,0.2,"R")
flow(ax,-1.1,1.19,-1.1,0.5,"Q₁ = 100 kJ"); flow(ax,-1.1,-0.1,-1.1,-0.79,"Q₂")
flow(ax,1.1,1.19,1.1,0.5,"Q₃"); flow(ax,1.1,-0.1,1.1,-0.79,"Q₄")
arrow(ax,-0.8,0.2,0.8,0.2,lw=1.3); label(ax,0,0.38,"W",fs=9)
fin(fig,ax,-2.0,2.0,-1.35,1.75,"d38p_q11.png")
