import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from matplotlib.patches import Arc
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
G="#bbbbbb"

# Q6 rolling with speeds (schematic)
fig,ax=new(4.4,2.9)
R=2.0; h0=1.2; hf=0.96; cy=hf/2+R
x_in=-np.sqrt(R**2-(cy-h0/2)**2)
xs=np.linspace(x_in,0,40); top=[[x,cy-np.sqrt(R**2-x**2)] for x in xs]
pts=[[-4.0,-h0/2],[-4.0,h0/2]]+top+[[3.3,hf/2],[3.3,-hf/2]]+[[x,-y] for x,y in top[::-1]]
ax.add_patch(Polygon(pts,closed=True,fc=G,ec=K,lw=1.2,zorder=1))
for s in (1,-1):
    ax.add_patch(Circle((0,s*cy),R,fc="#ececec",ec=K,lw=1.3,zorder=2)); ax.plot(0,s*cy,"+",color=K,ms=6,zorder=3)
ax.text(2.0,cy+0.9,"roll surface speed\n2.4 m/s (both rolls)",fontsize=7,ha="left",va="center")
arrow(ax,-3.8,0,-2.9,0,lw=1.3); ax.text(-3.35,0.85,"2 m/s",fontsize=7.5,ha="center")
arrow(ax,2.2,0,3.1,0,lw=1.3)
vdim(ax,-4.4,-h0/2,h0/2,"20 mm ",side="left",fs=7.5)
ax.plot([-4.0,-4.5],[h0/2,h0/2],color=K,lw=0.5); ax.plot([-4.0,-4.5],[-h0/2,-h0/2],color=K,lw=0.5)
vdim(ax,3.7,-hf/2,hf/2," 16 mm",side="right",fs=7.5)
ax.plot([3.3,3.8],[hf/2,hf/2],color=K,lw=0.5); ax.plot([3.3,3.8],[-hf/2,-hf/2],color=K,lw=0.5)
fin(fig,ax,-5.9,5.6,-cy-R-0.1,cy+R+0.1,"d56p_q6.png")

# Q6 solution: strip speed and roll speed along the roll gap
fig,ax=plt.subplots(figsize=(3.8,2.3))
x=np.linspace(0,1,100); v=2.0/(1.0-0.2*x**1.0)   # schematic: thickness falls linearly -> v = v0 h0/h
ax.plot(x,v,color=K,lw=1.5); ax.plot([0,1],[2.4,2.4],color=K,lw=1.0,ls="--")
xn=(1-2.0/2.4)/0.2; ax.plot(xn,2.4,"o",color=K,ms=4); ax.plot([xn,xn],[1.9,2.4],color=K,lw=0.5,ls=":")
ax.text(xn,1.86,"N (neutral point)",fontsize=7,ha="center",va="top")
ax.text(0.02,2.43,"roll surface 2.4",fontsize=7,va="bottom"); ax.text(0.97,2.6,"exit 2.5 (strip faster than rolls)",fontsize=6.5,ha="right",va="bottom")
ax.text(0.02,1.95,"entry 2.0",fontsize=7,va="top")
ax.text(0.3,2.3,"strip slower than rolls",fontsize=6.5,ha="center")
ax.set_xlim(0,1); ax.set_ylim(1.7,2.72); ax.set_xticks([0,1]); ax.set_xticklabels(["entry","exit"],fontsize=7)
ax.set_yticks([]); ax.set_ylabel("speed (m/s)",fontsize=7.5); ax.set_xlabel("position in roll gap",fontsize=7.5)
for s in ("top","right"): ax.spines[s].set_visible(False)
save(fig,F+"d56p_s6.png")

# Q8 direct extrusion
fig,ax=new(4.4,1.9)
ax.add_patch(Rectangle((-3.2,0.9),4.6,0.35,fc="#d0d0d0",ec=K,lw=1.1,hatch="////"))
ax.add_patch(Rectangle((-3.2,-1.25),4.6,0.35,fc="#d0d0d0",ec=K,lw=1.1,hatch="////"))
ax.text(-1.0,1.42,"container",fontsize=7,ha="center")
ax.add_patch(Rectangle((-1.6,-0.9),2.9,1.8,fc=G,ec=K,lw=1.2))                     # billet
ax.add_patch(Rectangle((-3.6,-0.55),2.0,1.1,fc="white",ec=K,lw=1.2)); ax.add_patch(Rectangle((-2.0,-0.9),0.4,1.8,fc="white",ec=K,lw=1.2))
ax.text(-2.85,0,"ram",fontsize=7.5,ha="center",va="center")
ax.add_patch(Polygon([[1.3,0.9],[1.9,0.9],[1.9,0.3],[1.3,0.3]],closed=True,fc="#888888",ec=K,lw=1.1))
ax.add_patch(Polygon([[1.3,-0.9],[1.9,-0.9],[1.9,-0.3],[1.3,-0.3]],closed=True,fc="#888888",ec=K,lw=1.1))
ax.add_patch(Rectangle((1.3,-0.3),2.6,0.6,fc=G,ec=K,lw=1.2)); ax.plot([1.3,1.3],[-0.29,0.29],color=G,lw=2.4)
ax.text(1.6,1.42,"die",fontsize=7,ha="center"); ax.plot([1.6,1.6],[1.3,0.92],color=K,lw=0.6)
arrow(ax,-4.6,0,-3.65,0,lw=1.3); ax.text(-4.6,0.18,"F",fontsize=9,style="italic")
vdim(ax,-0.5,-0.9,0.9,"Ø120",side="right",fs=7.5)
vdim(ax,4.2,-0.3,0.3,"Ø40",side="right",fs=7.5); ax.plot([3.9,4.3],[0.3,0.3],color=K,lw=0.5); ax.plot([3.9,4.3],[-0.3,-0.3],color=K,lw=0.5)
fin(fig,ax,-4.9,5.0,-1.35,1.65,"d56p_q8.png")

# Q12 90° bend: inner radius 6 mm, thickness 2 mm, neutral axis at 0.4t
fig,ax=new(3.4,2.6)
ri,t=1.5,0.5
th=np.linspace(np.pi,1.5*np.pi,50)
cx,cy=0,0
outer=[[cx+(ri+t)*np.cos(a),cy+(ri+t)*np.sin(a)] for a in th]; inner=[[cx+ri*np.cos(a),cy+ri*np.sin(a)] for a in th[::-1]]
leg1=[[-(ri+t),2.2],[-ri,2.2]]
poly=[[-ri,2.2],[-(ri+t),2.2]]+outer+[[2.2,-(ri+t)],[2.2,-ri]]+inner
ax.add_patch(Polygon(poly,closed=True,fc=G,ec=K,lw=1.2))
na=[[cx+(ri+0.4*t)*np.cos(a),cy+(ri+0.4*t)*np.sin(a)] for a in th]
ax.plot([p[0] for p in na],[p[1] for p in na],color=K,lw=0.9,ls="-.")
ax.plot(0,0,"+",color=K,ms=6)
ax.annotate("",xy=(ri*np.cos(np.radians(200)),ri*np.sin(np.radians(200))),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",lw=0.9,color=K))
ax.text(-0.15,0.12,"R = 6 mm",fontsize=7.5,ha="right",va="bottom")
ax.annotate("neutral axis",xy=(na[30][0],na[30][1]),xytext=(-2.9,-2.5),fontsize=7.5,ha="center",arrowprops=dict(arrowstyle="-",lw=0.6))
hdim(ax,-(ri+t),-ri,2.35,"t = 2 mm",fs=7.5)
ax.text(0.6,-0.6,"90°",fontsize=8,ha="center")
fin(fig,ax,-3.9,2.4,-2.8,2.85,"d56p_q12.png")
