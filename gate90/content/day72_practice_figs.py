import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WATER="#d6e8f7"

# P4 rope wrapped 1.5 turns round a fixed post
fig,ax=new(2.6,2.6)
R=0.5
ax.add_patch(Circle((0,0),R,fc="#c8a272",ec=K,lw=1.4,zorder=3))
hatch_wall(ax,0.0,-0.18,0.18,left=True,size=0.1)
ax.add_patch(Circle((0,0),0.06,fc="white",ec=K,lw=1,zorder=5))
for r in (R+0.04,R+0.10):
    ax.add_patch(Circle((0,0),r,fill=False,ec="#555555",lw=1.6,zorder=2))
ax.plot([-R-0.07,-R-0.07],[0,-1.6],color="#555555",lw=1.8)   # load side
ax.plot([R+0.07,R+0.07],[0,-1.0],color="#555555",lw=1.8)     # hand side
block(ax,-R-0.07,-1.85,0.8,0.4,"2000 N",fs=7.5)
arrow(ax,R+0.07,-1.0,R+0.07,-1.6,lw=1.4); label(ax,R+0.2,-1.45,"P",fs=9,ha="left")
label(ax,0,0.85,"fixed post, μ = 0.25",fs=7.5)
label(ax,0,-0.95,"1.5 turns",fs=7.5)
fin(fig,ax,-1.3,1.3,-2.15,1.05,"d72p_q4.png")

# P5 overhanging beam
fig,ax=new(4.0,1.9)
s=0.6
beam(ax,0,6*s,t=0.16)
pin(ax,0,-0.08,0.3); roller(ax,4*s,-0.08,0.3)
udl(ax,0,4*s,"10 kN/m",y=0.08,h=0.4)
pload(ax,6*s,"20 kN",y0=0.08,L=0.75)
label(ax,-0.15,0.25,"A",fs=9,ha="right"); label(ax,4*s+0.15,0.25,"B",fs=9,ha="left"); label(ax,6*s+0.15,-0.2,"C",fs=9,ha="left")
y=-0.65
hdim(ax,0,4*s,y,"4 m",above=False); hdim(ax,4*s,6*s,y,"2 m",above=False)
for xx in (0,4*s): ext(ax,xx,-0.4,xx,y-0.05)
ext(ax,6*s,-0.1,6*s,y-0.05)
fin(fig,ax,-0.5,6*s+0.5,-1.0,1.25,"d72p_q5.png")
x=np.linspace(0,6,601); V=np.where(x<4,10-10*x,20.0); V[-1]=20
M=np.where(x<=4,10*x-5*x*x,-20*(6-x))
diagrams(F+"d72p_s5.png",6,x,V,M,vmarks=[(0,10,"10"),(4,-30,"−30"),(5,20,"+20")],mmarks=[(1,5,"+5"),(2,0,"0 (x = 2 m)"),(4,-40,"−40")])

# P9 tank draining through a bottom orifice
fig,ax=new(2.4,2.6)
W=1.2; H=2.0
ax.add_patch(Rectangle((-W/2,0),W,H,fc=WATER,ec="none",zorder=1))
ax.plot([-W/2,-W/2,-0.05],[2.5,0,0],color=K,lw=1.6); ax.plot([0.05,W/2,W/2],[0,0,2.5],color=K,lw=1.6)
ax.plot([-W/2,W/2],[H,H],color="#2a6fb0",lw=1.2)
ax.plot([-0.15,0.1,-0.025,-0.15],[H+0.12,H+0.12,H+0.01,H+0.12],color="#2a6fb0",lw=1.0)
ax.plot([-0.04,-0.02,-0.01],[0,-0.25,-0.6],color="#2a6fb0",lw=1.2); ax.plot([0.04,0.02,0.01],[0,-0.25,-0.6],color="#2a6fb0",lw=1.2)
label(ax,0.15,-0.35,"orifice 50 mm",fs=7,ha="left")
vdim(ax,W/2+0.2,0,H,"2 m",side="right",fs=7.5)
hdim(ax,-W/2,W/2,2.7,"1.2 m",fs=7.5)
fin(fig,ax,-0.9,1.4,-0.75,3.05,"d72p_q9.png")

# P15 activity-on-arrow network
fig,ax=new(3.6,1.8)
N={1:(0,0),2:(1.4,0.65),3:(1.4,-0.65),4:(2.8,0),5:(4.0,0)}
for k,(x,y) in N.items():
    ax.add_patch(Circle((x,y),0.18,fc="white",ec=K,lw=1.3,zorder=5)); label(ax,x,y,str(k),fs=8,zorder=6)
def act(a,b,t,off):
    p,q=np.array(N[a]),np.array(N[b]); u=(q-p)/np.hypot(*(q-p))
    arrow(ax,*(p+0.18*u),*(q-0.18*u),lw=1.2); m=(p+q)/2; label(ax,m[0]+off[0],m[1]+off[1],t,fs=8)
act(1,2,"A (4)",(-0.3,0.2)); act(1,3,"B (5)",(-0.3,-0.2)); act(2,4,"C (6)",(0.3,0.2)); act(3,4,"D (3)",(0.3,-0.2)); act(4,5,"E (2)",(0,0.18))
fin(fig,ax,-0.4,4.4,-1.0,1.0,"d72p_q15.png")
