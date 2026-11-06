import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def mid_arrow(ax,xs,ys):
    i=len(xs)//2; arrow(ax,xs[i-1],ys[i-1],xs[i+1],ys[i+1],lw=1.1)
def adiabat(ax,Va,pa,Vb,pb,rev=False):
    """schematic isentrope through (Va,pa) and (Vb,pb), Va < Vb, drawn as a smooth falling curve"""
    V=np.linspace(Va,Vb,60); p=pb+(pa-pb)*((Vb-V)/(Vb-Va))**2.2
    ax.plot(V,p,color=K,lw=1.5); mid_arrow(ax,V[::-1] if rev else V,p[::-1] if rev else p)
def pt(ax,x,y,t,dx,dy): ax.add_patch(Circle((x,y),0.035,fc=K,zorder=6)); label(ax,x+dx,y+dy,t,fs=9)

# Q9 dual cycle p-V
fig,ax=new(3.4,2.6); ts_axes(ax,3.2,2.5,xl="V",yl="p")
V1,V2,V4=2.8,0.4,0.85; p1,p2,p3,p5=0.3,1.45,2.1,0.85
adiabat(ax,V2,p2,V1,p1,rev=True)
ax.plot([V2,V2],[p2,p3],color=K,lw=1.5); arrow(ax,V2,1.72,V2,1.84,lw=1.1)
ax.plot([V2,V4],[p3,p3],color=K,lw=1.5); arrow(ax,0.58,p3,0.68,p3,lw=1.1)
adiabat(ax,V4,p3,V1,p5)
ax.plot([V1,V1],[p5,p1],color=K,lw=1.5); arrow(ax,V1,0.62,V1,0.52,lw=1.1)
pt(ax,V1,p1,"1",0.1,-0.05); pt(ax,V2,p2,"2",-0.12,0); pt(ax,V2,p3,"3",-0.12,0.06); pt(ax,V4,p3,"4",0.02,0.14); pt(ax,V1,p5,"5",0.1,0.05)
fin(fig,ax,-0.15,3.4,-0.2,2.6,"d49p_q9.png")

# S12 Otto cycle p-V with the numbers of the question
fig,ax=new(3.4,2.6); ts_axes(ax,3.2,2.5,xl="V",yl="p")
V1,V2=2.8,0.4; p1,p2,p3,p4=0.3,0.85,2.2,0.62
adiabat(ax,V2,p2,V1,p1,rev=True); adiabat(ax,V2,p3,V1,p4)
ax.plot([V2,V2],[p2,p3],color=K,lw=1.5); arrow(ax,V2,1.45,V2,1.6,lw=1.1)
ax.plot([V1,V1],[p4,p1],color=K,lw=1.5); arrow(ax,V1,0.5,V1,0.42,lw=1.1)
pt(ax,V1,p1,"1",0.1,-0.05); pt(ax,V2,p2,"2",-0.12,0); pt(ax,V2,p3,"3",-0.12,0.05); pt(ax,V1,p4,"4",0.1,0.05)
label(ax,V2+0.1,p3+0.08,"7.41 MPa, 2778 K",fs=7,ha="left")
label(ax,V1-0.05,p1-0.17,"100 kPa, 300 K",fs=7,ha="right")
label(ax,0.5,1.0,"q = 1500 kJ/kg",fs=6.5,ha="left")
fin(fig,ax,-0.15,3.4,-0.2,2.6,"d49p_s12.png")
