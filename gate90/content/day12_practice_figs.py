import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
sys.path.insert(0,"/home/claude/deewane-reels/gate90/tooling")
from figlib import *
from beamsolve import solve
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,name,y0=-1.3,y1=1.7): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def shaft(ax,x0,x1,d,fc="#dddddd"): ax.add_patch(Rectangle((x0,-d/2),x1-x0,d,fc=fc,ec=K,lw=1.3))
def torque(ax,x,r,txt,up=True,fs=8,lx=0.0):
    t=np.radians(np.linspace(-75,75,40)) if up else np.radians(np.linspace(75,-75,40))
    xs=x+0.13*np.cos(t); ys=r*np.sin(t)
    ax.plot(xs[:-3],ys[:-3],color=K,lw=1.4); arrow(ax,xs[-4],ys[-4],xs[-1],ys[-1],lw=1.4)
    label(ax,x+lx,r+0.2,txt,fs=fs,va="bottom")

# P1: SS beam 6 m, triangular load 0 at A to 18 kN/m at B
S=0.6
fig,ax=new(3.4,2.0); beam(ax,0,6*S); pin(ax,0,-0.1,0.4); roller(ax,6*S,-0.1,0.4)
tri_load(ax,0,6*S,"18 kN/m",h=0.9)
label(ax,-0.25,0.05,"A",fs=9); label(ax,6*S+0.25,0.05,"B",fs=9)
dim(ax,0,-0.9,6*S,-0.9,"6 m")
fin(fig,ax,-0.5,6*S+0.5,"d12p_q1.png",y0=-1.25,y1=1.45)

# P2: overhanging beam, A pin, B roller at 5 m, C at 6.5 m, UDL 10 kN/m throughout
S=0.55
fig,ax=new(3.4,1.9); beam(ax,0,6.5*S); pin(ax,0,-0.1,0.4); roller(ax,5*S,-0.1,0.4)
udl(ax,0,6.5*S,"10 kN/m")
label(ax,-0.25,0.05,"A",fs=9); label(ax,5*S+0.05,-0.75,"B",fs=9,ha="left"); label(ax,6.5*S+0.25,0.05,"C",fs=9)
dim(ax,0,-1.0,5*S,-1.0,"5 m"); dim(ax,5*S,-1.0,6.5*S,-1.0,"1.5 m"); ext(ax,6.5*S,-0.15,6.5*S,-1.1)
fin(fig,ax,-0.5,6.5*S+0.5,"d12p_q2.png",y0=-1.4,y1=1.25)
x,V,M,R=solve(6.5,(0,5),[('U',0,6.5,10)])
diagrams(F+"d12p_s2.png",6.5,x,V,M,vmarks=[(0.3,22.75,"22.75"),(4.6,-27.25,"−27.25"),(5.3,15,"15")],
         mmarks=[(2.275,25.88,"25.88 at x = 2.275 m"),(5.0,-11.25,"−11.25")],w=3.4,h=2.6)

# P4: unequal I-section (top flange 100x20, web 10x160, bottom flange 160x20)
s=0.01; yb=84.12
fig,ax=new(2.8,2.6)
section(ax,[(30*s,180*s,100*s,20*s),(75*s,20*s,10*s,160*s),(0,0,160*s,20*s)])
na_line(ax,-0.1,1.75,yb*s,"N.A.")
hdim(ax,30*s,130*s,2.12,"100 mm"); ext(ax,0.3,2.0,0.3,2.2); ext(ax,1.3,2.0,1.3,2.2)
hdim(ax,0,1.6,-0.15,"160 mm",above=False); ext(ax,0,0,0,-0.25); ext(ax,1.6,0,1.6,-0.25)
vdim(ax,-0.25,0,2.0,"200 mm",side="left"); ext(ax,0,0,-0.35,0); ext(ax,0.3,2.0,-0.35,2.0)
arrow(ax,1.75,1.9,1.3,1.9,lw=0.8); label(ax,1.8,1.9,"20 mm",fs=7,ha="left")
arrow(ax,1.75,0.1,1.6,0.1,lw=0.8); label(ax,1.8,0.1,"20 mm",fs=7,ha="left")
arrow(ax,1.25,1.35,0.85,1.35,lw=0.8); label(ax,1.3,1.35,"web 10 mm",fs=7,ha="left")
fin(fig,ax,-1.15,2.6,"d12p_q4.png",y0=-0.6,y1=2.45)
# P4 solution: bending stress distribution
fig,ax=new(3.4,2.4)
section(ax,[(30*s,180*s,100*s,20*s),(75*s,20*s,10*s,160*s),(0,0,160*s,20*s)])
na_line(ax,-0.1,1.7,yb*s,"")
x0=2.4; k=0.012
ax.plot([x0,x0],[0,2.0],color=K,lw=0.9)
ax.add_patch(Polygon([[x0,yb*s],[x0-65.86*k,2.0],[x0,2.0]],fc="#cccccc",ec=K,lw=1.0))
ax.add_patch(Polygon([[x0,yb*s],[x0+47.80*k,0],[x0,0]],fc="#cccccc",ec=K,lw=1.0))
label(ax,x0-0.4,2.13,"65.86 MPa (C)",fs=7.5,va="bottom"); label(ax,x0+0.35,-0.1,"47.80 MPa (T)",fs=7.5,va="top")
label(ax,x0+0.1,yb*s,"0",fs=7.5,ha="left"); label(ax,0.8,-0.15,"N.A. 84.12 mm above base",fs=7,va="top")
fin(fig,ax,-0.2,3.5,"d12p_s4.png",y0=-0.5,y1=2.4)

# P6: T-beam made of two 50 x 150 planks nailed together
fig,ax=new(2.6,2.4)
section(ax,[(0,1.5,1.5,0.5),(0.5,0,0.5,1.5)])
for xx in (0.75,): ax.plot([xx,xx],[2.0,1.25],color=K,lw=1.6); ax.plot([xx-0.06,xx+0.06],[2.0,2.0],color=K,lw=2.2)
label(ax,0.95,2.25,"nail",fs=7,ha="left"); arrow(ax,0.95,2.25,0.79,2.02,lw=0.7)
hdim(ax,0,1.5,2.35,"150 mm"); ext(ax,0,2.0,0,2.45); ext(ax,1.5,2.0,1.5,2.45)
vdim(ax,1.75,1.5,2.0,"50 mm",side="right"); ext(ax,1.5,1.5,1.85,1.5); ext(ax,1.5,2.0,1.85,2.0)
vdim(ax,1.25,0,1.5,"150 mm",side="right"); ext(ax,1.0,0,1.35,0)
hdim(ax,0.5,1.0,-0.15,"50 mm",above=False); ext(ax,0.5,0,0.5,-0.25); ext(ax,1.0,0,1.0,-0.25)
fin(fig,ax,-0.3,2.6,"d12p_q6.png",y0=-0.55,y1=2.75)

# P10: cantilever 4 m, UDL 6 kN/m over 2 m next to the fixed end
S=0.75
fig,ax=new(3.2,1.8); beam(ax,0,4*S); fixed(ax,0,left=True)
udl(ax,0,2*S,"6 kN/m")
label(ax,-0.3,0.5,"A",fs=9); label(ax,4*S+0.25,0.05,"B",fs=9)
dim(ax,0,-0.75,2*S,-0.75,"2 m"); dim(ax,2*S,-0.75,4*S,-0.75,"2 m"); ext(ax,2*S,-0.15,2*S,-0.85); ext(ax,4*S,-0.15,4*S,-0.85)
label(ax,3.2*S,0.3,"EI = 12 000 kN·m²",fs=7)
fin(fig,ax,-0.5,4*S+0.5,"d12p_q10.png",y0=-1.1,y1=1.2)
# P10 solution: deflected shape (curved over the loaded part, straight beyond)
xx=np.linspace(0,4,401); w=6; a=2; EI=1.0
def yc(x):
    x=np.minimum(x,a); return w*x**2*(6*a**2-4*a*x+x**2)/(24*EI)
ya=yc(np.array([a]))[0]; th=w*a**3/(6*EI)
y=np.where(xx<=a,yc(xx),ya+th*(xx-a)); kk=0.7/y.max()
fig,ax=new(3.2,1.5); fixed(ax,0,left=True,h=0.6)
ax.plot([0,4*S],[0,0],color=K,lw=0.8,ls="--"); ax.plot(xx*S,-y*kk,color=K,lw=1.8)
label(ax,1.6*S,-0.5,"curved (loaded)",fs=7); label(ax,3.2*S,-0.12,"straight",fs=7)
arrow(ax,4*S+0.15,0,4*S+0.15,-y.max()*kk,lw=0.9,both=True); label(ax,4*S+0.25,-0.35,"δB = 2.33 mm",fs=7.5,ha="left")
fin(fig,ax,-0.4,4*S+1.3,"d12p_s10.png",y0=-0.95,y1=0.4)

# P15: solid shaft 60 mm, 1.2 m, torque 1.5 kN·m
fig,ax=new(3.2,1.6); L=2.6; d=0.5
shaft(ax,0,L,d); ax.plot([-0.2,L+0.3],[0,0],color=K,lw=0.6,ls="-."); hatch_wall(ax,0,-0.5,0.5,left=True,size=0.15)
torque(ax,L,0.42,"T = 1.5 kN·m",lx=-0.3)
vdim(ax,L+0.45,-d/2,d/2,"60 mm",side="right"); ext(ax,L,d/2,L+0.5,d/2); ext(ax,L,-d/2,L+0.5,-d/2)
hdim(ax,0,L,-0.65,"1.2 m",above=False)
label(ax,1.2,0.42,"G = 80 GPa",fs=8)
ax.set_xlim(-0.4,L+1.4); ax.set_ylim(-1.0,1.0); save(fig,F+"d12p_q15.png")
print("practice figs ok")
