import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P1 heat Q received at constant T on T-s, with T0 line
fig,ax=new(3.4,2.6)
ts_axes(ax,2.8,2.3)
T,T0=1.7,0.6; a,b=0.6,2.0
ax.add_patch(Rectangle((a,T0),b-a,T-T0,fc="#f3d9d9",ec="none")); ax.add_patch(Rectangle((a,0),b-a,T0,fc="#dddddd",ec="none"))
ax.plot([a,b],[T,T],color=K,lw=1.6); arrow(ax,1.2,T,1.4,T,lw=1.2)
ax.plot([a,a],[0,T],color=K,lw=0.6,ls=":"); ax.plot([b,b],[0,T],color=K,lw=0.6,ls=":")
ax.plot([0,2.5],[T0,T0],color=K,lw=0.9,ls="--"); label(ax,2.55,T0,"T₀",fs=9,ha="left")
label(ax,-0.06,T,"T",fs=9,ha="right")
label(ax,1.3,1.15,"X",fs=10); label(ax,1.3,0.3,"Y",fs=10)
label(ax,1.3,T+0.15,"heat Q received at T",fs=7.5)
fin(fig,ax,-0.35,3.0,-0.2,2.55,"d40p_q1.png")

# P11 adiabatic air compressor
fig,ax=new(3.4,2.0)
ax.add_patch(Polygon([[1.0,0.9],[2.2,0.5],[2.2,-0.5],[1.0,-0.9]],closed=True,fc="#e8e8e8",ec=K,lw=1.5))
label(ax,1.55,0,"compressor\n(adiabatic)",fs=7)
ax.add_patch(Rectangle((0.2,-0.75),0.8,0.22,fc="#dbe9f6",ec=K,lw=1.1)); arrow(ax,-0.2,-0.64,0.3,-0.64,lw=1.2)
label(ax,0.35,-1.05,"(1) 100 kPa, 300 K",fs=7.5)
ax.add_patch(Rectangle((2.2,0.15),0.8,0.22,fc="#dbe9f6",ec=K,lw=1.1)); arrow(ax,2.8,0.26,3.3,0.26,lw=1.2)
label(ax,2.75,0.62,"(2) 600 kPa, 550 K",fs=7.5)
ax.plot([0.3,1.0],[0.2,0.2],color=K,lw=3); arrow(ax,-0.2,0.2,0.4,0.2,lw=1.4); label(ax,-0.1,0.42,"W",fs=9)
fin(fig,ax,-0.5,3.6,-1.25,1.05,"d40p_q11.png")
