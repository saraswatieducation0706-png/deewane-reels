import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
W="#cfe3f3"; HG="#9a9a9a"
def surface(ax,x,y,s=0.12):  # free-surface triangle symbol
    ax.add_patch(Polygon([[x,y],[x-s,y+1.4*s],[x+s,y+1.4*s]],closed=True,fill=False,ec=K,lw=0.9))
    ax.plot([x-1.5*s,x+1.5*s],[y-0.4*s,y-0.4*s],color=K,lw=0.6); ax.plot([x-0.9*s,x+0.9*s],[y-0.8*s,y-0.8*s],color=K,lw=0.6)

# P1 jet striking a stationary flat plate inclined at 30 deg to the jet axis
fig,ax=new(3.2,2.4)
ax.add_patch(Polygon([[-0.6,0.22],[0.1,0.1],[0.1,-0.1],[-0.6,-0.22]],closed=True,fc="#dddddd",ec=K,lw=1.2))
ax.add_patch(Rectangle((0.1,-0.07),1.9,0.14,fc=W,ec="none"))
arrow(ax,0.35,0,1.25,0,lw=1.2); label(ax,0.8,0.22,"V = 15 m/s",fs=7.5)
t=np.radians(30); u=np.array([np.cos(t),np.sin(t)]); c=np.array([2.0,0.0])
p0=c-1.2*u; p1=c+1.2*u
ax.plot([p0[0],p1[0]],[p0[1],p1[1]],color=K,lw=4,solid_capstyle="butt")
# spread sheets of water along plate
for s in (1,-1):
    q0=c+s*0.15*u+np.array([-0.07,0.0]); q1=c+s*1.0*u+np.array([-0.07,0.0])*1
    ax.plot([q0[0]-0.03,q1[0]-0.03],[q0[1]+0.04*s,q1[1]+0.04*s],color="#5b8fbf",lw=2.5)
ax.plot([c[0],c[0]+1.1],[0,0],color=K,lw=0.5,ls=":")
angarc(ax,c[0],0,0.55,0,30,"30°",fs=8,lr=0.78)
label(ax,-0.3,-0.45,"d = 40 mm",fs=7.5)
fin(fig,ax,-0.8,3.3,-0.9,1.0,"d31p_q1.png")

# P3 horizontal 45-degree bend (plan view), same diameter
def bend45(ax,with_forces=False):
    R=1.2; c=np.array([0.0,R]); r1,r2=R-0.3,R+0.3
    th=np.radians(np.linspace(-90,-45,40))
    ax.add_patch(Rectangle((-1.6,-0.3),1.6,0.6,fc=W,ec="none"))
    ax.add_patch(Polygon(np.r_[np.c_[c[0]+r2*np.cos(th),c[1]+r2*np.sin(th)],np.c_[c[0]+r1*np.cos(th[::-1]),c[1]+r1*np.sin(th[::-1])]],closed=True,fc=W,ec="none"))
    e=np.radians(-45); d=np.array([np.cos(np.radians(45)),np.sin(np.radians(45))])
    a1=c+r1*np.array([np.cos(e),np.sin(e)]); a2=c+r2*np.array([np.cos(e),np.sin(e)])
    ax.add_patch(Polygon([a1,a2,a2+1.2*d,a1+1.2*d],closed=True,fc=W,ec="none"))
    ax.plot([-1.6,0],[0.3,0.3],color=K,lw=1.4); ax.plot([-1.6,0],[-0.3,-0.3],color=K,lw=1.4)
    for r,a in ((r1,a1),(r2,a2)):
        ax.plot(c[0]+r*np.cos(th),c[1]+r*np.sin(th),color=K,lw=1.4); ax.plot([a[0],a[0]+1.2*d[0]],[a[1],a[1]+1.2*d[1]],color=K,lw=1.4)
    m2=(a1+a2)/2+1.2*d
    if not with_forces:
        arrow(ax,-2.2,0,-1.3,0,lw=1.5); label(ax,-1.9,0.2,"1",fs=9,fontweight="bold")
        arrow(ax,m2[0]-0.3*d[0],m2[1]-0.3*d[1],m2[0]+0.5*d[0],m2[1]+0.5*d[1],lw=1.5); label(ax,m2[0]+0.15,m2[1]+0.55,"2",fs=9,fontweight="bold")
        label(ax,-0.9,-0.6,"d = 250 mm",fs=7.5)
        ax.plot([a2[0],a2[0]+0.9],[a2[1]+0.0,a2[1]+0.0],color=K,lw=0.5,ls=":")
        angarc(ax,a2[0],a2[1],0.4,0,45,"45°",fs=8,lr=0.62)
    else:
        arrow(ax,-2.4,0,-1.65,0,lw=1.3); label(ax,-2.0,0.22,"p₁A",fs=8)
        arrow(ax,m2[0]+0.7*d[0],m2[1]+0.7*d[1],m2[0]+0.05*d[0],m2[1]+0.05*d[1],lw=1.3); label(ax,m2[0]+0.85,m2[1]+0.3,"p₂A",fs=8,ha="left")
        arrow(ax,0.35,0.1,-0.55,0.47,lw=1.3,color="#D7191F"); label(ax,-0.9,0.75,"R (bend on water)",fs=7.5,color="#D7191F")
        label(ax,-0.9,-0.65,"control volume",fs=7.5)
        arrow(ax,1.6,-0.8,2.1,-0.8,lw=0.8); arrow(ax,1.6,-0.8,1.6,-0.3,lw=0.8)
        label(ax,2.22,-0.8,"x",fs=8); label(ax,1.6,-0.17,"y",fs=8)
fig,ax=new(3.0,2.4); bend45(ax); fin(fig,ax,-2.4,2.4,-1.0,2.2,"d31p_q3.png")
fig,ax=new(3.2,2.4); bend45(ax,True); fin(fig,ax,-2.6,2.6,-1.0,2.2,"d31p_q3s.png")

# P6 vertical venturimeter (flow upward) with a mercury U-tube manometer
fig,ax=new(2.6,3.4)
R1,R2=0.45,0.22
ys=[0,0.8,1.8,2.1,3.6,4.2]; rs=[R1,R1,R2,R2,R1,R1]
ax.add_patch(Polygon([(-r,y) for y,r in zip(ys,rs)]+[(r,y) for y,r in zip(ys[::-1],rs[::-1])],closed=True,fc=W,ec="none"))
ax.plot([-r for r in rs],ys,color=K,lw=1.4); ax.plot(rs,ys,color=K,lw=1.4)
arrow(ax,0,0.05,0,0.7,lw=1.2); label(ax,-0.55,0.3,"flow",fs=9,ha="right")
y1,y2=0.4,1.95
# tappings to the right
wl=0.1; xm1,xm2=1.3,1.9; yb=-1.0; hl,hr=-0.4,0.2
ax.add_patch(Rectangle((R1,y1-wl/2),xm1-R1+wl/2,wl,fc=W,ec=K,lw=0.8))
ax.add_patch(Rectangle((R2,y2-wl/2),xm2-R2+wl/2,wl,fc=W,ec=K,lw=0.8))
for x,yt,hh in ((xm1,y1-wl/2,hl),(xm2,y2-wl/2,hr)):
    ax.add_patch(Rectangle((x-wl/2,hh),wl,yt-hh,fc=W,ec="none"))
    ax.add_patch(Rectangle((x-wl/2,yb),wl,hh-yb,fc=HG,ec="none"))
    ax.plot([x-wl/2,x-wl/2],[yb,yt],color=K,lw=0.9); ax.plot([x+wl/2,x+wl/2],[yb,yt],color=K,lw=0.9)
    ax.plot([x-wl/2,x+wl/2],[hh,hh],color=K,lw=0.8)
ax.add_patch(Rectangle((xm1-wl/2,yb-wl),xm2-xm1+wl,wl,fc=HG,ec="none"))
ax.plot([xm1-wl/2,xm2+wl/2],[yb-wl,yb-wl],color=K,lw=0.9); ax.plot([xm1+wl/2,xm2-wl/2],[yb,yb],color=K,lw=0.9)
ext(ax,xm1+wl/2,hl,2.45,hl); ext(ax,xm2+wl/2,hr,2.45,hr); vdim(ax,2.35,hl,hr,"120 mm",side="right",fs=10)
ext(ax,-R1,y1,-1.0,y1); ext(ax,-R2,y2,-1.0,y2); vdim(ax,-0.9,y1,y2,"300 mm",side="left",fs=10)
label(ax,1.6,-1.35,"mercury",fs=10)
label(ax,0,4.45,"150 mm × 75 mm",fs=10)
fin(fig,ax,-2.3,3.6,-1.55,4.65,"d31p_q6.png")

# P8 pitot tube in an open channel
fig,ax=new(3.0,2.2)
ax.add_patch(Rectangle((0,0),3.2,1.2,fc=W,ec="none")); ax.plot([0,3.2],[1.2,1.2],color=K,lw=0.9)
hatch_ground(ax,0,3.2,0,size=0.18); surface(ax,0.5,1.2)
for yy in (0.35,0.75): arrow(ax,0.25,yy,0.95,yy,lw=1.1)
label(ax,0.6,0.55,"V",fs=8)
tw=0.09; x0=2.0; ytip=0.5
ax.add_patch(Rectangle((1.5,ytip-tw/2),x0-1.5+tw/2,tw,fc=W,ec="none"))
ax.plot([1.5,x0-tw/2],[ytip+tw/2,ytip+tw/2],color=K,lw=1.1); ax.plot([1.5,x0+tw/2],[ytip-tw/2,ytip-tw/2],color=K,lw=1.1)
ax.plot([x0-tw/2,x0-tw/2],[ytip+tw/2,2.2],color=K,lw=1.1); ax.plot([x0+tw/2,x0+tw/2],[ytip-tw/2,2.2],color=K,lw=1.1)
ax.add_patch(Rectangle((x0-tw/2,ytip),tw,1.5-ytip+0.0,fc=W,ec="none"))
ax.plot([x0-tw/2,x0+tw/2],[1.5,1.5],color=K,lw=0.9)
ext(ax,x0+tw/2,1.5,2.75,1.5); vdim(ax,2.65,1.2,1.5,"0.3 m",side="right",fs=7.5)
label(ax,1.1,1.75,"pitot tube",fs=7.5)
fin(fig,ax,-0.2,3.4,-0.35,2.3,"d31p_q8.png")
print("figs ok")
