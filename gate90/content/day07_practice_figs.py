import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from beamsolve import solve
F=sys.argv[1] if len(sys.argv)>1 else "fig/"
S=0.7
def fin(fig,ax,x0,x1,name,y0=-1.3,y1=1.6): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
# P1 cantilever: UDL 4 kN/m + 5 kN at free end, L = 3 m (fixed at left)
fig,ax=new(3.0,1.7); beam(ax,0,3*S*1.3); fixed(ax,0,left=True)
udl(ax,0,3*S*1.3,"4 kN/m"); pload(ax,3*S*1.3,"5 kN",y0=0.62,L=0.6)
dim(ax,0,-0.6,3*S*1.3,-0.6,"3 m"); fin(fig,ax,-0.5,3*S*1.3+0.5,"d7p_q1.png",y0=-1.1,y1=1.7)
# P2 SS beam, 20 kN at 1.5 m and 4.5 m, span 6 m
fig,ax=new(3.4,1.8); beam(ax,0,6*S); pin(ax,0,-0.1,0.4); roller(ax,6*S,-0.1,0.4)
pload(ax,1.5*S,"20 kN"); pload(ax,4.5*S,"20 kN"); label(ax,-0.3,0,"A",fs=9); label(ax,6*S+0.3,0,"B",fs=9)
dim(ax,0,-0.85,1.5*S,-0.85,"1.5 m"); dim(ax,1.5*S,-0.85,4.5*S,-0.85,"3 m"); dim(ax,4.5*S,-0.85,6*S,-0.85,"1.5 m")
fin(fig,ax,-0.6,6*S+0.6,"d7p_q2.png")
x,V,M,_=solve(6,(0,6),[('P',1.5,20),('P',4.5,20)],n=1201)
diagrams(F+"d7p_s2.png",6,x,V,M,vmarks=[(0.75,20,"+20"),(5.25,-20,"−20"),(3,0,"0")],mmarks=[(3,30,"30 (constant)")])
# P4 SS 5 m, 40 kN at 2 m + UDL 10 kN/m
fig,ax=new(3.2,1.8); beam(ax,0,5*S); pin(ax,0,-0.1,0.4); roller(ax,5*S,-0.1,0.4)
udl(ax,0,5*S,"10 kN/m",lx=3.9*S); pload(ax,2*S,"40 kN",y0=0.58,L=0.6); label(ax,-0.3,0,"A",fs=9); label(ax,5*S+0.3,0,"B",fs=9)
dim(ax,0,-0.85,2*S,-0.85,"2 m"); dim(ax,2*S,-0.85,5*S,-0.85,"3 m")
fin(fig,ax,-0.6,5*S+0.6,"d7p_q4.png",y1=1.9)
x,V,M,_=solve(5,(0,5),[('P',2,40),('U',0,5,10)],n=1001)
diagrams(F+"d7p_s4.png",5,x,V,M,vmarks=[(0.15,49,"49"),(1.7,29,"29"),(2.4,-11,"−11"),(4.8,-41,"−41")],mmarks=[(2,78,"78")])
# P6 overhang: span 4 m, overhang 1 m, 20 kN at 2 m, 10 kN at C
fig,ax=new(3.2,1.8); beam(ax,0,5*S); pin(ax,0,-0.1,0.4); roller(ax,4*S,-0.1,0.4)
pload(ax,2*S,"20 kN"); pload(ax,5*S,"10 kN"); label(ax,-0.3,0,"A",fs=9); label(ax,4*S+0.5,-0.25,"B",fs=9); label(ax,5*S+0.3,0,"C",fs=9)
dim(ax,0,-0.85,2*S,-0.85,"2 m"); dim(ax,2*S,-0.85,4*S,-0.85,"2 m"); dim(ax,4*S,-0.85,5*S,-0.85,"1 m")
fin(fig,ax,-0.6,5*S+0.6,"d7p_q6.png")
x,V,M,_=solve(5,(0,4),[('P',2,20),('P',5,10)],n=1001)
diagrams(F+"d7p_s6.png",5,x,V,M,vmarks=[(1,7.5,"+7.5"),(3,-12.5,"−12.5"),(4.5,10,"+10")],mmarks=[(2,15,"+15"),(4,-10,"−10"),(3.45,2,"0 at 3.2 m")])
# P8 couple 40 kN·m anticlockwise at 3 m on 8 m span
fig,ax=new(3.6,1.8); beam(ax,0,8*S); pin(ax,0,-0.1,0.4); roller(ax,8*S,-0.1,0.4)
couple(ax,3*S,"40 kN·m",cw=False); ax.add_patch(Circle((3*S,0),0.05,fc=K)); label(ax,3*S,-0.35,"C",fs=9)
label(ax,-0.3,0,"A",fs=9); label(ax,8*S+0.3,0,"B",fs=9)
dim(ax,0,-0.85,3*S,-0.85,"3 m"); dim(ax,3*S,-0.85,8*S,-0.85,"5 m")
fin(fig,ax,-0.6,8*S+0.6,"d7p_q8.png")
# P12 UDL 20 kN/m on right half of 6 m span
fig,ax=new(3.4,1.8); beam(ax,0,6*S); pin(ax,0,-0.1,0.4); roller(ax,6*S,-0.1,0.4)
udl(ax,3*S,6*S,"20 kN/m"); label(ax,-0.3,0,"A",fs=9); label(ax,6*S+0.3,0,"B",fs=9)
dim(ax,0,-0.85,3*S,-0.85,"3 m"); dim(ax,3*S,-0.85,6*S,-0.85,"3 m")
fin(fig,ax,-0.6,6*S+0.6,"d7p_q12.png")
# P14 cantilever with inclined end load
fig,ax=new(3.0,1.8); beam(ax,0,2*S*1.6); fixed(ax,0,left=True)
pload(ax,2*S*1.6,"10 kN",y0=0.1,L=1.0,ang=150)
xe=2*S*1.6; aa=np.radians(np.linspace(150,180,15)); ax.plot(xe+0.45*np.cos(aa),0.1+0.45*np.sin(aa),color=K,lw=0.8); label(ax,xe-0.72,0.28,"30°",fs=8)
dim(ax,0,-0.6,xe,-0.6,"2 m"); fin(fig,ax,-0.5,xe+0.5,"d7p_q14.png",y0=-1.1,y1=1.0)
print("ok")
