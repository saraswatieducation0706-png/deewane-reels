"""Day 68 (GA Revision) practice figures. Usage: python3 day68_practice_figs.py <outdir>
Spatial shapes are lists of primitives that can be reflected exactly, so each option is generated from
(and checked against) the operation it represents."""
# ---- spatial-aptitude figure library (shapes as transformable primitives) ----
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, itertools
from matplotlib.patches import Polygon as _Poly, Circle as _Circ, Rectangle as _Rect, PathPatch as _PP
from matplotlib.path import Path as _Path
from matplotlib.textpath import TextPath as _TP
from matplotlib.font_manager import FontProperties as _FP
K="black"; GREY="#777777"
# primitive: dict(k='poly'|'line'|'circ'|'path', ...)
def poly(pts,fill=False): return dict(k="poly",p=np.array(pts,float),fill=fill)
def line(pts,lw=1.6): return dict(k="line",p=np.array(pts,float),lw=lw)
def circ(c,r,fill=False): return dict(k="circ",p=np.array([c],float),r=r,fill=fill)
def arrowp(p,q,head=0.22,w=0.13):
    p,q=np.array(p,float),np.array(q,float); d=(q-p)/np.linalg.norm(q-p); n=np.array([-d[1],d[0]])
    b=q-d*head; return [line([p,b]),poly([q,b+n*w,b-n*w],fill=True)]
def text_shape(s,x,y,h=0.5,weight="bold",per_letter=False):
    """returns list of 'path' primitives; centred at (x,y), cap height ~h"""
    fp=_FP(family="DejaVu Sans",weight=weight)
    tp=_TP((0,0),s,size=1,prop=fp); v=tp.vertices.copy(); bb=tp.get_extents()
    sc=h/0.73; v=(v-[bb.x0+bb.width/2,bb.y0+bb.height/2])*sc+[x,y]
    return [dict(k="path",p=v,codes=tp.codes.copy())]
def letters(s,x,y,h=0.5,gap=0.08):
    """each character its own path, laid left to right, centred at x"""
    fp=_FP(family="DejaVu Sans",weight="bold"); out=[]; ws=[]
    tps=[_TP((0,0),c,size=1,prop=fp) for c in s]; sc=h/0.73
    for tp in tps: e=tp.get_extents(); ws.append(e.width*sc)
    tot=sum(ws)+gap*(len(s)-1); cx=x-tot/2
    for tp,w in zip(tps,ws):
        e=tp.get_extents(); v=(tp.vertices-[e.x0+e.width/2,0.365])*sc+[cx+w/2,y]
        out.append(dict(k="path",p=v,codes=tp.codes.copy())); cx+=w+gap
    return out
def tf(shape,M,t=(0,0),about=(0,0)):
    M=np.array(M,float); a=np.array(about,float); out=[]
    for e in shape:
        e2=dict(e); e2["p"]=(e["p"]-a)@M.T+a+np.array(t,float); out.append(e2)
    return out
def rot(shape,deg,about=(0,0)):
    c,s=np.cos(np.radians(deg)),np.sin(np.radians(deg)); return tf(shape,[[c,-s],[s,c]],about=about)
def mirror_x(shape,about=(0,0)): return tf(shape,[[-1,0],[0,1]],about=about)   # vertical mirror (left-right)
def mirror_y(shape,about=(0,0)): return tf(shape,[[1,0],[0,-1]],about=about)   # water image (top-bottom)
def shift(shape,dx,dy): return tf(shape,np.eye(2),t=(dx,dy))
def scale(shape,s): return tf(shape,np.eye(2)*s)
# ---- canonical key for equality tests ----
def _r(a): return tuple(map(tuple,np.round(np.array(a)+0.0,3)+0.0))
def key(shape):
    ks=[]
    for e in shape:
        p=_r(e["p"])
        if e["k"]=="poly":
            n=len(p); cands=[]
            for seq in (p,p[::-1]):
                for i in range(n): cands.append(seq[i:]+seq[:i])
            ks.append(("poly",min(cands),e["fill"]))
        elif e["k"]=="line": ks.append(("line",min(p,p[::-1])))
        elif e["k"]=="circ": ks.append(("circ",p,round(e["r"],3),e["fill"]))
        else: ks.append(("path",tuple(sorted(p))))
    return tuple(sorted(ks,key=repr))
def same(a,b): return key(a)==key(b)
def D4(shape):
    """the 8 images under the square's symmetry group, by name"""
    r={}
    for d in (0,90,180,270):
        r[f"rot{d}"]=rot(shape,d); r[f"mir_rot{d}"]=rot(mirror_x(shape),d)
    return r
def which(shape,ref):
    return [n for n,s in D4(ref).items() if same(shape,s)]
# ---- drawing ----
def draw(ax,shape,x=0,y=0,s=1.0,lw=1.6,frame=True,fsz=1.0):
    if frame: ax.add_patch(_Rect((x-fsz*s,y-fsz*s),2*fsz*s,2*fsz*s,fill=False,ec=K,lw=1.0))
    for e in shape:
        p=e["p"]*s+[x,y]
        if e["k"]=="poly": ax.add_patch(_Poly(p,closed=True,fc=K if e["fill"] else "none",ec=K,lw=lw,joinstyle="miter"))
        elif e["k"]=="line": ax.plot(p[:,0],p[:,1],color=K,lw=e.get("lw",lw)*(lw/1.6),solid_capstyle="butt")
        elif e["k"]=="circ": ax.add_patch(_Circ(p[0],e["r"]*s,fc=K if e["fill"] else "white",ec=K,lw=lw))
        else: ax.add_patch(_PP(_Path(p,e["codes"]),fc=K,ec="none"))
def cap(ax,x,y,t,fs=10): ax.text(x,y,t,fontsize=fs,ha="center",va="top",fontweight="bold")
def canvas(w,h):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_aspect("equal"); ax.axis("off"); return fig,ax
def savefig(fig,ax,path,lim=None):
    if lim: ax.set_xlim(lim[0],lim[1]); ax.set_ylim(lim[2],lim[3])
    fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="white",pad_inches=0.04); plt.close(fig)
def options_fig(path,prob,opts,prob_title="Problem figure",extra=None,wide=False,fs=10,lw=1.6):
    """prob: shape (or callable(ax,x,y) drawing it); opts: 4 shapes. Layout: problem left, options 2x2 right (or 1 row if wide)."""
    if wide:   # two rows: problem figure on top, the four options below
        fig,ax=canvas(6.6,3.2); px=4.6
        if callable(prob): prob(ax,px,1.3)
        else: draw(ax,prob,px,1.3,lw=lw)
        ax.text(px,2.42,prob_title,fontsize=fs-1,ha="center",va="bottom")
        for i,o in enumerate(opts):
            x=1.15+2.3*i; draw(ax,o,x,-1.3,lw=lw); cap(ax,x,-2.4,"(%s)"%"ABCD"[i],fs)
        if extra: extra(ax)
        savefig(fig,ax,path,(-0.2,9.5,-2.85,2.75))
    else:
        fig,ax=canvas(5.0,3.0)
        if callable(prob): prob(ax,0,0)
        else: draw(ax,prob,0,0,lw=lw)
        ax.text(0,1.2,prob_title,fontsize=fs-1,ha="center",va="bottom")
        ax.plot([1.9,1.9],[-2.9,2.6],color=GREY,lw=0.8)
        pos=[(3.3,1.15),(5.8,1.15),(3.3,-1.75),(5.8,-1.75)]
        for i,(o,(x,y)) in enumerate(zip(opts,pos)):
            draw(ax,o,x,y,s=0.95,lw=lw); cap(ax,x,y-1.03,f"({'ABCD'[i]})",fs)
        if extra: extra(ax)
        savefig(fig,ax,path,(-1.3,7.0,-3.15,2.55))
# ---- paper folding ----
FOLDS={ # name: (reflection about fold line as function, kept-half test, line endpoints in full square)
 "R2L":(lambda s: mirror_x(s), "x=0"),   # right half folded over onto left half
 "L2R":(lambda s: mirror_x(s), "x=0"),
 "T2B":(lambda s: mirror_y(s), "y=0"),
 "B2T":(lambda s: mirror_y(s), "y=0"),
}
def unfold(holes,folds):
    """holes: shape in coordinates of the full square; folds applied in order; returns unfolded hole pattern"""
    h=list(holes)
    for f in reversed(folds):
        if f in FOLDS: h=h+FOLDS[f][0](h)
        elif f=="D1": h=h+tf(h,[[0,1],[1,0]])     # fold about y = x
        elif f=="D2": h=h+tf(h,[[0,-1],[-1,0]])   # fold about y = -x
        elif isinstance(f,tuple) and f[0]=="vx":  # fold about vertical line x=a
            a=f[1]; h=h+mirror_x(h,about=(a,0))
        elif isinstance(f,tuple) and f[0]=="hy":
            a=f[1]; h=h+mirror_y(h,about=(0,a))
    return h
import sys,os
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"; os.makedirs(F,exist_ok=True)

# Q10 line graph: monthly sales of products P and Q
m=["Jan","Feb","Mar","Apr","May","Jun"]; Pv=[40,46,52,48,60,66]; Qv=[36,42,40,50,44,48]
fig,ax=plt.subplots(figsize=(4.4,2.6)); x=np.arange(6)
ax.plot(x,Pv,"-o",color=K,lw=1.5,ms=4,label="P"); ax.plot(x,Qv,"--s",color="#666666",lw=1.5,ms=4,label="Q")
for i in range(6):
    up=Pv[i]>=Qv[i]
    ax.text(x[i],Pv[i]+(2.0 if up else -2.0),str(Pv[i]),ha="center",va="bottom" if up else "top",fontsize=7)
    ax.text(x[i],Qv[i]+(-2.0 if up else 2.0),str(Qv[i]),ha="center",va="top" if up else "bottom",fontsize=7,color="#444444")
ax.set_xticks(x); ax.set_xticklabels(m,fontsize=8); ax.set_ylim(20,80); ax.tick_params(axis="y",labelsize=7)
ax.set_ylabel("Units sold (thousands)",fontsize=8); ax.legend(fontsize=7.5,frameon=False,loc="upper left",ncol=2)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(F+"d68p_q10.png",dpi=150,facecolor="white"); plt.close(fig)

# Q11 paper folded twice (top half down onto bottom half, then right half onto left half), two holes punched
holes=[circ((-0.35,-0.35),0.13,True),poly([(-0.85,-0.85),(-0.55,-0.85),(-0.85,-0.6)],True)]
corr=unfold(holes,["T2B","R2L"])
o_tr=holes+shift(holes,1.0,0)+shift(holes,0,1.0)+shift(holes,1.0,1.0)       # copies by translation
o_rot=holes+rot(holes,90)+rot(holes,180)+rot(holes,270)                      # copies by rotation
o_one=unfold(holes,["R2L"])                                                  # only one fold undone
opts=[o_tr,o_rot,corr,o_one]
assert len({key(o) for o in opts})==4 and same(opts[2],corr)
fig,ax=canvas(6.6,3.4)
draw(ax,[],0,1.4); ax.plot([-1,1],[1.4,1.4],color=K,lw=1.0,ls="--"); ax.text(0,2.55,"fold 1",fontsize=8,ha="center")
ax.annotate("",xy=(0.35,0.75),xytext=(0.35,2.05),arrowprops=dict(arrowstyle="-|>",lw=1.1,connectionstyle="arc3,rad=-0.45",color=K))
ax.add_patch(_Rect((1.8,0.4),2.0,1.0,fill=False,ec=K,lw=1.0)); ax.plot([2.8,2.8],[0.4,1.4],color=K,lw=1.0,ls="--")
ax.annotate("",xy=(2.35,0.9),xytext=(3.35,0.9),arrowprops=dict(arrowstyle="-|>",lw=1.1,connectionstyle="arc3,rad=0.45",color=K))
ax.text(2.8,1.55,"fold 2",fontsize=8,ha="center")
ax.add_patch(_Rect((4.5,0.4),1.0,1.0,fill=False,ec=K,lw=1.0)); draw(ax,holes,5.5,1.4,frame=False)
ax.text(5.0,1.55,"punch",fontsize=8,ha="center")
for xa,xb in ((1.15,1.65),(3.95,4.35)): ax.annotate("",xy=(xb,0.9),xytext=(xa,0.9),arrowprops=dict(arrowstyle="-|>",lw=1.0,color=K))
for i,o in enumerate(opts):
    x=2.45*i; draw(ax,o,x,-1.3); cap(ax,x,-2.4,f"({'ABCD'[i]})")
savefig(fig,ax,F+"d68p_q11.png",(-1.2,8.6,-2.85,2.75))
# solution figure: unfolding steps
fig,ax=canvas(5.0,1.9)
ax.add_patch(_Rect((-0.5,-0.5),1.0,1.0,fill=False,ec=K,lw=1.0)); draw(ax,holes,0.5,0.5,frame=False)
u1=unfold(holes,["R2L"]); ax.add_patch(_Rect((1.6,-0.5),2.0,1.0,fill=False,ec=K,lw=1.0)); ax.plot([2.6,2.6],[-0.5,0.5],color=K,lw=0.8,ls="--")
draw(ax,u1,2.6,0.5,frame=False)
draw(ax,corr,5.9,0,frame=True); ax.plot([4.9,6.9],[0,0],color=K,lw=0.8,ls="--"); ax.plot([5.9,5.9],[-1,1],color=K,lw=0.8,ls="--")
for xa,xb in ((0.65,1.45),(3.75,4.75)): ax.annotate("",xy=(xb,0),xytext=(xa,0),arrowprops=dict(arrowstyle="-|>",lw=1.0,color=K))
ax.text(1.05,0.12,"undo 2",fontsize=7.5,ha="center",va="bottom"); ax.text(4.25,0.12,"undo 1",fontsize=7.5,ha="center",va="bottom")
savefig(fig,ax,F+"d68p_s11.png",(-0.7,7.1,-1.15,1.15))
