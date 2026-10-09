import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sections8 import *
F=sys.argv[1] if len(sys.argv)>1 else "fig/"
# P4 T-section 120x20 flange, 20x100 web
tsec_fig(F+"d8p_q4.png",120,20,20,100,s=0.018)
# P4 solution: bending stress distribution
ybar=37.27; D=120; fig,ax=new(3.4,2.4); s=0.018
section(ax,[(-1.08,(D-20)*s,2.16,20*s),(-0.18,0,0.36,(D-20)*s)])
yna=(D-ybar)*s; ax.plot([-1.15,3.9],[yna,yna],color=K,lw=0.8,ls="-."); label(ax,3.92,yna,"N.A.",fs=7,ha="left")
x0=2.0; k=1.4/87.48
ax.plot([x0,x0],[0,D*s],color=K,lw=0.9)
ax.add_patch(Polygon([[x0,yna],[x0-39.41*k,D*s],[x0,D*s]],fc="#cccccc",ec=K,lw=1))
ax.add_patch(Polygon([[x0,yna],[x0+87.48*k,0],[x0,0]],fc="#cccccc",ec=K,lw=1))
label(ax,x0-39.41*k-0.05,D*s+0.15,"39.4 MPa (C)",fs=7); label(ax,x0+87.48*k,-0.15,"87.5 MPa (T)",fs=7)
label(ax,-1.45,yna/2,"82.7",fs=7,ha="right"); vdim(ax,-1.2,0,yna,"",side="left")
label(ax,-1.45,(yna+D*s)/2,"37.3",fs=7,ha="right"); vdim(ax,-1.2,yna,D*s,"",side="left")
ax.set_xlim(-2.1,4.5); ax.set_ylim(-0.45,D*s+0.45); save(fig,F+"d8p_s4.png")
# P6 I-section 150x20 flanges, web 10, H 300
isec_fig(F+"d8p_q6.png",150,20,10,300,s=0.01)
# P6 solution: shear stress distribution
fig,ax=new(3.4,2.6); s=0.01; H=300
section(ax,[(-0.75,0,1.5,0.2),(-0.05,0.2,0.1,2.6),(-0.75,2.8,1.5,0.2)])
x0=1.4; k=1.3/38.09; import numpy as np
ys=np.linspace(-130,130,200); Qf=150*20*140; I=132446666.7
tau=100e3*(Qf+10*(130**2-ys**2)/2)/(I*10)
xs=x0+tau*k; yy=(ys+150)*s
ax.add_patch(Polygon(list(zip(xs,yy))+[(x0,yy[-1]),(x0,yy[0])],fc="#cccccc",ec=K,lw=1))
# flange parts (small)
for yb,yt in ((0,0.2),(2.8,3.0)):
    yv=np.linspace(yb,yt,20); d=np.where(yb==0,yv,3.0-yv)  # distance from outer face
    t=100e3*150*(d/s)*(150-(d/s)/2)/(I*150); ax.add_patch(Polygon(list(zip(x0+t*k,yv))+[(x0,yt),(x0,yb)],fc="#cccccc",ec=K,lw=1))
ax.plot([x0,x0],[0,3.0],color=K,lw=0.9)
label(ax,x0+38.09*k+0.05,1.5,"38.1 (max, N.A.)",fs=7,ha="left"); label(ax,x0+31.71*k+0.05,2.62,"31.7",fs=7,ha="left")
label(ax,x0+0.35,3.0+0.12,"2.1 in flange",fs=7,ha="left"); label(ax,x0+0.65,-0.25,"τ (MPa)",fs=7)
ax.set_xlim(-0.9,4.4); ax.set_ylim(-0.45,3.35); save(fig,F+"d8p_s6.png")
# P12 diamond section
fig,ax=new(2.2,2.2); d=1.6
ax.add_patch(Polygon([[0,d/2],[d/2,0],[0,-d/2],[-d/2,0]],fc="#dddddd",ec=K,lw=1.3))
ax.plot([-0.9,1.05],[0,0],color=K,lw=0.8,ls="-."); label(ax,1.1,0,"N.A.",fs=8,ha="left")
arrow(ax,0,-0.95,0,-0.7,lw=1.2); label(ax,0.12,-1.0,"V",fs=9,ha="left")
ext(ax,-0.05,d/2,-1.15,d/2); ext(ax,-0.05,-d/2,-1.15,-d/2); vdim(ax,-1.05,-d/2,d/2,"d",side="left")
ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.15,1.0); save(fig,F+"d8p_q12.png")
# P14 flitched beam section
fig,ax=new(2.8,2.4); s=0.006
section(ax,[(-75*s,0,150*s,300*s)],fc="#e8d9b5"); section(ax,[(-85*s,0,10*s,300*s),(75*s,0,10*s,300*s)],fc="#888888")
label(ax,0,150*s,"timber",fs=8); 
ext(ax,-75*s,300*s+0.05,-75*s,300*s+0.3); ext(ax,75*s,300*s+0.05,75*s,300*s+0.3); hdim(ax,-75*s,75*s,300*s+0.25,"150")
ext(ax,-85*s-0.05,0,-85*s-0.4,0); ext(ax,-85*s-0.05,300*s,-85*s-0.4,300*s); vdim(ax,-85*s-0.3,0,300*s,"300",side="left")
arrow(ax,85*s+0.35,0.35,85*s,0.35,lw=0.9); label(ax,85*s+0.4,0.35,"steel plate\n10 mm",fs=7,ha="left")
ax.set_xlim(-1.4,1.6); ax.set_ylim(-0.2,2.3); save(fig,F+"d8p_q14.png")
print("ok")
