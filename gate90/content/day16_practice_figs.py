import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

def slider_crank(ax,r,l,thd,s=0.35,bw=0.8,bh=0.5):
    """crank pivot O at origin (pin), slider B to the right on a guided line y = 0"""
    t=np.radians(thd); A=(r*np.cos(t),r*np.sin(t)); B=(A[0]+np.sqrt(l*l-A[1]**2),0)
    pin(ax,0,0,s)
    hatch_ground(ax,B[0]-1.3,B[0]+0.7,-bh/2,down=True,size=0.14)
    hatch_ground(ax,B[0]-bw/2,B[0]+0.7,bh/2,down=False,size=0.14)
    ax.add_patch(Rectangle((B[0]-bw/2,-bh/2),bw,bh,fc="#dddddd",ec=K,lw=1.3,zorder=3))
    member(ax,(0,0),A); member(ax,A,B); joint(ax,*A); joint(ax,*B)
    return A,B

def tmd(ax,areas,widths,scale=180,labels=None,pts=None):
    """turning-moment curve as sine lobes about a mean line at y = 1; returns crossing x positions"""
    x0=0; xs=[]; ys=[]; cross=[0]
    for i,(a,wd) in enumerate(zip(areas,widths)):
        x=np.linspace(x0,x0+wd,60); h=a/wd/scale
        y=1.0+h*np.sin(np.pi*(x-x0)/wd); xs+=list(x); ys+=list(y)
        ax.fill_between(x,1.0,y,color="#d6d6d6" if a>0 else "#f0f0f0",lw=0)
        t=labels[i] if labels else f"{'+' if a>0 else '−'}{abs(a)}"
        label(ax,x0+wd/2,1.0+(h*0.45 if abs(a)>=60 else h+np.sign(a)*0.2),t,fs=8)
        x0+=wd; cross.append(x0)
    ax.plot(xs,ys,color=K,lw=1.5); ax.axhline(1.0,color=K,lw=0.9,ls="--")
    if pts:
        for x,p in zip(cross,pts):
            ax.plot([x],[1.0],"o",ms=3.5,color=K); label(ax,x+(0.1 if p in "bd" else 0),0.8 if p not in "bd" else 1.2,p,fs=9,fontweight="bold",ha="left" if p in "bd" else "center")
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    return cross

# Q1 slider-crank: theta = 40 deg, r = 100 mm, l = 450 mm, bore 150 mm
fig,ax=new(3.8,2.0)
A,B=slider_crank(ax,1.0,4.5,40)
ax.plot([0,0.9],[0,0],color=K,lw=0.6,ls="--")
aa=np.radians(np.linspace(0,40,30)); ax.plot(0.45*np.cos(aa),0.45*np.sin(aa),color=K,lw=0.8)
label(ax,0.72,0.15,"40°",fs=8)
label(ax,-0.25,0.2,"O",fs=9); label(ax,A[0]-0.05,A[1]+0.22,"A",fs=9); label(ax,B[0]-0.2,0.48,"B",fs=9,va="bottom")
label(ax,0.15,0.85,"r = 100 mm",fs=7.5,ha="right")
label(ax,2.4,0.15,"l = 450 mm",fs=7.5)
arrow(ax,B[0]+1.5,0,B[0]+0.42,0); label(ax,B[0]+1.05,0.2,"p = 1.5 MPa\nbore 150 mm",fs=7,va="bottom",ha="left")
fin(fig,ax,-0.9,B[0]+2.5,-0.7,1.2,"d16p_q1.png")

# S1 force diagram: forces on the piston (B) and on the crank pin (A)
fig,ax=new(3.8,2.6)
A,B=slider_crank(ax,1.0,4.5,40)
u=np.array(B)-np.array(A); u=u/np.linalg.norm(u)           # unit vector A -> B
arrow(ax,B[0]+1.5,0,B[0]+0.42,0); label(ax,B[0]+1.0,0.2,"$F_P$",fs=9,va="bottom")
arrow(ax,B[0],-1.05,B[0],-0.27); label(ax,B[0]-0.12,-0.85,"$F_N$",fs=9,ha="right")
tA=np.radians(40); rad=np.array([np.cos(tA),np.sin(tA)]); tan_=np.array([-np.sin(tA),np.cos(tA)])
p=np.array(A); q1=p-1.1*u; arrow(ax,*p,*q1); label(ax,q1[0]-0.1,q1[1]+0.05,"$F_Q$",fs=9,ha="right")
arrow(ax,*(p+0.08*tan_),*(p+0.9*tan_)); label(ax,*(p+1.05*tan_),"$F_T$",fs=9)
off=0.32*np.array([np.sin(tA),-np.cos(tA)]); arrow(ax,*(p+off),*(p+off-0.7*rad)); label(ax,*(p+off-0.35*rad+np.array([0.25,-0.1])),"$F_R$",fs=9,ha="left")
label(ax,-0.25,0.2,"O",fs=9); label(ax,A[0]+0.05,A[1]+0.25,"A",fs=9); label(ax,B[0]-0.6,0.4,"B",fs=9)
label(ax,2.6,0.95,"β = 8.21°",fs=8)
fin(fig,ax,-1.5,B[0]+2.0,-1.2,2.1,"d16p_s1.png")

# Q6 parallel linkage lifting a platform
fig,ax=new(3.4,2.4); r=1.6; t=np.radians(30); d=2.2
O2=(0,0); O4=(d,0); A=(r*np.cos(t),r*np.sin(t)); B=(d+A[0],A[1])
pin(ax,*O2,0.35); pin(ax,*O4,0.35)
member(ax,O2,A); member(ax,O4,B)
ax.add_patch(Rectangle((A[0]-0.15,A[1]),d+0.3,0.18,fc="#dddddd",ec=K,lw=1.3,zorder=2))
joint(ax,*A); joint(ax,*B)
cx=A[0]+d/2+0.3; arrow(ax,cx,A[1]+0.95,cx,A[1]+0.2); label(ax,cx+0.1,A[1]+0.8,"W = 600 N",fs=7.5,ha="left")
ax.plot([0,0.9],[0,0],color=K,lw=0.6,ls="--"); aa=np.radians(np.linspace(0,30,20)); ax.plot(0.5*np.cos(aa),0.5*np.sin(aa),color=K,lw=0.8)
label(ax,0.72,0.14,"30°",fs=7.5)
label(ax,-0.3,0.05,"O₂",fs=9); label(ax,d+0.35,-0.05,"O₄",fs=9); label(ax,A[0]-0.25,A[1]+0.1,"A",fs=9); label(ax,B[0]+0.3,B[1]+0.1,"B",fs=9)
label(ax,0.45,0.6,"O₂A = O₄B = 0.4 m",fs=7.5,ha="right")
label(ax,A[0]+0.55,A[1]+0.35,"platform AB",fs=7.5)
fin(fig,ax,-1.9,B[0]+0.8,-0.5,A[1]+1.1,"d16p_q6.png")

# Q9 TMD with crossing points a..e
fig,ax=plt.subplots(figsize=(4.0,1.9))
c=tmd(ax,[40,-70,60,-30],[0.7,1.0,0.9,0.6],scale=60,pts="abcde")
ax.text(c[-1]+0.1,1.05,"mean torque",fontsize=7,va="bottom",ha="left")
ax.set_xlim(-0.1,c[-1]+0.9); ax.set_ylim(-0.4,2.8); ax.set_xlabel("crank angle θ (one cycle)",fontsize=8); ax.set_ylabel("T",fontsize=8)
ax.text(c[-1]+0.85,2.75,"areas in mm²",fontsize=7,va="top",ha="right",style="italic")
fig.tight_layout(); fig.savefig(F+"d16p_q9.png",dpi=150,facecolor="white"); plt.close(fig)

# Q10 TMD areas and S10 energy curve
ar=[30,-55,70,-40,25,-30]; wd=[0.55,0.8,0.9,0.65,0.5,0.6]
fig,ax=plt.subplots(figsize=(4.2,1.9))
c=tmd(ax,ar,wd,scale=60)
ax.text(c[-1]+0.05,1.05,"mean torque",fontsize=7,va="bottom",ha="left")
ax.set_xlim(0,c[-1]+0.8); ax.set_ylim(-0.4,2.6); ax.set_xlabel("crank angle θ (one cycle)",fontsize=8); ax.set_ylabel("T",fontsize=8)
ax.text(0.02,2.55,"loop areas in mm² (not to scale)",fontsize=7,va="top",style="italic")
fig.tight_layout(); fig.savefig(F+"d16p_q10.png",dpi=150,facecolor="white"); plt.close(fig)

fig,(a1,a2)=plt.subplots(2,1,figsize=(4.2,3.2),sharex=True,gridspec_kw={"height_ratios":[1,1]})
c=tmd(a1,ar,wd,scale=60); a1.set_ylim(-0.4,2.6); a1.set_ylabel("T",fontsize=8)
E=[0]+list(np.cumsum(ar))
a2.plot(c,E,"-o",color=K,lw=1.3,ms=3.5); a2.axhline(0,color=K,lw=0.6,ls=":")
for x,e in zip(c,E): a2.text(x,e+(6 if e>=0 else -6),f"{e:+d}" if e else "0",fontsize=7,ha="center",va="bottom" if e>=0 else "top")
i1,i0=int(np.argmax(E)),int(np.argmin(E)); xd=c[-1]+0.45
a2.annotate("",xy=(xd,E[i1]),xytext=(xd,E[i0]),arrowprops=dict(arrowstyle="<|-|>",color=K,lw=0.9))
a2.plot([c[i0],xd+0.1],[E[i0],E[i0]],color=K,lw=0.5,ls="--"); a2.plot([c[i1],xd+0.1],[E[i1],E[i1]],color=K,lw=0.5,ls="--")
a2.text(xd+0.08,(E[i1]+E[i0])/2,"ΔE =\n70 mm²",fontsize=7.5,ha="left",va="center")
a2.set_ylim(-45,65); a2.set_yticks([]); a2.set_ylabel("energy (mm²)",fontsize=8)
for s in ("top","right"): a2.spines[s].set_visible(False)
a2.set_xticks([]); a2.set_xlim(0,c[-1]+1.2); a2.set_xlabel("crank angle θ",fontsize=8)
fig.tight_layout(); fig.savefig(F+"d16p_s10.png",dpi=150,facecolor="white"); plt.close(fig)

# S11 T = 2000 + 800 sin 3θ over one period, shaded excess loop
fig,ax=plt.subplots(figsize=(3.8,2.1))
th=np.linspace(0,120,300); T=2000+800*np.sin(np.radians(3*th))
ax.plot(th,T,color=K,lw=1.5); ax.plot([0,120],[2000,2000],color=K,lw=0.9,ls="--")
m=th<=60; ax.fill_between(th[m],2000,T[m],color="#d6d6d6")
ax.text(30,2300,"ΔE = 533.3 J",fontsize=7.5,ha="center")
ax.text(123,2000,"mean\n2000",fontsize=7,va="center",ha="left")
ax.set_xticks([0,30,60,90,120]); ax.tick_params(labelsize=7); ax.set_yticks([1200,2000,2800])
ax.set_xlabel("crank angle θ (degrees)",fontsize=8); ax.set_ylabel("T (N·m)",fontsize=8); ax.set_xlim(0,150); ax.set_ylim(1100,2950)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(F+"d16p_s11.png",dpi=150,facecolor="white"); plt.close(fig)
print("ok")
