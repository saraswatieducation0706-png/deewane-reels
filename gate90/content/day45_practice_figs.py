import sys,os
# shared DI chart helpers for Day 45 (exam-style: every value printed, grayscale-safe)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
RED="#D7191F"; DARK="#333333"; MID="#9a9a9a"; LIGHT="#d9d9d9"
plt.rcParams.update({"font.size":8,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#555","axes.linewidth":0.8})
def save(fig,path): fig.savefig(path,dpi=150,bbox_inches="tight",facecolor="white"); plt.close(fig)
def bars(path,cats,vals,title,ylab,w=3.6,h=2.3,color=MID):
    fig,ax=plt.subplots(figsize=(w,h)); b=ax.bar(cats,vals,width=0.55,color=color,edgecolor="#222",lw=0.8)
    for r,v in zip(b,vals): ax.text(r.get_x()+r.get_width()/2,v+max(vals)*0.02,f"{v:g}",ha="center",va="bottom",fontsize=7.5)
    ax.set_ylim(0,max(vals)*1.18); ax.set_ylabel(ylab,fontsize=7.5); ax.set_title(title,fontsize=8,pad=6)
    ax.yaxis.grid(True,color="#e5e5e5",lw=0.6); ax.set_axisbelow(True); ax.tick_params(labelsize=7.5); save(fig,path)
def bars2(path,cats,a,b,la,lb,title,ylab,w=3.9,h=2.4):
    fig,ax=plt.subplots(figsize=(w,h)); x=np.arange(len(cats)); wd=0.36
    r1=ax.bar(x-wd/2-0.01,a,wd,color=DARK,edgecolor="#222",lw=0.8,label=la)
    r2=ax.bar(x+wd/2+0.01,b,wd,color="white",edgecolor="#222",lw=0.8,hatch="////",label=lb)
    for rs,vs in ((r1,a),(r2,b)):
        for r,v in zip(rs,vs): ax.text(r.get_x()+r.get_width()/2,v+1,f"{v:g}",ha="center",va="bottom",fontsize=7)
    ax.set_xticks(x,cats); ax.set_ylim(0,max(a+b)*1.22); ax.set_ylabel(ylab,fontsize=7.5); ax.set_title(title,fontsize=8,pad=6)
    ax.legend(fontsize=7,frameon=False,ncol=2,loc="upper left"); ax.yaxis.grid(True,color="#e5e5e5",lw=0.6); ax.set_axisbelow(True)
    ax.tick_params(labelsize=7.5); save(fig,path)
def pie(path,labels,vals,title,fmt,w=3.4,h=2.6):
    fig,ax=plt.subplots(figsize=(w,h)); greys=["#444444","#8a8a8a","#c4c4c4","#ffffff","#e2e2e2","#a8a8a8"]
    hat=["","","","....","",""]
    wd,_=ax.pie(vals,colors=greys[:len(vals)],startangle=90,counterclock=False,wedgeprops=dict(edgecolor="#222",lw=0.8))
    for wdg,hh in zip(wd,hat): wdg.set_hatch(hh)
    for wdg,l,v in zip(wd,labels,vals):
        a=np.deg2rad((wdg.theta1+wdg.theta2)/2); x,y=np.cos(a),np.sin(a)
        ax.plot([0.85*x,1.08*x],[0.85*y,1.08*y],color="#222",lw=0.6)
        ax.text(1.14*x,1.14*y,f"{l}\n{fmt(v)}",ha="left" if x>0 else "right",va="center",fontsize=7.5)
    ax.set_aspect("equal"); ax.set_title(title,fontsize=8,pad=10); save(fig,path)
def lines(path,cats,series,title,ylab,w=3.8,h=2.4,offs=None):
    fig,ax=plt.subplots(figsize=(w,h)); sty=[("-","o",DARK),("--","s","#777777")]
    for k,(lab,v) in enumerate(series):
        ls,mk,c=sty[k]; ax.plot(cats,v,ls=ls,marker=mk,color=c,lw=1.6,ms=4.5,label=lab)
        for i,(xx,yy) in enumerate(zip(cats,v)):
            dy=(offs[k][i] if offs else 7)
            ax.annotate(f"{yy:g}",(xx,yy),textcoords="offset points",xytext=(0,dy),ha="center",va="center",fontsize=7)
    allv=[x for _,v in series for x in v]; ax.set_ylim(min(allv)*0.75,max(allv)*1.15)
    ax.set_ylabel(ylab,fontsize=7.5); ax.set_title(title,fontsize=8,pad=6)
    if len(series)>1: ax.legend(fontsize=7,frameon=False,loc="upper left")
    ax.yaxis.grid(True,color="#e5e5e5",lw=0.6); ax.set_axisbelow(True); ax.tick_params(labelsize=7.5); save(fig,path)
def table(path,header,rows,title,w=3.6,colw=None):
    h=0.28*(len(rows)+1)+0.35
    fig,ax=plt.subplots(figsize=(w,h)); ax.axis("off")
    t=ax.table(cellText=[[str(c) for c in r] for r in rows],colLabels=header,loc="center",cellLoc="center",colWidths=colw)
    t.auto_set_font_size(False); t.set_fontsize(7.5); t.scale(1,1.35)
    for (r,c),cell in t.get_celld().items():
        cell.set_edgecolor("#444"); cell.set_linewidth(0.6)
        if r==0: cell.set_facecolor("#dddddd"); cell.set_text_props(weight="bold")
    ax.set_title(title,fontsize=8,pad=2); save(fig,path)
F=(sys.argv[1] if len(sys.argv)>1 else "fig")+"/"; os.makedirs(F,exist_ok=True)
# P7 profit bar chart
bars(F+"d45p_q7.png",["2020","2021","2022","2023","2024"],[40,52,46,60,75],"Profit of a company","₹ lakh")
# P8 family budget pie (central angles)
pie(F+"d45p_q8.png",["Food","Rent","Education","Transport","Savings"],[108,90,54,36,72],"Monthly budget of a family (total ₹60,000)",lambda v:f"{v:g}°")
# P9 two plants line chart
lines(F+"d45p_q9.png",["2019","2020","2021","2022","2023","2024"],[("Plant A",[30,35,40,38,45,50]),("Plant B",[25,32,34,42,40,44])],"Output of two plants","thousand tonnes",offs=[[8,8,8,-9,8,8],[-9,-9,-9,8,-9,-9]])
# P10 marks table
table(F+"d45p_q10.png",["Student","Maths","Physics","Chemistry"],[["Asha",72,85,64],["Bala",58,90,77],["Chetan",81,66,70],["Divya",95,74,88],["Esha",64,79,92]],"Marks (out of 100) of five students",w=3.2)
