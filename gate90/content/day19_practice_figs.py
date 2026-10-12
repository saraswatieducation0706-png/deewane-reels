import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)
# Q3 Porter governor: arms and links 300 mm, radius 180 mm, h = 240 mm (scale 1 m = 5 units)
s=5.0; r,h=0.18*s,0.24*s
fig,ax=new(2.8,3.2)
ys=porter(ax,r,h)
label(ax,r+0.12,-h-0.32,"6 kg",fs=8,ha="left"); label(ax,0.42,ys,"30 kg",fs=8,ha="left")
label(ax,-r*0.5-0.15,-h*0.5+0.05,"300",fs=7.5,ha="right"); label(ax,-r*0.5-0.15,-1.5*h-0.05,"300",fs=7.5,ha="right")
hdim(ax,0,r-0.13,-h,"180",above=False,fs=7)
vdim(ax,1.55,-h,0,"h",side="right",fs=8); ext(ax,0.1,0,1.65,0); ext(ax,r+0.16,-h,1.65,-h)
omega(ax,0,0.3,0.25,"N",ccw=True,a0=200,a1=340,fs=8,lpos=(0.45,0.45))
label(ax,0,ys-0.85,"dimensions in mm; 180 = radius of rotation",fs=7)
fin(fig,ax,-1.7,2.0,ys-1.05,0.8,"d19p_q3.png")
# Q6 four masses in one plane
fig,ax=new(3.0,3.0)
polar_masses(ax,[(0,"A: 10 kg\n100 mm",0.67),(75,"B: 8 kg\n120 mm",0.8),(150,"C: 6 kg\n150 mm",1.0),(260,"D: 5 kg\n100 mm",0.67)])
angarc(ax,0,0,0.28,0,75,"75°",fs=7,lr=0.42); angarc(ax,0,0,0.5,75,150,"75°",fs=7,lr=0.64)
fin(fig,ax,-1.75,1.75,-1.45,1.6,"d19p_q6.png")
# Q8 shaft with two masses and two balancing planes (side view, lengths in m)
fig,ax=new(3.8,1.9)
shaft(ax,-0.3,4.3,0); 
for x,t in ((0,"L"),(4.0,"M")):
    ax.plot([x,x],[-0.9,0.9],color=K,lw=0.9,ls="--"); label(ax,x,1.05,t,fs=9,fontweight="bold")
for x,y,t in ((1.0,0.55,"A"),(2.5,0.65,"B")):
    ax.plot([x,x],[0,y],color=K,lw=1.4); ax.add_patch(Circle((x,y),0.11,fc="#999999",ec=K,zorder=5)); label(ax,x+0.22,y,t,fs=9,ha="left")
hdim(ax,0,1.0,-0.55,"0.2",above=False,fs=7.5); hdim(ax,0,2.5,-0.95,"0.5",above=False,fs=7.5); hdim(ax,0,4.0,-1.35,"0.8",above=False,fs=7.5)
label(ax,2.0,-1.95,"distances from plane L in m",fs=7); fin(fig,ax,-0.6,4.6,-2.15,1.25,"d19p_q8.png")
