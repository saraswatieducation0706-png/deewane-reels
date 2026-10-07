import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch
K="black"
def new(w=3.6,h=2.6):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_aspect("equal"); ax.axis("off"); return fig,ax
def save(fig,path):
    fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="white"); plt.close(fig)
def arrow(ax,x1,y1,x2,y2,lw=1.6,both=False,color=K):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="<|-|>" if both else "-|>",mutation_scale=11,lw=lw,color=color,shrinkA=0,shrinkB=0))
def hatch_ground(ax,x0,x1,y,down=True,n=None,size=0.12):
    ax.plot([x0,x1],[y,y],color=K,lw=1.2)
    n=n or max(3,int((x1-x0)/size))
    xs=np.linspace(x0,x1,n)
    for x in xs: ax.plot([x,x-size*0.7],[y,y-size*0.7] if down else [y,y+size*0.7],color=K,lw=0.8)
def hatch_wall(ax,x,y0,y1,left=True,size=0.12):
    ax.plot([x,x],[y0,y1],color=K,lw=1.2)
    for y in np.linspace(y0,y1,max(3,int((y1-y0)/size))):
        ax.plot([x,x-size*0.7 if left else x+size*0.7],[y,y-size*0.7],color=K,lw=0.8)
def pin(ax,x,y,s=0.3):
    ax.add_patch(Polygon([[x,y],[x-s/2,y-s*0.8],[x+s/2,y-s*0.8]],closed=True,fill=False,ec=K,lw=1.2))
    ax.add_patch(Circle((x,y),s*0.1,fc="white",ec=K,lw=1,zorder=5))
    hatch_ground(ax,x-s*0.8,x+s*0.8,y-s*0.8,size=s*0.4)
def roller(ax,x,y,s=0.3):
    ax.add_patch(Polygon([[x,y],[x-s/2,y-s*0.6],[x+s/2,y-s*0.6]],closed=True,fill=False,ec=K,lw=1.2))
    ax.add_patch(Circle((x,y),s*0.1,fc="white",ec=K,lw=1,zorder=5))
    for dx in (-s*0.3,0,s*0.3): ax.add_patch(Circle((x+dx,y-s*0.6-s*0.1),s*0.1,fill=False,ec=K,lw=1))
    hatch_ground(ax,x-s*0.8,x+s*0.8,y-s*0.8,size=s*0.4)
def joint(ax,x,y,r=0.06): ax.add_patch(Circle((x,y),r,fc="white",ec=K,lw=1.2,zorder=6))
def member(ax,p,q,lw=2): ax.plot([p[0],q[0]],[p[1],q[1]],color=K,lw=lw,solid_capstyle="round")
def label(ax,x,y,t,fs=10,**k): ax.text(x,y,t,fontsize=fs,ha=k.pop("ha","center"),va=k.pop("va","center"),**k)
def dim(ax,x1,y1,x2,y2,t,off=(0,-0.25)):
    arrow(ax,x1,y1,x2,y2,lw=0.9,both=True)
    label(ax,(x1+x2)/2+off[0],(y1+y2)/2+off[1],t,fs=9)
