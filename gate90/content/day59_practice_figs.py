"""Day 59 (Machining Mechanics & Tool Life) practice figures. Usage: python3 day59_practice_figs.py <outdir>
The orthogonal-cutting sketch and the Merchant's circle are drawn from exact geometry: the chip thickness follows
from t, alpha and phi, and every right-angle vertex of the force diagram lies on the circle with R as diameter."""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
from matplotlib.patches import Polygon, Circle
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def U(deg): r=np.radians(deg); return np.array([np.cos(r),np.sin(r)])

def orth_cut(ax,t,alpha,phi,tlab="t",tclab="$t_c$",alab="α",plab=None,clear=7,show_tc=True,V=True,s=1.0):
    """Orthogonal cutting, tool moving relative to work; tool tip at origin, work moves to the right (V).
    Uncut thickness t (drawing units), rake angle alpha (deg, +ve), shear angle phi (deg).
    Chip thickness tc = t cos(phi-alpha)/sin(phi) follows from the geometry."""
    a=np.radians(alpha); f=np.radians(phi)
    ur=np.array([np.sin(a),np.cos(a)])          # up the rake face
    nr=np.array([-np.cos(a),np.sin(a)])         # rake-face normal, towards the chip
    S=np.array([-t/np.tan(f),t])                # top of shear plane
    tc=t*np.cos(f-a)/np.sin(f)
    W=4.2*t; H=-1.6*t
    # work
    ax.add_patch(Polygon([(-W,H),(1.9*t+1.3*t,H),(3.2*t,0),(0,0),tuple(S),(-W,t)],closed=True,fc="#e4e4e4",ec=K,lw=1.2))
    # chip (between the rake face and its parallel at distance tc)
    L=2.6*t
    chip=[(0,0),tuple(S),tuple(S+ur*(L-np.dot(S,ur))),tuple(ur*L)]
    ax.add_patch(Polygon(chip,closed=True,fc="#bdbdbd",ec=K,lw=1.2))
    # tool
    Ht=3.0*t; top=ur*(Ht/np.cos(a)); g=np.radians(clear)
    fl=np.array([np.cos(g),np.sin(g)])*2.2*t
    ax.add_patch(Polygon([(0,0),tuple(top),(fl[0]+0.6*t,top[1]),tuple(fl)],closed=True,fc="white",ec=K,lw=1.5,hatch="///"))
    ax.text(fl[0]*0.75+0.25*t,top[1]*0.62,"Tool",fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.5))
    ax.text(-W*0.55,H*0.55,"Work",fontsize=8,ha="center",va="center")
    ax.text(*(ur*2.25*t+nr*0.5*tc),"Chip",fontsize=8,ha="center",va="center",rotation=-alpha)
    # reference vertical and rake angle
    ax.plot([0,0],[0,Ht*1.25],color=K,lw=0.6,ls="--"); e=ur*Ht*1.25/np.cos(a); ax.plot([top[0],e[0]],[top[1],e[1]],color=K,lw=0.6,ls="--")
    r1=Ht*1.18; aa=np.linspace(90-alpha,90,20)
    ax.plot(r1*np.cos(np.radians(aa)),r1*np.sin(np.radians(aa)),color=K,lw=0.8)
    ax.text(0.05*t,r1+0.12*t,alab,fontsize=8,ha="left",va="bottom")
    # shear angle (between the line of the cut surface, extended back, and the shear plane)
    ax.plot([0,-1.5*t],[0,0],color=K,lw=0.6,ls="--")
    r2=1.15*t; aa=np.linspace(180-phi,180,20)
    ax.plot(r2*np.cos(np.radians(aa)),r2*np.sin(np.radians(aa)),color=K,lw=0.8)
    pm=U(180-phi/2)*(r2+0.28*t); ax.text(pm[0],pm[1]-0.02*t,plab or "φ",fontsize=8,ha="center",va="center")
    # t dimension
    xd=-W+0.35*t; ax.plot([xd-0.15*t,-1.5*t],[0,0],color=K,lw=0.5)
    arrow(ax,xd,0,xd,t,lw=0.8,both=True); ax.text(xd+0.12*t,t/2,tlab,fontsize=8,ha="left",va="center")
    # tc dimension across the chip, perpendicular to the rake face
    if show_tc:
        q=ur*(1.25*t); p2=q+nr*tc
        arrow(ax,*q,*p2,lw=0.8,both=True)
        lp=p2+nr*0.15*t+ur*0.0; ax.text(*(p2+nr*0.12*t),tclab,fontsize=8,ha="right",va="center",bbox=dict(fc="white",ec="none",pad=0.3))
    if V: arrow(ax,-W+0.6*t,H+0.35*t,-W+1.9*t,H+0.35*t,lw=1.1); ax.text(-W+1.25*t,H+0.5*t,"V",fontsize=8,ha="center",va="bottom")
    return tc

def merchant(ax,Fc,Ft,alpha,phi,lab=None,angles=("φ","α","β"),fs=8,vals=None,show_beta=True,where=None,lead=None,ang_pos=None):
    """Merchant's circle for the resultant R=(Fc,Ft) (Fc along V, Ft normal to the machined surface).
    Components: Fs along the shear plane (at phi below Fc), Fn normal to it; N normal to the rake face (at alpha below Fc), F along it.
    All right-angle vertices lie on the circle with R as diameter."""
    lab=lab or dict(Fc="$F_c$",Ft="$F_t$",R="$R$",Fs="$F_s$",Fn="$F_n$",F="$F$",N="$N$")
    R=np.array([Fc,Ft],float); Rm=np.hypot(*R); c=R/2
    ax.add_patch(Circle(tuple(c),Rm/2,fill=False,ec=K,lw=0.9,ls="-"))
    us=U(-phi); un=U(-alpha)
    A=np.array([Fc,0.]); B=us*np.dot(R,us); C=un*np.dot(R,un)
    def seg(p,q,lw=1.6,ls="-"): ax.plot([p[0],q[0]],[p[1],q[1]],color=K,lw=lw,ls=ls)
    O=np.zeros(2)
    seg(O,R,2.0); seg(O,A); seg(A,R); seg(O,B); seg(B,R); seg(O,C); seg(C,R)
    for P_ in (A,B,C): ax.plot(*P_,"o",color=K,ms=2.5)
    def mid(p,q,frac,off,key):
        m=p+(q-p)*frac; d=(q-p)/np.linalg.norm(q-p); n=np.array([-d[1],d[0]])
        ax.text(*(m+n*off*Rm),lab[key],fontsize=fs,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.3))
    P=dict(R=(0.5,0.06),Fc=(0.5,0.05),Ft=(0.5,-0.06),Fs=(0.5,-0.06),Fn=(0.16,0.06),N=(0.86,-0.05),F=(0.2,0.045))
    if where: P.update(where)
    ends=dict(R=(O,R),Fc=(O,A),Ft=(A,R),Fs=(O,B),Fn=(B,R),N=(O,C),F=(C,R))
    for kk,(p,q) in ends.items():
        if lead and kk in lead:      # label away from the lines, joined by a thin leader
            fr,(tx,ty)=lead[kk]; m=p+(q-p)*fr
            ax.plot([m[0],tx],[m[1],ty],color=K,lw=0.5); ax.text(tx,ty,lab[kk],fontsize=fs,ha="left" if tx>m[0] else "right",va="center")
        else: mid(p,q,*P[kk],kk)
    # angle arcs at O
    def arc(a0,a1,r,txt,lr,am):
        aa=np.radians(np.linspace(a0,a1,30)); ax.plot(r*np.cos(aa),r*np.sin(aa),color=K,lw=0.8)
        m=np.radians(am); ax.text(lr*np.cos(m),lr*np.sin(m),txt,fontsize=fs,ha="center",va="center")
    thR=np.degrees(np.arctan2(Ft,Fc))
    AP=dict(phi=(0.40,0.46,-(alpha+phi)/2-2),alpha=(0.24,0.30,-alpha/2),beta=(0.13,0.19,thR/2+1.5))
    if ang_pos: AP.update(ang_pos)
    arc(-phi,0,Rm*AP["phi"][0],angles[0],Rm*AP["phi"][1],AP["phi"][2])
    arc(-alpha,0,Rm*AP["alpha"][0],angles[1],Rm*AP["alpha"][1],AP["alpha"][2])
    if show_beta: arc(-alpha,thR,Rm*AP["beta"][0],angles[2],Rm*AP["beta"][1],AP["beta"][2])
    ax.plot(0,0,"o",color=K,ms=3)
    ax.set_xlim(-Rm*0.12,Rm*1.12); ax.set_ylim(c[1]-Rm*0.56,c[1]+Rm*0.56)
    return dict(A=A,B=B,C=C,Fs=np.dot(R,us),Fn=np.linalg.norm(R-B),N=np.dot(R,un),F=np.linalg.norm(R-C))

# Q2 orthogonal cutting: t = 0.20 mm, tc = 0.45 mm, alpha = 15 deg (drawn to scale)
t,tc,al=0.20,0.45,15.0; r=t/tc; ph=np.degrees(np.arctan(r*np.cos(np.radians(al))/(1-r*np.sin(np.radians(al)))))
fig,ax=new(3.9,2.9); tcd=orth_cut(ax,1.0,al,ph,tlab="t = 0.20 mm",tclab="$t_c$ = 0.45 mm",alab="\u03b1 = 15\u00b0",plab="\u03c6")
assert abs(tcd-tc/t)<1e-9
ax.set_xlim(-4.3,3.6); ax.set_ylim(-1.7,4.3); save(fig,F+"d59p_q2.png")

# Q5 solution: Merchant's circle to scale, Fc = 1500 N, Ft = 600 N, alpha = 8 deg, phi = 18.35 deg
Fc,Ft,al=1500.,600.,8.0; r=0.32; ph=np.degrees(np.arctan(r*np.cos(np.radians(al))/(1-r*np.sin(np.radians(al)))))
fig,ax=new(5.0,3.4)
v=merchant(ax,Fc,Ft,al,ph,fs=8,
   lead=dict(Fn=(0.35,(1950,250)),F=(0.6,(1950,560)),Ft=(0.75,(1950,800)),N=(0.97,(1650,-300))),
   where=dict(Fc=(0.52,0.035),Fs=(0.45,-0.05)),
   ang_pos=dict(alpha=(0.62,0.67,-4.0),phi=(0.42,0.47,-13.2),beta=(0.16,0.21,8.0)))
ax.text(2350,300,"$F_c$ = 1500 N\n$F_t$ = 600 N\nR = 1615.5 N\n$F_s$ = 1234.9 N\n$F_n$ = 1041.7 N\nF = 802.9 N\nN = 1401.9 N\n\u03c6 = 18.35\u00b0, \u03b1 = 8\u00b0\n\u03b2 = 29.80\u00b0",fontsize=8,va="center",ha="left",linespacing=1.5)
assert abs(v["Fs"]-1234.86)<0.1 and abs(v["N"]-1401.90)<0.1
ax.set_xlim(-200,3200); save(fig,F+"d59p_s5.png")
