import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def cplane(ax,x0,x1,y0,y1):
    arrow(ax,x0,0,x1,0,lw=1.0); arrow(ax,0,y0,0,y1,lw=1.0)
    label(ax,x1+0.05,0,"Re z",fs=8,ha="left"); label(ax,0,y1+0.15,"Im z",fs=8)
def contour(ax,c,r,ang=60):
    t=np.linspace(0,2*np.pi,200); ax.plot(c[0]+r*np.cos(t),c[1]+r*np.sin(t),color=K,lw=1.5)
    a=np.radians(ang); p=np.array([c[0]+r*np.cos(a),c[1]+r*np.sin(a)]); d=np.array([-np.sin(a),np.cos(a)])*0.08
    arrow(ax,*(p-d),*(p+d),lw=1.2)
def pole(ax,x,y,t,dy=-0.25):
    ax.plot([x],[y],marker="x",color=K,ms=7,mew=1.6); label(ax,x,y+dy,t,fs=8)

# Q4 |z| = 3 enclosing poles 0 and 2
fig,ax=new(3.0,3.0); cplane(ax,-3.6,3.9,-3.5,3.6)
contour(ax,(0,0),3,ang=45)
pole(ax,0,0,"",dy=-0.35); label(ax,-0.25,-0.35,"0",fs=8,ha="right"); pole(ax,2,0,"2",dy=-0.35)
label(ax,2.3,-2.6,"|z| = 3",fs=8,ha="left")
fin(fig,ax,-3.8,4.6,-3.7,4.0,"d51p_q4.png")

# Q11 |z| = 1 with the singular point z = 3 outside
fig,ax=new(3.4,2.0); cplane(ax,-1.5,3.8,-1.3,1.3)
contour(ax,(0,0),1,ang=45)
pole(ax,3,0,"3",dy=-0.25)
label(ax,0.75,-0.95,"|z| = 1",fs=8,ha="left")
label(ax,-0.1,-0.15,"0",fs=8,ha="right")
fin(fig,ax,-1.6,4.4,-1.4,1.6,"d51p_q11.png")

# S8 trapezoidal rule on sin x, 4 strips
fig,ax=plt.subplots(figsize=(3.4,2.2)); ax.axis("off")
x=np.linspace(0,np.pi,200); ax.plot(x,np.sin(x),color=K,lw=1.5)
xs=np.linspace(0,np.pi,5); ys=np.sin(xs)
ax.fill_between(xs,ys,color="#dddddd",zorder=0); ax.plot(xs,ys,color=K,lw=1.0,ls="--")
for a,b in zip(xs,ys): ax.plot([a,a],[0,b],color=K,lw=0.7)
ax.annotate("",xy=(3.5,0),xytext=(-0.1,0),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.0))
ax.annotate("",xy=(0,1.25),xytext=(0,-0.05),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.0))
for a,t in zip(xs,["0","π/4","π/2","3π/4","π"]): ax.text(a,-0.1,t,fontsize=7.5,ha="center",va="top")
ax.text(3.55,0,"x",fontsize=9,va="center"); ax.text(0.05,1.25,"y = sin x",fontsize=8,va="center",ha="left")
ax.text(1.95,0.45,"trapezia\n(shaded)",fontsize=7,ha="center")
ax.set_xlim(-0.2,3.8); ax.set_ylim(-0.3,1.35)
save(fig,F+"d51p_s8.png")
