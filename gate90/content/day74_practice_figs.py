import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
MET="#cfcfcf"

# P4 Brinell indentation (section)
fig,ax=new(3.4,2.4)
R=1.0; d=0.8; c=np.sqrt(R**2-(d/2)**2)   # ball centre height above surface
yc=c
ax.add_patch(Rectangle((-1.8,-0.9),3.6,0.9,fc=MET,ec=K,lw=1.2))
# indentation (spherical cap) cut out of the specimen
phi=np.linspace(-np.pi/2-np.arcsin(d/2/R),-np.pi/2+np.arcsin(d/2/R),60)
cap=np.c_[R*np.cos(phi),yc+R*np.sin(phi)]
ax.add_patch(Polygon(np.r_[cap,[[d/2,0],[-d/2,0]]],closed=True,fc="white",ec="none",zorder=2))
ax.plot([-1.8,-d/2],[0,0],color=K,lw=1.2,zorder=3); ax.plot([d/2,1.8],[0,0],color=K,lw=1.2,zorder=3)
ax.add_patch(Circle((0,yc),R,fc="#e8e8e8",ec=K,lw=1.3,zorder=4))
arrow(ax,0,yc+R+0.7,0,yc+R+0.05,lw=1.5); label(ax,0.12,yc+R+0.45,"P = 3000 kgf",fs=7.5,ha="left")
hdim(ax,-d/2,d/2,-0.25,"d = 4 mm",above=False,fs=7)
ax.plot([-d/2,-d/2],[-0.05,-0.3],color=K,lw=0.5); ax.plot([d/2,d/2],[-0.05,-0.3],color=K,lw=0.5)
ax.add_patch(FancyArrowPatch((-R,yc),(R,yc),arrowstyle="<|-|>",mutation_scale=9,lw=0.9,color=K,shrinkA=0,shrinkB=0,zorder=6))
label(ax,0,yc+0.17,"D = 10 mm",fs=7,zorder=6)
label(ax,1.25,-0.55,"specimen",fs=7.5)
fin(fig,ax,-1.9,1.9,-1.0,yc+R+0.8,"d74p_q4.png")

# P11 upsetting between flat platens (before / after)
fig,ax=new(3.8,2.3)
def platen(x0,x1,y,top):
    ax.add_patch(Rectangle((x0,y if not top else y),x1-x0,0.18 if top else -0.18,fc="#b0b0b0",ec=K,lw=1.1))
# before
w0,h0=0.8,1.2; x0=0.0
ax.add_patch(Rectangle((x0-w0/2,0),w0,h0,fc=MET,ec=K,lw=1.3))
platen(-0.75,0.75,h0,True); platen(-0.75,0.75,0,False)
hdim(ax,x0-w0/2,x0+w0/2,h0+0.42,"Ø40",fs=7)
vdim(ax,-0.95,0,h0,"60",side="left",fs=7)
label(ax,0,-0.45,"before",fs=8)
# after
w1,h1=0.8*np.sqrt(2),0.6; x1=2.6
ax.add_patch(Rectangle((x1-w1/2,0),w1,h1,fc=MET,ec=K,lw=1.3))
platen(x1-0.85,x1+0.85,h1,True); platen(x1-0.85,x1+0.85,0,False)
vdim(ax,x1+1.05,0,h1,"30",side="right",fs=7)
arrow(ax,x1,h1+0.75,x1,h1+0.2,lw=1.4); label(ax,x1+0.1,h1+0.55,"F",fs=8.5,ha="left")
label(ax,x1,-0.45,"after (frictionless)",fs=8)
label(ax,1.3,0.6,"→",fs=14)
label(ax,1.3,-0.8,"dimensions in mm",fs=7)
fin(fig,ax,-1.4,3.9,-0.95,2.0,"d74p_q11.png")
