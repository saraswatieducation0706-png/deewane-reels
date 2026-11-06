"""Day 66 (Week 11 Revision) practice figures. Usage: python3 day66_practice_figs.py <outdir>"""
import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)

# Q1 short taper turned on a bar (side view)
fig,ax=new(4.0,2.2)
R,r,L,Ls=30,25,40,30
pts=[(-Ls,R),(0,R),(L,r),(L+25,r),(L+25,-r),(L,-r),(0,-R),(-Ls,-R)]
ax.add_patch(Polygon(pts,closed=True,fc="#eeeeee",ec=K,lw=1.3))
ax.plot([0,0],[-R,R],color=K,lw=0.8); ax.plot([L,L],[-r,r],color=K,lw=0.8)
ax.plot([-Ls-6,L+31],[0,0],color=K,lw=0.6,ls="-.")
# diameters
vdim(ax,-Ls-10,-R,R,"",side="left"); ext(ax,-Ls,R,-Ls-14,R); ext(ax,-Ls,-R,-Ls-14,-R)
ax.text(-Ls-14,0,"Ø60",fontsize=8,ha="right",va="center")
vdim(ax,L+33,-r,r,"",side="right"); ext(ax,L+25,r,L+37,r); ext(ax,L+25,-r,L+37,-r)
ax.text(L+37,0,"Ø50",fontsize=8,ha="left",va="center")
# taper length
ext(ax,0,R,0,R+12); ext(ax,L,r,L,R+12); hdim(ax,0,L,R+9,"40",above=True,fs=8)
ax.set_xlim(-Ls-30,L+52); ax.set_ylim(-R-8,R+22); save(fig,F+"d66p_q1.png")
