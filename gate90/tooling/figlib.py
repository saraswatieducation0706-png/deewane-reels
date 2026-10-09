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
# --- strength-of-materials helpers (added Day 5) ---
def stress_element(ax,sx,sy,txy,a=1.0,L=0.7,units="MPa",plane=None):
    """Square element of side a centred at origin. sx, sy, txy are numbers (sign = direction; 0 = omitted).
    Normal arrows outward for tension. txy>0 acts +y on the +x face. plane=angle (deg) draws a dashed inclined plane."""
    h=a/2; ax.add_patch(Rectangle((-h,-h),a,a,fill=False,ec=K,lw=1.6))
    if sx:
        for s in (1,-1):
            p0,p1=((h+0.08)*s,(h+0.08+L)*s) if sx>0 else ((h+0.08+L)*s,(h+0.08)*s)
            arrow(ax,p0,0,p1,0)
        label(ax,h+0.16+L,0,f"σx = {abs(sx)} {units}",fs=8,ha="left")
    if sy:
        for s in (1,-1):
            p0,p1=((h+0.08)*s,(h+0.08+L)*s) if sy>0 else ((h+0.08+L)*s,(h+0.08)*s)
            arrow(ax,0,p0,0,p1)
        label(ax,0,h+0.22+L,f"σy = {abs(sy)} {units}",fs=8,va="bottom")
    if txy:
        d=1 if txy>0 else -1; g=0.12; l=0.7*a/2
        arrow(ax,h+g,-l*d,h+g,l*d); arrow(ax,-h-g,l*d,-h-g,-l*d)
        arrow(ax,-l*d,h+g,l*d,h+g); arrow(ax,l*d,-h-g,-l*d,-h-g)
        label(ax,l+0.12,h+g+0.02,f"τxy = {abs(txy)} {units}",fs=8,ha="left",va="bottom")
    if plane is not None:
        t=np.radians(plane); ux,uy=np.sin(t),-np.cos(t)  # plane line through centre; normal at angle `plane` from x
        ax.plot([-0.75*a*ux,0.75*a*ux],[-0.75*a*uy,0.75*a*uy],color=K,lw=1.0,ls="--")
        arrow(ax,0,0,0.45*a*np.cos(t),0.45*a*np.sin(t),lw=1.0); label(ax,0.45*a*np.cos(t)-0.08,0.45*a*np.sin(t)+0.1,"n",fs=9)
        aa=np.linspace(0,t,20); ax.plot(0.25*a*np.cos(aa),0.25*a*np.sin(aa),color=K,lw=0.8)
        ax.plot([0,0.45*a],[0,0],color=K,lw=0.6,ls=":")
        label(ax,0.4*a*np.cos(t*0.3),0.4*a*np.sin(t*0.3)-0.02,f"{plane}°",fs=7)
def mohr(ax,sx,sy,txy,unit="MPa",pts=True):
    """Mohr's circle (axes sigma right, tau down-positive convention not used: tau plotted up for clockwise-positive)."""
    c=(sx+sy)/2; R=float(np.hypot((sx-sy)/2,txy)); th=np.linspace(0,2*np.pi,200)
    lo=min(0,c-R)-0.25*R; hi=max(0,c+R)+0.25*R
    arrow(ax,lo,0,hi,0,lw=0.9); arrow(ax,0,-1.3*R,0,1.3*R,lw=0.9)
    label(ax,hi+0.06*R,0,"σ",fs=10,ha="left"); label(ax,0.1*R,1.3*R,"τ",fs=10,ha="left")
    ax.plot(c+R*np.cos(th),R*np.sin(th),color=K,lw=1.5)
    if pts:
        ax.plot([sx,sy],[-txy,txy],color=K,lw=0.9,ls="--")
        for x,y in ((sx,-txy),(sy,txy)): ax.add_patch(Circle((x,y),0.03*R,fc=K))
    for x in (c-R,c+R): ax.add_patch(Circle((x,0),0.03*R,fc="white",ec=K,zorder=6))
    return c,R
# --- beam helpers (added Day 7) ---
def beam(ax,x0,x1,t=0.2):
    ax.add_patch(Rectangle((x0,-t/2),x1-x0,t,fc="#dddddd",ec=K,lw=1.3))
def fixed(ax,x,left=True,h=0.8): hatch_wall(ax,x,-h/2,h/2,left=left,size=0.15)
def pload(ax,x,txt,y0=0.1,L=0.9,fs=8,ang=90):
    t=np.radians(ang); sx,sy=x+L*np.cos(t),y0+L*np.sin(t)
    arrow(ax,sx,sy,x,y0); label(ax,sx,sy+0.2,txt,fs=fs)
def udl(ax,x0,x1,txt,y=0.1,h=0.45,fs=8,lx=None):
    n=max(3,int(round((x1-x0)/0.45))+1)
    for x in np.linspace(x0,x1,n): arrow(ax,x,y+h,x,y,lw=0.9)
    ax.plot([x0,x1],[y+h,y+h],color=K,lw=1.0); label(ax,(x0+x1)/2 if lx is None else lx,y+h+0.22,txt,fs=fs)
def tri_load(ax,x0,x1,txt,y=0.1,h=0.8,up_at_right=True,fs=8):
    n=max(4,int(round((x1-x0)/0.45))+1)
    for x in np.linspace(x0,x1,n):
        f=(x-x0)/(x1-x0) if up_at_right else (x1-x)/(x1-x0)
        if f*h>0.12: arrow(ax,x,y+f*h,x,y,lw=0.9)
    ax.plot([x0,x1],[y,y+h] if up_at_right else [y+h,y],color=K,lw=1.0)
    label(ax,x1 if up_at_right else x0,y+h+0.22,txt,fs=fs)
def couple(ax,x,txt,cw=True,r=0.4,fs=8,y=0.12):
    a=np.radians(np.linspace(165,15,40)) if cw else np.radians(np.linspace(15,165,40))
    xs,ys=x+r*np.cos(a),y+r*np.sin(a)
    ax.plot(xs[:-3],ys[:-3],color=K,lw=1.3); arrow(ax,xs[-4],ys[-4],xs[-1],ys[-1],lw=1.3)
    label(ax,x,y+r+0.25,txt,fs=fs)
def diagrams(path,L,x,V,M,vunit="kN",munit="kN·m",vmarks=(),mmarks=(),w=3.6,h=2.6):
    """SFD and BMD stacked. x, V, M arrays (sagging +). marks = list of (x, value, text)."""
    fig,(a1,a2)=plt.subplots(2,1,figsize=(w,h),sharex=True)
    for a,y,nm,mk in ((a1,V,f"SFD ({vunit})",vmarks),(a2,M,f"BMD ({munit})",mmarks)):
        a.fill_between(x,y,0,color="#cccccc"); a.plot(x,y,color=K,lw=1.4); a.axhline(0,color=K,lw=0.9)
        a.set_ylabel(nm,fontsize=8); a.tick_params(labelsize=7); a.set_yticks([])
        for s in ("top","right","left"): a.spines[s].set_visible(False)
        rng=max(abs(np.min(y)),abs(np.max(y))) or 1
        a.set_ylim(min(np.min(y),0)-0.55*rng,max(np.max(y),0)+0.35*rng)
        for (xx,yy,t) in mk: a.text(xx,yy+(0.08*rng if yy>=0 else -0.08*rng),t,fontsize=7,ha="center",va="bottom" if yy>=0 else "top")
    a1.spines["bottom"].set_visible(False); a1.tick_params(bottom=False)
    a2.set_xlabel("x (m)",fontsize=8); a1.set_xlim(-0.05*L,1.05*L)
    fig.tight_layout(); fig.savefig(path,dpi=150,facecolor="white"); plt.close(fig)
# --- cross-section helpers (added Day 8) ---
def section(ax,rects,fc="#dddddd"):
    """rects = list of (x, y, w, h) in drawing units; drawn grey with black outline."""
    for (x,y,w,h) in rects: ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=K,lw=1.3))
def vdim(ax,x,y0,y1,t,side="left",fs=8,ext=None):
    """vertical dimension line at x from y0 to y1, label to the side; ext=(xa,xb) draws thin extension ticks."""
    arrow(ax,x,y0,x,y1,lw=0.9,both=True)
    label(ax,x-0.08 if side=="left" else x+0.08,(y0+y1)/2,t,fs=fs,ha="right" if side=="left" else "left")
def hdim(ax,x0,x1,y,t,above=True,fs=8):
    arrow(ax,x0,y,x1,y,lw=0.9,both=True)
    label(ax,(x0+x1)/2,y+0.12 if above else y-0.12,t,fs=fs,va="bottom" if above else "top")
def ext(ax,x0,y0,x1,y1): ax.plot([x0,x1],[y0,y1],color=K,lw=0.5)
def na_line(ax,x0,x1,y,txt="N.A.",fs=8):
    ax.plot([x0,x1],[y,y],color=K,lw=0.9,ls="-."); label(ax,x1+0.05,y,txt,fs=fs,ha="left")
