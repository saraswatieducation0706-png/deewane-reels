import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
W="#cfe3f3"
def surface(ax,x,y,s=0.12):  # free-surface triangle symbol
    ax.add_patch(Polygon([[x,y],[x-s,y+1.4*s],[x+s,y+1.4*s]],closed=True,fill=False,ec=K,lw=0.9))
    ax.plot([x-1.5*s,x+1.5*s],[y-0.4*s,y-0.4*s],color=K,lw=0.6); ax.plot([x-0.9*s,x+0.9*s],[y-0.8*s,y-0.8*s],color=K,lw=0.6)
# S1 (solution figure) streamlines xy = C of the flow u = x, v = -y (first quadrant, stagnation point at O)
fig,ax=new(2.6,2.4)
x=np.linspace(0.12,2.6,200)
for C in (0.25,0.6,1.1,1.8):
    y=C/x; m=y<=2.6; ax.plot(x[m],y[m],color="#2b6aa0",lw=1.2)
    i=np.argmin(abs(x-np.sqrt(C)*1.25)); arrow(ax,x[i],C/x[i],x[i+6],C/x[i+6],lw=1.0,color="#2b6aa0")
arrow(ax,0,0,2.9,0,lw=0.9); arrow(ax,0,0,0,2.9,lw=0.9); label(ax,2.95,-0.15,"x",fs=8); label(ax,-0.15,2.95,"y",fs=8)
joint(ax,0,0,r=0.05); label(ax,0.12,-0.2,"O (stagnation)",fs=7,ha="left")
label(ax,1.75,1.55,"xy = C",fs=8)
fin(fig,ax,-0.4,3.2,-0.45,3.1,"d29p_s1.png")
# P9 horizontal pipe tapering from 250 mm (section 1) to 125 mm (section 2)
fig,ax=new(3.6,1.6)
pts=[[0,0.5],[1.6,0.5],[2.4,0.25],[4.0,0.25],[4.0,-0.25],[2.4,-0.25],[1.6,-0.5],[0,-0.5]]
ax.add_patch(Polygon(pts,closed=True,fc=W,ec="none"))
ax.plot([0,1.6,2.4,4.0],[0.5,0.5,0.25,0.25],color=K,lw=1.4); ax.plot([0,1.6,2.4,4.0],[-0.5,-0.5,-0.25,-0.25],color=K,lw=1.4)
ax.plot([-0.1,4.1],[0,0],color=K,lw=0.6,ls="-.")
for xx,tx in ((0.8,"1"),(3.3,"2")):
    ax.plot([xx,xx],[-0.62,0.62] if tx=="1" else [-0.37,0.37],color=K,lw=0.8,ls="--"); label(ax,xx,0.75 if tx=="1" else 0.5,tx,fs=9,fontweight="bold")
arrow(ax,0.15,0.18,0.6,0.18,lw=1.2); label(ax,0.38,-0.2,"Q",fs=8)
label(ax,0.8,-0.8,"D₁ = 250 mm\np₁ = 150 kPa",fs=7.5,va="top"); label(ax,3.3,-0.55,"D₂ = 125 mm\np₂ = ?",fs=7.5,va="top")
fin(fig,ax,-0.2,4.2,-1.35,0.95,"d29p_q9.png")
# P14 closed tank with air at 50 kPa (gauge) over water; outlet 2 m below the water surface
fig,ax=new(3.0,2.4)
ax.add_patch(Rectangle((0,0),2.0,1.6,fc=W,ec="none")); ax.add_patch(Rectangle((0,1.6),2.0,0.8,fc="#f2f2f2",ec="none"))
ax.add_patch(Rectangle((0,0),2.0,2.4,fill=False,ec=K,lw=1.5)); ax.plot([0,2.0],[1.6,1.6],color=K,lw=0.9); surface(ax,1.5,1.6)
label(ax,1.0,2.0,"air, 50 kPa (gauge)",fs=7.5); label(ax,0.7,0.8,"water",fs=8)
# outlet nozzle at the bottom right side, centre at y = 0.2 (2 m below surface: scale 0.7 unit per m)
ax.add_patch(Rectangle((2.0,0.12),0.45,0.16,fc=W,ec=K,lw=1.2)); ax.add_patch(Rectangle((1.97,0.135),0.06,0.13,fc=W,ec="none"))
arrow(ax,2.5,0.2,3.2,0.2,lw=1.3); label(ax,3.28,0.2,"jet, V = ?",fs=7.5,ha="left")
ext(ax,2.05,1.6,2.8,1.6); vdim(ax,2.7,0.2,1.6,"2 m",side="right",fs=7.5)
label(ax,0.55,2.62,"pressure gauge",fs=7,ha="left"); ax.add_patch(Circle((0.35,2.6),0.12,fc="white",ec=K,lw=1)); ax.plot([0.35,0.35],[2.4,2.48],color=K,lw=1)
hatch_ground(ax,-0.2,2.2,0,size=0.2)
fin(fig,ax,-0.4,4.3,-0.35,2.9,"d29p_q14.png")
