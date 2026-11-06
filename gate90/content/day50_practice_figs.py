import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def seg(ax,p,q,lw=1.5,arr=True):
    p,q=np.array(p,float),np.array(q,float); ax.plot([p[0],q[0]],[p[1],q[1]],color=K,lw=lw)
    if arr: m=(p+q)/2; d=(q-p)/np.hypot(*(q-p))*0.06; arrow(ax,*(m-d),*(m+d),lw=1.1)
def dot(ax,p): ax.add_patch(Circle(p,0.03,fc=K,zorder=6))
def ph_dome(ax,xl=0.45,xt=1.35,xr=2.3,base=0.2,top=1.95):
    """schematic saturation dome on p-h axes; returns the liquid/vapour-line h at a plot pressure y"""
    u=np.linspace(0,1,80); h=top-base
    ax.plot(xt-(xt-xl)*np.sin(u*np.pi/2),top-h*u**2,color=K,lw=0.8,ls="--")
    ax.plot(xt+(xr-xt)*np.sin(u*np.pi/2),top-h*u**2,color=K,lw=0.8,ls="--")
    fl=lambda y: xt-(xt-xl)*np.sin(np.pi/2*np.sqrt((top-y)/h)); fv=lambda y: xt+(xr-xt)*np.sin(np.pi/2*np.sqrt((top-y)/h))
    return fl,fv
def vcr(ax,yL=0.6,yH=1.55):
    """simple saturated VCR cycle on p-h: 1 sat. vapour, 2 superheated, 3 sat. liquid, 4 wet"""
    fl,fv=ph_dome(ax)
    p3=(fl(yH),yH); p4=(p3[0],yL); p1=(fv(yL),yL); p2=(p1[0]+0.6,yH)
    seg(ax,p4,p1); seg(ax,p1,p2); seg(ax,p2,p3); seg(ax,p3,p4)
    for p in (p1,p2,p3,p4): dot(ax,p)
    return p1,p2,p3,p4
def psy_axes(ax,W=3.2,H=2.2):
    ax.plot([0,W],[0,0],color=K,lw=1.0); ax.plot([W,W],[0,H],color=K,lw=1.0)
    label(ax,W/2,-0.18,"dry-bulb temperature  →",fs=8); label(ax,W+0.12,H/2,"specific humidity ω  →",fs=8,rotation=90)
    x=np.linspace(0,W,200); sat=0.2*np.exp(x/1.05)
    m=sat<=H; ax.plot(x[m],sat[m],color=K,lw=1.3)
    for f in (0.6,0.35):
        y=f*sat; m2=y<=H; ax.plot(x[m2],y[m2],color=K,lw=0.6,ls="--")

# Q5 p-h diagram, states numbered only
fig,ax=new(3.4,2.6); ts_axes(ax,3.4,2.3,xl="h",yl="p")
p1,p2,p3,p4=vcr(ax)
label(ax,p1[0]+0.08,p1[1]-0.14,"1",fs=9); label(ax,p2[0]+0.1,p2[1]+0.06,"2",fs=9)
label(ax,p3[0]-0.1,p3[1]+0.08,"3",fs=9); label(ax,p4[0]-0.12,p4[1]-0.1,"4",fs=9)
fin(fig,ax,-0.15,3.7,-0.2,2.5,"d50p_q5.png")

# Q11 psychrometric chart with processes O-1 ... O-4
fig,ax=new(3.6,2.6); psy_axes(ax)
O=np.array([2.2,0.55]); dot(ax,O); label(ax,O[0]-0.16,O[1]+0.06,"O",fs=9)
P1=O+[0.45,0.45]; P2=O+[0,0.6]; P3=O+[-0.6,-0.3]; P4=O+[0.6,-0.32]
for P,t,dx,dy in ((P1,"1",0.08,0.08),(P2,"2",0.0,0.12),(P3,"3",-0.1,-0.06),(P4,"4",0.1,-0.06)):
    arrow(ax,*O,*P,lw=1.3); label(ax,P[0]+dx,P[1]+dy,t,fs=9)
label(ax,1.6,1.3,"φ = 100 %",fs=7.5,ha="right")
fin(fig,ax,-0.1,3.6,-0.35,2.35,"d50p_q11.png")

# S4 the cycle with the enthalpies of the question
fig,ax=new(3.4,2.6); ts_axes(ax,3.4,2.3,xl="h",yl="p")
p1,p2,p3,p4=vcr(ax)
label(ax,p1[0]+0.08,p1[1]-0.14,"1",fs=9); label(ax,p2[0]+0.1,p2[1]+0.06,"2",fs=9)
label(ax,p3[0]-0.1,p3[1]+0.08,"3",fs=9); label(ax,p4[0]-0.12,p4[1]-0.1,"4",fs=9)
for x in (p3[0],p1[0],p2[0]): ax.plot([x,x],[0,p4[1] if x==p3[0] else (p1[1] if x==p1[0] else p2[1])],color=K,lw=0.5,ls=":")
label(ax,p3[0],-0.13,"236",fs=7.5); label(ax,p1[0],-0.13,"388",fs=7.5); label(ax,p2[0],-0.13,"421",fs=7.5)
label(ax,p2[0],-0.3,"(kJ/kg)",fs=7)
label(ax,(p4[0]+p1[0])/2,p1[1]+0.13,"RE = 152",fs=7.5); label(ax,p2[0]+0.12,(p1[1]+p2[1])/2,"w = 33",fs=7.5,ha="left")
fin(fig,ax,-0.15,3.8,-0.4,2.5,"d50p_s4.png")
