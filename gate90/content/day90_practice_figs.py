"""Day 90 (Grand Mock) practice figures. Usage: python3 day90_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

th=np.radians(30); c,s=np.cos(th),np.sin(th)
def incline(ax,L=3.2):
    ax.plot([0,L*c],[0,L*s],color=K,lw=1.4); ax.plot([0,L*c],[0,0],color=K,lw=1.0)
    hatch_ground(ax,0,L*c,0,size=0.1)
    angarc(ax,0,0,0.55,0,30,"30°",fs=8,lr=0.78)
def blockat(ax,d,w=0.7,h=0.45,txt="50 kg"):
    # block resting on the incline at distance d along it
    ux,uy=c,s; nx,ny=-s,c
    p0=(d*ux,d*uy); pts=[p0,(p0[0]+w*ux,p0[1]+w*uy),(p0[0]+w*ux+h*nx,p0[1]+w*uy+h*ny),(p0[0]+h*nx,p0[1]+h*ny)]
    ax.add_patch(Polygon(pts,closed=True,fc="#dddddd",ec=K,lw=1.2,zorder=4))
    cx=p0[0]+w/2*ux+h/2*nx; cy=p0[1]+w/2*uy+h/2*ny
    label(ax,cx,cy,txt,fs=7.5,rotation=30,zorder=5)
    return p0,(cx,cy),(ux,uy),(nx,ny),w,h

# Q5 block pushed up the incline by P parallel to the plane
fig,ax=new(3.6,2.4)
incline(ax)
p0,cg,u,n,w,h=blockat(ax,1.4)
# push force P applied at the lower face centre, acting up the plane
tail=(p0[0]+h/2*n[0]-0.75*u[0],p0[1]+h/2*n[1]-0.75*u[1]); head=(p0[0]+h/2*n[0]-0.03*u[0],p0[1]+h/2*n[1]-0.03*u[1])
arrow(ax,*tail,*head,lw=1.4); label(ax,tail[0]-0.05,tail[1]+0.22,"P",fs=9)
label(ax,2.55,0.55,"μ = 0.2",fs=8)
fin(fig,ax,-0.2,3.0,-0.3,1.95,"d90p_q5.png")

# S5 free-body diagram of the block
fig,ax=new(3.4,2.8)
w,h=1.0,0.6
ux,uy=c,s; nx,ny=-s,c
p0=(0,0); pts=[p0,(w*ux,w*uy),(w*ux+h*nx,w*uy+h*ny),(h*nx,h*ny)]
ax.add_patch(Polygon(pts,closed=True,fc="#eeeeee",ec=K,lw=1.2))
cx=w/2*ux+h/2*nx; cy=w/2*uy+h/2*ny
ax.plot([cx],[cy],marker="o",ms=3,color=K)
arrow(ax,cx,cy,cx,cy-1.15,lw=1.3); label(ax,cx+0.25,cy-1.05,"mg",fs=9)
mid=(w/2*ux,w/2*uy)
arrow(ax,mid[0]-0.85*nx,mid[1]-0.85*ny,mid[0]-0.02*nx,mid[1]-0.02*ny,lw=1.3); label(ax,mid[0]-0.85*nx+0.18,mid[1]-0.85*ny-0.05,"N",fs=9)
fo=(-0.07*nx,-0.07*ny)
arrow(ax,fo[0],fo[1],fo[0]-0.75*ux,fo[1]-0.75*uy,lw=1.3); label(ax,fo[0]-0.75*ux+0.05,fo[1]-0.75*uy-0.22,"F = μN",fs=8)
pl=(h/2*nx,h/2*ny)
arrow(ax,pl[0]-0.9*ux,pl[1]-0.9*uy,pl[0]-0.03*ux,pl[1]-0.03*uy,lw=1.3); label(ax,pl[0]-0.9*ux-0.1,pl[1]-0.9*uy+0.15,"P",fs=9)
fin(fig,ax,-1.3,1.6,-1.0,1.05,"d90p_s5.png")
print("ok")
