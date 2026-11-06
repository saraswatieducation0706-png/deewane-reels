"""Day 65 (Operations Research) practice figures. Usage: python3 day65_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
WB=dict(fc="white",ec="none",pad=0.6)

def aoa(ax,N,acts,r=0.22,fs=8,off=0.27):
    """activity-on-arrow network: N = {id:(x,y)}, acts = [(i,j,text,side)], side +1 = label left of the arrow"""
    for k,(x,y) in N.items():
        ax.add_patch(Circle((x,y),r,fc="white",ec=K,lw=1.3,zorder=5)); ax.text(x,y,str(k),fontsize=fs+1,ha="center",va="center",zorder=6)
    for i,j,t,side in acts:
        (x1,y1),(x2,y2)=N[i],N[j]; L=np.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/L,(y2-y1)/L
        ax.annotate("",xy=(x2-ux*r,y2-uy*r),xytext=(x1+ux*r,y1+uy*r),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.2,mutation_scale=11),zorder=3)
        mx,my=(x1+x2)/2,(y1+y2)/2; nx,ny=-uy*side,ux*side
        ax.text(mx+nx*off,my+ny*off,t,fontsize=fs,ha="center",va="center",bbox=WB,zorder=4)

# Q8 project network (activity on arrow)
N={1:(0,0),2:(1.6,1.1),3:(1.6,-1.3),4:(3.3,0),5:(4.9,1.1),6:(6.4,0)}
acts=[(1,2,"A, 5",1),(1,3,"B, 2",-1),(2,4,"C, 6",-1),(3,4,"D, 8",1),(2,5,"E, 4",1),(4,6,"F, 5",1),(5,6,"G, 9",1),(3,6,"H, 10",-1)]
fig,ax=new(4.8,2.4); aoa(ax,N,acts)
ax.text(5.6,-1.55,"activity, duration (days)",fontsize=7,ha="center",va="center",color="#444444")
ax.set_xlim(-0.35,6.75); ax.set_ylim(-1.8,1.5); save(fig,F+"d65p_q8.png")

# S1 graphical LP
fig,ax=new(3.6,3.0); ax.set_aspect("auto")
ax.add_patch(Polygon([(0,0),(7,0),(6,2),(3,5),(0,6)],closed=True,fc="#dde8f3",ec="none"))
ax.plot([0,8],[8,0],color=K,lw=1.1); ax.plot([0,10],[6,8/3],color=K,lw=1.1); ax.plot([2.5,7],[9,0],color=K,lw=1.1)
arrow(ax,0,0,10.2,0,lw=0.9); arrow(ax,0,0,0,9.8,lw=0.9)
ax.text(10.2,-0.3,"x",fontsize=9,ha="right",va="top"); ax.text(-0.3,9.8,"y",fontsize=9,ha="right",va="top")
ax.text(0.45,8.0,"x + y = 8",fontsize=7.5,ha="left",va="bottom")
ax.text(9.0,2.55,"x + 3y = 18",fontsize=7.5,ha="center",va="top")
ax.text(2.85,9.05,"2x + y = 14",fontsize=7.5,ha="left",va="center")
ax.text(-0.2,6,"(0, 6)",fontsize=7.5,ha="right",va="center"); ax.text(6.35,2.05,"(6, 2)",fontsize=7.5,ha="left",va="bottom")
ax.text(7,-0.3,"(7, 0)",fontsize=7.5,ha="center",va="top")
for px,py in [(0,6),(3,5),(6,2),(7,0)]: ax.plot(px,py,"o",color=K,ms=3.5,zorder=5)
ax.plot([3.1,5.4],[5.1,6.4],color=K,lw=0.5); ax.text(5.5,6.4,"optimum (3, 5)\nZ = 21",fontsize=7.5,ha="left",va="center")
ax.text(2.2,2.0,"feasible\nregion",fontsize=7.5,ha="center",va="center")
ax.set_xlim(-1.6,10.6); ax.set_ylim(-0.9,9.9); ax.axis("off"); save(fig,F+"d65p_s1.png")
