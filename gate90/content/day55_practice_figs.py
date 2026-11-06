import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
SAND="#e6dcc3"

# Q9 cooling curves: P pure metal (thermal arrest), Q alloy (freezing range)
fig,axs=plt.subplots(1,2,figsize=(5.4,2.3))
t=np.linspace(0,10,400)
def liquid(t,T0,Ta,k): return Ta+(T0-Ta)*np.exp(-k*t)
ax=axs[0]                                                     # pure metal
Tf=0.6; t1=np.linspace(0,1.5,60); T1=Tf-0.03+(1.0-Tf+0.03)*(1-t1/1.5)**1.3   # liquid cooling with slight undercooling
tr=np.linspace(t1[-1],t1[-1]+0.25,10); Tr=Tf-0.03+0.03*np.sin(np.linspace(0,np.pi/2,10))   # undercooling recovery
tp=np.linspace(tr[-1],6.0,50); Tp=np.full_like(tp,Tf)          # thermal arrest
ts=np.linspace(6.0,10,80); Ts=0.1+(Tf-0.1)*np.exp(-0.6*(ts-6.0))
ax.plot(np.r_[t1,tr,tp,ts],np.r_[T1,Tr,Tp,Ts],color=K,lw=1.5)
ax.plot([0,10],[Tf,Tf],color=K,lw=0.5,ls=":"); ax.text(10,Tf+0.03,"freezing point",fontsize=6.5,ha="right",va="bottom")
ax.set_title("P",fontsize=10,fontweight="bold")
ax=axs[1]                                                     # solid-solution alloy
TL,TS=0.7,0.45
ta=np.linspace(0,1.6,60); Ta=liquid(ta,1.0,0.4,0.0); Ta=1.0-(1.0-TL)*ta/1.6
tb=np.linspace(1.6,6.4,80); Tb=TL-(TL-TS)*(tb-1.6)/4.8
tc=np.linspace(6.4,10,60); Tc=0.1+(TS-0.1)*np.exp(-0.7*(tc-6.4))
ax.plot(np.r_[ta,tb,tc],np.r_[Ta,Tb,Tc],color=K,lw=1.5)
for T,lab in ((TL,"liquidus"),(TS,"solidus")):
    ax.plot([0,10],[T,T],color=K,lw=0.5,ls=":"); ax.text(10,T+0.03,lab,fontsize=6.5,ha="right",va="bottom")
ax.set_title("Q",fontsize=10,fontweight="bold")
for ax in axs:
    ax.set_xlim(0,10.2); ax.set_ylim(0,1.08); ax.set_xticks([]); ax.set_yticks([])
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_xlabel("Time",fontsize=8); ax.set_ylabel("Temperature",fontsize=8)
fig.tight_layout(); save(fig,F+"d55p_q9.png")

# Q14 plate cavity in the drag, metal head above the parting plane
fig,ax=new(4.2,2.6)
ax.add_patch(Rectangle((0,0),6,3.2,fc=SAND,ec="none"))
ax.add_patch(Rectangle((2.0,1.0),3.2,0.6,fc="#bcd2e8",ec=K,lw=1.2))            # plate cavity (filled with metal)
ax.add_patch(Rectangle((0.8,1.6),0.4,1.5,fc="#bcd2e8",ec=K,lw=1.1))             # sprue, metal up to 3.1
ax.add_patch(Rectangle((0.8,1.3),1.2,0.3,fc="#bcd2e8",ec=K,lw=1.1))             # runner/gate
ax.plot([0.81,1.19],[1.6,1.6],color="#bcd2e8",lw=2.4); ax.plot([2.0,2.0],[1.31,1.59],color="#bcd2e8",lw=2.4)
ax.plot([0.8,0.8],[3.1,3.2],color=K,lw=1.1); ax.plot([1.2,1.2],[3.1,3.2],color=K,lw=1.1)
ax.add_patch(Rectangle((0,0),6,3.2,fill=False,ec=K,lw=2.0))
for a,b in ((0,0.8),(1.2,2.0),(5.2,6)): ax.plot([a,b],[1.6,1.6],color=K,lw=2.0)
ax.plot([2.0,5.2],[1.6,1.6],color=K,lw=1.2)
ax.text(6.15,2.4,"cope",fontsize=8,ha="left",va="center"); ax.text(6.15,0.8,"drag",fontsize=8,ha="left",va="center")
ax.text(6.15,1.6,"parting plane",fontsize=7,ha="left",va="center")
for x in (2.6,3.6,4.6): arrow(ax,x,1.75,x,2.35,lw=1.1)
ax.text(3.6,2.62,"metallostatic force on cope",fontsize=7,ha="center")
ax.text(3.2,0.5,"plate 400 mm × 300 mm (plan)",fontsize=7,ha="center")
vdim(ax,-0.3,1.6,3.1,"150 mm",side="left",fs=7.5)
ax.plot([-0.45,0.8],[3.1,3.1],color=K,lw=0.5); ax.plot([-0.45,0],[1.6,1.6],color=K,lw=0.5)
ax.annotate("liquid level",xy=(1.0,3.1),xytext=(1.9,3.5),fontsize=7,ha="left",arrowprops=dict(arrowstyle="-",lw=0.6))
fin(fig,ax,-1.6,7.6,-0.15,3.75,"d55p_q14.png")
