"""Day 84 (Formula Sprint: Manufacturing & IE) practice figures. Usage: python3 day84_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def bez(P,u):
    return [(1-u)**3*P[0][k]+3*u*(1-u)**2*P[1][k]+3*u*u*(1-u)*P[2][k]+u**3*P[3][k] for k in (0,1)]
def grid_axes(ax,xmax,ymax):
    for x in range(0,xmax+1): ax.plot([x,x],[0,ymax],color="#dddddd",lw=0.5,zorder=0)
    for y in range(0,ymax+1): ax.plot([0,xmax],[y,y],color="#dddddd",lw=0.5,zorder=0)
    arrow(ax,0,0,xmax+0.6,0,lw=0.9); arrow(ax,0,0,0,ymax+0.6,lw=0.9)
    label(ax,xmax+0.75,0,"x",fs=9,ha="left"); label(ax,0,ymax+0.8,"y",fs=9)
    for x in range(2,xmax+1,2): label(ax,x,-0.35,str(x),fs=7)
    for y in range(1,ymax+1): label(ax,-0.3,y,str(y),fs=7,ha="right")

# Q4 cube casting with a cylindrical side riser (elevation), units 10 mm
fig,ax=new(3.4,2.2)
ax.add_patch(Rectangle((0,0),10,10,fc="#cccccc",ec=K,lw=1.3))
ax.add_patch(Rectangle((10,3),2.0,1.4,fc="#cccccc",ec=K,lw=1.0))      # neck
ax.add_patch(Rectangle((12,0),12,12,fc="#e6e6e6",ec=K,lw=1.3))
label(ax,5,5.6,"casting",fs=8); label(ax,5,4.2,"100 mm cube",fs=7.5)
label(ax,18,6.7,"riser",fs=8); label(ax,18,5.3,"(cylinder)",fs=7.5)
hdim(ax,0,10,-1.6,"100 mm",above=False,fs=7.5); ext(ax,0,0,0,-2.0); ext(ax,10,0,10,-2.0)
hdim(ax,12,24,-1.6,"D = 120 mm",above=False,fs=7.5); ext(ax,12,0,12,-2.0); ext(ax,24,0,24,-2.0)
vdim(ax,25.6,0,12,"H = 120 mm",side="right",fs=7.5); ext(ax,24,12,26.0,12); ext(ax,24,0,26.0,0)
fin(fig,ax,-1,33,-4.2,13.5,"d84p_q4.png")

P=[(0,0),(2,4),(6,5),(8,1)]
# Q13 control polygon only
fig,ax=new(3.2,2.4)
grid_axes(ax,8,5)
ax.plot([p[0] for p in P],[p[1] for p in P],color=K,lw=1.0,ls="--",marker="o",ms=4,mfc="white")
for (x,y),t,dx,dy in zip(P,["P₀(0, 0)","P₁(2, 4)","P₂(6, 5)","P₃(8, 1)"],[0.45,-0.2,0.2,0.2],[0.3,0.4,0.35,0.35]):
    label(ax,x+dx,y+dy,t,fs=7.5,ha="left" if dx>0 else "right")
fin(fig,ax,-0.9,9.6,-0.8,6.2,"d84p_q13.png")

# Q13 solution: the curve with its tangent at u = 0.5
fig,ax=new(3.2,2.4)
grid_axes(ax,8,5)
ax.plot([p[0] for p in P],[p[1] for p in P],color="#888888",lw=0.8,ls="--",marker="o",ms=3.5,mfc="white")
us=[i/100 for i in range(101)]; cv=[bez(P,u) for u in us]
ax.plot([c[0] for c in cv],[c[1] for c in cv],color=K,lw=1.8)
m=(4,3.5); s=1.5/9
ax.plot([m[0]-2.6,m[0]+2.6],[m[1]-2.6*s,m[1]+2.6*s],color=K,lw=0.9,ls="-.")
ax.plot([m[0]],[m[1]],"o",color=K,ms=4)
label(ax,4.0,2.95,"u = 0.5",fs=7.5)
label(ax,4.0,2.35,"slope 1/6",fs=7.5)
fin(fig,ax,-0.9,9.6,-0.8,6.2,"d84p_s13.png")
print("ok")
