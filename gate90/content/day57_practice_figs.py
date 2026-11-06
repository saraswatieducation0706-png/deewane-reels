"""Day 57 (Spatial Aptitude) practice figures. Usage: python3 day57_practice_figs.py <outdir>
Shapes are lists of primitives that can be reflected/rotated exactly, so every option figure is generated
from (and checked against) the transformation it represents."""
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
# ---- cube / dice ----
# abstract cube: faces keyed by outward normal; orientation = dict normal->label
N={"U":(0,0,1),"D":(0,0,-1),"F":(0,-1,0),"B":(0,1,0),"R":(1,0,0),"L":(-1,0,0)}
INV={v:k for k,v in N.items()}
def rotcube(cube,axis,times=1):
    """rotate the cube 90 deg about axis 'x','y','z' (right-handed), times"""
    for _ in range(times%4):
        new={}
        for n,lab in cube.items():
            x,y,z=N[n]
            if axis=="x": v=(x,-z,y)
            elif axis=="y": v=(z,y,-x)
            else: v=(-y,x,z)
            new[INV[v]]=lab
        cube=new
    return cube
def all_orients(cube):
    seen=[]; out=[]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                o=rotcube(rotcube(rotcube(cube,"x",a),"y",b),"z",c)
                k=tuple(sorted(o.items()))
                if k not in seen: seen.append(k); out.append(o)
    return out
def view(cube): return (cube["U"],cube["F"],cube["R"])
def consistent_cubes(views,labels):
    """all labelings (up to rotation) of a cube with the given labels that can show every view (top, front, right)"""
    sols=[]; base=labels[0]
    for perm in itertools.permutations(labels[1:]):
        cube=dict(zip(["U","D","F","B","R","L"],(base,)+perm))
        vs={view(o) for o in all_orients(cube)}
        if all(v in vs for v in views):
            canon=min(tuple(sorted(o.items())) for o in all_orients(cube))
            if canon not in sols: sols.append(canon)
    return [dict(c) for c in sols]
def opposite(cube,lab):
    opp={"U":"D","D":"U","F":"B","B":"F","R":"L","L":"R"}
    for n,l in cube.items():
        if l==lab: return cube[opp[n]]
def draw_cube(ax,x,y,top,front,right,a=1.0,fs=12):
    """isometric-ish cube: front face square, right face and top face oblique"""
    d=0.45*a
    P=lambda pts:_Poly([(x+u,y+v) for u,v in pts],closed=True,fc="white",ec=K,lw=1.4)
    ax.add_patch(P([(0,0),(a,0),(a,a),(0,a)]))
    ax.add_patch(P([(a,0),(a+d,d),(a+d,a+d),(a,a)]))
    ax.add_patch(P([(0,a),(a,a),(a+d,a+d),(d,a+d)]))
    ax.text(x+a/2,y+a/2,str(front),fontsize=fs,ha="center",va="center",fontweight="bold")
    ax.text(x+a+d/2,y+a/2+d/2,str(right),fontsize=fs*0.85,ha="center",va="center",fontweight="bold")
    ax.text(x+a/2+d/2,y+a+d/2,str(top),fontsize=fs*0.85,ha="center",va="center",fontweight="bold")
def fold_net(cells):
    """cells: dict (col,row)->label (row increases downward). Rolls a cube over the net; returns dict normal->label."""
    start=next(iter(cells)); cube={n:n for n in N}  # physical face ids
    stamp={}; seen=set()
    def roll(c,d):
        # rolling east: new D = old R ; new R = old U ; new U = old L ; new L = old D
        m={"E":{"D":"R","R":"U","U":"L","L":"D"},"W":{"D":"L","L":"U","U":"R","R":"D"},
           "S":{"D":"F","F":"U","U":"B","B":"D"},"N":{"D":"B","B":"U","U":"F","F":"D"}}[d]
        out=dict(c)
        for newpos,oldpos in m.items(): out[newpos]=c[oldpos]
        return out
    def dfs(cell,c):
        seen.add(cell); stamp[c["D"]]=cells[cell]
        for d,(dx,dy) in {"E":(1,0),"W":(-1,0),"S":(0,1),"N":(0,-1)}.items():
            nb=(cell[0]+dx,cell[1]+dy)
            if nb in cells and nb not in seen: dfs(nb,roll(c,d))
    dfs(start,cube)
    # rolling ON TOP of the net gives the mirror cube; a real net folds away from the viewer -> swap U and D
    stamp['U'],stamp['D']=stamp['D'],stamp['U']
    return stamp   # physical face id -> label ; physical ids are N keys, so opposite pairs are U/D, F/B, R/L
def net_opposites(cells):
    st=fold_net(cells); opp={"U":"D","F":"B","R":"L"}
    return {frozenset((st[a],st[b])) for a,b in opp.items()}
def net_cube(cells):
    st=fold_net(cells); return dict(st)   # normal -> label (a valid labeling of a cube)
def draw_net(ax,cells,x=0,y=0,a=1.0,fs=13):
    for (c,r),lab in cells.items():
        ax.add_patch(_Rect((x+c*a,y-r*a),a,a,fill=False,ec=K,lw=1.4))
        ax.text(x+c*a+a/2,y-r*a+a/2,str(lab),fontsize=fs,ha="center",va="center",fontweight="bold")
# ---- counting triangles in a line figure ----
def count_triangles(segs,tol=1e-9):
    segs=[(np.array(a,float),np.array(b,float)) for a,b in segs]
    pts=[]
    def add(p):
        for q in pts:
            if np.linalg.norm(q-p)<1e-7: return
        pts.append(p)
    for a,b in segs: add(a); add(b)
    for (a,b),(c,d) in itertools.combinations(segs,2):
        r=b-a; s=d-c; den=r[0]*s[1]-r[1]*s[0]
        if abs(den)<tol: continue
        t=((c-a)[0]*s[1]-(c-a)[1]*s[0])/den; u=((c-a)[0]*r[1]-(c-a)[1]*r[0])/den
        if -1e-9<=t<=1+1e-9 and -1e-9<=u<=1+1e-9: add(a+t*r)
    def on(p,a,b):
        r=b-a; return abs((p-a)[0]*r[1]-(p-a)[1]*r[0])<1e-7 and -1e-9<=np.dot(p-a,r)<=np.dot(r,r)+1e-9
    def conn(p,q): return any(on(p,a,b) and on(q,a,b) for a,b in segs)
    n=0
    for p,q,r in itertools.combinations(pts,3):
        area=(q-p)[0]*(r-p)[1]-(q-p)[1]*(r-p)[0]
        if abs(area)<1e-9: continue
        if conn(p,q) and conn(q,r) and conn(p,r): n+=1
    return n
def count_squares(segs):
    """axis-aligned squares whose 4 sides lie on given segments"""
    segs=[(np.array(a,float),np.array(b,float)) for a,b in segs]
    xs=sorted({round(v,6) for a,b in segs for v in (a[0],b[0])}); ys=sorted({round(v,6) for a,b in segs for v in (a[1],b[1])})
    def covered(p,q):
        p,q=np.array(p,float),np.array(q,float)
        for a,b in segs:
            r=b-a
            if abs((p-a)[0]*r[1]-(p-a)[1]*r[0])<1e-7 and abs((q-a)[0]*r[1]-(q-a)[1]*r[0])<1e-7:
                t1=np.dot(p-a,r)/np.dot(r,r); t2=np.dot(q-a,r)/np.dot(r,r)
                if -1e-9<=min(t1,t2) and max(t1,t2)<=1+1e-9: return True
        return False
    n=0
    for x in xs:
        for y in ys:
            for x2 in xs:
                L=x2-x
                if L<=0: continue
                y2=y+L
                if not any(abs(y2-v)<1e-6 for v in ys): continue
                if covered((x,y),(x2,y)) and covered((x,y2),(x2,y2)) and covered((x,y),(x,y2)) and covered((x2,y),(x2,y2)): n+=1
    return n

# =================== Day 57 practice figures ===================
import sys,os
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"; os.makedirs(F,exist_ok=True)
CHECK={}
def distinct8(s): return len({key(v) for v in D4(s).values()})==8
def all_distinct(o): return len({key(x) for x in o})==len(o)
def arr(ax,x0,y0,x1,y1,rad=0.0,lw=1.1):
    ax.annotate("",xy=(x1,y1),xytext=(x0,y0),arrowprops=dict(arrowstyle="-|>",lw=lw,color=K,connectionstyle=f"arc3,rad={rad}"))

# Q1 mirror image of GATE90 (mirror on the right)
base=letters("GATE90",0,0,h=0.5)
def per_letter(sh,fn):
    out=[]
    for e in sh:
        v=e["p"]; c=(v.min(0)+v.max(0))/2; out+=fn([e],tuple(c))
    return out
opts=[mirror_y(base),per_letter(base,lambda s,c: mirror_x(s,about=c)),mirror_x(base),rot(base,180)]
assert all_distinct(opts)
fig,ax=canvas(5.4,2.4)
draw(ax,base,0,1.9,frame=False); ax.plot([1.85,1.85],[1.5,2.3],color=K,lw=1.2,ls="--"); ax.text(1.95,1.9,"mirror",fontsize=8,va="center")
for i,(x,y) in enumerate([(-2.1,0.35),(2.1,0.35),(-2.1,-1.05),(2.1,-1.05)]):
    draw(ax,opts[i],x,y,frame=False); ax.text(x-1.85,y,"(%s)"%"ABCD"[i],fontsize=10,fontweight="bold",ha="right",va="center")
savefig(fig,ax,F+"d57p_q1.png",(-4.7,4.0,-1.6,2.4))
CHECK[1]=[i for i,o in enumerate(opts) if same(o,mirror_x(base))]

# Q2 water image of a figure
FE=[poly([(-0.75,0.75),(-0.25,0.75),(-0.75,0.25)],True),circ((0.45,0.5),0.2),line([(-0.7,-0.1),(0.0,-0.1),(0.0,-0.75)]),
    poly([(0.3,-0.75),(0.75,-0.75),(0.75,-0.3)])]+arrowp((-0.15,0.2),(0.35,-0.25))
assert distinct8(FE)
opts=[mirror_y(FE),mirror_x(FE),rot(FE,180),rot(FE,90)]; assert all_distinct(opts)
def p2(ax,x,y):
    draw(ax,FE,x,y); ax.plot([x-1.0,x+1.0],[y-1.15,y-1.15],color=K,lw=1.2,ls="--"); ax.text(x+1.1,y-1.15,"water surface",fontsize=7.5,ha="left",va="center")
options_fig(F+"d57p_q2.png",p2,opts,wide=True)
CHECK[2]=[i for i,o in enumerate(opts) if same(o,mirror_y(FE))]

# Q4 rotation 90 deg anticlockwise
FF=[line([(-0.75,0.75),(-0.1,0.75),(-0.1,0.3)]),poly([(0.2,0.75),(0.75,0.75),(0.75,0.45),(0.45,0.45),(0.45,0.2),(0.2,0.2)],True),
    circ((-0.45,-0.45),0.2,True),line([(0.2,-0.2),(0.75,-0.75)])]+arrowp((-0.55,0.1),(-0.05,0.1))
assert distinct8(FF)
opts=[rot(FF,-90),rot(FF,90),rot(mirror_x(FF),90),rot(FF,180)]; assert all_distinct(opts)
options_fig(F+"d57p_q4.png",FF,opts,wide=True)
CHECK[4]=[i for i,o in enumerate(opts) if same(o,rot(FF,90))]

# Q5 diagonal fold (upper-right triangle folded onto lower-left triangle) and punch
holes=[circ((-0.7,-0.2),0.14),poly([(0.05,-0.85),(0.45,-0.85),(0.05,-0.45)],True)]
corr=unfold(holes,["D2"])
opts=[holes+mirror_y(holes),holes+rot(holes,180),holes+tf(holes,[[0,1],[1,0]]),corr]; assert all_distinct(opts)
fig,ax=canvas(5.0,3.4)
ax.add_patch(_Rect((-1,0.3),2,2,fill=False,ec=K,lw=1.0)); ax.plot([-1,1],[2.3,0.3],color=K,lw=1.0,ls="--")
arr(ax,0.6,1.9,-0.3,0.9,rad=0.35); ax.text(0,2.42,"fold",fontsize=8,ha="center")
arr(ax,1.15,1.3,1.6,1.3)
ax.add_patch(_Poly([(1.8,2.3),(1.8,0.3),(3.8,0.3)],closed=True,fill=False,ec=K,lw=1.0)); draw(ax,holes,2.8,1.3,frame=False)
ax.text(2.8,2.42,"punch",fontsize=8,ha="center")
ax.text(4.1,1.3,"Unfolded?",fontsize=9,va="center")
for i,o in enumerate(opts):
    x=-0.1+2.35*i; draw(ax,o,x,-1.3,s=0.95); cap(ax,x,-2.32,"(%s)"%"ABCD"[i])
savefig(fig,ax,F+"d57p_q5.png",(-1.2,8.2,-2.75,2.6))
CHECK[5]=[i for i,o in enumerate(opts) if same(o,corr)]
fig,ax=canvas(1.9,1.9); draw(ax,corr,0,0); ax.plot([-1,1],[1,-1],color=K,lw=0.9,ls="--"); savefig(fig,ax,F+"d57p_s5.png",(-1.05,1.05,-1.05,1.05))

# Q6 dice: three views
die={"U":"1","D":"3","F":"2","B":"6","R":"4","L":"5"}
O=all_orients(die)
def find(top,front): return next(view(o) for o in O if view(o)[0]==top and view(o)[1]==front)
import itertools as _it
vs=None
for combo in _it.combinations(sorted({view(o) for o in O}),3):
    if len(set().union(*map(set,combo)))<6 or len({c[0] for c in combo})<3: continue
    if any("4" in c and "5" in c for c in combo): continue
    sl=consistent_cubes(list(combo),list("123456"))
    if len({opposite(c,"4") for c in sl})==1 and len(sl)==1: vs=list(combo); break
sols=consistent_cubes(vs,list("123456")); ans6={opposite(c,"4") for c in sols}
print("P6 views",vs,"solutions",len(sols),"opposite of 4",ans6)
fig,ax=canvas(4.6,1.6)
for i,v in enumerate(vs): draw_cube(ax,2.1*i,0,*v,a=1.0,fs=13); ax.text(2.1*i+0.7,-0.25,"(%s)"%["i","ii","iii"][i],fontsize=9,ha="center",va="top")
savefig(fig,ax,F+"d57p_q6.png",(-0.2,5.9,-0.6,1.55))
CHECK[6]=ans6

# Q7 series: polygon gains a side, dots inside decrease
def reg(n,r=0.62):
    th=np.radians(90+np.arange(n)*360/n); return poly(np.c_[r*np.cos(th),r*np.sin(th)])
dotpos=[(-0.2,0.15),(0.2,0.15),(-0.2,-0.2),(0.2,-0.2)]
def fr7(n,d): return [reg(n)]+[circ(dotpos[i],0.08,True) for i in range(d)]
seq=[fr7(3+k,4-k) for k in range(4)]; ans=fr7(7,0)
opts=[fr7(6,0),fr7(7,1),ans,fr7(8,0)]; assert all_distinct(opts)
fig,ax=canvas(6.6,3.2)
for k in range(4): draw(ax,seq[k],2.3*k,1.3)
ax.add_patch(_Rect((2.3*4-1,0.3),2,2,fill=False,ec=K,lw=1.0)); ax.text(2.3*4,1.3,"?",fontsize=22,ha="center",va="center")
for i,o in enumerate(opts):
    x=1.15+2.3*i; draw(ax,o,x,-1.3); cap(ax,x,-2.4,"(%s)"%"ABCD"[i])
savefig(fig,ax,F+"d57p_q7.png",(-1.2,10.4,-2.85,2.45))
CHECK[7]=[i for i,o in enumerate(opts) if same(o,ans)]

# Q8 net (letters)
net8={(0,0):"A",(0,1):"B",(1,1):"C",(2,1):"D",(3,1):"E",(3,2):"F"}
opp8=net_opposites(net8); print("P8 pairs",sorted(tuple(sorted(p)) for p in opp8))
fig,ax=canvas(2.9,2.0); draw_net(ax,net8,0,0,a=0.7,fs=12); savefig(fig,ax,F+"d57p_q8.png",(-0.1,2.9,-1.5,0.8))
CHECK[8]=opp8

# Q10 triangles: triangle, three lines from the apex to the base, one line parallel to the base
Ap=(3,5); base_pts=[(0,0),(1.5,0),(3.2,0),(4.4,0),(6,0)]
segs=[((0,0),(6,0))]+[(Ap,b) for b in base_pts]+[((1.5,2.5),(4.5,2.5))]
n10=count_triangles(segs); print("P10 triangles",n10); CHECK[10]=n10
fig,ax=canvas(2.6,2.2)
for a,b in segs: ax.plot([a[0],b[0]],[a[1],b[1]],color=K,lw=1.4)
savefig(fig,ax,F+"d57p_q10.png",(-0.2,6.2,-0.2,5.2))

# Q11 squares in a 3 x 5 grid of unit squares
segs11=[((0,y),(5,y)) for y in range(4)]+[((x,0),(x,3)) for x in range(6)]
n11=count_squares(segs11); print("P11 squares",n11); CHECK[11]=n11
fig,ax=canvas(2.6,1.6)
for a,b in segs11: ax.plot([a[0],b[0]],[a[1],b[1]],color=K,lw=1.4)
savefig(fig,ax,F+"d57p_q11.png",(-0.1,5.1,-0.1,3.1))

# Q12 rectangle folded in half, two cuts
fig,ax=canvas(5.6,2.3)
ax.add_patch(_Rect((0,0),2.0,1.2,fill=False,ec=K,lw=1.2)); ax.plot([1.0,1.0],[0,1.2],color=K,lw=0.9,ls="--")
ax.text(1.0,1.3,"20 cm × 12 cm",fontsize=8,ha="center",va="bottom"); arr(ax,1.7,0.8,0.5,0.8,rad=0.4)
arr(ax,2.25,0.6,2.85,0.6); ax.text(2.55,0.7,"fold",fontsize=7.5,ha="center",va="bottom")
ox=3.2   # folded piece drawn at 0.15 unit per cm
s=0.15; ax.add_patch(_Rect((ox,-0.3),10*s,12*s,fill=False,ec=K,lw=1.2))
fx=ox+10*s   # fold edge on the right
th=np.linspace(np.pi/2,1.5*np.pi,30); r=3*s; cy=-0.3+6*s
ax.add_patch(_Poly(np.c_[fx+r*np.cos(th),cy+r*np.sin(th)],closed=True,fc="#777777",ec=K,lw=1.1))
ax.add_patch(_Rect((ox,-0.3+10*s),2*s,2*s,fc="#777777",ec=K,lw=1.1))
ax.text(fx+0.08,cy+0.62,"fold",fontsize=7.5,ha="left",va="center"); ax.plot([fx,fx],[-0.3,-0.3+12*s],color=K,lw=2.0)
ax.text(fx-r-0.05,cy,"r = 3 cm",fontsize=7,ha="right",va="center")
ax.text(ox+2*s+0.05,-0.3+11*s,"2 cm × 2 cm",fontsize=7,ha="left",va="center")
ax.text(ox+5*s,-0.38,"10 cm",fontsize=7.5,ha="center",va="top"); ax.text(fx+0.08,-0.3+3*s,"12 cm",fontsize=7.5,ha="left",va="center")
savefig(fig,ax,F+"d57p_q12.png",(-0.1,5.2,-0.75,1.75))

# Q13 solution: cube surface unfolded
fig,ax=canvas(2.2,2.6)
ax.add_patch(_Rect((0,0),1,1,fill=False,ec=K,lw=1.2)); ax.add_patch(_Rect((0,1),1,1,fill=False,ec=K,lw=1.2))
ax.plot([0,1],[0,2],color=K,lw=1.5,ls="--"); ax.plot(0,0,"o",color=K,ms=4); ax.plot(1,2,"o",color=K,ms=4)
ax.text(-0.06,-0.04,"P",fontsize=9,ha="right",va="top",fontweight="bold"); ax.text(1.06,2.04,"Q",fontsize=9,ha="left",va="bottom",fontweight="bold")
ax.text(0.5,-0.06,"10",fontsize=8,ha="center",va="top"); ax.text(1.06,1.0,"20",fontsize=8,ha="left",va="center")
ax.text(1.06,0.5,"front",fontsize=7,ha="left",va="center",color="#444"); ax.text(1.06,1.5,"top",fontsize=7,ha="left",va="center",color="#444")
savefig(fig,ax,F+"d57p_s13.png",(-0.35,1.6,-0.3,2.25))
print("CHECK",CHECK)
