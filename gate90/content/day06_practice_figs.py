import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=sys.argv[1] if len(sys.argv)>1 else "fig/"
def udl(ax,x0,x1,y,h=0.45,n=None,lab=None):
    n=n or int((x1-x0)/0.5)+1
    for x in np.linspace(x0,x1,n): arrow(ax,x,y+h,x,y,lw=1.0)
    ax.plot([x0,x1],[y+h,y+h],color=K,lw=1.0)
    if lab: label(ax,(x0+x1)/2,y+h+0.25,lab,fs=8)
# P1 block on incline, pull P at angle
fig,ax=new(3.2,2.0)
a=np.radians(20); L=5
ax.plot([0,L*np.cos(a)],[0,L*np.sin(a)],color=K,lw=1.4); ax.plot([0,L*np.cos(a)],[0,0],color=K,lw=1.2)
hatch_ground(ax,0,L*np.cos(a),0,size=0.2)
u=np.array([np.cos(a),np.sin(a)]); n=np.array([-np.sin(a),np.cos(a)]); p0=2.2*u
blk=[p0,p0+1.0*u,p0+1.0*u+0.7*n,p0+0.7*n]; ax.add_patch(Polygon(blk,closed=True,fill=False,ec=K,lw=1.4))
c=p0+0.5*u+0.35*n; label(ax,*c,"1000 N",fs=7,rotation=20)
d=np.array([np.cos(a+np.radians(35)),np.sin(a+np.radians(35))]); s=p0+1.0*u+0.35*n
arrow(ax,*s,*(s+1.2*d)); label(ax,*(s+1.35*d+np.array([0.15,0])),"P",fs=10)
ax.plot(*zip(s,s+1.0*u),color=K,lw=0.6,ls=":"); label(ax,*(s+0.75*u+np.array([0.05,0.18])),"θ",fs=9)
aa=np.linspace(0,a,20); ax.plot(1.0*np.cos(aa),1.0*np.sin(aa),color=K,lw=0.8); label(ax,1.35,0.17,"20°",fs=8)
ax.set_xlim(-0.3,5.2); ax.set_ylim(-0.4,3.2); save(fig,F+"d6p_q1.png")
# P2 overhanging beam
fig,ax=new(3.8,1.7)
ax.add_patch(Rectangle((0,-0.1),8,0.2,fc="#dddddd",ec=K,lw=1.3))
pin(ax,0,-0.1,0.5); roller(ax,6,-0.1,0.5)
udl(ax,0,6,0.1,lab="10 kN/m")
arrow(ax,8,1.1,8,0.12); label(ax,8,1.3,"30 kN",fs=8)
label(ax,-0.5,-0.1,"A",fs=9); label(ax,6.5,-0.45,"B",fs=9); label(ax,8.35,-0.05,"C",fs=9)
dim(ax,0,-0.95,6,-0.95,"6 m",off=(0,-0.25)); dim(ax,6,-0.95,8,-0.95,"2 m",off=(0,-0.25))
ax.set_xlim(-0.7,8.7); ax.set_ylim(-1.4,1.5); save(fig,F+"d6p_q2.png")
# P3 stacked blocks
fig,ax=new(3.0,1.7)
hatch_ground(ax,-0.5,4.5,0,size=0.2)
ax.add_patch(Rectangle((0.5,0),3,0.8,fill=False,ec=K,lw=1.4)); label(ax,2.0,0.4,"B (200 N)",fs=7)
ax.add_patch(Rectangle((1.2,0.8),1.4,0.7,fill=False,ec=K,lw=1.4)); label(ax,1.9,1.15,"A (100 N)",fs=7)
hatch_wall(ax,-0.3,0.8,1.6,left=True,size=0.15); ax.plot([-0.3,1.2],[1.15,1.15],color=K,lw=1.0)
arrow(ax,3.5,0.4,4.6,0.4); label(ax,4.4,0.65,"P",fs=10)
ax.set_xlim(-0.8,4.9); ax.set_ylim(-0.3,1.8); save(fig,F+"d6p_q3.png")
# P6 drum with hanging mass
fig,ax=new(2.0,2.4)
ax.add_patch(Circle((0,2),0.6,fill=False,ec=K,lw=1.6)); joint(ax,0,2,0.06)
hatch_ground(ax,-0.4,0.4,3.0,down=False,size=0.12); ax.plot([0,0],[2,3.0],color=K,lw=1.6)
ax.plot([0.6,0.6],[2,0.75],color=K,lw=1.0)
ax.add_patch(Rectangle((0.3,0.25),0.6,0.5,fill=False,ec=K,lw=1.4)); label(ax,0.6,0.5,"10 kg",fs=7)
dim(ax,0,2,-0.6*np.cos(np.radians(40)),2+0.6*np.sin(np.radians(40)),"",off=(0,0)); label(ax,-0.5,2.55,"r = 0.25 m",fs=7,ha="right")
label(ax,-0.1,1.2,"I = 0.5 kg·m²",fs=7,ha="right")
ax.set_xlim(-1.9,1.3); ax.set_ylim(0.1,3.2); save(fig,F+"d6p_q6.png")
print("ok")
