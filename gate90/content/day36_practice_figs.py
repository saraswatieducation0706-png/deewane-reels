import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
W="#cfe3f3"
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def surface(ax,x,y,s=0.1):
    ax.add_patch(Polygon([[x,y],[x-s,y+1.4*s],[x+s,y+1.4*s]],closed=True,fill=False,ec=K,lw=0.9))
    ax.plot([x-1.5*s,x+1.5*s],[y-0.4*s,y-0.4*s],color=K,lw=0.6); ax.plot([x-0.9*s,x+0.9*s],[y-0.8*s,y-0.8*s],color=K,lw=0.6)

# P3 jet on a fixed curved vane, deflected through 150 degrees
fig,ax=new(3.6,2.2)
# nozzle
ax.add_patch(Polygon([[-0.6,0.22],[0,0.08],[0,-0.08],[-0.6,-0.22]],closed=True,fc="#dddddd",ec=K,lw=1.2))
ax.add_patch(Rectangle((0,-0.08),1.3,0.16,fc=W,ec="none"))
arrow(ax,0.15,0,0.9,0,lw=1.1); label(ax,0.55,0.25,"V = 25 m/s",fs=7.5); label(ax,0.55,-0.27,"d = 30 mm",fs=7.5)
# vane: arc centred (1.3,0.45) radius 0.45 from -90 deg turning ccw to +60 deg (150 deg turn)
c=np.array([1.3,0.45]); R=0.45
th=np.radians(np.linspace(-90,60,60)); ax.plot(c[0]+R*np.cos(th),c[1]+R*np.sin(th),color=K,lw=2.4)
# outgoing jet tangent at 60 deg: direction of motion at angle 150 deg
p=c+R*np.array([np.cos(np.radians(60)),np.sin(np.radians(60))]); d=np.array([np.cos(np.radians(150)),np.sin(np.radians(150))])
arrow(ax,*(p+0.1*d),*(p+0.75*d),lw=1.1)
ax.plot([p[0],p[0]+0.9],[p[1],p[1]],color=K,lw=0.5,ls=":")
angarc(ax,p[0],p[1],0.35,0,150,"150°",fs=8,lr=0.5)
# support hatch behind vane
hatch_wall(ax,1.95,0.05,0.85,left=False)
ax.plot([1.75,1.95],[0.45,0.45],color=K,lw=1.5)
fin(fig,ax,-0.7,2.2,-0.45,1.5,"d36p_q3.png")

# P12 reservoir draining through a pipe to atmosphere
fig,ax=new(3.8,2.0)
ax.add_patch(Rectangle((0,0),1.0,1.6,fc=W,ec="none")); ax.plot([0,0,1.0,1.0],[1.8,0,0,0.25],color=K,lw=1.5); ax.plot([1.0,1.0],[0.39,1.8],color=K,lw=1.5)
ax.plot([0,1.0],[1.6,1.6],color=K,lw=0.8); surface(ax,0.5,1.6)
ax.add_patch(Rectangle((1.0,0.25),2.6,0.14,fc=W,ec="none")); ax.plot([1.0,3.6],[0.25,0.25],color=K,lw=1.3); ax.plot([1.0,3.6],[0.39,0.39],color=K,lw=1.3)
arrow(ax,3.6,0.32,4.0,0.32,lw=1.1); label(ax,3.8,0.6,"free jet",fs=7.5)
ax.plot([1.0,4.0],[0.32,0.32],color=K,lw=0.5,ls="-."); ax.plot([1.0,4.5],[1.6,1.6],color=K,lw=0.5,ls=":")
vdim(ax,4.5,0.32,1.6,"H = 10 m",side="right",fs=8)
label(ax,2.75,0.07,"L = 50 m, D = 50 mm, f = 0.025",fs=7.5)
label(ax,1.75,0.75,"sharp entry",fs=7); ax.plot([1.45,1.05],[0.7,0.42],color=K,lw=0.5)
fin(fig,ax,-0.2,5.4,-0.15,1.95,"d36p_q12.png")
