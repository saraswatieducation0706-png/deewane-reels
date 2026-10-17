import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
W="#cfe3f3"; OIL="#e8d9a8"
def surface(ax,x,y,s=0.12):
    ax.add_patch(Polygon([[x,y],[x-s,y+1.4*s],[x+s,y+1.4*s]],closed=True,fill=False,ec=K,lw=0.9))
    ax.plot([x-1.5*s,x+1.5*s],[y-0.4*s,y-0.4*s],color=K,lw=0.6); ax.plot([x-0.9*s,x+0.9*s],[y-0.8*s,y-0.8*s],color=K,lw=0.6)
# P10 inclined-tube manometer: reservoir (area A) on the left, tube at 20 deg, reading L = 150 mm along the tube
fig,ax=new(3.6,2.0)
t=np.radians(20); u=np.array([np.cos(t),np.sin(t)])
ax.add_patch(Rectangle((0,0),1.0,0.5,fc=OIL,ec="none")); ax.plot([0,0,1.0,1.0],[1.3,0,0,1.3],color=K,lw=1.3)
ax.plot([0,1.0],[1.3,1.3],color=K,lw=1.3); ax.plot([0,1.0],[0.5,0.5],color=K,lw=0.9)
ax.plot([0.5,0.5],[1.3,1.75],color=K,lw=1.2); label(ax,0.5,1.9,"p₁",fs=9)
w=0.07; p0=np.array([1.0,0.1]); n=np.array([-u[1],u[0]])
Lt=3.6; a=p0-w/2*n; b=p0+w/2*n
ax.plot(*np.c_[a,a+Lt*u],color=K,lw=1.1); ax.plot(*np.c_[b,b+Lt*u],color=K,lw=1.1)
fl=3.0  # liquid length in tube (drawing units)
ax.add_patch(Polygon([a,a+fl*u,b+fl*u,b],closed=True,fc=OIL,ec="none"))
e=p0+fl*u; ax.plot(*np.c_[e-w/2*n,e+w/2*n],color=K,lw=1.0)
tip=p0+Lt*u; label(ax,tip[0]+0.05,tip[1]+0.15,"p₂ (atm)",fs=8,ha="left")
# reading along tube from the zero level (reservoir level extended) to the meniscus
z0=p0+((0.5-p0[1])/u[1])*u  # point on tube axis at reservoir free-surface height
ax.plot([1.0,z0[0]],[0.5,0.5],color=K,lw=0.5,ls=":")
q0=z0+0.32*n; q1=e+0.32*n; arrow(ax,q0[0],q0[1],q1[0],q1[1],lw=0.9,both=True)
ax.plot(*np.c_[z0+0.06*n,z0+0.4*n],color=K,lw=0.5); ax.plot(*np.c_[e+0.06*n,e+0.4*n],color=K,lw=0.5)
m=(q0+q1)/2+0.18*n; label(ax,m[0],m[1],"L = 150 mm",fs=7.5,rotation=20)
ax.plot([1.0,2.2],[0.1,0.1],color=K,lw=0.6); ax.plot(1.0+0.75*np.cos(np.linspace(0,t,20)),0.1+0.75*np.sin(np.linspace(0,t,20)),color=K,lw=0.8)
label(ax,1.95,0.21,"20°",fs=8,ha="left")
label(ax,0.5,0.27,"S = 0.85",fs=7.5)
fin(fig,ax,-0.3,4.9,-0.2,2.1,"d30p_q10.png")
# P12 vertical triangular plate, apex at the free surface, base 2 m horizontal at depth 3 m
fig,ax=new(2.6,2.4)
ax.add_patch(Polygon([[-1.6,0.0],[-1.6,3.0],[1.6,3.0],[1.6,0.0]],closed=True,fc=W,ec="none",zorder=0))
ax.plot([-1.6,1.6],[3.0,3.0],color=K,lw=0.9); surface(ax,1.1,3.0)
ax.add_patch(Polygon([[0,3.0],[-1.0,0.0],[1.0,0.0]],closed=True,fc="#bbbbbb",ec=K,lw=1.4,zorder=3))
hdim(ax,-1.0,1.0,-0.35,"2 m",above=False,fs=8); ext(ax,-1.0,-0.05,-1.0,-0.5); ext(ax,1.0,-0.05,1.0,-0.5)
vdim(ax,-1.35,0.0,3.0,"3 m",side="left",fs=8); ext(ax,-0.95,0.0,-1.45,0.0)
label(ax,0,1.0,"plate",fs=7.5,zorder=4); label(ax,1.25,1.4,"water",fs=8)
fin(fig,ax,-2.1,1.8,-0.8,3.4,"d30p_q12.png")
# P14 cylindrical tank draining through a bottom orifice, head falls from 4 m to 1 m
fig,ax=new(2.6,2.6)
ax.add_patch(Rectangle((0,0),2.0,3.2,fc=W,ec="none")); ax.plot([0,0,0.92],[4.0,0,0],color=K,lw=1.3); ax.plot([1.08,2.0,2.0],[0,0,4.0],color=K,lw=1.3)
ax.plot([0,2.0],[3.2,3.2],color=K,lw=0.9); surface(ax,1.5,3.2)
ax.plot([0,2.0],[0.8,0.8],color=K,lw=0.7,ls="--"); label(ax,1.5,0.95,"final level",fs=6.5)
xs=np.linspace(0,0.5,20); ax.plot(1.0-0.05+0*xs,-xs*1.0,alpha=0)
ax.plot(0.95+0.03*np.linspace(0,1,20)**0.5,-np.linspace(0,0.6,20),color="#5b8fbf",lw=1.0); ax.plot(1.05-0.03*np.linspace(0,1,20)**0.5,-np.linspace(0,0.6,20),color="#5b8fbf",lw=1.0)
label(ax,1.25,-0.35,"orifice, d = 50 mm",fs=7,ha="left")
vdim(ax,2.35,0,3.2,"H₁ = 4 m",side="right",fs=7.5); ext(ax,2.05,3.2,2.45,3.2); ext(ax,2.05,0,2.45,0)
vdim(ax,-0.3,0,0.8,"H₂ = 1 m",side="left",fs=7.5); ext(ax,-0.05,0.8,-0.4,0.8); ext(ax,-0.05,0,-0.4,0)
hdim(ax,0,2.0,3.65,"D = 1.5 m",fs=7.5)
fin(fig,ax,-1.4,3.4,-0.8,4.1,"d30p_q14.png")
