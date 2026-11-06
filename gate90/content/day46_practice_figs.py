import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
RED="#D7191F"; BLUE="#2B6CB0"
def resistor(ax,p,q,txt,fs=9.5,dy=0.24):
    spring(ax,p,q,n=4,w=0.09,lead=0.12,lw=1.1); label(ax,(p[0]+q[0])/2,p[1]+dy,txt,fs=fs)
def node(ax,x,y,txt,dy=-0.26,fs=10): ax.plot(x,y,"o",color=K,ms=4); label(ax,x,y+dy,txt,fs=fs)

# P4 sphere inside a cubical box (front view)
fig,ax=new(2.4,2.1)
ax.add_patch(Rectangle((0,0),1.5,1.5,fill=False,ec=K,lw=1.4))
ax.plot([0,0.35,1.85,1.5],[1.5,1.85,1.85,1.5],color=K,lw=1.0); ax.plot([1.85,1.85],[1.85,0.35],color=K,lw=1.0); ax.plot([1.5,1.85],[0,0.35],color=K,lw=1.0)
ax.add_patch(Circle((0.75,0.75),0.3,fc="#cccccc",ec=K,lw=1.2))
arrow(ax,0.45,0.75,1.05,0.75,lw=0.8,both=True); label(ax,0.75,1.18,"d = 0.2 m",fs=7)
hdim(ax,0,1.5,-0.2,"0.5 m",above=False,fs=7.5)
label(ax,0.75,0.3,"sphere (1)",fs=7); label(ax,1.0,1.68,"box (2)",fs=7)
fin(fig,ax,-0.2,2.0,-0.5,2.0,"d46p_q4.png")

# P5 two long parallel plates with crossed and uncrossed strings
fig,ax=new(2.6,2.2)
ax.add_patch(Rectangle((0,1.5),1.5,0.08,fc="#999999",ec=K,lw=1.0)); ax.add_patch(Rectangle((0,-0.08),1.5,0.08,fc="#999999",ec=K,lw=1.0))
ax.plot([0,1.5],[0,1.5],color=RED,lw=0.9,ls="--"); ax.plot([1.5,0],[0,1.5],color=RED,lw=0.9,ls="--")
ax.plot([0,0],[0,1.5],color=BLUE,lw=0.9,ls=":"); ax.plot([1.5,1.5],[0,1.5],color=BLUE,lw=0.9,ls=":")
label(ax,0.75,1.75,"plate 1, width w",fs=7); label(ax,0.75,-0.27,"plate 2, width w",fs=7)
vdim(ax,1.85,0,1.5,"h = w",side="right",fs=7.5)
label(ax,0.75,1.2,"crossed",fs=6.5,color=RED); label(ax,-0.1,0.75,"uncrossed",fs=6.5,color=BLUE,rotation=90,ha="right")
fin(fig,ax,-0.45,2.5,-0.45,1.95,"d46p_q5.png")

# S7 radiation network for two surfaces
fig,ax=new(4.0,1.0)
node(ax,0,0,"Eb1"); resistor(ax,(0,0),(1.2,0),"(1−ε₁)/(ε₁A₁)")
node(ax,1.2,0,"J₁"); resistor(ax,(1.2,0),(2.4,0),"1/(A₁F₁₂)")
node(ax,2.4,0,"J₂"); resistor(ax,(2.4,0),(3.6,0),"(1−ε₂)/(ε₂A₂)")
node(ax,3.6,0,"Eb2")
arrow(ax,1.4,-0.32,2.2,-0.32,lw=0.9,color=RED); label(ax,1.8,-0.5,"q₁₂",fs=9.5,color=RED)
fin(fig,ax,-0.3,3.9,-0.6,0.4,"d46p_s7.png")

# S11 balanced counter-flow temperature profiles
fig,ax=new(3.2,2.1)
arrow(ax,0,0,2.8,0,lw=1.0); arrow(ax,0,0,0,1.9,lw=1.0)
label(ax,2.85,-0.12,"x",fs=8,ha="left"); label(ax,-0.08,1.9,"T",fs=8,ha="right")
sy=0.012
ax.plot([0,2.4],[140*sy,80*sy],color=RED,lw=1.8); ax.plot([0,2.4],[100*sy,40*sy],color=BLUE,lw=1.8)
label(ax,-0.06,140*sy,"140",fs=7,ha="right"); label(ax,2.46,80*sy,"80",fs=7,ha="left")
label(ax,-0.06,100*sy,"100",fs=7,ha="right"); label(ax,2.46,40*sy,"40",fs=7,ha="left")
label(ax,0.5,1.74,"oil",fs=7.5,color=RED); label(ax,0.95,0.5,"water (flows ←)",fs=7.5,color=BLUE)
arrow(ax,1.6,62*sy,1.6,98*sy,lw=0.8,both=True); label(ax,1.3,0.22,"ΔT = 40 °C at every section",fs=6.5)
fin(fig,ax,-0.45,3.6,-0.25,2.0,"d46p_s11.png")
