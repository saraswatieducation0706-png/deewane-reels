import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def vec(ax,p,q,t,off,fs=8,lw=1.4,ha="center"):
    """velocity vector p -> q with a label offset from its midpoint"""
    arrow(ax,*p,*q,lw=lw); m=((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1]); label(ax,*m,t,fs=fs,ha=ha)
def arc(ax,c,r,a0,a1,t,lr,la,fs=8):
    th=np.radians(np.linspace(a0,a1,30)); ax.plot(c[0]+r*np.cos(th),c[1]+r*np.sin(th),color=K,lw=0.8)
    a=np.radians(la); label(ax,c[0]+lr*np.cos(a),c[1]+lr*np.sin(a),t,fs=fs)

# Q5 separate inlet and outlet velocity triangles, symmetrical impulse blade
s=200.; a=np.radians(18); V1=500; u=200
vw1,vf=V1*np.cos(a)/s,V1*np.sin(a)/s; us=u/s; xr=vw1-us; b=np.degrees(np.arctan2(vf,xr))
fig,ax=new(4.4,2.0)
P0=(0,0); U=(us,0); A=(vw1,-vf)
vec(ax,P0,U,"u",(0,0.13)); vec(ax,P0,A,"V₁",(-0.15,-0.2)); vec(ax,U,A,"Vr₁",(0.4,0.12))
arc(ax,P0,0.75,-18,0,"α₁",0.95,-8,fs=7.5); arc(ax,U,0.35,-b,0,"β₁",0.52,-14,fs=7.5)
label(ax,1.2,0.5,"Inlet",fs=8.5)
Q0=(3.4,0); U2=(3.4+us,0); C=(3.4+us-xr,-vf)
vec(ax,Q0,U2,"u",(0,0.13)); vec(ax,U2,C,"Vr₂",(0.18,-0.12)); vec(ax,Q0,C,"V₂",(-0.22,0))
ax.plot([U2[0]-0.65,U2[0]],[0,0],color=K,lw=0.6,ls=":")
arc(ax,U2,0.45,180,180+b,"β₂",0.66,180+b/2-4,fs=7.5)
label(ax,3.9,0.5,"Outlet",fs=8.5)
arrow(ax,2.5,-0.95,3.2,-0.95,lw=1.0); label(ax,2.85,-1.1,"blade motion",fs=7)
fin(fig,ax,-0.3,5.0,-1.25,0.7,"d52p_q5.png")

# S6 combined diagram with the numbers of Q6 (k = 0.9)
k=0.9; vr2x=k*xr; vf2=k*vf
fig,ax=new(3.8,2.4)
O=(0,0); U=(us,0); A=(vw1,-vf); C=(us-vr2x,-vf2)
vec(ax,O,U,"",(0,0))
vec(ax,O,A,"",(0,0)); label(ax,2.0,-0.88,"V₁ = 500",fs=7.5)
vec(ax,U,A,"Vr₁",(0.22,0.06),fs=7.5)
vec(ax,O,C,"V₂",(-0.2,0.0),fs=7.5)
vec(ax,U,C,"",(0,0)); label(ax,0.3,-0.8,"Vr₂ = 0.9 Vr₁",fs=7.5,ha="left")
yd=-1.25
for x,y0 in ((0,0),(A[0],A[1]),(C[0],C[1])): ax.plot([x,x],[y0,yd],color=K,lw=0.5,ls=":")
hdim(ax,0,A[0],yd,"Vw₁ = 475.5",above=False,fs=7.5)
ax.plot([C[0],C[0]],[yd,yd-0.4],color=K,lw=0.5,ls=":"); ax.plot([0,0],[yd,yd-0.4],color=K,lw=0.5,ls=":"); ax.plot([C[0],0],[yd-0.35,yd-0.35],color=K,lw=0.9); label(ax,C[0]-0.08,yd-0.35,"Vw₂ = 48.0",fs=7.5,ha="right")
ax.plot([0,0],[0,0.3],color=K,lw=0.5,ls=":"); ax.plot([us,us],[0,0.3],color=K,lw=0.5,ls=":")
hdim(ax,0,us,0.3,"u = 200",fs=7.5)
label(ax,2.6,0.45,"ΔVw = 523.5 m/s",fs=7.5)
fin(fig,ax,-1.2,3.4,-1.8,0.75,"d52p_s6.png")
