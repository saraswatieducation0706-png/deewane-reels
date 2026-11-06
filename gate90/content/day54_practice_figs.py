import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
WB=dict(fc="white",ec="none",pad=0.6)

# Q13 engineering stress-strain curve of mild steel (schematic, not to scale)
from scipy.interpolate import PchipInterpolator
fig,ax=plt.subplots(figsize=(4.2,2.8))
A=(0.08,250); B=(0.1,300); C=(0.15,252)
ax.plot([0,A[0]],[0,A[1]],color=K,lw=1.5)
ax.plot([A[0],0.092,B[0]],[A[1],285,B[1]],color=K,lw=1.5)                       # A to upper yield B
ax.plot([B[0],0.11,0.13,C[0],0.17,0.19,0.21,0.23],[B[1],254,266,C[1],266,256,265,262],color=K,lw=1.3)  # yield plateau
x=[0.23,0.33,0.48,0.62,0.78,0.88]; y=[262,350,405,420,390,340]
f=PchipInterpolator(x,y); xx=np.linspace(0.23,0.88,200); ax.plot(xx,f(xx),color=K,lw=1.5)
D=(0.62,420); E=(0.88,340)
for (p,t,dx,dy) in [(A,"A",-0.04,12),(B,"B",-0.01,32),(C,"C",0.0,-34),(D,"D",0,30),(E,"E",0.04,-10)]:
    ax.plot(*p,"o",color=K,ms=3.5,zorder=5); ax.text(p[0]+dx,p[1]+dy,t,fontsize=9,fontweight="bold",ha="center",va="center")
ax.set_xlim(0,1.0); ax.set_ylim(0,480); ax.set_xticks([]); ax.set_yticks([])
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.set_xlabel("Engineering strain (not to scale)",fontsize=8); ax.set_ylabel("Engineering stress",fontsize=8)
save(fig,F+"d54p_q13.png")
