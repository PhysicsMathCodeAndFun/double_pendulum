import pygame
import sys
import random
import math

# IMPORTANT
# To learn more about how the solution is derived see: https://www.jousefmurad.com/engineering/double-pendulum-1/


pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()


delta_time = 0.0
dt = 0.01

# constants
l1, l2 = 150.0, 150.0
m1 = m2 = 10.0
g = 9.8
# ---

# variables
t = 0
th1 = [math.pi * (170.0 / 180.0), math.pi * (170.1 / 180.0), math.pi * (170.2 / 180.0)]
th2 = [math.pi * (160.0 / 180.0), math.pi * (160.1 / 180.0), math.pi * (160.2 / 180.0)]

omg1, omg2, alp1, alp2  = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
# ---

points1 = []
points2 = []
points3 = []

def dtheta1_dt(omega1):
    return omega1
def dtheta2_dt(omega2):
    return omega2
def domega1_dt(theta1, theta2, omega1, omega2, alpha2):
    global l1
    global l2
    global m1
    global m2
    
    return (-((l2 * m2) / (l1 * (m1 + m2))) * alpha2 * math.cos(theta2 - theta1) +
        ((l2 * m2) / (l1 * (m1 + m2))) * (omega2**2) * math.sin(theta2 - theta1) - 
        (g / l1) * math.sin(theta1))
def domega2_dt(theta1, theta2, omega1, omega2, alpha1):
    global l1
    global l2
    global m1
    global m2
    
    return (-(l1 / l2) * alpha1 * math.cos(theta2 - theta1) - (l1 / l2) * (omega1**2) * math.sin(theta2 - theta1) -
    (g / l2) * math.sin(theta2))
    



def Update(screen):
    global delta_time
    global dt
    global t
    global th1, th2, omg1, omg2, alp1, alp2
    global h,w
    
    
    # Runge
    h2 = 0.5 * dt

    for k in range(3):
        k11 = dtheta1_dt(omg1[k])
        k21 = dtheta2_dt(omg2[k])
        k31 = domega1_dt(th1[k], th2[k], omg1[k], omg2[k], alp2[k])
        k41 = domega2_dt(th1[k], th2[k], omg1[k], omg2[k], alp1[k])
    
        k12 = dtheta1_dt(omg1[k] + h2 * k31)
        k22 = dtheta2_dt(omg2[k] + h2 * k41)
        k32 = domega1_dt(th1[k] + h2 * k11, th2[k] + h2 * k21 , omg1[k] + h2 * k31, omg2[k] + h2 * k41, alp2[k])  
        k42 = domega2_dt(th1[k] + h2 * k11, th2[k] + h2 * k21 , omg1[k] + h2 * k31, omg2[k] + h2 * k41, alp1[k])
    
        k13 = dtheta1_dt(omg1[k] + h2 * k32)
        k23 = dtheta2_dt(omg2[k] + h2 * k42)
        k33 = domega1_dt(th1[k] + h2 * k12, th2[k] + h2 * k22 , omg1[k] + h2 * k32, omg2[k] + h2 * k42, alp2[k])  
        k43 = domega2_dt(th1[k] + h2 * k12, th2[k] + h2 * k22 , omg1[k] + h2 * k32, omg2[k] + h2 * k42, alp1[k])
    
        k14 = dtheta1_dt(omg1[k] + dt * k33)
        k24 = dtheta2_dt(omg2[k] + dt * k43)
        k34 = domega1_dt(th1[k] + dt * k13, th2[k] + dt * k23 , omg1[k] + dt * k33, omg2[k] + dt * k43, alp2[k])  
        k44 = domega2_dt(th1 [k]+ dt * k13, th2[k] + dt * k23 , omg1[k] + dt * k33, omg2[k] + dt * k43, alp1[k])
 
        th1[k] += (dt / 6) * (k11 + 2 * k12 + 2 * k13 + k14)
        th2[k] += (dt / 6) * (k21 + 2 * k22 + 2 * k23 + k24)
        omg1[k] += (dt / 6) * (k31 + 2 * k32 + 2 * k33 + k34)
        omg2[k] += (dt / 6) * (k41 + 2 * k42 + 2 * k43 + k44)
        alp1[k] = domega1_dt(th1[k], th2[k], omg1[k], omg2[k], alp2[k])
        alp2[k] = domega1_dt(th1[k], th2[k], omg1[k], omg2[k], alp1[k])
    # ---
    
    pos1_1 = [l1 * math.sin(th1[0]), -l1 * math.cos(th1[0])]
    pos2_1 = [pos1_1[0] + l2 * math.sin(th2[0]), pos1_1[1] - l2 * math.cos(th2[0])]   
    pos1_1[1] = -pos1_1[1]
    pos2_1[1] = -pos2_1[1]   
    pos1_1[0] += w // 2
    pos1_1[1] += h // 2
    pos2_1[0] += w // 2
    pos2_1[1] += h // 2
    
    pos1_2 = [l1 * math.sin(th1[1]), -l1 * math.cos(th1[1])]
    pos2_2 = [pos1_2[0] + l2 * math.sin(th2[1]), pos1_2[1] - l2 * math.cos(th2[1])]   
    pos1_2[1] = -pos1_2[1]
    pos2_2[1] = -pos2_2[1]   
    pos1_2[0] += w // 2
    pos1_2[1] += h // 2
    pos2_2[0] += w // 2
    pos2_2[1] += h // 2
    
    pos1_3 = [l1 * math.sin(th1[2]), -l1 * math.cos(th1[2])]
    pos2_3 = [pos1_3[0] + l2 * math.sin(th2[2]), pos1_3[1] - l2 * math.cos(th2[2])]   
    pos1_3[1] = -pos1_3[1]
    pos2_3[1] = -pos2_3[1]   
    pos1_3[0] += w // 2
    pos1_3[1] += h // 2
    pos2_3[0] += w // 2
    pos2_3[1] += h // 2
    
     
    points1.append((pos2_1[0], pos2_1[1]))
    points2.append((pos2_2[0], pos2_2[1]))
    points3.append((pos2_3[0], pos2_3[1]))
    
    pygame.draw.line(screen, (255, 0, 0), (w // 2, h // 2), pos1_1, 7)
    pygame.draw.line(screen, (255, 0, 0), pos1_1, pos2_1, 7)
    
    pygame.draw.line(screen, (0, 255, 0), (w // 2, h // 2), pos1_2, 7)
    pygame.draw.line(screen, (0, 255, 0), pos1_2, pos2_2, 7)
    
    pygame.draw.line(screen, (0, 0, 255), (w // 2, h // 2), pos1_3, 7)
    pygame.draw.line(screen, (0, 0, 255), pos1_3, pos2_3, 7)
       

    if len(points1) >= 2:
        pygame.draw.lines(screen, (250,127,77), False, points1, 2)
    if len(points2) >= 2:
        pygame.draw.lines(screen, (75,250,20), False, points2, 2)
    if len(points3) >= 2:
        pygame.draw.lines(screen, (90,127,240), False, points3, 2)
    
    pygame.draw.circle(screen, (30, 30, 30), (w // 2, h // 2), 9)
    
    pygame.draw.circle(screen, (255, 0, 0), pos1_1, 13)
    pygame.draw.circle(screen, (255, 0, 0), pos2_1, 13)
    
    pygame.draw.circle(screen, (0, 255, 0), pos1_2, 13)
    pygame.draw.circle(screen, (0, 255, 0), pos2_2, 13)
    
    
    pygame.draw.circle(screen, (0, 0, 255), pos1_3, 13)
    pygame.draw.circle(screen, (0, 0, 255), pos2_3, 13)
    
    
    text = font.render('github.com/PhysicsMathCodeAndFun', True, (255,255,255))
    screen.blit(text, pygame.Rect(100, 0, 400,300))
       
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    
    
isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
            
    screen.fill((0,0,0))       
    Update(screen)
    
pygame.quit()
sys.exit()
