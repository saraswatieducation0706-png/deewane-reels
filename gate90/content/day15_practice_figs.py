import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def axes(ax,x0,x1,y0,y1,xl="x",yl="y"):
    arrow(ax,x0,0,x1,0,lw=1.0); arrow(ax,0,y0,0,y1,lw=1.0)
    label(ax,x1+0.05,-0.02,xl,fs=9,ha="left",va="top"); label(ax,0.07,y1,yl,fs=9,ha="left",va="top")

# Q13: region between y = x^2 and y = 2x (horizontal strip for dx dy order)
fig,ax=new(2.9,3.3); s=0.8   # drawing units: x scale 1, y scale s
axes(ax,-0.3,2.6,-0.3,4*s+0.5)
xx=np.linspace(0,2,200)
ax.fill_between(xx,xx**2*s,2*xx*s,color="#dddddd",lw=0)
ax.plot(xx,xx**2*s,color=K,lw=1.6); ax.plot([0,2],[0,4*s],color=K,lw=1.6)
label(ax,1.42,0.75,"y = x²",fs=8.5,ha="left")
label(ax,0.95,2.6,"y = 2x",fs=8.5,ha="right")
ys=2.0; xa,xb=ys/2,np.sqrt(ys)          # strip at y = 2
ax.add_patch(Rectangle((xa,ys*s-0.05),xb-xa,0.1,fc="white",ec=K,lw=0.9,hatch="////"))
label(ax,xa-0.1,ys*s,"x = y/2",fs=7.5,ha="right"); label(ax,xb+0.1,ys*s,"x = √y",fs=7.5,ha="left")
ax.plot([0,2],[4*s,4*s],color=K,lw=0.6,ls="--"); label(ax,-0.08,4*s,"4",fs=8,ha="right")
ax.add_patch(Circle((2,4*s),0.045,fc=K,ec=K)); label(ax,2.1,4*s,"(2, 4)",fs=8,ha="left")
label(ax,-0.08,-0.12,"O",fs=8,ha="right",va="top")
fin(fig,ax,-0.45,3.0,-0.4,4*s+0.6,"d15p_q13.png")

# S6: f(x) = x^3 - 6x^2 + 9x + 15 on [0, 5]: local max vs absolute max at the end point
fig,ax=new(3.4,2.8); sy=1/9.0
axes(ax,-0.3,5.6,-0.3,40*sy,"x","f(x)")
xx=np.linspace(0,5,300); f=lambda x: x**3-6*x**2+9*x+15
ax.plot(xx,f(xx)*sy,color=K,lw=1.8)
for (px,txt,dx,dy,ha) in [(0,"(0, 15)",0.12,-0.25,"left"),(1,"local max (1, 19)",0.0,0.3,"center"),
                          (3,"local min (3, 15)",0.0,-0.32,"center"),(5,"absolute max (5, 35)",-0.12,0.0,"right")]:
    ax.add_patch(Circle((px,f(px)*sy),0.06,fc=K,ec=K,zorder=6)); label(ax,px+dx,f(px)*sy+dy,txt,fs=7.5,ha=ha)
ax.plot([5,5],[0,f(5)*sy],color=K,lw=0.6,ls="--"); label(ax,5,-0.12,"5",fs=8,va="top")
label(ax,1,-0.12,"1",fs=8,va="top"); label(ax,3,-0.12,"3",fs=8,va="top")
ax.plot([1,1],[0,f(1)*sy],color=K,lw=0.5,ls=":"); ax.plot([3,3],[0,f(3)*sy],color=K,lw=0.5,ls=":")
fin(fig,ax,-0.4,6.0,-0.45,40*sy+0.2,"d15p_s6.png")

# Q15: paraboloid z = 4 - x^2 - y^2 cut by the plane z = 0 (side view + base circle)
fig,ax=new(3.0,2.8)
rr=np.linspace(-2,2,200); ax.plot(rr,4-rr**2,color=K,lw=1.8)
ax.fill_between(rr,0,4-rr**2,color="#eeeeee",lw=0)
t=np.linspace(0,2*np.pi,200); ax.plot(2*np.cos(t),0.45*np.sin(t),color=K,lw=1.0)
ax.plot(2*np.cos(t[t>np.pi]),0.45*np.sin(t[t>np.pi]),color=K,lw=1.4)
arrow(ax,0,-0.6,0,4.8,lw=1.0); label(ax,0.1,4.75,"z",fs=9,ha="left")
arrow(ax,-2.6,0,2.7,0,lw=1.0); label(ax,2.75,0,"x",fs=9,ha="left")
ax.add_patch(Circle((0,4),0.06,fc=K,ec=K,zorder=6)); label(ax,-0.15,4.15,"(0, 0, 4)",fs=8,ha="right",va="bottom")
label(ax,1.2,3.0,"z = 4 − x² − y²",fs=8,ha="left")
label(ax,-0.9,-0.75,"base: x² + y² ≤ 4 (z = 0)",fs=7.5)
hdim(ax,0,2,-1.15,"r = 2",above=False,fs=8); ext(ax,2,-0.05,2,-1.25); ext(ax,0,-0.65,0,-1.25)
fin(fig,ax,-2.9,3.2,-1.6,5.0,"d15p_q15.png")
