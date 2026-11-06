import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
WATER="#d6e8f7"; WOOD="#c8a272"
def point(ax,x,y,t,dx=0.12,fs=8):
    ax.add_patch(Circle((x,y),0.035,fc=K,zorder=7)); label(ax,x+dx,y,t,fs=fs,ha="left",zorder=7)

# P1 floating cylinder (axis vertical), with G, B and M
fig,ax=new(3.0,2.8)
D,H=1.2,1.5; h=0.6*H; wl=1.0
ax.add_patch(Rectangle((-1.5,0),3.0,wl,fc=WATER,ec="none",zorder=1))
ax.plot([-1.5,1.5],[wl,wl],color="#2a6fb0",lw=1.2,zorder=2)
ax.plot([-1.2,-0.95,-1.075,-1.2],[wl+0.11,wl+0.11,wl+0.01,wl+0.11],color="#2a6fb0",lw=1.0)
y0=wl-h
ax.add_patch(Rectangle((-D/2,y0),D,H,fc=WOOD,ec=K,lw=1.4,zorder=3))
ax.plot([0,0],[y0-0.1,y0+H+0.1],color=K,lw=0.6,ls="-.",zorder=4)
point(ax,0,y0+H/2,"G"); point(ax,0,y0+h/2,"B")
label(ax,1.05,0.45,"water",fs=8)
label(ax,-0.3,y0+H*0.82,"S = 0.6",fs=7.5,zorder=6)
hdim(ax,-D/2,D/2,y0+H+0.12,"D",above=True,fs=8.5)
vdim(ax,-D/2-0.22,y0,y0+H,"H",side="left",fs=8.5); ext(ax,-D/2,y0,-D/2-0.32,y0); ext(ax,-D/2,y0+H,-D/2-0.32,y0+H)
fin(fig,ax,-1.6,1.6,y0-0.25,y0+H+0.5,"d71p_q1.png")

# P3 radial outflow between two parallel discs (section)
fig,ax=new(4.0,2.2)
g=0.35; t=0.12; Rd=2.0; rp=0.25
for s in (1,-1):
    yb=s*g/2
    if s==1:
        ax.add_patch(Rectangle((-Rd,yb),Rd-rp,t,fc="#bbbbbb",ec=K,lw=1.2,zorder=3))
        ax.add_patch(Rectangle((rp,yb),Rd-rp,t,fc="#bbbbbb",ec=K,lw=1.2,zorder=3))
    else:
        ax.add_patch(Rectangle((-Rd,yb-t),2*Rd,t,fc="#bbbbbb",ec=K,lw=1.2,zorder=3))
# supply pipe through the upper disc
ax.add_patch(Rectangle((-rp,g/2),2*rp,0.9,fc=WATER,ec="none",zorder=2))
ax.plot([-rp,-rp],[g/2+t,g/2+0.9],color=K,lw=1.3); ax.plot([rp,rp],[g/2+t,g/2+0.9],color=K,lw=1.3)
ax.add_patch(Rectangle((-rp,g/2),2*rp,t,fc=WATER,ec="none",zorder=4))
ax.add_patch(Rectangle((-Rd,-g/2),2*Rd,g,fc=WATER,ec="none",zorder=1))
arrow(ax,0,g/2+0.85,0,g/2+0.25,lw=1.2); label(ax,0.35,g/2+0.7,"Q = 0.01 m³/s",fs=7.5,ha="left")
for s in (1,-1): arrow(ax,s*0.5,0,s*1.6,0,lw=1.0)
ax.plot([0,0],[-g/2-t-0.15,g/2+1.0],color=K,lw=0.6,ls="-.")
# radii
r1,r2=0.6,1.8
for r in (r1,r2): ext(ax,r,-g/2-t,r,-g/2-t-0.62)
arrow(ax,0,-g/2-t-0.3,r1,-g/2-t-0.3,lw=0.9,both=True); label(ax,r1/2,-g/2-t-0.42,"0.1 m",fs=7,va="top")
arrow(ax,0,-g/2-t-0.62,r2,-g/2-t-0.62,lw=0.9,both=True); label(ax,1.25,-g/2-t-0.74,"0.3 m",fs=7,va="top")
for r,t_ in ((r1,"1"),(r2,"2")):
    ax.plot([r,r],[-g/2,g/2+t+0.18],color=K,lw=0.7,ls="--",zorder=5); label(ax,r,g/2+t+0.3,t_,fs=8)
vdim(ax,-1.8,-g/2,g/2,"",side="left"); label(ax,-1.95,g/2+t+0.25,"gap 5 mm",fs=7,ha="left")
fin(fig,ax,-2.2,2.2,-1.25,g/2+1.15,"d71p_q3.png")

# P4 lawn sprinkler, plan view
fig,ax=new(3.4,2.4)
L=1.6
ax.plot([-L,L],[0,0],color=K,lw=3,solid_capstyle="butt",zorder=3)
ax.add_patch(Circle((0,0),0.14,fc="white",ec=K,lw=1.3,zorder=5)); ax.add_patch(Circle((0,0),0.03,fc=K,zorder=6))
for s in (1,-1):
    ax.plot([s*L,s*L],[0,-s*0.28],color=K,lw=3,solid_capstyle="butt",zorder=3)
    arrow(ax,s*L,-s*0.32,s*L,-s*1.0,lw=1.2); label(ax,s*L+s*0.12,-s*0.75,"jet",fs=7.5,ha="left" if s==1 else "right")
hdim(ax,0,L,0.25,"r = 0.2 m",above=True,fs=7.5)
label(ax,-0.75,0.4,"5 mm nozzles",fs=7)
fin(fig,ax,-2.1,2.1,-1.15,1.15,"d71p_q4.png")

# P13 cylinder inside a square duct (section)
fig,ax=new(2.6,2.4)
a=1.0
ax.add_patch(Rectangle((-a,-a),2*a,2*a,fc="white",ec=K,lw=2.0))
ax.add_patch(Circle((0,0),0.5,fc="#dddddd",ec=K,lw=1.4))
label(ax,0,0.22,"1",fs=9); label(ax,0.72,0.72,"2",fs=9)
hdim(ax,-a,a,-a-0.22,"2D",above=False,fs=8)
arrow(ax,-0.5,-0.05,0.5,-0.05,lw=0.9,both=True); label(ax,0,-0.24,"D",fs=8)
fin(fig,ax,-1.3,1.3,-1.6,1.25,"d71p_q13.png")

# S14 temperature profiles in the counter-flow exchanger
fig,ax=plt.subplots(figsize=(3.6,2.3))
x=np.linspace(0,1,100); NTU,Cr=1.5,0.25
# local solution of counter-flow: hot from x=0, cold from x=1
Th_in,Tc_in=140.0,20.0
Q=0.7350*1.5*120; Th_out=Th_in-Q/1.5; Tc_out=Tc_in+Q/6
k=NTU*(1-Cr)
dT0=Th_in-Tc_out
dT=dT0*np.exp(-k*x)
Th=Th_in-NTU*dT0*(1-np.exp(-k*x))/k
Tc=Th-dT
ax.plot(x,Th,color="#b03030",lw=1.8,label="oil (hot)"); ax.plot(x,Tc,color="#2a6fb0",lw=1.8,label="water (cold)")
ax.annotate("",xy=(0.55,Th[55]+0),xytext=(0.4,Th[40]),arrowprops=dict(arrowstyle="-|>",color="#b03030"))
ax.annotate("",xy=(0.4,Tc[40]),xytext=(0.55,Tc[55]),arrowprops=dict(arrowstyle="-|>",color="#2a6fb0"))
for xx,yy,t in [(0,140,"140"),(1,Th_out,f"{Th_out:.1f}"),(0,Tc_out,f"{Tc_out:.1f}"),(1,20,"20")]:
    ax.text(xx+(0.03 if xx==0 else -0.03),yy+(5 if xx==0 else 9),t,fontsize=7,ha="left" if xx==0 else "right")
ax.set_xlim(0,1); ax.set_ylim(0,160); ax.set_xlabel("position along exchanger",fontsize=8); ax.set_ylabel("T (°C)",fontsize=8)
ax.set_xticks([]); ax.tick_params(labelsize=7); ax.legend(fontsize=7,frameon=False,loc="upper right")
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(F+"d71p_s14.png",dpi=150,facecolor="white"); plt.close(fig)
