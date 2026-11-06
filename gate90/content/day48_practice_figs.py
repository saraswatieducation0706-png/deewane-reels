import sys,os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","tooling"))
from figlib import *
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"
os.makedirs(F,exist_ok=True)
def fin(fig,ax,x0,x1,y0,y1,name): ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); save(fig,F+name)

# Q9 line graph of profits of X and Y
fig,ax=plt.subplots(figsize=(3.8,2.4))
yrs=[2020,2021,2022,2023,2024]; X=[40,48,54,60,72]; Y=[50,55,50,66,70]
ax.plot(yrs,X,"-o",color="#2C7BB6",ms=4,lw=1.6,label="Company X")
ax.plot(yrs,Y,"--s",color="#D7191F",ms=4,lw=1.6,label="Company Y")
for x,a,b in zip(yrs,X,Y):
    ax.text(x,a+(-6 if a<b else 3),str(a),ha="center",fontsize=7,color="#2C7BB6")
    ax.text(x,b+(3 if b>a else -6),str(b),ha="center",fontsize=7,color="#D7191F")
ax.set_xticks(yrs); ax.set_ylim(20,85); ax.tick_params(labelsize=7.5)
ax.set_ylabel("Profit (₹ crore)",fontsize=7.5); ax.legend(fontsize=7,frameon=False,loc="upper left")
ax.grid(axis="y",lw=0.4,alpha=0.5)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.savefig(F+"d48p_q9.png",dpi=150,bbox_inches="tight",facecolor="white"); plt.close(fig)

# S11 counter-flow temperature profiles
fig,ax=new(3.4,2.4)
arrow(ax,0,0,3.0,0,lw=1.0); arrow(ax,0,0,0,2.1,lw=1.0)
label(ax,3.05,0,"x",fs=9,ha="left"); label(ax,0,2.25,"T (°C)",fs=8)
sc=lambda T:(T-20)/80
xs=np.linspace(0.1,2.7,50); f=(xs-0.1)/2.6
Th=160-60*f; Tc=90-50*f
ax.plot(xs,sc(Th),color="#D7191F",lw=1.8); ax.plot(xs,sc(Tc),color="#2C7BB6",lw=1.8)
arrow(ax,1.3,sc(160-60*0.462)+0.12,1.6,sc(160-60*0.577)+0.12,lw=1.0,color="#D7191F")
arrow(ax,1.6,sc(90-50*0.577)-0.12,1.3,sc(90-50*0.462)-0.12,lw=1.0,color="#2C7BB6")
label(ax,0.12,sc(160)+0.12,"hot in 160",fs=7,ha="left",color="#D7191F"); label(ax,2.7,sc(100)+0.3,"hot out 100",fs=7,ha="right",color="#D7191F")
label(ax,0.15,sc(90)-0.3,"cold out 90",fs=7,ha="left",color="#2C7BB6"); label(ax,2.6,sc(40)-0.17,"cold in 40",fs=7,ha="right",color="#2C7BB6")
for xx,a,b,t in ((0.1,160,90,"ΔT₁ = 70"),(2.7,100,40,"ΔT₂ = 60")):
    arrow(ax,xx,sc(b),xx,sc(a),lw=0.8,both=True); label(ax,xx+(0.08 if xx<1 else -0.08),(sc(a)+sc(b))/2,t,fs=7,ha="left" if xx<1 else "right")
fin(fig,ax,-0.2,3.3,-0.25,2.4,"d48p_s11.png")
