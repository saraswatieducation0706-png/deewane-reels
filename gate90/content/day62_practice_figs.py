"""Day 62 (Metrology & CIM) practice figures. Usage: python3 day62_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# Q6 optical flat: curved fringes, bow a = 0.4 of the fringe spacing b
fig,ax=new(3.6,2.5)
W,b,a=3.0,0.6,0.4*0.6
ax.add_patch(Rectangle((0,0),W,5*b,fc="#f4f4f4",ec=K,lw=1.2))
xs=np.linspace(0,W,100)
for k in range(1,5):
    y0=k*b; ys=y0+a*(1-((xs-W/2)/(W/2))**2)
    ax.plot(xs,ys,color=K,lw=2.2)
# bow and spacing dimensions on fringe 2/3 (right side)
k=2; y0=k*b
ax.plot([0,W+0.25],[y0,y0],color=K,lw=0.6,ls="--")
ax.plot([W/2,W+0.25],[y0+a,y0+a],color=K,lw=0.6,ls="--")
ax.plot([W,W+0.25],[y0+b,y0+b],color=K,lw=0.6,ls="--")
arrow(ax,W+0.15,y0,W+0.15,y0+a,lw=0.8,both=True); ax.text(W+0.27,y0+a/2,"a",fontsize=8,ha="left",va="center")
arrow(ax,W+0.55,y0,W+0.55,y0+b,lw=0.8,both=True); ax.plot([W+0.25,W+0.65],[y0,y0],color=K,lw=0.6,ls="--"); ax.plot([W+0.25,W+0.65],[y0+b,y0+b],color=K,lw=0.6,ls="--")
ax.text(W+0.67,y0+b*0.72,"b",fontsize=8,ha="left",va="center")
ax.text(W/2,-0.15,"fringes seen through the optical flat   (a/b = 0.4)",fontsize=7.5,ha="center",va="top")
ax.set_xlim(-0.1,W+0.85); ax.set_ylim(-0.45,5*b+0.1); save(fig,F+"d62p_q6.png")

# Q14 three spacers in a housing with a gap G
fig,ax=new(4.4,2.1)
L=100.0; g=10.0; s=(L-g)/3          # gap exaggerated for clarity (true nominal gap 1 mm)
t=8.0; h=20.0
# housing: U-shaped section (end walls + base)
ax.add_patch(Rectangle((-t,-t),L+2*t,t,fc="#cccccc",ec=K,lw=1.2,hatch="///"))
ax.add_patch(Rectangle((-t,0),t,h+4,fc="#cccccc",ec=K,lw=1.2,hatch="///"))
ax.add_patch(Rectangle((L,0),t,h+4,fc="#cccccc",ec=K,lw=1.2,hatch="///"))
for i in range(3):
    ax.add_patch(Rectangle((i*s,0),s,h,fc="white",ec=K,lw=1.3))
    ax.text(i*s+s/2,h/2,"33.00 ± 0.02",fontsize=7,ha="center",va="center")
ax.text(3*s+g/2,h*0.55,"G",fontsize=8.5,ha="center",va="center")
ax.text(L/2,-t-2,"(not to scale)",fontsize=7,ha="center",va="top")
ext(ax,0,h+4,0,h+15); ext(ax,L,h+4,L,h+15)
hdim(ax,0,L,h+12,"100.00 ± 0.10 (housing)",fs=7.5)
ax.set_xlim(-14,L+14); ax.set_ylim(-17,h+22); save(fig,F+"d62p_q14.png")
