"""Day 63 (Probability & Statistics) practice figures. Usage: python3 day63_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# S5 normal curve, mean 10, sd 2, area between 8 and 12 shaded
fig,ax=new(3.8,2.2); ax.set_aspect("auto")
mu,sd=10,2
x=np.linspace(3,17,400); f=np.exp(-((x-mu)/sd)**2/2)/(sd*np.sqrt(2*np.pi))
ax.plot(x,f,color=K,lw=1.5); ax.plot([3,17],[0,0],color=K,lw=1.0)
m=(x>=8)&(x<=12); ax.fill_between(x[m],0,f[m],color="#bbbbbb")
for v,t in [(8,"8\n(z = −1)"),(10,"10"),(12,"12\n(z = +1)")]:
    ax.plot([v,v],[0,-0.006],color=K,lw=1.0); ax.text(v,-0.01,t,fontsize=7.5,ha="center",va="top")
ax.plot([10,10],[0,f.max()],color=K,lw=0.6,ls="--")
ax.text(10,0.07,"0.6826",fontsize=8,ha="center",va="center",bbox=dict(fc="#bbbbbb",ec="none",pad=1))
ax.text(14.6,0.12,"σ = 2",fontsize=8,ha="center")
ax.set_xlim(3,17); ax.set_ylim(-0.05,0.215); save(fig,F+"d63p_s5.png")
