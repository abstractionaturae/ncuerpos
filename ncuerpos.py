import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

def aceleracion(i,j,x,y):
    rij=(x[i]-x[j])**2+(y[i]-y[j])**2
    ax=-G*m[i]*(x[j]-x[i])/rij**(3/2)
    ay=-G*m[i]*(y[j]-y[i])/rij**(3/2)
    return ax,ay

def Fk(k,x,y,vx,vy):
    akx=0
    aky=0
    for i in range(len(x)):
        if i!=k:
            aki=aceleracion(i,k,x,y)
            akx+=aki[0]
            aky+=aki[1]
    return np.array([vx[k],vy[k],akx,aky])

def siguiente_valor(x,y,vx,vy):
    k1=[]
    for k in range(len(m)):
        k1.append(h*Fk(k,x,y,vx,vy))

    x1=tuple(x[i]+k1[i][0]/2 for i in range(len(m)))
    y1=tuple(y[i]+k1[i][1]/2 for i in range(len(m)))
    vx1=tuple(vx[i]+k1[i][2]/2 for i in range(len(m)))
    vy1=tuple(vy[i]+k1[i][3]/2 for i in range(len(m)))

    k2=[]
    for k in range(len(m)):
        k2.append(h*Fk(k,x1,y1,vx1,vy1))

    x2=tuple(x[i]+k2[i][0]/2 for i in range(len(m)))
    y2=tuple(y[i]+k2[i][1]/2 for i in range(len(m)))
    vx2=tuple(vx[i]+k2[i][2]/2 for i in range(len(m)))
    vy2=tuple(vy[i]+k2[i][3]/2 for i in range(len(m)))

    k3=[]
    for k in range(len(m)):
        k3.append(h*Fk(k,x2,y2,vx2,vy2))

    x3=tuple(x[i]+k3[i][0] for i in range(len(m)))
    y3=tuple(y[i]+k3[i][1] for i in range(len(m)))
    vx3=tuple(vx[i]+k3[i][2] for i in range(len(m)))
    vy3=tuple(vy[i]+k3[i][3] for i in range(len(m)))

    k4=[]
    for k in range(len(m)):
        k4.append(h*Fk(k,x3,y3,vx3,vy3))

    xf=tuple(x[i]+(k1[i][0]+2*k2[i][0]+2*k3[i][0]+k4[i][0])/6 for i in range(len(m)))
    yf=tuple(y[i]+(k1[i][1]+2*k2[i][1]+2*k3[i][1]+k4[i][1])/6 for i in range(len(m)))
    vxf=tuple(vx[i]+(k1[i][2]+2*k2[i][2]+2*k3[i][2]+k4[i][2])/6 for i in range(len(m)))
    vyf=tuple(vy[i]+(k1[i][3]+2*k2[i][3]+2*k3[i][3]+k4[i][3])/6 for i in range(len(m)))

    return xf,yf,vxf,vyf

try:
    tipo=str(sys.argv[1])
    if tipo!='r' and tipo!='nr':
        print('Tipo de movimiento incorrecto')
        quit()
except:
    print('Falta parametro tipo de movimiento (r o nr)')
    quit()
x=(0,-400*pow(10,9),150*pow(10,9),206*pow(10,9))
y=(0,160*pow(10,9),0,0)
vx=(0,4000,0,0)
vy=(-2000,0,30000,24000)

m=(2*pow(10,30),2*pow(10,14),6*pow(10,24),6*pow(10,23))
N=15000
h=20000
G=6.67*pow(10,-11)

X=[x]
Y=[y]
Vx=[vx]
Vy=[vy]

for t in range(N):
    sig=siguiente_valor(X[t],Y[t],Vx[t],Vy[t])
    X.append(sig[0])
    Y.append(sig[1])
    Vx.append(sig[2])
    Vy.append(sig[3])

X=np.array(X)
Y=np.array(Y)

fig=plt.figure()
ax=fig.gca()

def actualizar(i):
    ax.clear()
    for t in range(len(m)):
        if tipo=='nr':
            x=X[:,t]
            y=Y[:,t]
        else:
            x=X[:,t]-X[:,0]
            y=Y[:,t]-Y[:,0]
        if t==0:
            ax.plot(x[:i],y[:i],'-')
            ax.plot(x[i],y[i],'o',markersize=15,color='y',label='Estrella')
        elif t==1:
            ax.plot(x[:i],y[:i],'--')
            ax.plot(x[i],y[i],'*',markersize=10,color='c',label='Cometa')
        else:
            ax.plot(x[:i],y[:i],'-',label=f'Planeta {t-1}')
            ax.plot(x[i],y[i],'o',markersize=10,color='b')

    plt.xlim(-3*pow(10,11),3*pow(10,11))
    plt.ylim(-0.75*pow(10,12),0.25*pow(10,12))
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Grafica de trayectoria')
    plt.legend()
    plt.grid()
ani=animation.FuncAnimation(fig,actualizar,range(0,N,40))
plt.show()
