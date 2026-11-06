import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P6 slot milling with an end mill (plan view)
fig,ax=new(4.0,2.0)
L=3.0; W=1.6; D=0.48
ax.add_patch(Rectangle((0,0),L,W,fc="#e6e6e6",ec=K,lw=1.3))
ax.add_patch(Rectangle((0,W/2-D/2),L,D,fc="white",ec=K,lw=0.9,ls="--"))
ax.add_patch(Circle((-D/2,W/2),D/2,fc="#b8b8b8",ec=K,lw=1.2))
label(ax,-D-0.05,W/2,"Ø16\nend mill",fs=7,ha="right")
arrow(ax,0.25,W/2,0.85,W/2,lw=1.2); label(ax,0.92,W/2,"feed",fs=7,ha="left")
hdim(ax,0,L,-0.25,"100 mm",above=False,fs=7)
ax.plot([0,0],[-0.05,-0.3],color=K,lw=0.5); ax.plot([L,L],[-0.05,-0.3],color=K,lw=0.5)
label(ax,2.2,W-0.2,"workpiece",fs=7.5)
label(ax,L+0.1,W/2,"z = 4, 0.05 mm/tooth\n1200 rpm",fs=7,ha="left")
fin(fig,ax,-1.5,L+1.9,-0.7,W+0.25,"d75p_q6.png")

# S14 cubic Bezier curve with its control polygon
P=np.array([[0,0],[1,3],[3,3],[4,0]],float)
u=np.linspace(0,1,200)[:,None]
C=(1-u)**3*P[0]+3*u*(1-u)**2*P[1]+3*u**2*(1-u)*P[2]+u**3*P[3]
fig,ax=new(3.4,2.4)
ax.plot(P[:,0],P[:,1],color="#888",lw=0.9,ls="--",marker="s",ms=4,mfc="white",mec=K)
ax.plot(C[:,0],C[:,1],color=K,lw=1.6)
names=["P₀(0, 0)","P₁(1, 3)","P₂(3, 3)","P₃(4, 0)"]; offs=[(-0.05,-0.3),(-0.1,0.28),(0.1,0.28),(0.05,-0.3)]
for (x,y),t,(dx,dy) in zip(P,names,offs): label(ax,x+dx,y+dy,t,fs=7.5)
q=(1.552,2.16); ax.add_patch(Circle(q,0.06,fc="#D7191F",ec="none",zorder=6))
label(ax,q[0]+0.15,q[1]-0.35,"u = 0.4\n(1.552, 2.16)",fs=7,ha="left")
ax.plot([-0.3,4.4],[0,0],color=K,lw=0.6); ax.plot([0,0],[-0.3,3.4],color=K,lw=0.6)
label(ax,4.5,0,"x",fs=8,ha="left"); label(ax,0,3.55,"y",fs=8)
fin(fig,ax,-0.8,4.8,-0.6,3.7,"d75p_s14.png")
