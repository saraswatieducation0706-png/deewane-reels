import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
G="#e8eef5"
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# P5 piston-cylinder with a piston of mass m, open to the atmosphere
fig,ax=new(2.8,2.6)
ax.add_patch(Rectangle((0,0),1.2,0.9,fc=G,ec="none"))
ax.plot([0,0,1.2,1.2],[2.0,0,0,2.0],color=K,lw=1.6)
ax.add_patch(Rectangle((0.02,0.9),1.16,0.22,fc="#bbbbbb",ec=K,lw=1.3,zorder=4))
label(ax,0.6,1.01,"piston, 50 kg",fs=7.5,zorder=5)
label(ax,0.6,0.45,"gas",fs=9)
for x in (0.3,0.6,0.9): arrow(ax,x,1.75,x,1.2,lw=1.0)
label(ax,1.35,1.55,"atmosphere\n100 kPa",fs=7.5,ha="left")
hdim(ax,0,1.2,-0.18,"A = 0.01 m²",above=False,fs=7.5)
fin(fig,ax,-0.2,2.6,-0.5,2.1,"d35p_q5.png")

# P8 T-v diagram with saturation dome and one isobar
fig,ax=new(3.6,2.6); ax.set_aspect("auto")
arrow(ax,0,0,4.2,0,lw=1); arrow(ax,0,0,0,3.2,lw=1)
label(ax,4.25,0,"v",fs=9,ha="left"); label(ax,0,3.3,"T",fs=9,va="bottom")
# dome: saturated-liquid (left) and saturated-vapour (right) lines meeting at the critical point C
xc,yc=1.4,2.6; yb=0.3
y=np.linspace(yb,yc,80); u=(yc-y)/(yc-yb)
L=lambda u:xc-(xc-0.55)*(0.4*u**0.5+0.6*u**1.6); Rt=lambda u:xc+(3.9-xc)*(0.3*u**0.5+0.7*u**2.2)
lx=L(u); rx=Rt(u)
ax.plot(lx,y,color=K,lw=1.4); ax.plot(rx,y,color=K,lw=1.4)
ax.add_patch(Circle((xc,yc),0.05,fc=K,zorder=5)); label(ax,xc,yc+0.2,"C",fs=8)
yT=1.4; uT=(yc-yT)/(yc-yb); xL=L(uT); xR=Rt(uT)
xO,yO=xL-0.05,yT-0.6
ax.plot([xL-0.08,xL],[yT-0.95,yT],color=K,lw=1.1,ls="--"); ax.plot([xL,xR],[yT,yT],color=K,lw=1.1,ls="--")
xs=np.linspace(xR,4.1,20); ys=yT+0.9*(1-np.exp(-(xs-xR)*1.6)); ax.plot(xs,ys,color=K,lw=1.1,ls="--")
pts={"O":(xL-0.08*0.6/0.95,yO,0.17,0),"P":(xL,yT,-0.17,0.12),"Q":((xL+xR)/2,yT,0,0.18),"R":(xR,yT,-0.02,0.2),"S":(xs[-3],ys[-3],0,0.2)}
for k,(x,yy,dx,dy) in pts.items():
    ax.add_patch(Circle((x,yy),0.05,fc=K,zorder=5)); label(ax,x+dx,yy+dy,k,fs=8)
fin(fig,ax,-0.3,4.6,-0.25,3.5,"d35p_q8.png")

# P14 polytropic expansion on p-V (solution figure)
fig,ax=new(3.2,2.4); ax.set_aspect("auto")
arrow(ax,0,0,3.0,0,lw=1); arrow(ax,0,0,0,3.0,lw=1)
label(ax,3.05,0,"V (m³)",fs=8,ha="left"); label(ax,0,3.1,"p (kPa)",fs=8,va="bottom")
n=np.log(5)/np.log(4); V=np.linspace(0.1,0.4,60); p=1000*(0.1/V)**n
X=V*6; Y=p/400
ax.fill_between(X,0,Y,color="#e5e5e5"); ax.plot(X,Y,color=K,lw=1.6)
for (x,y,t) in [(X[0],Y[0],"1"),(X[-1],Y[-1],"2")]:
    ax.add_patch(Circle((x,y),0.04,fc=K,zorder=5)); label(ax,x+0.12,y+0.12,t,fs=9)
    ax.plot([x,x],[0,y],color=K,lw=0.5,ls=":"); ax.plot([0,x],[y,y],color=K,lw=0.5,ls=":")
label(ax,X[0],-0.18,"0.1",fs=7.5); label(ax,X[-1],-0.18,"0.4",fs=7.5)
label(ax,-0.08,Y[0],"1000",fs=7.5,ha="right"); label(ax,-0.08,Y[-1],"200",fs=7.5,ha="right")
label(ax,1.5,0.25,"W = area",fs=8)
label(ax,1.6,1.35,"pV$^{n}$ = C",fs=8,ha="left")
fin(fig,ax,-0.6,3.6,-0.4,3.2,"d35p_q14.png")
