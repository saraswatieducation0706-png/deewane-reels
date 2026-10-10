import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def column(ax,x,y0,y1,w=0.18): ax.add_patch(Rectangle((x-w/2,y0),w,y1-y0,fc="#dddddd",ec=K,lw=1.3))
def pin_down(ax,x,y,s=0.3):
    """inverted pin: hinge at (x,y), triangle above, hatched bearing plate on top"""
    ax.add_patch(Polygon([[x,y],[x-s/2,y+s*0.8],[x+s/2,y+s*0.8]],closed=True,fill=False,ec=K,lw=1.2))
    ax.add_patch(Circle((x,y),s*0.1,fc="white",ec=K,lw=1,zorder=5))
    hatch_ground(ax,x-s*0.8,x+s*0.8,y+s*0.8,down=False,size=s*0.4)
def pin_wall(ax,x,y,s=0.3):
    """pin on a vertical wall at x (wall to the left), hinge at (x+0.8s, y)"""
    hx=x+s*0.8
    ax.add_patch(Polygon([[hx,y],[x,y-s/2],[x,y+s/2]],closed=True,fill=False,ec=K,lw=1.2))
    ax.add_patch(Circle((hx,y),s*0.1,fc="white",ec=K,lw=1,zorder=5)); return hx
def gauge(ax,ang,r0,r1,w=0.16,nz=4):
    t=np.radians(ang); u=np.array([np.cos(t),np.sin(t)]); n=np.array([-u[1],u[0]])
    ts=np.linspace(r0,r1,2*nz+1); pts=np.array([s*u+(w/2 if i%2 else -w/2)*n for i,s in enumerate(ts)])
    ax.plot(pts[:,0],pts[:,1],color=K,lw=1.0)
    c=[r0*u-0.6*w*n,r1*u-0.6*w*n,r1*u+0.6*w*n,r0*u+0.6*w*n]; ax.add_patch(Polygon(c,closed=True,fill=False,ec=K,lw=1.1))

# P1 pinned-pinned tube column
fig,ax=new(2.2,3.0); H=2.6
column(ax,0,0.3,H-0.3); pin(ax,0,0.3,0.4); pin_down(ax,0,H-0.3,0.4)
arrow(ax,0,H+0.95,0,H+0.05); label(ax,0.15,H+0.75,"P",fs=10,ha="left")
vdim(ax,-0.85,0.3,H-0.3,"2.5 m",side="left"); ext(ax,-0.1,0.3,-0.95,0.3); ext(ax,-0.1,H-0.3,-0.95,H-0.3)
label(ax,0.2,H*0.5,"tube\nD = 50 mm\nd = 40 mm",fs=7.5,ha="left")
fin(fig,ax,-1.6,1.4,-0.2,H+1.1,"d13p_q1.png")

# P2 fixed-base, unrestrained-top column (rectangular section)
fig,ax=new(2.6,3.0); H=2.4
column(ax,0,0,H); hatch_ground(ax,-0.6,0.6,0,down=True,size=0.14)
arrow(ax,0,H+0.9,0,H+0.02); label(ax,0.15,H+0.7,"P",fs=10,ha="left")
vdim(ax,-0.75,0,H,"0.8 m",side="left"); ext(ax,-0.1,H,-0.85,H)
label(ax,0.3,H-0.25,"top end\nfree",fs=7.5,ha="left"); label(ax,0.7,0.25,"fixed",fs=7.5,ha="left")
# section inset
ax.add_patch(Rectangle((0.75,0.9),0.8,0.5,fc="#dddddd",ec=K,lw=1.2))
hdim(ax,0.75,1.55,1.5,"40 mm",fs=7); vdim(ax,1.65,0.9,1.4,"25 mm",side="right",fs=7)
label(ax,1.15,0.72,"section",fs=7)
fin(fig,ax,-1.5,2.6,-0.35,H+1.05,"d13p_q2.png")

# S2 buckled shape fixed-base column and its mirror (Le = 2L)
fig,ax=new(2.8,3.0); H=1.4; d=0.35
y=np.linspace(0,H,100); x=d*(1-np.cos(np.pi*y/(2*H)))
ax.plot([0,0],[0,H],color=K,lw=0.7,ls="--"); ax.plot(x,y,color=K,lw=2)
y2=np.linspace(H,2*H,100); x2=d*(1-np.cos(np.pi*(2*H-y2)/(2*H)))
ax.plot(x2,y2,color=K,lw=1.2,ls=":"); ax.plot([0,0],[H,2*H],color=K,lw=0.7,ls="--")
hatch_ground(ax,-0.45,0.45,0,down=True,size=0.14)
arrow(ax,d,H+0.6,d,H+0.03); label(ax,d+0.12,H+0.45,"P",fs=9,ha="left")
vdim(ax,-0.55,0,H,"L",side="left"); vdim(ax,1.7,0,2*H,"Le = 2L",side="right"); ext(ax,0.05,2*H,1.8,2*H); ext(ax,0.45,0,1.8,0)
label(ax,0.45,0.45,"actual",fs=7,ha="left"); label(ax,0.45,2*H-0.35,"mirror image",fs=7,ha="left")
fin(fig,ax,-1.0,2.9,-0.35,2*H+0.2,"d13p_s2.png")

# P8 weight dropped on SS beam
fig,ax=new(3.2,2.1); S=1.4; Lb=2*S
beam(ax,0,Lb); pin(ax,0,-0.1,0.35); roller(ax,Lb,-0.1,0.35)
wy=0.1+0.75
ax.add_patch(Rectangle((S-0.22,wy),0.44,0.32,fc="white",ec=K,lw=1.3)); label(ax,S,wy+0.16,"W",fs=8)
label(ax,S+0.3,wy+0.16,"500 N",fs=8,ha="left")
ext(ax,S-0.22,0.1,S-0.6,0.1); ext(ax,S-0.22,wy,S-0.6,wy); vdim(ax,S-0.5,0.1,wy,"h = 20 mm",side="left",fs=7.5)
dim(ax,0,-0.8,Lb,-0.8,"2 m")
label(ax,-0.3,0.05,"A",fs=9); label(ax,Lb+0.3,0.05,"B",fs=9)
fin(fig,ax,-0.6,Lb+0.6,-1.1,wy+0.55,"d13p_q8.png")

# P10 stepped cantilever
fig,ax=new(3.2,1.9); S=1.5
ax.add_patch(Rectangle((0,-0.16),S,0.32,fc="#dddddd",ec=K,lw=1.3)); ax.add_patch(Rectangle((S,-0.1),S,0.2,fc="#dddddd",ec=K,lw=1.3))
fixed(ax,0,left=True,h=0.8)
pload(ax,2*S,"5 kN",y0=0.1,L=0.7)
label(ax,S/2,0.35,"2EI",fs=8); label(ax,1.5*S,0.3,"EI",fs=8)
label(ax,-0.25,0.55,"A",fs=9); label(ax,S,-0.35,"B",fs=9); label(ax,2*S+0.2,-0.2,"C",fs=9)
dim(ax,0,-0.65,S,-0.65,"1 m"); dim(ax,S,-0.65,2*S,-0.65,"1 m")
fin(fig,ax,-0.4,2*S+0.4,-1.0,1.05,"d13p_q10.png")

# S11 propped cantilever FBD
fig,ax=new(3.2,1.9); Lb=3.0
beam(ax,0,Lb); udl(ax,0,Lb,"w per unit length",lx=Lb/2)
arrow(ax,0.05,-0.95,0.05,-0.12); label(ax,0.2,-0.75,"R_A",fs=8,ha="left")
arrow(ax,Lb,-0.95,Lb,-0.12); label(ax,Lb-0.12,-0.75,"R_B = 3wL/8",fs=8,ha="right")
couple(ax,-0.12,"",cw=False,r=0.3,y=0.0); label(ax,-0.5,0.45,"M_A",fs=8,ha="right")
dim(ax,0,-1.2,Lb,-1.2,"L")
fin(fig,ax,-1.2,Lb+0.4,-1.5,1.0,"d13p_s11.png")

# P12 wall bracket
fig,ax=new(3.0,2.4); s=0.3; W=1.6; Hh=1.2
hatch_wall(ax,0,-0.4,Hh+0.4,left=True,size=0.15)
ax_=pin_wall(ax,0,Hh,s); bx=pin_wall(ax,0,0,s)
cx=W
member(ax,(ax_,Hh),(cx,0)); member(ax,(bx,0),(cx,0)); joint(ax,cx,0)
arrow(ax,cx,-0.05,cx,-0.85); label(ax,cx+0.1,-0.7,"30 kN",fs=8,ha="left")
label(ax,ax_+0.05,Hh+0.2,"A",fs=9); label(ax,bx+0.05,0.2,"B",fs=9); label(ax,cx+0.15,0.15,"C",fs=9)
hdim(ax,0,cx,Hh+0.5,"1.6 m",above=True); ext(ax,cx,0.1,cx,Hh+0.6)
vdim(ax,-0.45,0,Hh,"1.2 m",side="left")
fin(fig,ax,-1.2,2.3,-1.0,Hh+0.95,"d13p_q12.png")

# P14 delta rosette
fig,ax=new(2.8,2.6)
ax.plot([0,0.5],[0,0],color=K,lw=0.7); arrow(ax,1.75,0,2.3,0,lw=0.7); label(ax,2.38,0,"x",fs=9,ha="left"); ax.add_patch(Circle((0,0),0.03,fc=K))
gauge(ax,0,0.55,1.6); label(ax,1.08,0.28,"a",fs=10,fontweight="bold")
for ang,lb in ((60,"b"),(120,"c")):
    gauge(ax,ang,0.55,1.6); t=np.radians(ang); label(ax,1.85*np.cos(t),1.85*np.sin(t),lb,fs=10,fontweight="bold")
for a0,a1,r in ((0,60,0.35),(60,120,0.42)):
    aa=np.radians(np.linspace(a0,a1,30)); ax.plot(r*np.cos(aa),r*np.sin(aa),color=K,lw=0.7)
    m=np.radians((a0+a1)/2); label(ax,(r+0.18)*np.cos(m),(r+0.18)*np.sin(m),"60°",fs=7)
fin(fig,ax,-1.3,2.6,-0.3,1.85,"d13p_q14.png")

# S13 Mohr's circle of strain (units 1e-6): ex=300, ey=500, gxy/2=250
fig,ax=new(3.0,2.6); sc=1/250
ex,ey,h=300,500,250; c=(ex+ey)/2; R=np.hypot((ex-ey)/2,h)
arrow(ax,-0.2,0,(c+R)*sc+0.5,0,lw=0.9); arrow(ax,0,-1.35,0,1.35,lw=0.9)
label(ax,(c+R)*sc+0.55,0,"ε",fs=10,ha="left"); label(ax,0.08,1.35,"γ/2",fs=9,ha="left")
th=np.linspace(0,2*np.pi,200); ax.plot(c*sc+R*sc*np.cos(th),R*sc*np.sin(th),color=K,lw=1.5)
ax.plot([ex*sc,ey*sc],[-h*sc,h*sc],color=K,lw=0.9,ls="--")
for x,y_ in ((ex,-h),(ey,h)): ax.add_patch(Circle((x*sc,y_*sc),0.04,fc=K))
label(ax,ex*sc-0.1,-h*sc-0.12,"X (300, −250)",fs=7,ha="right"); label(ax,ey*sc+0.1,h*sc+0.12,"Y (500, 250)",fs=7,ha="left")
for v,t in ((c-R,"ε₂ = 130.7"),(c+R,"ε₁ = 669.3")):
    ax.add_patch(Circle((v*sc,0),0.04,fc="white",ec=K,zorder=6)); label(ax,v*sc+(0.1 if v<c else -0.1),-0.15,t,fs=7,va="top",ha="left" if v<c else "right")
label(ax,c*sc,0.12,"C (400)",fs=7,va="bottom")
label(ax,(c+R)*sc+0.1,-1.2,"R = 269.3\n(all ×10⁻⁶)",fs=7,ha="center")
fin(fig,ax,-0.3,(c+R)*sc+0.9,-1.45,1.45,"d13p_s13.png")
print("ok")
