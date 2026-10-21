import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
G="#e8e8e8"; Gas="#dbe9f6"
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
def pt(ax,x,y,t,dx=0,dy=0):
    ax.add_patch(Circle((x,y),0.04,fc=K,zorder=6)); label(ax,x+dx,y+dy,t,fs=9)

# P3 piston-cylinder with stops
fig,ax=new(2.8,2.8)
ax.plot([0,0,1.6,1.6],[2.6,0,0,2.6],color=K,lw=1.8)
ax.add_patch(Rectangle((0.02,0.02),1.56,0.78,fc=Gas,ec="none"))
ax.add_patch(Rectangle((0.02,0.8),1.56,0.2,fc="#bbbbbb",ec=K,lw=1.2))
label(ax,0.8,0.4,"air\nV₁ = 0.02 m³",fs=8)
for x0 in (0.02,1.43): ax.add_patch(Rectangle((x0,1.95),0.15,0.12,fc=K,ec=K))
ax.plot([1.6,1.8],[2.01,2.01],color=K,lw=0.6); label(ax,1.85,2.01,"stops\n(V = 0.05 m³)",fs=7.5,ha="left")
arrow(ax,2.2,0.4,1.7,0.4,lw=1.3); label(ax,2.2,0.6,"Q",fs=9)
fin(fig,ax,-0.3,2.9,-0.15,2.75,"d37p_q3.png")

# P6 turbine with elevation difference
fig,ax=new(3.8,2.6)
ax.add_patch(Polygon([[1.2,0.55],[2.4,0.95],[2.4,-0.95],[1.2,-0.55]],closed=True,fc=G,ec=K,lw=1.5))
label(ax,1.8,0,"TURBINE",fs=8)
ax.add_patch(Rectangle((0.3,0.3),0.9,0.22,fc=Gas,ec=K,lw=1.2)); arrow(ax,-0.2,0.41,0.35,0.41,lw=1.2)
label(ax,0.25,0.85,"(1) 5 m above exit\nh₁ = 3300 kJ/kg, V₁ = 40 m/s",fs=7)
ax.add_patch(Rectangle((2.4,-0.85),0.75,0.22,fc=Gas,ec=K,lw=1.2)); arrow(ax,3.0,-0.74,3.5,-0.74,lw=1.2)
label(ax,3.3,-1.25,"(2) h₂ = 2500 kJ/kg\nV₂ = 120 m/s",fs=7)
ax.plot([2.4,3.3],[0.15,0.15],color=K,lw=3); arrow(ax,3.3,0.15,3.7,0.15,lw=1.4); label(ax,3.55,0.38,"W",fs=9)
arrow(ax,1.8,-0.95,1.8,-1.4,lw=1.1); label(ax,1.8,-1.55,"50 kW lost",fs=7.5)
fin(fig,ax,-0.3,4.1,-1.75,1.3,"d37p_q6.png")

# P10 tank charged from a supply line
fig,ax=new(3.2,2.2)
ax.add_patch(Rectangle((0,0),1.4,1.2,fc=Gas,ec=K,lw=1.6)); label(ax,0.7,0.55,"rigid tank\n0.5 m³\n100 kPa, 300 K",fs=7.5)
ax.add_patch(Rectangle((0.62,1.2),0.16,0.6,fc=Gas,ec=K,lw=1.2))
ax.add_patch(Polygon([[0.5,1.42],[0.9,1.62],[0.9,1.42],[0.5,1.62]],closed=True,fc="white",ec=K,lw=1.2,zorder=5))
label(ax,1.15,1.52,"valve",fs=7.5,ha="left")
ax.add_patch(Rectangle((-0.6,1.8),2.8,0.2,fc=Gas,ec=K,lw=1.2)); arrow(ax,-0.5,1.9,0.2,1.9,lw=1.2)
label(ax,1.6,2.2,"supply line: 600 kPa, 300 K",fs=7.5)
fin(fig,ax,-0.7,2.3,-0.15,2.4,"d37p_q10.png")

# P11 triangular cycle on p-V
fig,ax=new(3.4,2.6)
sx,sy=3.5,0.0045
arrow(ax,0,0,2.6,0,lw=1.0); arrow(ax,0,0,0,2.2,lw=1.0); label(ax,2.65,0,"V",fs=10,ha="left"); label(ax,0,2.32,"p",fs=10)
P=[(0.2,100),(0.2,400),(0.6,100)]; Q=[(v*sx,p*sy) for v,p in P]
offs=[(-0.12,-0.12),(-0.12,0.12),(0.12,0.12)]
for i in range(3):
    a,b=Q[i],Q[(i+1)%3]; ax.plot([a[0],b[0]],[a[1],b[1]],color=K,lw=1.5)
    m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2]); d=np.array(b)-np.array(a); d=d/np.hypot(*d)*0.06
    arrow(ax,*(m-d),*(m+d),lw=1.2); pt(ax,*a,str(i+1),*offs[i])
ax.plot([0,0.2*sx],[400*sy,400*sy],color=K,lw=0.5,ls=":"); ax.plot([0.2*sx,0.2*sx],[0,100*sy],color=K,lw=0.5,ls=":"); ax.plot([0.6*sx,0.6*sx],[0,100*sy],color=K,lw=0.5,ls=":")
ax.plot([0,0.2*sx],[100*sy,100*sy],color=K,lw=0.5,ls=":")
label(ax,-0.05,100*sy,"100",fs=7.5,ha="right"); label(ax,-0.05,400*sy,"400",fs=7.5,ha="right")
label(ax,0.2*sx,-0.12,"0.2",fs=7.5); label(ax,0.6*sx,-0.12,"0.6",fs=7.5)
label(ax,-0.42,1.0,"p (kPa)",fs=7.5,rotation=90); label(ax,1.4,-0.3,"V (m³)",fs=7.5)
fin(fig,ax,-0.6,2.85,-0.42,2.4,"d37p_q11.png")
