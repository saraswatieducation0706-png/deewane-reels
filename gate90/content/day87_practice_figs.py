"""Day 87 (Full-Length Mock 7) practice figures. Usage: python3 day87_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q6 cantilever AB with UDL over the whole length; mid-span M marked
fig,ax=new(3.8,1.9)
L=4.0
fixed(ax,0,left=True,h=0.8)
beam(ax,0,L,t=0.16)
udl(ax,0,L,"w (uniform)",y=0.08,h=0.42)
label(ax,-0.32,-0.62,"A",fs=9); label(ax,L+0.2,0,"B",fs=9)
ax.plot([L/2],[0],marker="o",ms=3.5,color=K,zorder=6); label(ax,L/2,-0.28,"M",fs=9)
yd=-0.75
hdim(ax,0,L/2,yd,"L/2",above=False); hdim(ax,L/2,L,yd,"L/2",above=False)
for xx in (0,L/2,L): ext(ax,xx,-0.1 if xx!=L/2 else -0.42,xx,yd-0.06)
fin(fig,ax,-0.45,L+0.45,-1.2,1.0,"d87p_q6.png")

print("ok")
