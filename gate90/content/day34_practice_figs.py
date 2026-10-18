import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
W="#cfe3f3"
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def surface(ax,x,y,s=0.1):
    ax.add_patch(Polygon([[x,y],[x-s,y+1.4*s],[x+s,y+1.4*s]],closed=True,fill=False,ec=K,lw=0.9))
    ax.plot([x-1.5*s,x+1.5*s],[y-0.4*s,y-0.4*s],color=K,lw=0.6); ax.plot([x-0.9*s,x+0.9*s],[y-0.8*s,y-0.8*s],color=K,lw=0.6)
def tank(ax,x0,x1,yb,yw,yt):
    """open tank: walls from yb to yt, water to yw"""
    ax.add_patch(Rectangle((x0,yb),x1-x0,yw-yb,fc=W,ec="none"))
    ax.plot([x0,x0,x1,x1],[yt,yb,yb,yt],color=K,lw=1.5)
    ax.plot([x0,x1],[yw,yw],color=K,lw=0.8); surface(ax,(x0+x1)/2,yw)
def pipe(ax,pts,d):
    """straight pipe through polyline pts (horizontal/vertical/inclined segments) with bore d"""
    pts=np.array(pts,float)
    for a,b in zip(pts[:-1],pts[1:]):
        t=(b-a)/np.linalg.norm(b-a); n=np.array([-t[1],t[0]])*d/2
        ax.add_patch(Polygon([a+n,b+n,b-n,a-n],closed=True,fc=W,ec="none"))
    for s in (1,-1):
        line=[]
        for i,p in enumerate(pts):
            if i==0: t=pts[1]-pts[0]
            elif i==len(pts)-1: t=pts[-1]-pts[-2]
            else: t=(pts[i+1]-pts[i])/np.linalg.norm(pts[i+1]-pts[i])+(pts[i]-pts[i-1])/np.linalg.norm(pts[i]-pts[i-1])
            t=t/np.linalg.norm(t); n=np.array([-t[1],t[0]])
            if 0<i<len(pts)-1:
                t1=(pts[i]-pts[i-1])/np.linalg.norm(pts[i]-pts[i-1]); n1=np.array([-t1[1],t1[0]])
                k=1/np.dot(n,n1)
            else: k=1
            line.append(p+s*n*d/2*k)
        line=np.array(line); ax.plot(line[:,0],line[:,1],color=K,lw=1.3)

# P3 sudden expansion
fig,ax=new(3.6,1.5)
ax.add_patch(Rectangle((0,-0.25),1.6,0.5,fc=W,ec="none")); ax.add_patch(Rectangle((1.6,-0.5),2.0,1.0,fc=W,ec="none"))
ax.plot([0,1.6,1.6,3.6],[0.25,0.25,0.5,0.5],color=K,lw=1.5); ax.plot([0,1.6,1.6,3.6],[-0.25,-0.25,-0.5,-0.5],color=K,lw=1.5)
arrow(ax,0.3,0,1.0,0,lw=1.1); label(ax,0.65,0.12,"Q",fs=8)
vdim(ax,0.15,-0.25,0.25,"",side="left"); label(ax,0.8,-0.42,"D₁ = 150 mm",fs=7.5)
label(ax,2.6,-0.68,"D₂ = 300 mm",fs=7.5); vdim(ax,3.4,-0.5,0.5,"",side="right")
label(ax,0.8,0.42,"section 1",fs=7.5); label(ax,2.9,0.68,"section 2",fs=7.5)
fin(fig,ax,-0.1,3.75,-0.85,0.85,"d34p_q3.png")

# P6 two reservoirs joined by two pipes in series
fig,ax=new(3.8,2.2)
tank(ax,0,0.9,0,1.6,1.8); tank(ax,3.6,4.5,-0.2,0.5,1.0)
pipe(ax,[(0.9,0.25),(2.3,0.25)],0.22); pipe(ax,[(2.3,0.25),(3.6,0.25)],0.14)
ax.plot([2.3,2.3],[0.07,0.11],color=K,lw=1.3); ax.plot([2.3,2.3],[0.39,0.43],color=K,lw=1.3)
label(ax,1.6,0.7,"pipe 1\n400 m, 300 mm",fs=7.5); label(ax,2.95,-0.25,"pipe 2\n300 m, 200 mm",fs=7.5)
ax.plot([0.9,3.45],[1.6,1.6],color=K,lw=0.5,ls=":"); ax.plot([3.2,3.6],[0.5,0.5],color=K,lw=0.5,ls=":")
vdim(ax,3.3,0.5,1.6,"15 m",side="left",fs=8)
fin(fig,ax,-0.2,4.7,-0.6,2.0,"d34p_q6.png")

# P11 siphon over a ridge
fig,ax=new(3.8,2.5)
tank(ax,0,0.9,-0.6,0.6,0.9); tank(ax,3.5,4.4,-1.6,-0.6,-0.3)
ax.add_patch(Polygon([[1.1,-1.8],[1.9,1.1],[2.3,1.1],[3.3,-1.8]],closed=True,fc="#e6e0d0",ec=K,lw=0.8))
pipe(ax,[(0.72,-0.3),(0.72,1.35),(2.1,1.35),(4.15,1.35),(4.15,-1.1)],0.12)
label(ax,2.1,1.6,"S (summit)",fs=7.5)
ax.plot([0.2,2.1],[0.6,0.6],color=K,lw=0.5,ls=":"); vdim(ax,1.25,0.6,1.35,"4 m",side="right",fs=7.5)
ax.plot([0.9,3.5],[0.6,0.6],color=K,lw=0.5,ls=":"); ax.plot([3.2,3.5],[-0.6,-0.6],color=K,lw=0.5,ls=":"); vdim(ax,3.35,-0.6,0.6,"6 m",side="left",fs=7.5)
fin(fig,ax,-0.2,4.6,-1.95,1.85,"d34p_q11.png")
