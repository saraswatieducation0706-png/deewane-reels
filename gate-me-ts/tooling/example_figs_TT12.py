import sys; sys.path.insert(0,'~/deewane-reels/gate90/tooling')
from figlib import *
import numpy as np
D='fig/'
# Q12 cantilever fixed at left, UDL on left half
f,ax=new(3.8,2.0); fixed(ax,0); beam(ax,0,4); udl(ax,0,2,"w per unit length"); hdim(ax,0,2,-0.45,"L/2",above=False); hdim(ax,2,4,-0.45,"L/2",above=False); label(ax,4.25,0,"B",fs=9); save(f,D+"q12.png")
# Q14 cantilever tip load + full UDL
f,ax=new(3.8,2.2); fixed(ax,0); beam(ax,0,4); udl(ax,0,4,"2 kN/m",lx=1.6); pload(ax,4,"5 kN",y0=0.1,L=1.1); hdim(ax,0,4,-0.45,"2 m",above=False); save(f,D+"q14.png")
# Q17 overhang
f,ax=new(4.2,2.2); beam(ax,0,4); pin(ax,0,-0.1); roller(ax,3,-0.1); pload(ax,4,"P"); label(ax,-0.2,0.3,"A",fs=9); label(ax,3,0.35,"B",fs=9); label(ax,4.2,0.3,"C",fs=9)
hdim(ax,0,3,-0.75,"L",above=False); hdim(ax,3,4,-0.75,"a",above=False); save(f,D+"q17.png")
# Q18 SS beam, 30 kN at 2 m, span 6 m
f,ax=new(4.2,2.2); beam(ax,0,6); pin(ax,0,-0.1); roller(ax,6,-0.1); pload(ax,2,"30 kN"); hdim(ax,0,2,-0.75,"2 m",above=False); hdim(ax,2,6,-0.75,"4 m",above=False); save(f,D+"q18.png")
# Q21 L-frame: fixed at base A, vertical AB = L, horizontal BC = L, load P down at C
f,ax=new(3.0,3.0); member(ax,(0,0),(0,3),lw=3); member(ax,(0,3),(3,3),lw=3); hatch_ground(ax,-0.5,0.5,0,size=0.15)
pload(ax,3,"P",y0=3.05,L=0.8); label(ax,-0.3,0.25,"A",fs=9); label(ax,-0.3,3.1,"B",fs=9); label(ax,3.25,2.85,"C",fs=9)
vdim(ax,-0.8,0,3,"L"); hdim(ax,0,3,2.55,"L",above=False); save(f,D+"q21.png")
# Q24 two-bar truss, bars at 30 deg to vertical, load P at joint
f,ax=new(3.4,2.8); L=2.0; t=np.radians(30); top=0.0; jx,jy=0,-L*np.cos(t)
A=(-L*np.sin(t),0); B=(L*np.sin(t),0); member(ax,A,(jx,jy)); member(ax,B,(jx,jy))
hatch_ground(ax,-1.6,1.6,0,down=False,size=0.15); joint(ax,*A); joint(ax,*B); joint(ax,jx,jy)
arrow(ax,jx,jy-0.1,jx,jy-0.9); label(ax,jx+0.25,jy-0.75,"P",fs=10)
dline(ax,(0,0),(0,jy)); angarc(ax,0,jy,0.45,90,120,"30°",fs=8,lr=0.7); angarc(ax,0,jy,0.45,60,90,"30°",fs=8,lr=0.7)
label(ax,A[0]/2-0.35,jy/2,"L",fs=9); label(ax,B[0]/2+0.35,jy/2,"L",fs=9); save(f,D+"q24.png")
# Q30 SS 5 m, UDL 12 kN/m over 0-3 m
f,ax=new(4.2,2.2); beam(ax,0,5); pin(ax,0,-0.1); roller(ax,5,-0.1); udl(ax,0,3,"12 kN/m"); hdim(ax,0,3,-0.75,"3 m",above=False); hdim(ax,3,5,-0.75,"2 m",above=False); save(f,D+"q30.png")
# Q32 SS beam with couple M0 at left support
f,ax=new(4.0,2.0); beam(ax,0,4); pin(ax,0,-0.1); roller(ax,4,-0.1); couple(ax,0,"M₀",cw=True); label(ax,-0.25,-0.05,"A",fs=9); label(ax,4.25,-0.05,"B",fs=9); hdim(ax,0,4,-0.75,"L",above=False); save(f,D+"q32.png")
print("ok")
