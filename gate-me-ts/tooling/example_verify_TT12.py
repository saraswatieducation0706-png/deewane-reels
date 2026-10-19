import numpy as np, math
from scipy.integrate import cumulative_trapezoid as ct
pi=math.pi
def defl_ss(L,M_of_x,EI,n=200001):
    x=np.linspace(0,L,n); k=M_of_x(x)/EI
    th=ct(k,x,initial=0); y=ct(th,x,initial=0)
    C=-y[-1]/L; y=y+C*x   # y(0)=0,y(L)=0 ; sagging M -> y'' = -M/EI handled by sign below
    return x,-y
# Q1 cantilever UDL tip/mid
r=(1/8)/(17/384); assert abs(r-48/17)<1e-12; print("Q1",r)
# Q5 fixed-fixed UDL: wL^4/384EI
d=10*4**4/(384*2e4)*1000; print("Q5",d); assert 0.33<=d<=0.34
# Q8 5/8*8
print("Q8",5/8*8)
# Q9
print("Q9",(0.5+0.5/4))
# Q10
I=pi*20**4/64; P=pi**2*200000*I/((1000/math.sqrt(2))**2)/1000; print("Q10",P); assert 30.85<=P<=31.16
# Q14
d=(5*8/(3*5000)+2*16/(8*5000))*1000; print("Q14",d); assert 3.44<=d<=3.50
# Q16 theta=4 delta/L : M L^2/8EI=delta, theta=ML/2EI
print("Q16",4*6/4000*1000)
# Q17 overhang numeric: L=3,a=1,P=1,EI=1
L,a,P=3.0,1.0,1.0
x=np.linspace(0,L+a,400001); Rb=P*(L+a)/L; Ra=P-Rb
M=Ra*x+np.where(x>L,Rb*(x-L),0)  # sagging +
th=ct(M,x,initial=0); y=ct(th,x,initial=0); iL=np.searchsorted(x,L); C=-y[iL]/x[iL]; y=y+C*x
print("Q17",y[-1],"formula",P*a**2*(L+a)/3)
# Q18 & max: L=6,a=2,P=30,EI=4e4
L,a,P,EI=6.0,2.0,30.0,4e4; b=L-a; Ra=P*b/L
x,y=defl_ss(L,lambda x:Ra*x-np.where(x>a,P*(x-a),0),EI)
yl=np.interp(a,x,y)*1000; print("Q18 under load",yl, P*a*a*b*b/(3*EI*L)*1000, "max",y.max()*1000,"at",x[y.argmax()])
# Q19
print("Q19",15/9)
# Q20
dT=pi**2*(10**2/16)/(12e-6*1000**2); print("Q20",dT); assert 5.10<=dT<=5.18
# Q21 L-frame vertical tip defl: 4PL^3/3EI (energy)
ss=np.linspace(0,1,200001); dU=lambda P: np.trapezoid((P*ss)**2/2,ss)+np.trapezoid((P*1.0)**2/2*np.ones_like(ss),ss)
print("Q21",(dU(1+1e-6)-dU(1-1e-6))/2e-6, 4/3)
# Q22 propped cantilever central load fixed moment 3PL/16 numeric
L,P=1.0,1.0
# cantilever fixed at x=0, prop at x=L. tip defl from P at L/2: 5PL^3/48; prop R: RL^3/3 =5PL^3/48 -> R=5P/16
R=5/16; Mfix=P*L/2-R*L; print("Q22",R,Mfix,3/16)
# Q24
d=20000*1500/(2*200*200000*math.cos(math.radians(30))**2); print("Q24",d); assert 0.49<=d<=0.51
# Q25
print("Q25 weak",4*(1/6),"strong",2/3)
# Q26
Lc=pi*math.sqrt(200000/300)*12.5/1000; print("Q26",Lc); assert 1.00<=Lc<=1.03
# Q28
print("Q28",0.5*(1+math.sqrt(1+2*12/0.5)))
# Q29 SS UDL vs point same total W: U ratio numeric
L,EI,W=1.0,1.0,1.0
x=np.linspace(0,L,200001)
Mu=W/L*x*(L-x)/2; Mp=np.where(x<L/2,W*x/2,W*(L-x)/2)
print("Q29",np.trapezoid(Mu**2,x)/np.trapezoid(Mp**2,x))
# Q30 SS 5 m, UDL 12 kN/m on 0..3, EI 2e4 -> midspan deflection
L,EI=5.0,2e4; Ra=12*3*(L-1.5)/L
x,y=defl_ss(L,lambda x:Ra*x-12*np.minimum(x,3)*(x-np.minimum(x,3)/2),EI)
print("Q30 mid mm",np.interp(2.5,x,y)*1000,"max",y.max()*1000)
# Q31
print("Q31",(1/24)/(5/384))
# Q32 SS beam couple at left end: max deflection location
L,M0=1.0,1.0
x,y=defl_ss(L,lambda x:M0*(1-x/L),1.0); print("Q32 xmax",x[np.abs(y).argmax()], 1-1/math.sqrt(3))
# Q33
s=pi**2*200000/150**2; print("Q33",s,s/2.5)
# Q12 tip slope cantilever UDL on half near fixed: w(L/2)^3/6EI = wL^3/48
print("Q12",(0.5**3)/6, 1/48)
# Q6, Q27
print("Q27",1/24+1/16,5/48)
# Q4 ratio
print("Q4",(1/6)/(1/96))
