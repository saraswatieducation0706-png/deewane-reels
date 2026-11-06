import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def dot(ax,p): ax.add_patch(Circle(p,0.035,fc=K,zorder=6))
def dome(ax,xl=0.3,xt=1.2,xr=3.0,base=0.25,top=1.75):
    u=np.linspace(0,1,80); h=top-base
    ax.plot(xt-(xt-xl)*u,base+h*np.sqrt(1-u**2),color=K,lw=0.8,ls="--")
    ax.plot(xt+(xr-xt)*u,base+h*np.sqrt(1-u**2),color=K,lw=0.8,ls="--")

# P4 reversible engine with three reservoirs
fig,ax=new(3.6,2.6)
reservoir(ax,0,1.6,"1000 K",w=1.4)
reservoir(ax,-1.0,-1.1,"600 K",w=1.2,fc="#dbe9f6"); reservoir(ax,1.0,-1.1,"300 K",w=1.2,fc="#dbe9f6")
device(ax,0,0.25,"HE",r=0.32)
flow(ax,0,1.39,0,0.57,"3000 kJ",side="right",fs=7.5)
arrow(ax,-0.24,0.04,-0.85,-0.89,lw=1.3); label(ax,-0.7,-0.3,"Q₂",fs=8.5,ha="right")
arrow(ax,0.24,0.04,0.85,-0.89,lw=1.3); label(ax,0.7,-0.3,"Q₃",fs=8.5,ha="left")
arrow(ax,0.32,0.25,1.3,0.25,lw=1.3); label(ax,1.38,0.25,"W = 1500 kJ",fs=7.5,ha="left")
label(ax,-0.4,0.25,"reversible",fs=7,ha="right")
fin(fig,ax,-1.8,2.6,-1.45,1.95,"d73p_q4.png")

# S6 ideal Rankine cycle on T-s
fig,ax=new(3.4,2.6); ts_axes(ax,3.5,2.45); dome(ax)
yb=1.45; u=np.sqrt(1-((yb-0.25)/1.5)**2); sl=(1.2-0.9*u,yb); sv=(1.2+1.8*u,yb)
p1=(2.6,2.15); p2=(2.6,0.3); p3=(0.3,0.3); p4=(0.34,0.45)
xs=np.linspace(p4[0],sl[0],20); ys=p4[1]+(yb-p4[1])*((xs-p4[0])/(sl[0]-p4[0]))**0.6; ax.plot(xs,ys,color=K,lw=1.5)
ax.plot([sl[0],sv[0]],[yb,yb],color=K,lw=1.5); arrow(ax,1.3,yb,1.42,yb,lw=1.1)
xs=np.linspace(sv[0],p1[0],20); ys=yb+(p1[1]-yb)*((xs-sv[0])/(p1[0]-sv[0]))**1.6; ax.plot(xs,ys,color=K,lw=1.5)
ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=K,lw=1.5); arrow(ax,2.6,1.3,2.6,1.15,lw=1.1)
ax.plot([p2[0],p3[0]],[0.3,0.3],color=K,lw=1.5); arrow(ax,1.6,0.3,1.45,0.3,lw=1.1)
ax.plot([p3[0],p4[0]],[p3[1],p4[1]],color=K,lw=1.5)
for p in (p1,p2,p3,p4): dot(ax,p)
label(ax,2.7,2.2,"1 (3423.1 kJ/kg)",fs=7,ha="left"); label(ax,2.6,0.12,"2 (x = 0.831, 2180.0)",fs=7)
label(ax,0.3,0.12,"3 (191.8)",fs=7,ha="left"); label(ax,0.2,0.47,"4",fs=7.5,ha="right")
label(ax,1.25,1.3,"6 MPa",fs=7); label(ax,1.1,0.42,"10 kPa",fs=7)
fin(fig,ax,-0.15,4.0,-0.2,2.6,"d73p_s6.png")
