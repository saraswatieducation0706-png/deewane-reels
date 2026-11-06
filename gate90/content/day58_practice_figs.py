import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q2 power source V-I characteristic (OCV 75 V, SCC 600 A)
fig,ax=plt.subplots(figsize=(3.7,2.5))
I=np.linspace(0,600,50); ax.plot(I,75-0.125*I,color=K,lw=1.6)
ax.text(260,55,"V = 75 − 0.125 I",fontsize=7.5,ha="left")
ax.set_xlim(0,660); ax.set_ylim(0,85); ax.set_xticks([0,600]); ax.set_yticks([0,75])
ax.tick_params(labelsize=7.5); ax.set_xlabel("Current I (A)",fontsize=8); ax.set_ylabel("Voltage V (V)",fontsize=8)
for s in ("top","right"): ax.spines[s].set_visible(False)
save(fig,F+"d58p_q2.png")

# Q2 solution: arc power P = V I along the characteristic
fig,ax=plt.subplots(figsize=(3.7,2.4))
P=I*(75-0.125*I)/1000; ax.plot(I,P,color=K,lw=1.6)
ax.plot(300,11.25,"o",color=K,ms=4); ax.plot([300,300],[0,11.25],color=K,lw=0.6,ls=":"); ax.plot([0,300],[11.25,11.25],color=K,lw=0.6,ls=":")
ax.text(310,11.6,"maximum 11.25 kW at\nI = 300 A, V = 37.5 V",fontsize=7,ha="left",va="bottom")
ax.set_xlim(0,660); ax.set_ylim(0,14.5); ax.set_xticks([0,300,600]); ax.set_yticks([0,11.25]); ax.set_yticklabels(["0","11.25"])
ax.tick_params(labelsize=7.5); ax.set_xlabel("Current I (A)",fontsize=8); ax.set_ylabel("Arc power (kW)",fontsize=8)
for s in ("top","right"): ax.spines[s].set_visible(False)
save(fig,F+"d58p_s2.png")

# Q10 single-action compaction of a gear blank
fig,ax=new(3.4,2.6)
ax.add_patch(Rectangle((-1.8,-1.0),1.0,2.0,fc="#d0d0d0",ec=K,lw=1.1,hatch="////"))
ax.add_patch(Rectangle((0.8,-1.0),1.0,2.0,fc="#d0d0d0",ec=K,lw=1.1,hatch="////"))
ax.add_patch(Rectangle((-0.8,-0.35),1.6,0.7,fc="#999999",ec=K,lw=1.1))                 # powder / compact
ax.add_patch(Rectangle((-0.78,0.35),1.56,1.25,fc="white",ec=K,lw=1.2))                 # upper punch
ax.add_patch(Rectangle((-0.78,-1.6),1.56,1.25,fc="white",ec=K,lw=1.2))                 # lower punch
arrow(ax,0,2.35,0,1.65,lw=1.4); ax.text(0.12,2.05,"F",fontsize=9,style="italic",ha="left")
ax.text(0,1.0,"upper punch",fontsize=7,ha="center",va="center"); ax.text(0,-1.0,"lower punch",fontsize=7,ha="center",va="center")
ax.text(-1.3,1.15,"die",fontsize=7.5,ha="center",va="bottom"); ax.text(1.3,1.15,"die",fontsize=7.5,ha="center",va="bottom")
ax.annotate("powder",xy=(0.5,0.0),xytext=(2.3,0.0),fontsize=7.5,va="center",arrowprops=dict(arrowstyle="-",lw=0.6))
fin(fig,ax,-2.0,3.2,-1.75,2.45,"d58p_q10.png")
