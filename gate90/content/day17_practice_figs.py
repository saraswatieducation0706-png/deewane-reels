import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

def follower_lift(th,h,b1=120,d1=60,b2=120):
    """SHM rise h over b1 deg, dwell d1, SHM return over b2, dwell rest (th in deg, array)"""
    th=np.mod(th,360); y=np.zeros_like(th)
    r=th<b1; y[r]=h/2*(1-np.cos(np.pi*th[r]/b1))
    d=(th>=b1)&(th<b1+d1); y[d]=h
    f=(th>=b1+d1)&(th<b1+d1+b2); y[f]=h/2*(1+np.cos(np.pi*(th[f]-b1-d1)/b2))
    return y

def roller_cam(ax,rp,rr,h,th_now,scale=0.02,b1=120,d1=60,b2=120):
    """radial cam (centre at origin) with an in-line translating roller follower on top; cam turned so that
    cam angle th_now is under the follower. Returns roller centre y."""
    phi=np.linspace(0,360,1441)                      # cam angle
    rho=(rp+follower_lift(phi,h,b1,d1,b2))*scale     # pitch curve radius
    ang=np.radians(90+(phi-th_now))                  # angle in the drawing (cam turns clockwise)
    px,py=rho*np.cos(ang),rho*np.sin(ang)
    dx,dy=np.gradient(px),np.gradient(py); L=np.hypot(dx,dy); nx,ny=dy/L,-dx/L   # outward normal (curve ccw)
    if np.mean(nx*px+ny*py)<0: nx,ny=-nx,-ny
    cx,cy=px-rr*scale*nx,py-rr*scale*ny
    ax.add_patch(Polygon(np.c_[cx,cy],closed=True,fc="#dddddd",ec=K,lw=1.4,zorder=2))
    ax.plot(px,py,color=K,lw=0.7,ls="--",zorder=3)
    ax.add_patch(Circle((0,0),0.08,fc="white",ec=K,lw=1,zorder=4))
    yc=(rp+float(follower_lift(np.array([th_now]),h,b1,d1,b2)[0]))*scale
    ax.add_patch(Circle((0,yc),rr*scale,fc="white",ec=K,lw=1.3,zorder=5)); joint(ax,0,yc,0.04)
    ax.add_patch(Rectangle((-0.07,yc),0.14,1.3,fc="white",ec=K,lw=1.3,zorder=4))
    for s in (-1,1): hatch_wall(ax,s*0.13,yc+0.55,yc+1.1,left=(s<0),size=0.1)
    return yc

# Q5: roller follower, SHM rise 40 mm over 120 deg, prime circle 50 mm, roller 10 mm, shown at 60 deg of rise
fig,ax=new(3.4,3.4)
yc=roller_cam(ax,50,10,40,60)
th=np.linspace(0,2*np.pi,200); ax.plot(1.0*np.cos(th),1.0*np.sin(th),color=K,lw=0.6,ls=":")
label(ax,0,-2.15,"dotted: prime circle, r = 50 mm\ndashed: pitch curve",fs=7,va="top")
omega(ax,0,0,0.38,"ω",ccw=False,a0=200,a1=330,fs=9,lpos=(0.0,-0.6))
label(ax,0.5,yc,"roller\nr = 10 mm",fs=7,ha="left")
label(ax,0.25,yc+0.95,"follower",fs=7,ha="left")
fin(fig,ax,-1.9,1.9,-2.7,3.0,"d17p_q5.png")

# S1: cycloidal motion curves (rise 25 mm over 100 deg)
b=100; th=np.linspace(0,b,300); t=th/b
s=25*(t-np.sin(2*np.pi*t)/(2*np.pi)); v=1-np.cos(2*np.pi*t); a=np.sin(2*np.pi*t)
fig,axs=plt.subplots(3,1,figsize=(3.4,3.2),sharex=True)
for axx,y,nm in zip(axs,(s,v,a),("y (mm)","velocity","accel.")):
    axx.plot(th,y,color=K,lw=1.5); axx.axhline(0,color=K,lw=0.6)
    axx.set_ylabel(nm,fontsize=7); axx.tick_params(labelsize=6); axx.set_yticks([])
    for sp in ("top","right"): axx.spines[sp].set_visible(False)
axs[0].text(98,24,"25",fontsize=7,ha="right",va="top")
axs[1].text(100,2.0,"v max = 2hω/β\nat θ = β/2",fontsize=7,ha="right",va="top")
axs[2].text(100,1.0,"a max = 2πhω²/β²\nat θ = β/4",fontsize=7,ha="right",va="top")
axs[2].set_xlabel("cam angle θ (deg)",fontsize=7); axs[2].set_xticks([0,25,50,75,100])
fig.tight_layout(); fig.savefig(F+"d17p_s1.png",dpi=150,facecolor="white"); plt.close(fig)

# Q11: compound gear train (side view)
fig,ax=new(3.8,2.4)
shaft(ax,-0.4,1.0,0); shaft(ax,0.0,2.4,1.25); shaft(ax,1.2,3.0,2.25)
shaft_gear(ax,0.6,0,0.45,"A (20)",lab_side="bottom"); shaft_gear(ax,0.6,1.25,0.8,"",lab_side="bottom"); label(ax,0.45,1.75,"B (50)",fs=8,ha="right")
shaft_gear(ax,2.0,1.25,0.55,"C (30)",lab_side="bottom"); shaft_gear(ax,2.0,2.25,0.45,"D (60)",lab_side="top")
# D meshes with C: C pitch radius 0.55 + D 0.45 = 1.0 = shaft spacing; A 0.45 + B 0.8 = 1.25
label(ax,-0.55,0,"input\n1500 rpm",fs=7,ha="right"); label(ax,3.15,2.25,"output",fs=7,ha="left")
fin(fig,ax,-1.5,3.9,-0.9,3.0,"d17p_q11.png")

# Q12: epicyclic gear train (front view): sun 24, planets 30, annulus 84, arm carries the planets
fig,ax=new(3.0,3.0)
epicyclic(ax,24,30,84)
label(ax,0,-3.0,"S = sun (24 T, fixed)   P = planets (30 T)\nA = annulus (84 T, internal)",fs=7,va="top")
fin(fig,ax,-3.1,3.1,-3.6,3.1,"d17p_q12.png")
