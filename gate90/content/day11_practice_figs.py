import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
sys.path.insert(0,"/home/claude/deewane-reels/gate90/tooling")
from figlib import *
F=sys.argv[1] if len(sys.argv)>1 else "fig/"
F=F if F.endswith("/") else F+"/"
os.makedirs(F,exist_ok=True)
# ---------- local helpers (shafts, torques, springs, shells) ----------
def shaft(ax,x0,x1,d,fc="#dddddd"): ax.add_patch(Rectangle((x0,-d/2),x1-x0,d,fc=fc,ec=K,lw=1.3))
def axis_line(ax,x0,x1): ax.plot([x0,x1],[0,0],color=K,lw=0.6,ls="-.")
def torque(ax,x,r,txt,fs=8,lx=0.0,rev=False):
    t=np.radians(np.linspace(75,-75,40) if rev else np.linspace(-75,75,40)); xs=x+0.13*np.cos(t); ys=r*np.sin(t)
    ax.plot(xs[:-3],ys[:-3],color=K,lw=1.4); arrow(ax,xs[-4],ys[-4],xs[-1],ys[-1],lw=1.4)
    label(ax,x+lx,r+0.2,txt,fs=fs,va="bottom")
def wall(ax,x,h,left=True): hatch_wall(ax,x,-h/2,h/2,left=left,size=0.15)
def ddim(ax,x,d,t,fs=8):
    arrow(ax,x,-d/2,x,d/2,lw=0.9,both=True)
    ax.text(x+0.07,d/4 if d>0.45 else 0.0,t,fontsize=fs,ha="left",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=7)
def spring_v(ax,x,y0,y1,w=0.22,n=8,lead=0.12):
    ys=np.linspace(y0-lead,y1+lead,2*n+1); xs=[x]+[x+(w/2 if i%2 else -w/2) for i in range(1,2*n)]+[x]
    ax.plot([x,x],[y0,y0-lead],color=K,lw=1.2); ax.plot(xs,ys,color=K,lw=1.2); ax.plot([x,x],[y1+lead,y1],color=K,lw=1.2)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P4 stepped shaft fixed at A, torques at B and C
fig,ax=new(3.8,1.9); a=2.6; b=1.6; d1=0.6; d2=0.36
wall(ax,0,1.2); shaft(ax,0,a,d1); shaft(ax,a,a+b,d2); axis_line(ax,-0.2,a+b+0.3)
torque(ax,a,0.48,"1.5 kN·m",lx=-0.25); torque(ax,a+b,0.32,"0.5 kN·m",lx=0.1)
label(ax,-0.25,0.75,"A",fs=9); label(ax,a+0.25,-0.48,"B",fs=9); label(ax,a+b+0.3,-0.3,"C",fs=9)
ddim(ax,0.3,d1,"50 mm"); ddim(ax,a+0.45,d2,"30 mm")
hdim(ax,0,a,-0.8,"1.0 m",above=False); hdim(ax,a,a+b,-0.8,"0.5 m",above=False)
ext(ax,a,-d1/2,a,-0.9); ext(ax,a+b,-d2/2,a+b,-0.9)
fin(fig,ax,-0.5,a+b+0.8,-1.2,1.15,"d11p_q4.png")
# P4 solution: internal torque diagram
fig,ax=new(3.6,1.6); s=0.45
ax.add_patch(Rectangle((0,0),a,2.0*s,fc="#cccccc",ec=K,lw=1.2)); ax.add_patch(Rectangle((a,0),b,0.5*s,fc="#cccccc",ec=K,lw=1.2))
ax.plot([-0.1,a+b+0.2],[0,0],color=K,lw=1.0)
label(ax,a/2,2.0*s+0.15,"T = 2.0 kN·m → τ = 81.5 MPa",fs=7.5,va="bottom")
label(ax,a+b/2,0.5*s+0.15,"0.5 kN·m",fs=7.5,va="bottom"); label(ax,a+b/2,0.5*s+0.48,"τ = 94.3 MPa",fs=7.5,va="bottom")
label(ax,0,-0.15,"A",fs=8,va="top"); label(ax,a,-0.15,"B",fs=8,va="top"); label(ax,a+b,-0.15,"C",fs=8,va="top")
label(ax,(a+b)/2,-0.5,"internal torque diagram",fs=7.5)
fin(fig,ax,-0.3,a+b+0.4,-0.7,1.4,"d11p_s4.png")

# P5 composite shaft cross-section
fig,ax=new(2.6,2.4); Ro=1.2; Ri=0.8
ax.add_patch(Circle((0,0),Ro,fc="#eeeeee",ec=K,lw=1.4,hatch="///")); ax.add_patch(Circle((0,0),Ri,fc="#aaaaaa",ec=K,lw=1.4))
label(ax,0,0.25,"steel",fs=8,bbox=dict(fc="white",ec="none",pad=0.5)); label(ax,0,Ri+0.2,"brass",fs=8,bbox=dict(fc="white",ec="none",pad=0.5))
arrow(ax,-Ri,-0.25,Ri,-0.25,lw=0.9,both=True); label(ax,0,-0.45,"40 mm",fs=8,bbox=dict(fc="#aaaaaa",ec="none",pad=0.3))
arrow(ax,-Ro,-Ro-0.25,Ro,-Ro-0.25,lw=0.9,both=True); label(ax,0,-Ro-0.45,"60 mm",fs=8)
ext(ax,-Ro,0,-Ro,-Ro-0.35); ext(ax,Ro,0,Ro,-Ro-0.35)
label(ax,0,Ro+0.3,"T = 2 kN·m",fs=8)
fin(fig,ax,-1.5,1.5,-1.9,1.6,"d11p_q5.png")
# P5 solution: shear stress distribution along a radius
fig,ax=new(3.6,2.0); sc=0.04  # 1 MPa -> 0.04 units ; radius 1 mm -> 0.06
r=lambda mm: mm*0.1
ax.plot([0,r(30)+0.2],[0,0],color=K,lw=0.9); arrow(ax,0,0,0,52.5*sc+0.5,lw=0.9)
label(ax,0,52.5*sc+0.6,"τ (MPa)",fs=8,va="bottom"); label(ax,r(30)+0.25,0,"r (mm)",fs=8,ha="left")
ax.fill([0,r(20),r(20)],[0,0,52.5*sc],color="#bbbbbb",ec=K,lw=1.2); ax.fill([r(20),r(30),r(30),r(20)],[0,0,39.38*sc,26.25*sc],color="#e4e4e4",ec=K,lw=1.2)
label(ax,r(20)-0.05,52.5*sc+0.15,"52.5",fs=7.5,ha="right"); label(ax,r(20)+0.07,26.25*sc-0.15,"26.3",fs=7.5,ha="left")
label(ax,r(30)+0.05,39.38*sc+0.15,"39.4",fs=7.5,ha="left")
label(ax,r(10),-0.5,"steel",fs=7.5,va="top"); label(ax,r(25),-0.5,"brass",fs=7.5,va="top")
label(ax,r(20),-0.18,"20",fs=7,va="top"); label(ax,r(30),-0.18,"30",fs=7,va="top")
fin(fig,ax,-0.4,r(30)+1.0,-0.85,52.5*sc+0.9,"d11p_s5.png")

# P7 shaft with 45 degree strain gauge
fig,ax=new(3.4,1.7); L=3.2; d=0.8
shaft(ax,0,L,d); axis_line(ax,-0.2,L+0.3)
torque(ax,0,0.55,"T",lx=-0.05,rev=True); torque(ax,L,0.55,"T",lx=0.05)
from matplotlib.transforms import Affine2D
g=Rectangle((-0.22,-0.07),0.44,0.14,fc="white",ec=K,lw=1.1,hatch="||||")
g.set_transform(Affine2D().rotate_deg(45).translate(1.4,0.05)+ax.transData); ax.add_patch(g)
ax.plot([1.1,1.7],[0.05,0.05],color=K,lw=0.6,ls=":")
aa=np.radians(np.linspace(0,45,20)); ax.plot(1.4+0.32*np.cos(aa),0.05+0.32*np.sin(aa),color=K,lw=0.8)
label(ax,1.95,0.2,"45°",fs=8); label(ax,2.3,-0.6,"gauge on surface",fs=7.5)
arrow(ax,2.2,-0.5,1.55,-0.05,lw=0.7)
ddim(ax,L-0.75,d,"80 mm")
fin(fig,ax,-0.5,L+0.6,-0.9,1.1,"d11p_q7.png")

# P8 thin cylinder longitudinal section
fig,ax=new(3.6,1.9); L=3.4; R=0.75; t=0.08
ax.add_patch(Rectangle((0,R-t),L,t,fc="#999999",ec=K,lw=1.0)); ax.add_patch(Rectangle((0,-R),L,t,fc="#999999",ec=K,lw=1.0))
ax.plot([0,0],[-R,R],color=K,lw=2.4); ax.plot([L,L],[-R,R],color=K,lw=2.4)
label(ax,L/2,0,"p = 1.5 MPa",fs=8)
vdim(ax,-0.3,-R,R,"1 m",side="left"); hdim(ax,0,L,-R-0.3,"closed thin cylinder",above=False)
arrow(ax,L*0.75,R+0.35,L*0.75,R,lw=0.8); label(ax,L*0.75,R+0.42,"t = 12 mm",fs=8,va="bottom")
fin(fig,ax,-1.0,L+0.3,-1.4,1.4,"d11p_q8.png")
# P8 solution: wall element
fig,ax=new(3.2,2.6); h=0.5; ax.add_patch(Rectangle((-h,-h),2*h,2*h,fc="#eeeeee",ec=K,lw=1.6))
for sgn in (1,-1):
    arrow(ax,sgn*(h+0.08),0,sgn*(h+0.55),0); arrow(ax,0,sgn*(h+0.08),0,sgn*(h+0.9))
label(ax,h+0.62,0.18,"σl = 31.25 MPa",fs=8,ha="left"); label(ax,0.12,h+0.75,"σh = 62.5 MPa",fs=8,ha="left")
label(ax,0,0,"wall",fs=8); arrow(ax,-1.6,1.35,-1.0,1.35,lw=0.8); label(ax,-1.6,1.15,"axis of cylinder",fs=7.5,ha="left")
fin(fig,ax,-1.7,2.4,-1.5,1.6,"d11p_s8.png")

# P12 spring system: k1 series with parallel (k2, k3)
fig,ax=new(2.8,3.0); hatch_ground(ax,-0.7,0.7,0,down=False,size=0.15)
spring_v(ax,0,0,-1.0,n=7); ax.add_patch(Rectangle((-0.6,-1.12),1.2,0.12,fc="#dddddd",ec=K,lw=1.1))
spring_v(ax,-0.4,-1.12,-2.0,n=6); spring_v(ax,0.4,-1.12,-2.0,n=6)
ax.add_patch(Rectangle((-0.6,-2.3),1.2,0.3,fc="#dddddd",ec=K,lw=1.2))
label(ax,0.22,-0.5,"k₁ = 10 N/mm",fs=7.5,ha="left"); label(ax,-0.6,-1.56,"k₂ = 20 N/mm",fs=7.5,ha="right"); label(ax,0.6,-1.56,"k₃ = 30 N/mm",fs=7.5,ha="left")
arrow(ax,0,-2.3,0,-2.8); label(ax,0,-2.95,"250 N",fs=8,va="top")
fin(fig,ax,-2.0,2.2,-3.2,0.2,"d11p_q12.png")
print("ok")
