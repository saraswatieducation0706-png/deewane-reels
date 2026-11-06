import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def seg(ax,p,q,lw=1.5,arr=True,ls="-"):
    p,q=np.array(p),np.array(q); ax.plot([p[0],q[0]],[p[1],q[1]],color=K,lw=lw,ls=ls)
    if arr: m=(p+q)/2; d=(q-p)/np.hypot(*(q-p))*0.06; arrow(ax,*(m-d),*(m+d),lw=1.1)
def curve(ax,xs,ys,lw=1.5,arr=True,color=K):
    ax.plot(xs,ys,color=color,lw=lw)
    if arr: i=len(xs)//2; arrow(ax,xs[i-1],ys[i-1],xs[i+1],ys[i+1],lw=1.1,color=color)
def dot(ax,p): ax.add_patch(Circle(p,0.03,fc=K,zorder=6))
def isobar(p,q,n=30):
    xs=np.linspace(p[0],q[0],n); return xs,p[1]*np.exp(np.log(q[1]/p[1])*(xs-p[0])/(q[0]-p[0]))
def dome(ax,xl=0.3,xt=1.2,xr=3.0,base=0.25,top=1.75):
    u=np.linspace(0,1,80); h=top-base
    ax.plot(xt-(xt-xl)*u,base+h*np.sqrt(1-u**2),color=K,lw=0.8,ls="--")
    ax.plot(xt+(xr-xt)*u,base+h*np.sqrt(1-u**2),color=K,lw=0.8,ls="--")

# Q9 ideal regenerative Brayton cycle
fig,ax=new(3.3,2.6); ts_axes(ax,3.1,2.5)
p1=(0.6,0.45); p2=(0.6,1.0); p3=(2.3,2.15); p4=(2.3,1.3)
x23,y23=isobar(p2,p3); x41,y41=isobar(p4,p1)
curve(ax,x23,y23); curve(ax,x41,y41); seg(ax,p1,p2); seg(ax,p3,p4)
ix=np.argmin(abs(y23-1.3)); px=(x23[ix],y23[ix]); iy=np.argmin(abs(y41-1.0)); py=(x41[iy],y41[iy])
for p in (p1,p2,p3,p4,px,py): dot(ax,p)
ax.plot([px[0],p4[0]],[1.3,1.3],color="#D7191F",lw=0.9,ls="--"); ax.plot([p2[0],py[0]],[1.0,1.0],color="#D7191F",lw=0.9,ls="--")
label(ax,0.5,0.45,"1",fs=8.5,ha="right"); label(ax,0.5,1.0,"2",fs=8.5,ha="right"); label(ax,2.3,2.28,"3",fs=8.5)
label(ax,2.4,1.3,"4",fs=8.5,ha="left"); label(ax,px[0]-0.08,1.38,"x",fs=8.5,ha="right"); label(ax,py[0]+0.06,0.88,"y",fs=8.5,ha="left")
fin(fig,ax,-0.15,3.3,-0.2,2.6,"d47p_q9.png")

# S2 simple Rankine cycle with superheat
fig,ax=new(3.3,2.5); ts_axes(ax,3.4,2.4); dome(ax)
yb=1.45; u=np.sqrt(1-((yb-0.25)/1.5)**2); sl=(1.2-0.9*u,yb); sv=(1.2+1.8*u,yb)
p1=(2.6,2.15); p2=(2.6,0.3); p3=(0.3,0.3); p4=(0.34,0.45)
xs=np.linspace(p4[0],sl[0],20); ys=p4[1]+(yb-p4[1])*((xs-p4[0])/(sl[0]-p4[0]))**0.6; ax.plot(xs,ys,color=K,lw=1.5)
ax.plot([sl[0],sv[0]],[yb,yb],color=K,lw=1.5); arrow(ax,1.3,yb,1.42,yb,lw=1.1)
xs=np.linspace(sv[0],p1[0],20); ys=yb+(p1[1]-yb)*((xs-sv[0])/(p1[0]-sv[0]))**1.6; ax.plot(xs,ys,color=K,lw=1.5)
seg(ax,p1,p2); seg(ax,p2,p3); seg(ax,p3,p4,arr=False)
for p in (p1,p2,p3,p4): dot(ax,p)
label(ax,2.72,2.2,"1  (3230 kJ/kg)",fs=7,ha="left"); label(ax,2.6,0.12,"2 (2140 kJ/kg)",fs=7)
label(ax,0.3,0.12,"3 (192 kJ/kg)",fs=7,ha="left"); label(ax,0.22,0.55,"4",fs=8,ha="right")
label(ax,1.25,1.3,"8 MPa",fs=7); label(ax,1.3,0.42,"10 kPa",fs=7)
label(ax,2.5,1.0,"turbine",fs=7,ha="right")
fin(fig,ax,-0.15,4.0,-0.2,2.55,"d47p_s2.png")

# S4 two-stage compression with intercooling on p-V
fig,ax=new(3.4,2.6); ts_axes(ax,3.2,2.4,xl="V",yl="p")
V1=2.8; P1=0.3; P2=0.9; P3=2.1     # plot pressures for 1, 3, 9 bar (schematic)
n=1.3
Va=V1*(P1/P2)**(1/n)               # end of stage 1
Vi=V1*(P1/P2)                      # intercooled to the isotherm
Vb=Vi*(P2/P3)**(1/n)               # end of stage 2
Vs=V1*(P1/P3)**(1/n)               # single stage end
Vt=V1*(P1/P3)                      # isothermal end
V=np.linspace(Va,V1,40); ax.plot(V,P1*(V1/V)**n,color=K,lw=1.5)
V=np.linspace(Vb,Vi,40); ax.plot(V,P2*(Vi/V)**n,color=K,lw=1.5)
V=np.linspace(Vs,Va,40); ax.plot(V,P1*(V1/V)**n,color=K,lw=0.9,ls="--")
V=np.linspace(Vt,V1,60); ax.plot(V,P1*V1/V,color="#2C7BB6",lw=0.9,ls=":")
ax.plot([Vi,Va],[P2,P2],color=K,lw=1.5); arrow(ax,(Va+Vi)/2+0.05,P2,(Va+Vi)/2-0.05,P2,lw=1.0)
ax.plot([0.15,V1],[P1,P1],color=K,lw=0.6); ax.plot([0.15,Vb],[P3,P3],color=K,lw=0.6)
V=np.linspace(Vb,Va,80); up=np.minimum(P1*(V1/V)**n,P3); lo=np.where(V<Vi,P2*(Vi/np.minimum(V,Vi))**n,P2)
ax.fill_between(V,lo,up,color="#D7191F",alpha=0.25,lw=0)
label(ax,-0.05,P1,"1 bar",fs=7,ha="right"); label(ax,-0.05,P2,"3 bar",fs=7,ha="right"); label(ax,-0.05,P3,"9 bar",fs=7,ha="right")
ax.plot([0,0.15],[P2,P2],color=K,lw=0.4,ls=":")
label(ax,2.3,0.62,"stage 1",fs=7); label(ax,1.0,1.65,"stage 2",fs=7,ha="left")
label(ax,1.45,1.0,"intercooler",fs=7,ha="left")
label(ax,2.4,2.1,"isotherm (dotted)",fs=6.5,color="#2C7BB6")
label(ax,2.4,1.9,"saved work (shaded)",fs=6.5,color="#D7191F")
fin(fig,ax,-0.6,3.4,-0.2,2.6,"d47p_s4.png")
