"""Day 80 (Formula Sprint: Mechanics & Design) practice figures. Usage: python3 day80_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q5 plane-stress element: sx = 60 (T), sy = 20 (C), txy = 30
fig,ax=new(2.8,2.8); stress_element(ax,60,-20,30,a=1.4)
fin(fig,ax,-1.9,3.2,-2.0,2.2,"d80p_q5.png")

# Q5 solution: Mohr's circle (centre 20, radius 50)
fig,ax=new(3.2,2.6); c,R=mohr(ax,60,-20,30)
label(ax,60+5,-30-7,"X (σx = 60)",fs=7,ha="left"); label(ax,-20-5,30+7,"Y (σy = −20)",fs=7,ha="right")
label(ax,c-R-2,-6,"σ₂ = −30",fs=7.5,ha="right",va="top"); label(ax,c+R+2,-6,"σ₁ = 70",fs=7.5,ha="left",va="top")
label(ax,c+4,5,"C (20, 0)",fs=7,va="bottom",ha="left")
ax.plot([c,c],[0,R],color=K,lw=0.6,ls=":"); label(ax,c+3,R+5,"τmax = R = 50",fs=7,ha="left")
fin(fig,ax,-62,110,-68,68,"d80p_s5.png")

# Q8 simple train with idler: A (20) -> B (50, idler) -> C (40)
fig,ax=new(3.8,2.0)
m=0.05; rA,rB,rC=20*m/2,50*m/2,40*m/2
xA,xB=0.0,rA+rB; xC=xB+rB+rC
gear(ax,xA,0,rA,20); gear(ax,xB,0,rB,50,fc="#eeeeee",rot=0.06); gear(ax,xC,0,rC,40,rot=0.04)
label(ax,xA,-rA-0.3,"A (20)",fs=8); label(ax,xB,-rB-0.3,"B (50), idler",fs=8); label(ax,xC,-rC-0.3,"C (40)",fs=8)
omega(ax,xA,0,rA+0.22,"400 rpm",ccw=False,a0=60,a1=170,fs=7.5,lpos=(xA-0.25,rA+0.55))
fin(fig,ax,-0.75,xC+rC+0.35,-rB-0.55,rB+0.25,"d80p_q8.png")

# Q13 k1 in series with (k2 || k3), mass 10 kg
fig,ax=new(2.4,2.9)
ax.plot([-0.9,0.9],[3.0,3.0],color=K,lw=1.5); hatch_ground(ax,-0.9,0.9,3.0,down=False,size=0.12)
spring(ax,(0,3.0),(0,2.05),n=5); label(ax,0.25,2.55,"k₁ = 6 kN/m",fs=7.5,ha="left")
ax.plot([-0.65,0.65],[2.0,2.0],color=K,lw=3.5,solid_capstyle="butt")
spring(ax,(-0.45,1.95),(-0.45,1.0),n=5); spring(ax,(0.45,1.95),(0.45,1.0),n=5)
label(ax,-0.68,1.5,"k₂",fs=8,ha="right"); label(ax,0.68,1.5,"k₃",fs=8,ha="left")
block(ax,0,0.7,1.3,0.6,"m = 10 kg",fs=7.5)
label(ax,0,-0.2,"k₂ = k₃ = 6 kN/m",fs=7.5)
fin(fig,ax,-1.3,1.6,-0.45,3.35,"d80p_q13.png")
