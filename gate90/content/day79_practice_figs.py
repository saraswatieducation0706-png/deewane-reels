import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WATER="#d6e8f7"

# P5 weight hung from two strings at 30 deg and 60 deg to the horizontal
fig,ax=new(3.2,2.2)
O=np.array([0.0,0.0])
L1,L2=2.0,1.155   # chosen so both supports lie on the same ceiling line y = 1.0
A=O+L1*np.array([-np.cos(np.radians(30)),np.sin(np.radians(30))])
B=O+L2*np.array([np.cos(np.radians(60)),np.sin(np.radians(60))])
yc=A[1]
ax.plot([A[0]-0.3,B[0]+0.3],[yc,yc],color=K,lw=1.6); hatch_ground(ax,A[0]-0.3,B[0]+0.3,yc,down=False,size=0.12)
member(ax,O,A,lw=1.2); member(ax,O,B,lw=1.2)
ax.plot([0,0],[0,-0.45],color=K,lw=1.2)
ax.add_patch(Rectangle((-0.25,-0.85),0.5,0.4,fc="#dddddd",ec=K,lw=1.2)); label(ax,0,-0.65,"100 N",fs=7.5)
a=np.radians(np.linspace(180,150,20)); ax.plot(0.55*np.cos(a),0.55*np.sin(a),color=K,lw=0.9)
ax.plot([-0.7,0.7],[0,0],color=K,lw=0.6,ls="--")
label(ax,-0.85,0.17,"30°",fs=8)
a=np.radians(np.linspace(0,60,20)); ax.plot(0.4*np.cos(a),0.4*np.sin(a),color=K,lw=0.9)
label(ax,0.55,0.22,"60°",fs=8)
label(ax,-1.0,0.68,"T₁",fs=8.5); label(ax,0.62,0.55,"T₂",fs=8.5,ha="left")
fin(fig,ax,A[0]-0.45,B[0]+0.5,-1.0,yc+0.3,"d79p_q5.png")

# P8 cantilever with an end mass
fig,ax=new(3.4,1.8)
s=2.6
beam(ax,0,s,t=0.14); fixed(ax,0,left=True,h=0.8)
ax.add_patch(Rectangle((s-0.3,0.07),0.4,0.36,fc="#999999",ec=K,lw=1.2)); label(ax,s-0.1,0.65,"10 kg",fs=8)
hdim(ax,0,s-0.1,-0.45,"0.5 m",above=False); ext(ax,s-0.1,-0.1,s-0.1,-0.5)
sx,sy=s+0.75,0.0
section(ax,[(sx-0.2,sy-0.2,0.4,0.4)])
label(ax,sx,sy-0.38,"20",fs=7); label(ax,sx+0.3,sy,"20",fs=7,ha="left"); label(ax,sx,sy+0.4,"section (mm)",fs=7)
fin(fig,ax,-0.4,s+1.4,-0.8,0.95,"d79p_q8.png")

# P10 vertical circular gate in a tank wall
fig,ax=new(3.0,2.6)
H=3.4
ax.add_patch(Rectangle((0,0),2.0,H,fc=WATER,ec="none"))
ax.plot([2.0,2.0],[-0.1,H+0.4],color=K,lw=1.6)   # tank wall (side view)
ax.plot([0,2.0],[H,H],color="#4a7fb0",lw=1.0)
ax.plot([0.85,1.05,0.95,0.85],[H+0.12,H+0.12,H,H+0.12],color="#4a7fb0",lw=0.9)  # free-surface mark
# gate on the wall (seen edge-on), 1 m tall, top 2 m below the surface (scale 1 m = 0.9)
sc=0.9; gt=H-2*sc; gb=gt-1*sc
ax.plot([2.0,2.0],[gb,gt],color=K,lw=4.5,solid_capstyle="butt")
ax.plot([2.0,2.3],[gt,gt],color=K,lw=0.5); ax.plot([2.0,2.3],[gb,gb],color=K,lw=0.5)
vdim(ax,2.25,gb,gt,"Ø 1 m",side="right",fs=7.5)
vdim(ax,0.45,gt,H,"2 m",side="left",fs=8)
ax.plot([0.35,2.0],[gt,gt],color=K,lw=0.5,ls="--")
label(ax,0.7,0.35,"water",fs=8,style="italic")
label(ax,2.45,gb-0.3,"gate",fs=7.5)
fin(fig,ax,-0.3,3.2,-0.2,H+0.55,"d79p_q10.png")
print("ok")
