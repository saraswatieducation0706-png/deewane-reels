"""Day 76 (IE Revision) practice figures. Usage: python3 day76_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
WB=dict(fc="white",ec="none",pad=0.6)

def aoa(ax,N,acts,r=0.22,fs=8,off=0.27):
    """activity-on-arrow network: N = {id:(x,y)}, acts = [(i,j,text,side,dashed)]"""
    for k,(x,y) in N.items():
        ax.add_patch(Circle((x,y),r,fc="white",ec=K,lw=1.3,zorder=5)); ax.text(x,y,str(k),fontsize=fs+1,ha="center",va="center",zorder=6)
    for i,j,t,side,dsh in acts:
        (x1,y1),(x2,y2)=N[i],N[j]; L=np.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/L,(y2-y1)/L
        ax.annotate("",xy=(x2-ux*r,y2-uy*r),xytext=(x1+ux*r,y1+uy*r),
                    arrowprops=dict(arrowstyle="-|>",color=K,lw=1.2,mutation_scale=11,ls="--" if dsh else "-"),zorder=3)
        mx,my=(x1+x2)/2,(y1+y2)/2; nx,ny=-uy*side,ux*side
        ax.text(mx+nx*off,my+ny*off,t,fontsize=fs,ha="center",va="center",bbox=WB,zorder=4)

# Q8 product structure tree
fig,ax=new(3.6,2.4)
def box(x,y,t): ax.add_patch(Rectangle((x-0.32,y-0.18),0.64,0.36,fc="#e8eef6",ec=K,lw=1.2,zorder=3)); label(ax,x,y,t,fs=8.5,zorder=4)
nodes={"P":(1.8,2.0),"A (2)":(0.9,1.0),"B (3)":(2.7,1.0),"C (2)":(0.4,0.0),"C (1)":(2.2,0.0),"D (2)":(3.2,0.0)}
for a,b in [("P","A (2)"),("P","B (3)"),("A (2)","C (2)"),("B (3)","C (1)"),("B (3)","D (2)")]:
    (x1,y1),(x2,y2)=nodes[a],nodes[b]; ax.plot([x1,x1,x2,x2],[y1-0.18,(y1+y2)/2,(y1+y2)/2,y2+0.18],color=K,lw=1.0)
for k,(x,y) in nodes.items(): box(x,y,k)
label(ax,-0.2,2.0,"level 0",fs=7,color="#555555"); label(ax,-0.2,1.0,"level 1",fs=7,color="#555555"); label(ax,-0.45,0.0,"level 2",fs=7,color="#555555",ha="center")
ax.set_xlim(-0.75,3.7); ax.set_ylim(-0.4,2.35); save(fig,F+"d76p_q8.png")

# S6 Gantt chart Q-S-R-T-P
fig,ax=new(4.6,1.7); ax.set_aspect("auto")
m1=[("Q",0,1),("S",1,4),("R",4,13),("T",13,23),("P",23,28)]
m2=[("Q",1,7),("S",7,15),("R",15,22),("T",23,27),("P",28,30)]
for row,y in [(m1,1.0),(m2,0.0)]:
    for j,s,e in row:
        ax.add_patch(Rectangle((s,y-0.3),e-s,0.6,fc="#dde8f3",ec=K,lw=1.0)); label(ax,(s+e)/2,y,j,fs=8)
for s,e in [(0,1),(22,23),(27,28)]: ax.add_patch(Rectangle((s,-0.3),e-s,0.6,fc="white",ec=K,lw=0.6,hatch="////"))
label(ax,-0.6,1.0,"M1",fs=8.5,ha="right"); label(ax,-0.6,0.0,"M2",fs=8.5,ha="right")
ax.plot([0,31],[-0.55,-0.55],color=K,lw=0.8)
for t in [0,4,13,23,28,30]: ax.plot([t,t],[-0.55,-0.62],color=K,lw=0.8); label(ax,t,-0.82,str(t),fs=7)
label(ax,31.5,-0.82,"h",fs=7.5,ha="left"); label(ax,25,1.55,"hatched = M2 idle",fs=7)
ax.set_xlim(-3,33); ax.set_ylim(-1.05,1.8); save(fig,F+"d76p_s6.png")

# S10 graphical LP (minimisation)
fig,ax=new(3.6,3.0); ax.set_aspect("auto")
ax.add_patch(Polygon([(0,13.5),(0,12),(2,6),(6,2),(12,0),(13.5,0),(13.5,13.5)],closed=True,fc="#dde8f3",ec="none"))
ax.plot([0,8],[8,0],color=K,lw=1.1); ax.plot([0,4],[12,0],color=K,lw=1.1); ax.plot([0,12],[4,0],color=K,lw=1.1)
ax.plot([0,6],[9,0],color=K,lw=0.8,ls="--")
arrow(ax,0,0,14,0,lw=0.9); arrow(ax,0,0,0,13.8,lw=0.9)
ax.text(14,-0.4,"x",fontsize=9,ha="right",va="top"); ax.text(-0.4,13.8,"y",fontsize=9,ha="right",va="top")
ax.text(5.4,3.4,"x + y = 8",fontsize=7.5,ha="left",va="bottom",bbox=WB)
ax.text(3.5,1.1,"3x + y = 12",fontsize=7.5,ha="left",va="center",bbox=WB)
ax.text(9.2,1.35,"x + 3y = 12",fontsize=7.5,ha="left",va="bottom",bbox=WB)
for px,py,t,ha in [(0,12,"(0, 12)  Z = 24","left"),(6,2,"(6, 2)  Z = 22","left"),(12,0,"","left")]:
    ax.plot(px,py,"o",color=K,ms=3.5,zorder=5)
    if t: ax.text(px+0.4,py+0.35,t,fontsize=7.5,ha=ha,va="bottom",bbox=WB)
ax.plot(2,6,"o",color=K,ms=4.5,zorder=5); ax.plot([2.2,4.8],[6.2,8.2],color=K,lw=0.5); ax.text(4.9,8.3,"optimum (2, 6)\nZ = 18",fontsize=7.5,ha="left",va="center",bbox=WB)
ax.text(12,-0.5,"(12, 0)",fontsize=7.5,ha="center",va="top")
ax.text(9.5,10.5,"feasible region\n(unbounded)",fontsize=7.5,ha="center",va="center")
ax.text(10.3,6.2,"dashed: Z line\n3x + 2y = 18",fontsize=7,ha="center",va="center",color="#333333")
ax.set_xlim(-1.5,14.5); ax.set_ylim(-1.4,14.2); ax.axis("off"); save(fig,F+"d76p_s10.png")

# S13 network for the activity table (activity on arrow, one dummy)
N={1:(0,0),2:(1.6,1.0),3:(1.6,-1.1),4:(3.2,0),5:(4.8,1.0),6:(6.4,0)}
acts=[(1,2,"A, 3",1,0),(1,3,"B, 4",-1,0),(2,4,"C, 5",-1,0),(2,5,"D, 6",1,0),(3,4,"",1,1),(4,5,"E, 2",-1,0),(5,6,"F, 4",1,0),(3,6,"G, 7",-1,0)]
fig,ax=new(4.6,2.4); aoa(ax,N,[(i,j,t,s,d) for i,j,t,s,d in acts]); ax.text(2.4,-0.3,"dummy",fontsize=8,ha="right",va="center")
ax.text(6.6,-1.45,"critical: A–C–E–F = 14 days",fontsize=7,ha="right",va="center")
ax.set_xlim(-0.35,6.75); ax.set_ylim(-1.7,1.5); save(fig,F+"d76p_s13.png")
