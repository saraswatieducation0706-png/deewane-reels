"""Day 88 (Mixed PYQ Traps) practice figures. Usage: python3 day88_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q9 eccentric circular cam (link 2) pinned to the frame (link 1) at O; roller (link 4) pinned to a
# translating follower (link 3) that slides in a fixed guide (part of the frame)
fig,ax=new(2.9,3.4)
R=0.9; e=0.3; cx,cy=0.0,0.0          # cam pivot O at origin, cam disc centre offset by e
ax.add_patch(Circle((cx,cy+e),R,fc="#dddddd",ec=K,lw=1.4))
joint(ax,cx,cy,r=0.06); label(ax,cx+0.2,cy-0.12,"O",fs=9)
ax.add_patch(Circle((cx,cy+e),0.03,fc=K))
rr=0.22; ry=cy+e+R+rr                 # roller centre on top of the cam
ax.add_patch(Circle((0,ry),rr,fc="white",ec=K,lw=1.4,zorder=5)); joint(ax,0,ry,r=0.045)
w=0.09; top=ry+1.35
ax.add_patch(Rectangle((-w,ry),2*w,top-ry,fc="#bbbbbb",ec=K,lw=1.2,zorder=4))
gy0,gy1=ry+0.5,ry+1.05
hatch_wall(ax,-w-0.01,gy0,gy1,left=True,size=0.12); hatch_wall(ax,w+0.01,gy0,gy1,left=False,size=0.12)
omega(ax,0,e,R+0.18,"ω",ccw=True,a0=200,a1=250,fs=9)
label(ax,0.62,-0.7,"2 (cam)",fs=8,ha="left")
label(ax,0.2,top-0.12,"3 (follower)",fs=8,ha="left")
label(ax,0.3,ry,"4 (roller)",fs=8,ha="left")
label(ax,-0.3,(gy0+gy1)/2,"1 (guide)",fs=8,ha="right")
label(ax,0.0,-0.35,"pin to frame 1",fs=7)
fin(fig,ax,-1.5,1.6,-0.85,top+0.15,"d88p_q9.png")
print("ok")
