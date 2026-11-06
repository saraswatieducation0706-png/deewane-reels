import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
WB=dict(fc="white",ec="none",pad=0.6)

def fe_c(ax, fs=8, small=7):
    """Iron–cementite diagram on real axes: x = wt % C (0–6.67), y = °C."""
    L=lambda pts: ax.plot([p[0] for p in pts],[p[1] for p in pts],color=K,lw=1.3)
    L([(0,1538),(0.53,1493),(4.3,1147),(6.67,1250)])            # liquidus
    L([(0,1538),(0.09,1493)]); L([(0.09,1493),(0.53,1493)])     # delta solidus, peritectic line
    L([(0,1394),(0.09,1493)]); L([(0,1394),(0.17,1493)])        # delta / gamma boundaries
    L([(0.17,1493),(2.11,1147)]); L([(2.11,1147),(6.67,1147)])  # gamma solidus, eutectic line
    L([(0,912),(0.76,727)]); L([(0.76,727),(2.11,1147)])        # A3, Acm
    L([(0,912),(0.022,727)]); L([(0.022,727),(0.006,400)])      # alpha solvus
    L([(0.022,727),(6.67,727)])                                 # eutectoid line
    ax.plot([6.67,6.67],[400,1250],color=K,lw=1.6)
    ax.set_xlim(0,7.0); ax.set_ylim(400,1600)
    ax.set_xticks([0,0.76,2.11,4.3,6.67]); ax.set_xticklabels(["0","0.76","2.11","4.3","6.67"],fontsize=small)
    ax.set_yticks([400,727,912,1147,1493,1538]); ax.set_yticklabels(["400","727","912","1147","1493","1538"],fontsize=small)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.set_xlabel("Carbon (wt %)",fontsize=fs); ax.set_ylabel("Temperature (°C)",fontsize=fs)
    for x,y in ((0.76,727),(2.11,1147),(4.3,1147)): ax.plot([x,x],[400,y],color=K,lw=0.4,ls=":")
    T=lambda x,y,t,f=fs: ax.text(x,y,t,fontsize=f,ha="center",va="center")
    T(3.3,1430,"Liquid (L)"); T(1.25,1330,"γ + L"); T(5.55,1178,"L + Fe₃C",small)
    T(0.75,1030,"γ\n(austenite)"); T(3.6,950,"γ + Fe₃C"); T(3.6,560,"α + Fe₃C")
    ax.text(0.28,775,"α+γ",fontsize=6,ha="center",va="center")
    ax.annotate("α",xy=(0.008,600),xytext=(0.45,480),fontsize=small,ha="center",arrowprops=dict(arrowstyle="-",lw=0.6))
    ax.annotate("δ",xy=(0.04,1480),xytext=(0.9,1575),fontsize=small,ha="center",arrowprops=dict(arrowstyle="-",lw=0.6))
    ax.text(6.75,820,"Fe₃C",fontsize=small,ha="left",va="center",rotation=90)

# Q5 Fe-C diagram with the three invariant points
fig,ax=plt.subplots(figsize=(5.2,3.9))
fe_c(ax)
for (x,y,t,tx,ty) in [(0.17,1493,"A",0.95,1500),(4.3,1147,"B",4.3,1060),(0.76,727,"C",1.25,800)]:
    ax.plot(x,y,"o",color=K,ms=4.5,zorder=6)
    ax.annotate(t,xy=(x,y),xytext=(tx,ty),fontsize=9.5,fontweight="bold",ha="center",va="center",bbox=WB,zorder=7,
                arrowprops=dict(arrowstyle="-",lw=0.6) if t!="B" else None)
save(fig,F+"d53p_q5.png")

# Q11 TTT diagram of eutectoid steel with cooling paths
from scipy.interpolate import PchipInterpolator
fig,ax=plt.subplots(figsize=(5.0,3.6))
Ts=[220,250,300,350,400,450,500,540,600,650,700,715]
st=[2.9,2.6,2.1,1.6,1.1,0.6,0.15,0.0,0.15,0.6,1.6,2.6]
fi=[4.2,4.0,3.5,3.0,2.5,1.8,1.2,1.0,1.2,1.8,2.9,3.9]
TT=np.linspace(220,715,200)
ax.plot(PchipInterpolator(Ts,st)(TT),TT,color=K,lw=1.5); ax.plot(PchipInterpolator(Ts,fi)(TT),TT,color=K,lw=1.5,ls="--")
ax.plot([-1.5,5.2],[727,727],color=K,lw=0.6,ls=":"); ax.text(5.15,742,"A₁ = 727 °C",fontsize=7,ha="right")
ax.plot([-1.5,5.2],[220,220],color=K,lw=1.0); ax.text(5.15,232,"Mₛ",fontsize=8,ha="right")
t=np.logspace(-1.3,5.2,400)
for tau,lab,lx in [(0.3,"1",-0.75),(3.0,"2",0.75),(2000.0,"3",3.0)]:
    T=20+760*np.exp(-(t-0.05)/tau); ax.plot(np.log10(t),T,color="#555555",lw=1.1)
    i=np.argmin(abs(np.log10(t)-lx)); ax.text(lx,T[i],lab,fontsize=8.5,fontweight="bold",ha="center",va="center",bbox=WB)
ax.plot([-1.3,-0.9,4.0,4.4],[780,300,300,20],color="#555555",lw=1.1); ax.text(1.25,300,"4",fontsize=8.5,fontweight="bold",ha="center",va="center",bbox=WB)
ax.text(0.35,680,"Austenite",fontsize=7.5,ha="center"); ax.text(3.6,640,"Pearlite",fontsize=7.5,ha="center")
ax.text(4.6,420,"Bainite",fontsize=7.5,ha="center"); ax.text(1.6,110,"Martensite",fontsize=7.5,ha="center")
ax.text(-0.2,470,"start",fontsize=7,ha="right"); ax.text(1.95,470,"finish",fontsize=7,ha="left")
ax.set_xlim(-1.5,5.2); ax.set_ylim(0,820)
ax.set_xticks([-1,0,1,2,3,4,5]); ax.set_xticklabels(["0.1","1","10","10²","10³","10⁴","10⁵"],fontsize=7)
ax.set_yticks([0,200,400,600,800]); ax.tick_params(labelsize=7)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.set_xlabel("Time (s, log scale)",fontsize=8); ax.set_ylabel("Temperature (°C)",fontsize=8)
save(fig,F+"d53p_q11.png")
