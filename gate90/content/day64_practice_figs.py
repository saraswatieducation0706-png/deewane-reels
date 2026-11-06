"""Day 64 (Production Planning & Inventory) practice figures. Usage: python3 day64_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# S5 Gantt chart for Johnson sequence Q, S, R, P
J={"P":(6,3),"Q":(2,5),"R":(8,6),"S":(4,7)}; seq="QSRP"
fig,ax=new(4.8,1.8); ax.set_aspect("auto")
a=b=0; bars=[]
for j in seq:
    s1=a; a+=J[j][0]; s2=max(a,b); b=s2+J[j][1]; bars.append((j,s1,a,s2,b))
for j,s1,e1,s2,e2 in bars:
    ax.add_patch(Rectangle((s1,1.0),e1-s1,0.5,fc="#dddddd",ec=K,lw=1.0)); ax.text((s1+e1)/2,1.25,j,fontsize=8,ha="center",va="center")
    ax.add_patch(Rectangle((s2,0.2),e2-s2,0.5,fc="#dddddd",ec=K,lw=1.0)); ax.text((s2+e2)/2,0.45,j,fontsize=8,ha="center",va="center")
ax.add_patch(Rectangle((0,0.2),2,0.5,fc="white",ec=K,lw=0.8,hatch="///"))
ax.text(-0.4,1.25,"M1",fontsize=8,ha="right",va="center"); ax.text(-0.4,0.45,"M2",fontsize=8,ha="right",va="center")
ax.plot([0,24],[0,0],color=K,lw=0.8)
for t in [0,2,6,7,14,20,23]:
    ax.plot([t,t],[0,-0.08],color=K,lw=0.8); ax.text(t,-0.12,str(t),fontsize=7,ha="center",va="top")
ax.text(24,-0.12,"h",fontsize=7,ha="left",va="top")
ax.text(1,0.85,"idle",fontsize=7,ha="center",va="center")
ax.set_xlim(-2.5,25); ax.set_ylim(-0.45,1.6); save(fig,F+"d64p_s5.png")

# S7 EPQ inventory profile
fig,ax=new(4.4,2.2)
tp,T=0.35,1.4; Im=0.75
ax.annotate("",xy=(3.0,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.0))
ax.annotate("",xy=(0,1.1),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=K,lw=1.0))
ax.text(0.05,1.1,"inventory",fontsize=8,ha="left",va="top"); ax.text(3.0,-0.05,"time",fontsize=8,ha="right",va="top")
for k in range(2):
    t0=k*T; ax.plot([t0,t0+tp,t0+T],[0,Im,0],color=K,lw=1.5)
ax.plot([T+tp,3.25],[Im,Im],color=K,lw=0.5,ls="--")
vdim(ax,3.2,0,Im,"",side="right"); ax.text(3.27,Im/2,"I max = Q(1 − D/P)",fontsize=7.5,ha="left",va="center")
ax.text(0.16,0.13,"slope P − D",fontsize=7,ha="left",va="center")
ax.text(0.78,0.55,"slope −D",fontsize=7,ha="left",va="center")
ext(ax,tp,0,tp,-0.14); arrow(ax,0,-0.1,tp,-0.1,lw=0.8,both=True); ax.text(tp+0.04,-0.1,"Q/P",fontsize=7,ha="left",va="center")
ext(ax,T,0,T,-0.3); ext(ax,0,0,0,-0.3); hdim(ax,0,T,-0.28,"cycle Q/D",above=False,fs=7)
ax.set_xlim(-0.1,4.4); ax.set_ylim(-0.5,1.15); save(fig,F+"d64p_s7.png")

# Q11 product structure tree
fig,ax=new(3.0,1.9)
def node(x,y,t): ax.add_patch(Rectangle((x-0.32,y-0.17),0.64,0.34,fc="#eeeeee",ec=K,lw=1.2)); ax.text(x,y,t,fontsize=8.5,ha="center",va="center")
node(1.0,1.2,"X"); node(0.4,0.2,"Y (2)"); node(1.6,0.2,"Z (1)")
ax.plot([1.0,1.0],[1.03,0.7],color=K,lw=1.1); ax.plot([0.4,1.6],[0.7,0.7],color=K,lw=1.1)
ax.plot([0.4,0.4],[0.7,0.37],color=K,lw=1.1); ax.plot([1.6,1.6],[0.7,0.37],color=K,lw=1.1)
ax.text(1.42,1.2,"LT 1 week",fontsize=7,ha="left",va="center"); ax.text(0.4,-0.08,"LT 2 weeks",fontsize=7,ha="center",va="top")
ax.text(1.6,-0.08,"(not needed)",fontsize=7,ha="center",va="top",color="#555555")
ax.set_xlim(-0.1,2.2); ax.set_ylim(-0.3,1.45); save(fig,F+"d64p_q11.png")
