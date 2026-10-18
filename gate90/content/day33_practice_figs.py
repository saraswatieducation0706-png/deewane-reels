import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
# P13: triangle with two lines from the apex to the base and one line parallel to the base
fig,ax=new(2.6,2.4)
for p,q in [((0,0),(4,0)),((0,0),(2,4)),((4,0),(2,4)),((2,4),(1,0)),((2,4),(3,0)),((1,2),(3,2))]:
    ax.plot([p[0],q[0]],[p[1],q[1]],color=K,lw=1.4)
ax.set_xlim(-0.2,4.2); ax.set_ylim(-0.2,4.2); save(fig,F+"d33p_q13.png")
# S11: solved circular arrangement (clockwise A C F D E B), everyone facing the centre
fig,ax=new(2.6,2.6)
ax.add_patch(Circle((0,0),1.0,fill=False,ec=K,lw=1.4))
order="ACFDEB"
for i,c in enumerate(order):
    a=np.radians(90-60*i)
    x,y=1.0*np.cos(a),1.0*np.sin(a)
    ax.add_patch(Circle((x,y),0.17,fc="#FBEAEA",ec=K,lw=1.1,zorder=5))
    label(ax,x,y,c,fs=9,zorder=6,fontweight="bold")
for c1,c2 in (("A","D"),("C","E"),("F","B")):
    i,j=order.index(c1),order.index(c2)
    a,b=np.radians(90-60*i),np.radians(90-60*j)
    ax.plot([0.8*np.cos(a),0.8*np.cos(b)],[0.8*np.sin(a),0.8*np.sin(b)],color="#999999",lw=0.8,ls="--")
t=np.radians(np.linspace(60,20,30)); ax.plot(1.42*np.cos(t),1.42*np.sin(t),color=K,lw=0.9)
arrow(ax,1.42*np.cos(t[-2]),1.42*np.sin(t[-2]),1.42*np.cos(t[-1]),1.42*np.sin(t[-1]),lw=0.9)
label(ax,1.45,1.15,"clockwise",fs=7)
label(ax,0,-1.45,"all face the centre",fs=7)
ax.set_xlim(-1.6,1.9); ax.set_ylim(-1.6,1.4); save(fig,F+"d33p_s11.png")
