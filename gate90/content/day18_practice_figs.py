import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

def ladder(ax,L=2.5,th=30):
    t=np.radians(th); A=(L*np.cos(t),0); B=(0,L*np.sin(t))
    hatch_ground(ax,-0.1,A[0]+0.8,-0.08,size=0.14); hatch_wall(ax,-0.08,-0.08,B[1]+0.6,left=True,size=0.14)
    member(ax,A,B,lw=3); joint(ax,*A,0.07); joint(ax,*B,0.07)
    return A,B
# Q5: rod AB (0.5 m) with A on the floor and B on the wall, at 30 deg to the floor
fig,ax=new(3.2,2.2)
A,B=ladder(ax)
arrow(ax,A[0]+0.12,0.12,A[0]+0.75,0.12); label(ax,A[0]+0.45,0.32,"2 m/s",fs=8)
angarc(ax,A[0],0,0.45,150,180,"30°",fs=8,lr=0.65)
label(ax,A[0]+0.05,-0.3,"A",fs=9); label(ax,0.2,B[1]+0.1,"B",fs=9)
label(ax,1.35,0.95,"AB = 0.5 m",fs=8,ha="left")
fin(fig,ax,-0.5,3.4,-0.5,1.95,"d18p_q5.png")
# S5: instantaneous centre I
fig,ax=new(3.2,2.4)
A,B=ladder(ax)
I=(A[0],B[1]); dline(ax,A,I); dline(ax,B,I); ax.plot(*I,"o",ms=5,color=K); label(ax,I[0]+0.15,I[1]+0.12,"I",fs=10,fontweight="bold")
arrow(ax,A[0]+0.12,0.12,A[0]+0.75,0.12); label(ax,A[0]+0.45,0.32,"vA",fs=8)
arrow(ax,0.15,B[1]-0.05,0.15,B[1]-0.75); label(ax,0.35,B[1]-0.5,"vB",fs=8,ha="left")
label(ax,A[0]+0.05,-0.3,"A",fs=9); label(ax,-0.3,B[1],"B",fs=9)
label(ax,1.1,B[1]+0.25,"IB = L cos 30°",fs=7); label(ax,A[0]+0.12,0.75,"IA = L sin 30°",fs=7,ha="left")
fin(fig,ax,-0.6,3.6,-0.5,2.0,"d18p_s5.png")
# Q12: horizontal engine at 120 deg from IDC
fig,ax=new(3.8,2.0)
A,B=slider_crank(ax,1.0,5.0,120)
ax.plot([0,0.9],[0,0],color=K,lw=0.6,ls="--")
angarc(ax,0,0,0.4,0,120,"120°",fs=8,lr=0.62)
label(ax,-0.42,0.08,"O",fs=9); label(ax,A[0]-0.2,A[1]+0.15,"A",fs=9); label(ax,B[0]-0.2,0.45,"B",fs=9,va="bottom")
label(ax,-0.8,0.45,"r = 100 mm",fs=7.5,ha="right"); label(ax,2.4,0.85,"l = 500 mm",fs=7.5)
arrow(ax,B[0]+1.9,0,B[0]+0.42,0); label(ax,B[0]+1.5,0.32,"F = 20 kN",fs=7.5,va="bottom")
fin(fig,ax,-2.0,B[0]+2.3,-0.7,1.4,"d18p_q12.png")
# Q14: epicyclic, sun 20, planets 20, annulus 60
fig,ax=new(3.0,3.0)
epicyclic(ax,20,20,60,m=0.065)
label(ax,0,-3.0,"S = sun (20 T)   P = planets (20 T)\nA = annulus (60 T, internal)",fs=7,va="top")
fin(fig,ax,-3.1,3.1,-3.6,3.1,"d18p_q14.png")
