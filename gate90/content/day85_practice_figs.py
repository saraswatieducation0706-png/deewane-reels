"""Day 85 (Full-Length Mock 6) practice figures. Usage: python3 day85_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q6 bars A (uniform d) and B (d over half, 2d over half), same length L, axial loads P
fig,ax=new(3.8,2.3)
L=3.0; r=0.12
def bar(y,stepped,name,load):
    hatch_wall(ax,0,y-0.45,y+0.45,left=True,size=0.13)
    if stepped:
        ax.add_patch(Rectangle((0,y-2*r),L/2,4*r,fc="#dddddd",ec=K,lw=1.2))
        ax.add_patch(Rectangle((L/2,y-r),L/2,2*r,fc="#dddddd",ec=K,lw=1.2))
        label(ax,L/4,y,"2d",fs=8); label(ax,3*L/4,y+r+0.15,"d",fs=8)
    else:
        ax.add_patch(Rectangle((0,y-r),L,2*r,fc="#dddddd",ec=K,lw=1.2)); label(ax,L/2,y+r+0.15,"d",fs=8)
    arrow(ax,L,y,L+0.6,y,lw=1.4); label(ax,L+0.75,y,load,fs=9,ha="left")
    label(ax,-0.35,y,name,fs=9,ha="right")
bar(1.45,False,"A","P"); bar(0.0,True,"B","P")
hdim(ax,0,L/2,-0.85,"L/2",above=False); hdim(ax,L/2,L,-0.85,"L/2",above=False)
for xx in (L/2,L): ext(ax,xx,-0.27 if xx==L/2 else -0.15,xx,-0.92)
ext(ax,0,-0.5,0,-0.92)
fin(fig,ax,-0.7,L+1.1,-1.25,1.95,"d85p_q6.png")

# Q11 horizontal pipe, laminar oil flow
fig,ax=new(3.8,1.4)
Lp=4.0; R=0.22
ax.plot([0,Lp],[R,R],color=K,lw=1.4); ax.plot([0,Lp],[-R,-R],color=K,lw=1.4)
ys=np.linspace(-R*0.7,R*0.7,5)
for y in ys:
    u=0.6*(1-(y/R)**2)
    arrow(ax,0.5,y,0.5+u,y,lw=0.8)
ax.plot(0.5+0.6*(1-(np.linspace(-R,R,40)/R)**2),np.linspace(-R,R,40),color=K,lw=0.8)
label(ax,2.4,0.0,"oil, Q = 1 L/s",fs=8)
vdim(ax,Lp+0.2,-R,R,"D = 40 mm",side="right",fs=8)
hdim(ax,0,Lp,-R-0.35,"L = 50 m",above=False,fs=8)
ext(ax,0,-R,0,-R-0.42); ext(ax,Lp,-R,Lp,-R-0.42)
label(ax,0.3,R+0.18,"1",fs=8.5); label(ax,Lp-0.2,R+0.18,"2",fs=8.5)
fin(fig,ax,-0.2,Lp+1.45,-R-0.75,R+0.4,"d85p_q11.png")

# Q12 pin fin with insulated tip projecting from a wall
fig,ax=new(3.6,1.7)
hatch_wall(ax,0,-0.7,0.7,left=True,size=0.14)
Lf=2.6; rf=0.14
ax.add_patch(Rectangle((0,-rf),Lf,2*rf,fc="#dddddd",ec=K,lw=1.2))
ax.plot([Lf+0.04,Lf+0.04],[-rf-0.05,rf+0.05],color=K,lw=3)
label(ax,Lf+0.1,rf+0.42,"insulated tip",fs=7.5,ha="left")
vdim(ax,Lf+0.5,-rf,rf,"d = 10 mm",side="right",fs=7.5)
ext(ax,Lf+0.08,rf,Lf+0.58,rf); ext(ax,Lf+0.08,-rf,Lf+0.58,-rf)
hdim(ax,0,Lf,-0.62,"L = 100 mm",above=False,fs=8)
ext(ax,Lf,-rf,Lf,-0.68)
label(ax,-0.35,0.55,"base",fs=8,ha="right"); label(ax,-0.35,0.3,"θ = 80 K",fs=7.5,ha="right")
label(ax,1.0,0.52,"air, h = 50 W/m²·K",fs=7.5)
fin(fig,ax,-1.25,Lf+1.75,-1.0,0.8,"d85p_q12.png")
print("ok")
