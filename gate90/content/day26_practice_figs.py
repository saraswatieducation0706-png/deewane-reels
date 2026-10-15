import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
# P1 shaft on bearings A and B (600 mm apart), pulley at C 200 mm from A, belt tensions both vertically down
fig,ax=new(3.6,2.2)
shaft(ax,-0.3,6.3,0,lw=3)
for xb,t in ((0,"A"),(6,"B")):
    ax.add_patch(Rectangle((xb-0.25,-0.55),0.5,0.4,fc="white",ec=K,lw=1.1,hatch="////"))
    ax.add_patch(Rectangle((xb-0.25,0.15),0.5,0.4,fc="white",ec=K,lw=1.1,hatch="////"))
    label(ax,xb,0.85,t,fs=9)
ax.add_patch(Rectangle((1.75,-1.0),0.5,2.0,fc="#dddddd",ec=K,lw=1.3,zorder=3)); label(ax,2.0,1.25,"C (pulley, Ø 400)",fs=7.5)
arrow(ax,1.85,-1.0,1.85,-2.3); arrow(ax,2.15,-1.0,2.15,-2.3)
label(ax,1.6,-1.9,"T₁ = 6.75 kN",fs=7.5,ha="right"); label(ax,2.4,-1.9,"T₂ = 2.25 kN",fs=7.5,ha="left")
hdim(ax,0,2,-2.85,"200",above=False,fs=8); hdim(ax,2,6,-2.85,"400",above=False,fs=8)
ext(ax,0,-0.6,0,-2.95); ext(ax,6,-0.6,6,-2.95); ext(ax,2,-2.35,2,-2.95)
label(ax,4.6,-1.0,"dimensions in mm",fs=7)
fin(fig,ax,-0.8,6.8,-3.3,1.5,"d26p_q1.png")
# P11 simple band brake: drum r = 200 mm, band ends on the lever 80 mm apart, tight end at fulcrum O, effort P at 600 mm from O
from math import hypot, atan2, acos, degrees
def tang(x,y,side):
    D=hypot(x,y); ph=atan2(y,x); a=acos(1/D); c=[ph+a,ph-a]
    return max(c,key=lambda t:side*np.cos(t))
yl=-1.0
for _ in range(60):   # choose lever level so that the lap angle is 270 deg
    ta=tang(-0.2,yl,-1); tb=tang(0.2,yl,1); lap=degrees((ta-tb))%360
    yl += -0.01 if lap>270 else 0.01
fig,ax=new(3.4,2.9)
ax.add_patch(Circle((0,0),1.0,fc="#eeeeee",ec=K,lw=1.3)); joint(ax,0,0,0.05)
t=np.linspace(tb,ta+2*np.pi if ta<tb else ta,200); t=np.linspace(ta,tb+2*np.pi,200) if tb<ta else t
aa=np.linspace(tb,ta if ta>tb else ta+2*np.pi,200)
ax.plot(1.04*np.cos(aa),1.04*np.sin(aa),color=K,lw=2.2)
ax.plot([1.04*np.cos(ta),-0.2],[1.04*np.sin(ta),yl],color=K,lw=2.2); ax.plot([1.04*np.cos(tb),0.2],[1.04*np.sin(tb),yl],color=K,lw=2.2)
member(ax,(-3.0,yl),(0.45,yl),lw=3.5)
pin(ax,0.2,yl-0.05,0.35); joint(ax,-0.2,yl,0.045); label(ax,0.62,yl-0.12,"O",fs=9,ha="left")
arrow(ax,-3.0,yl+0.9,-3.0,yl+0.06); label(ax,-3.0,yl+1.05,"P",fs=9)
omega(ax,0,0,0.55,"",ccw=False,a0=40,a1=140); label(ax,0,0.75,"cw",fs=8)
hdim(ax,-3.0,0.2,yl-0.85,"600",above=False,fs=8); ext(ax,-3.0,yl-0.1,-3.0,yl-0.95); ext(ax,0.2,yl-0.35,0.2,yl-0.95)
hdim(ax,-0.2,0.2,yl+0.55,"80",above=True,fs=7); ext(ax,-0.2,yl+0.05,-0.2,yl+0.65); ext(ax,0.2,yl+0.05,0.2,yl+0.65)
label(ax,1.2,0.95,"drum Ø 400",fs=8,ha="left"); label(ax,1.2,0.55,"band, lap 270°",fs=8,ha="left")
fin(fig,ax,-3.5,2.5,yl-1.2,1.4,"d26p_q11.png")
print("lever level",yl,"lap",lap)
