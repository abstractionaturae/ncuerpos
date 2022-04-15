clear all

global x=[0,-400*10^9,150*10^9,206*10^9]
global y=[0,160*10^9,0,0]
global vx=[0,4000,0,0]
global vy=[-2000,0,30000,24000]
global m=[2*10^30,2*10^14,6*10^24,6*10^23]
global N=3000
global h=20000
global G=6.67*10^(-11)

function aceleracion = aceleracion(i,j,x,y)
  global m
  global G
  rij=(x(i)-x(j))^2+(y(i)-y(j))^2;
  ax=-G*m(i)*(x(j)-x(i))/rij^(3/2);
  ay=-G*m(i)*(y(j)-y(i))/rij^(3/2);
  aceleracion=[ax, ay]
endfunction

function Fuerza = Fuerza(k,x,y,vx,vy)
    akx=0
    aky=0
    vxk=vx(k)
    vyk=vy(k)
    for i=1:length(x)
        if i!=k
            aki=aceleracion(i,k,x,y)
            akx+=aki(1)
            aky+=aki(2)
        endif
    endfor

    Fuerza=[vxk, vyk, akx, aky]

endfunction

function sig_valor=sig_valor(x,y,vx,vy)
    global m
    global h
    for i=1:length(m)
      k1(i,:)=h*Fuerza(i,x,y,vx,vy)
      x1(i)=x(i)+k1(i,1)/2
      y1(i)=y(i)+k1(i,2)/2
      vx1(i)=vx(i)+k1(i,3)/2
      vy1(i)=vy(i)+k1(i,4)/2

      k2(i,:)=h*Fuerza(i,x1,y1,vx1,vy1)
      x2(i)=x(i)+k2(i,1)/2
      y2(i)=y(i)+k2(i,2)/2
      vx2(i)=vx(i)+k2(i,3)/2
      vy2(i)=vy(i)+k2(i,4)/2

      k3(i,:)=h*Fuerza(i,x2,y2,vx2,vy2)
      x3(i)=x(i)+k3(i,1)
      y3(i)=y(i)+k3(i,2)
      vx3(i)=vx(i)+k3(i,3)
      vy3(i)=vy(i)+k3(i,4)

      k4(i,:)=h*Fuerza(i,x3,y3,vx3,vy3)
      xf(i)=x(i)+(k1(i,1)+2*k2(i,1)+2*k3(i,1)+k4(i,1))/6
      yf(i)=y(i)+(k1(i,2)+2*k2(i,2)+2*k3(i,2)+k4(i,2))/6
      vxf(i)=vx(i)+(k1(i,3)+2*k2(i,3)+2*k3(i,3)+k4(i,3))/6
      vyf(i)=vy(i)+(k1(i,4)+2*k2(i,4)+2*k3(i,4)+k4(i,4))/6
    endfor

    sig_valor=[xf;yf;vxf;vyf]
endfunction

X=[x] ;Y=[y]; Vx=[vx]; Vy=[vy]
for t=1:N
    sig=sig_valor(X(t,:),Y(t,:),Vx(t,:),Vy(t,:))
    X(t+1,:)=sig(1,:)
    Y(t+1,:)=sig(2,:)
    Vx(t+1,:)=sig(3,:)
    Vy(t+1,:)=sig(4,:)
endfor

hold on;
for i=1:length(m)
  plot(X(:,i),Y(:,i));
endfor

grid on
ylabel('Y');
xlabel('X');
title('Trayectorias');
hold off;

pause()
