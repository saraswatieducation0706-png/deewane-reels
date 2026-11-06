"""Day 60 (Week 10 Revision) practice figures. Usage: python3 day60_practice_figs.py <outdir>
The die views are generated from one labelling of a cube, and the answer is checked by trying every labelling."""
import sys,os,itertools; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from matplotlib.patches import Polygon
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
N={"U":(0,0,1),"D":(0,0,-1),"F":(0,-1,0),"B":(0,1,0),"R":(1,0,0),"L":(-1,0,0)}
INV={v:k for k,v in N.items()}; OPP={"U":"D","D":"U","F":"B","B":"F","R":"L","L":"R"}
def rotcube(cube,axis,times=1):
    for _ in range(times%4):
        new={}
        for n,lab in cube.items():
            x,y,z=N[n]; v={"x":(x,-z,y),"y":(z,y,-x),"z":(-y,x,z)}[axis]; new[INV[v]]=lab
        cube=new
    return cube
def all_orients(cube):
    out={}
    for a,b,c in itertools.product(range(4),repeat=3):
        o=rotcube(rotcube(rotcube(cube,"x",a),"y",b),"z",c); out[tuple(sorted(o.items()))]=o
    return list(out.values())
def view(c): return (c["U"],c["F"],c["R"])
def draw_cube(ax,x,y,top,front,right,a=1.0,fs=13):
    d=0.45*a; P=lambda pts:Polygon([(x+u,y+v) for u,v in pts],closed=True,fc="white",ec=K,lw=1.4)
    ax.add_patch(P([(0,0),(a,0),(a,a),(0,a)])); ax.add_patch(P([(a,0),(a+d,d),(a+d,a+d),(a,a)])); ax.add_patch(P([(0,a),(a,a),(a+d,a+d),(d,a+d)]))
    ax.text(x+a/2,y+a/2,front,fontsize=fs,ha="center",va="center",fontweight="bold")
    ax.text(x+a+d/2,y+a/2+d/2,right,fontsize=fs*0.85,ha="center",va="center",fontweight="bold")
    ax.text(x+a/2+d/2,y+a+d/2,top,fontsize=fs*0.85,ha="center",va="center",fontweight="bold")

# Q9 two views of a die
die={"U":"5","D":"2","F":"1","B":"6","R":"4","L":"3"}
views=[("5","1","4"),("5","6","3")]
assert all(v in [view(o) for o in all_orients(die)] for v in views)
ans=set()
for perm in itertools.permutations("23456"):
    c=dict(zip(["D","F","B","R","L"],perm)); c["U"]="1"
    if all(v in [view(o) for o in all_orients(c)] for v in views): ans.add(c["D"])
assert ans=={"6"}, ans                      # the face opposite 1 is fixed by the two views
fig,ax=new(3.6,1.7)
draw_cube(ax,0,0,*views[0]); draw_cube(ax,2.2,0,*views[1])
ax.text(0.7,-0.3,"(i)",fontsize=9,ha="center",va="top"); ax.text(2.9,-0.3,"(ii)",fontsize=9,ha="center",va="top")
ax.set_xlim(-0.2,3.8); ax.set_ylim(-0.65,1.6); save(fig,F+"d60p_q9.png")
