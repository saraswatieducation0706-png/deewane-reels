import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
OIL="#f3e3b5"

def plates(ax,L=3.0,h=0.9,moving=True,Ulab="U",profile=None,hlab="h",top_label=None,bot_label="fixed plate"):
    """lower fixed plate (hatched) at y=0, upper plate at y=h; profile(eta)->u/Umax in [0,1]"""
    ax.add_patch(Rectangle((0,0),L,h,fc=OIL,ec="none"))
    hatch_ground(ax,0,L,0,size=0.14)
    if moving:
        ax.add_patch(Rectangle((0.6,h),L-0.9,0.12,fc="#bbbbbb",ec=K,lw=1.2))
        arrow(ax,L-0.2,h+0.06,L+0.5,h+0.06,lw=1.4); label(ax,L+0.62,h+0.06,Ulab,fs=8,ha="left")
    else:
        hatch_ground(ax,0,L,h,down=False,size=0.14)
    if top_label: label(ax,1.0,h+0.32,top_label,fs=7.5)
    label(ax,L*0.25,-0.32,bot_label,fs=7.5)
    vdim(ax,-0.15,0,h,hlab,side="left",fs=8)
    if profile is not None:
        x0=1.6; eta=np.linspace(0,1,60); u=np.array([profile(e) for e in eta])*1.0
        ax.plot([x0,x0],[0,h],color=K,lw=0.8)
        ax.plot(x0+u,eta*h,color=K,lw=1.4)
        for e in (0.2,0.4,0.6,0.8):
            ue=profile(e)
            if ue>0.08: arrow(ax,x0,e*h,x0+ue,e*h,lw=0.8)

# P1: plate dragged over a thin oil film (linear Couette profile)
fig,ax=new(3.6,1.8)
plates(ax,profile=lambda e:e,hlab="0.4 mm",top_label="plate 0.5 m × 0.5 m",Ulab="0.6 m/s")
label(ax,3.05,0.22,"oil film",fs=7.5,ha="right")
fin(fig,ax,-0.9,4.2,-0.55,1.45,"d32p_q1.png")

# S2: parabolic profile between two fixed plates
fig,ax=new(3.6,1.8)
plates(ax,moving=False,profile=lambda e:4*e*(1-e),hlab="10 mm",bot_label="")
label(ax,2.95,-0.32,"two fixed plates;  u$_{max}$ = 0.6 m/s at the centre",fs=7.5,ha="right")
label(ax,2.4,1.12,"τ$_w$ = (−dp/dx)·h/2",fs=7.5)
fin(fig,ax,-0.9,3.4,-0.55,1.35,"d32p_s2.png")

# P7: boundary layer growing on a flat plate
fig,ax=new(3.8,1.9)
ax.add_patch(Rectangle((0,-0.12),3.4,0.12,fc="#bbbbbb",ec=K,lw=1.2))
xs=np.linspace(0,3.4,80); d=0.42*np.sqrt(xs/3.4)*1.6
ax.plot(xs,d,color=K,lw=1.2,ls="--"); label(ax,3.2,d[-1]+0.14,"δ(x)",fs=8)
ax.plot(xs,d*0.344,color="#555555",lw=0.9,ls=":"); label(ax,3.62,d[-1]*0.344,"δ*",fs=7.5)
for y in (0.15,0.45,0.75,0.95):
    arrow(ax,-0.75,y,-0.25,y,lw=1.0)
label(ax,-0.5,1.12,"U",fs=8)
x0=2.4; dd=0.42*np.sqrt(x0/3.4)*1.6; eta=np.linspace(0,1,40)
prof=2*eta-eta**2
ax.plot([x0,x0],[0,1.0],color=K,lw=0.7)
ax.plot(x0+0.55*prof,eta*dd,color=K,lw=1.3); ax.plot([x0+0.55,x0+0.55],[dd,1.0],color=K,lw=1.3)
label(ax,1.0,-0.33,"leading edge at x = 0",fs=7.5)
fin(fig,ax,-0.9,4.0,-0.5,1.3,"d32p_q7.png")

# P15: upper plate moving + favourable pressure gradient
fig,ax=new(3.6,1.8)
plates(ax,profile=lambda e:(0.6*e+1.6*e*(1-e))/1.0,hlab="10 mm",Ulab="1.2 m/s",top_label="",bot_label="")
label(ax,3.0,-0.32,"dp/dx = −1500 Pa/m,  μ = 0.8 Pa·s",fs=7.5,ha="right")
fin(fig,ax,-0.9,4.2,-0.55,1.3,"d32p_q15.png")
