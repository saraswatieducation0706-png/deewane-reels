"""Day 77 (Mixed PYQ Day) practice figures. Usage: python3 day77_practice_figs.py <outdir>"""
import sys,os,math; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
WB=dict(fc="white",ec="none",pad=0.6)

# S2 clock at 3:40
fig,ax=new(2.2,2.2)
ax.add_patch(Circle((0,0),1.0,fc="white",ec=K,lw=1.5))
for h in range(12):
    a=math.radians(90-30*h); ax.plot([0.88*math.cos(a),math.cos(a)],[0.88*math.sin(a),math.sin(a)],color=K,lw=1.2 if h%3==0 else 0.7)
for h,t in [(0,"12"),(3,"3"),(6,"6"),(9,"9")]:
    a=math.radians(90-30*h); label(ax,0.74*math.cos(a),0.74*math.sin(a),t,fs=7.5)
am=math.radians(90-240); ah=math.radians(90-110)
ax.plot([0,0.82*math.cos(am)],[0,0.82*math.sin(am)],color=K,lw=1.6)
ax.plot([0,0.5*math.cos(ah)],[0,0.5*math.sin(ah)],color=K,lw=2.6)
ax.add_patch(Circle((0,0),0.04,fc=K))
th=np.linspace(ah,am,40); ax.plot(0.3*np.cos(th),0.3*np.sin(th),color="#c0392b",lw=1.0)
label(ax,0.05,-0.42,"130°",fs=8,color="#c0392b",bbox=WB)
ax.set_xlim(-1.15,1.15); ax.set_ylim(-1.15,1.15); save(fig,F+"d77p_s2.png")

# Q5 ballistic pendulum
fig,ax=new(3.4,2.3)
hatch_ground(ax,0.6,2.4,2.0,down=False)
ax.plot([0.6,2.4],[2.0,2.0],color=K,lw=1.4)
ax.plot([1.1,1.1],[2.0,0.7],color=K,lw=0.9); ax.plot([1.9,1.9],[2.0,0.7],color=K,lw=0.9)
ax.add_patch(Rectangle((0.9,0.1),1.2,0.6,fc="#e3c9a3",ec=K,lw=1.3)); label(ax,1.5,0.4,"4 kg",fs=8)
ax.add_patch(Polygon([[-0.75,0.35],[-0.45,0.35],[-0.38,0.4],[-0.45,0.45],[-0.75,0.45]],closed=True,fc="#888888",ec=K,lw=0.8))
arrow(ax,-0.3,0.4,0.7,0.4,lw=1.2); label(ax,0.2,0.62,"400 m/s",fs=7.5); label(ax,-0.6,0.15,"20 g",fs=7.5)
ax.set_xlim(-1.0,3.2); ax.set_ylim(-0.1,2.35); save(fig,F+"d77p_q5.png")

# Q10 jet on a moving flat plate
fig,ax=new(3.6,1.9)
ax.add_patch(Polygon([[0,0.3],[0.7,0.3],[1.0,0.12],[1.0,-0.12],[0.7,-0.3],[0,-0.3]],closed=True,fc="#cccccc",ec=K,lw=1.2))
label(ax,0.4,0.55,"nozzle",fs=7.5)
ax.add_patch(Rectangle((1.0,-0.12),1.4,0.24,fc="#cfe3f3",ec="none"))
ax.plot([1.0,2.4],[0.12,0.12],color=K,lw=0.6); ax.plot([1.0,2.4],[-0.12,-0.12],color=K,lw=0.6)
label(ax,1.6,0.32,"Ø40 mm, V = 25 m/s",fs=7.5)
ax.add_patch(Rectangle((2.45,-0.8),0.12,1.6,fc="#888888",ec=K,lw=1.2))
for s in (1,-1):
    ax.plot([2.4,2.42],[0.12*s,0.25*s],color="#5b8db8",lw=1.0); arrow(ax,2.4,0.3*s,2.4,0.7*s,lw=0.9,color="#5b8db8")
arrow(ax,2.75,0,3.45,0,lw=1.4); label(ax,3.1,0.22,"u = 10 m/s",fs=7.5)
label(ax,2.51,-1.0,"plate",fs=7.5)
ax.set_xlim(-0.2,3.7); ax.set_ylim(-1.2,0.85); save(fig,F+"d77p_q10.png")

# Q14 top-gated mould
fig,ax=new(3.4,2.6)
ax.add_patch(Rectangle((0,0),3.0,2.2,fc="#e8dcc8",ec=K,lw=1.3))
ax.add_patch(Rectangle((0.8,0.25),1.6,0.9,fc="white",ec=K,lw=1.2)); label(ax,1.6,0.7,"cavity\n1.0 × 10⁶ mm³",fs=7.5)
ax.add_patch(Polygon([[1.45,1.15],[1.55,1.15],[1.6,2.05],[1.4,2.05]],closed=True,fc="#f2b38f",ec=K,lw=1.0))
ax.add_patch(Polygon([[1.25,2.05],[1.75,2.05],[1.9,2.45],[1.1,2.45]],closed=True,fc="#f2b38f",ec=K,lw=1.0))
label(ax,-0.1,2.62,"pouring basin",fs=7.5,ha="left"); ax.plot([0.95,1.2],[2.55,2.4],color=K,lw=0.5)
vdim(ax,3.35,1.15,2.45,"",side="right"); label(ax,3.55,1.8,"200 mm",fs=7.5,ha="left")
ax.plot([1.6,3.4],[2.45,2.45],color=K,lw=0.5,ls=":"); ax.plot([1.55,3.4],[1.15,1.15],color=K,lw=0.5,ls=":")
label(ax,0.5,1.6,"gate\n400 mm²",fs=7.5); ax.plot([0.85,1.47],[1.5,1.22],color=K,lw=0.5)
ax.set_xlim(-0.2,4.4); ax.set_ylim(-0.15,2.75); save(fig,F+"d77p_q14.png")
