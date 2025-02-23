# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:11:53 2023

@author: Bobke
"""
import numpy as np
import matplotlib.pyplot as plt

def gravity(m, h):
    G = 6.674*10**(-11)
    M = 5.9722*10**(24)
    R0 = 6375140
    Fg = -G*m*M/((R0+h)**2)
    return(Fg)

def drag(rho, v, s, Cd):
    Fd = -.5*rho*v**2*s*Cd
    return Fd

def density(h):
    p0 = 101325     #Pa
    T0 = 288.15     #K
    g0 = 9.80665    #m/s/s
    L = 0.0065      #temperature lapse rate K/m
    R = 8.31446     #Universal Gas Constant
    M = 0.0289652   #kg/mol (molar mass of dry air)
    
    hs = 125        #Start height above sea level, m
    rho = ((p0*M)/(R*T0))*(1-L*(h+hs)/T0)**(((g0*M)/(R*L))-1)
    return rho
    
    

def terminate(h1, h0, dt):
    run = True
    hdot = (h1 - h0)/dt
    if hdot <= 0:
        run = False
    return run

def solver(tb, mdot, ms, Ft, s, Cd, dt):
    """Launch Parameters"""
    h0 = 0      #m
    v0 = 0      #m/s
    t  = 0      #s
    
    mf = mdot*tb #initial fuel mass
    m0 = mf+ms
    F0 = gravity(m0, h0) + drag(1.225, v0, s, Cd)
    a0 = F0 / m0
    print(gravity(m0, h0)/m0)
    
    #Arrays
    m = [m0]
    h = [h0]
    v = [v0]
    a = [a0]
    F = [F0]
    rho = [density(h[0])]
    time = [t]
    
    
    
    run = True
    count = 0
    rail = True
    while run:
        
        Fsum = gravity(m[count], h[count]) + drag(rho[count], v[count], s, Cd)
        if m[count] > ms:
            Fsum += Ft
            m1 = m[count] - mdot*dt
            
        else:
            m1 = m[count]
            
        m.append(m1)
        F.append(Fsum)
        
        a1 = Fsum/m[count]
        a.append(a1)
        
        v1 = v[count] + (a[count+1]+a[count])*dt*0.5
        v.append(v1)
        
        h1 = h[count] + (v[count+1]+v[count])*dt*0.5
        h.append(h1)
        
        rho1 = density(h[count])
        rho.append(rho1)
        
        t = t + dt
        time.append(t)
        #print("Time: ",t," Force: ",Fsum, " Mass: ", m1)
        if h[count] > 11.9 and rail:
            """Saves rail exit velocity"""    
            vrail = v[count]
            rail = False
            print("v: ", v[count], "h: ", h[count])
        
        #print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )
        run = terminate(h[count+1], h[count], dt)
        
        count = count + 1
    print("Time: ",t," Force: ",Fsum," Acc: ", a1," v: ", v1, " h: ", h1, " Mass: ", m1 )    
    return m,h,v,a,F,rho,time
        
"""Rocket Parameters"""
thrust = 1500   #N
mdot = 0.785    #kg/s
ms = 25         #kg
s = np.pi*(.075**2)
Cd = 0.75

burn_time = 10.5  #s 
dt = 0.002 #time step, s


#tb, mdot, ms, Ft, s, Cd, dt
m,h,v,a,F,rho,t = solver(burn_time, mdot, ms, thrust, s, Cd, dt)


plt.figure(1)
plt.clf()

plt.plot(t, v)

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Velocity [m/s]")
plt.savefig('Velocity_vs_time.png', dpi=300)

plt.figure(2)
plt.clf()

plt.plot(t, F)

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Force [N]")

plt.savefig('Force_vs_time.png', dpi=300)

plt.figure(3)
plt.clf()

plt.plot(t, h)

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Distance [m]")

plt.savefig('Distance_vs_time.png', dpi=300)

plt.figure(4)
plt.clf()

plt.plot(t, a)

plt.grid(1)
plt.xlabel("time [s]")
plt.ylabel("Acceleration [m/s^2]")

plt.savefig('Acceleration_vs_time.png', dpi=300)


plt.figure(5)
plt.clf()

plt.plot(h, rho)

plt.grid(1)
plt.xlabel("height [m]")
plt.ylabel("Atmospheric Density [kg/m^3]")

plt.savefig('Density_vs_height.png', dpi=300)


    




    
    
    