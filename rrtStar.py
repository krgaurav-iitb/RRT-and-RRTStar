# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame, sys
from pygame.locals import *
from numpy.random import randint
import numpy as np
import quantumrandom
import random

#random.seed()
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('RRT_Star')
clock = pygame.time.Clock()
dis=20
radius=50
cyan = 0,180,105
dark_green = 0, 102, 0
run =True
rectangles=[]
ex=0
ey=0
class tree(object):
    #vertices=[]
    def __init__(self):
        self.vertices=[]
    
    def add_vertices(self,nodex,nodey,p,c):
        node=Node(nodex,nodey,p,c)
        self.vertices.append(node)

class Node():
    def __init__(self,x,y,p,c):
        self.x=x
        self.y=y
        self.parent=p
        self.cost=c

class Rectangle:
    def __init__(self, pos, color, size):
        self.pos = pos
        self.color = color
        self.size = size
    def draw(self):
        pygame.draw.rect(screen, self.color, Rect(self.pos, self.size))
       
def add_obstacle():
    run =True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                
def nearest_neighbor(valx,valy):
    valxmin=10000
    valymin=10000
    distmin=10000
    for vert in Tree.vertices:
        dist=np.sqrt(np.square(vert.x-valx)+ np.square(vert.y-valy))  
        #print(dist,distmin)
        if(dist<distmin):
            distmin=dist
            node=vert
    #node=Node(valxmin,valymin,valparent)
    #rrtStar optimization
    return node

def projectPoint(nearx,neary,valx,valy):
    theta=np.arctan2(valy-neary, valx-nearx)
    projx=nearx+(dis*np.cos(theta))
    projy=neary+(dis*np.sin(theta))
    return int(projx),int(projy)

def checkCollision(px,py):
    for rect in rectangles:
        if (rect.collidepoint((px,py))):
            return True
    return False

def checkReached(x,y):
    #print(ex,ey)
    if(np.sqrt(np.square(x-ex)+ np.square(y-ey))<17.6):
        return True
    else:
        return False

def optimise(projx,projy):
    Tree1=tree()
    cost=[]
    for vert in Tree.vertices:
        dist=np.sqrt(np.square(vert.x-projx)+ np.square(vert.y-projy))  
        if(dist<radius):
            Tree1.add_vertices(vert.x,vert.y,vert.parent,vert.cost)
            cost.append(vert.cost+dist)    
        #print(dist,distmin)
    return Tree1.vertices[np.argmin(np.array(cost))],np.min(np.array(cost))

def get_random():
    #while True:
    #p = round(np.random.uniform(0,1),3)*1000, round(np.random.uniform(0,1),3)*1000
    p=np.random.randint(0,1000,2)
    #p2=random.randint(0,1000000000)%1000
    #p=quantumrandom.randint(0,1000),quantumrandom.randint(0,1000)
    #print(p)
    #if checkCollision(p[0],p[1]) == False:
    return p

def getStartPoints():
    run =True
    count=0
    startX=0
    startY=0
    while run:
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                count+=1
                if(count==1):
                    startX,startY=pygame.mouse.get_pos()
                if(count==2):
                    return startX,startY,pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                
                
new_obstacle=False
new_obstacle2=False
x=0
y=0
x2=0
y2=0
sx=0
sy=0

points=False
obs_count=0
rectangles.append(pygame.Rect(150,920,150,50))
rectangles.append(pygame.Rect(400,920,150,50))
rectangles.append(pygame.Rect(600,920,300,50))
rectangles.append(pygame.Rect(200,550,300,300))
rectangles.append(pygame.Rect(700,300,200,300))

Tree=tree()
reached=False
while run:
    
    #sys_font = pygame.font.SysFont("None", 19)
    screen.fill((255,255,255))
    start_button = pygame.draw.rect(screen,(0,0,240),(150,920,150,50))
    font = pygame.font.Font('freesansbold.ttf', 32) 
    #pygame.display.update()
    screen.blit(font.render('Start', True, (255,0,0)), (180, 930))
    #pygame.display.update()

    reset_button = pygame.draw.rect(screen,(0,0,240),(400,920,150,50))
    #pygame.display.update()
    screen.blit(font.render('Reset', True, (255,0,0)), (430, 930))

    add_button = pygame.draw.rect(screen,(0,0,240),(600,920,300,50))
    #font = pygame.font.Font('freesansbold.ttf', 32) 
    #pygame.display.update()
    screen.blit(font.render('add obstacle', True, (0,255,0)), (630, 930))
    #pygame.display.update()
    #rendered = Sysfont.render('Hello World', 0, (255, 100, 100))
    #screen.blit(rendered, (100, 100))
    pygame.draw.rect(screen,(0,0,0),(200,550,150,150))
    pygame.draw.rect(screen,(0,0,0),(700,300,150,150))
    #pygame.display.update()

    for rect1 in rectangles[3:]:
       pygame.draw.rect(screen,(0,0,0),rect1)
       #new_obstacle=False

    """if(new_obstacle2):
       pygame.draw.rect(screen,(0,0,0),(x2,y2,150,150))"""

    if(points):
       
       pygame.draw.circle(screen,(0,255,0),(sx,sy),15)
       pygame.draw.circle(screen,(255,0,0),(ex,ey),15)
       valx,valy=get_random()
       #valx2,valy2=get_random()
       #valx3,valy3=get_random()
       nearNode=nearest_neighbor(valx,valy)
       #nearNode2=nearest_neighbor(valx2,valy2)
       #nearNode3=nearest_neighbor(valx3,valy3)
       #nearNode=Node(nearx,neary,)
       projx,projy=projectPoint(nearNode.x,nearNode.y,valx,valy)
       nearNode,cost=optimise(projx,projy)
       #projx2,projy2=projectPoint(nearNode2.x,nearNode2.y,valx2,valy2)
       #projx3,projy3=projectPoint(nearNode3.x,nearNode3.y,valx3,valy3)
       if((not checkCollision(projx,projy))):
            if (not reached):
                #print(nearNode.x,nearNode.y)
                Tree.add_vertices(projx,projy,nearNode,cost)
                #print(np.sqrt(np.square(nearNode.x-projx)+ np.square(nearNode.y-projy))  )
                reached=checkReached(projx,projy) 
       """if((not checkCollision(projx2,projy2))):
            if (not reached):
                Tree.add_vertices(projx2,projy2,nearNode2)
                reached=checkReached(projx2,projy2)
       if((not checkCollision(projx3,projy3))):
            if (not reached):
                Tree.add_vertices(projx3,projy3,nearNode3)
                reached=checkReached(projx3,projy3)"""
            #prevx=sx
            #prevy=sy
       for vert in Tree.vertices[1:]:
            
            pygame.draw.circle(screen,cyan,(vert.x,vert.y),5)
            pygame.draw.line(screen,(127,12,127),(vert.parent.x,vert.parent.y),(vert.x,vert.y),1)
            #prevx=vert[0]
            #prevy=vert[1]
       if (reached):
            currNode=Tree.vertices[-1]
            while(currNode.parent!=None):
                pygame.draw.line(screen,(255,0,0),(currNode.parent.x,currNode.parent.y),(currNode.x,currNode.y),4)
                currNode=currNode.parent

       
                
        
        
       


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] >= 150 and pygame.mouse.get_pos()[1] >= 920:
                if pygame.mouse.get_pos()[0] <= 300 and pygame.mouse.get_pos()[1] <= 970:
                        #run=False
                        sx,sy,ex,ey=getStartPoints()
                        Tree.add_vertices(sx,sy,None,0)
                        #print(sx,sy,ex,ey)
                        points=True
            if pygame.mouse.get_pos()[0] >= 600 and pygame.mouse.get_pos()[1] >= 920:
                if pygame.mouse.get_pos()[0] <= 900 and pygame.mouse.get_pos()[1] <= 970:
                        x,y=add_obstacle()
                        rectangles.append(pygame.Rect(x,y,150,150))

            if pygame.mouse.get_pos()[0] >= 400 and pygame.mouse.get_pos()[1] >= 920:
                if pygame.mouse.get_pos()[0] <= 550 and pygame.mouse.get_pos()[1] <= 970:
                        Tree.vertices=[]
                        rectangles=rectangles[0:4]
                        points=False
                        reached=False
                        """obs_count+=1
                        if(obs_count==1):
                            x,y=add_obstacle()
                            new_obstacle=True
                        else:
                            x2,y2=add_obstacle()
                            new_obstacle2=True"""
                     
                            

            
   
    #x,y,w,h=input('location of first obstacle')
    #pygame.draw.rect(screen,x,y,w,h)
    pygame.display.update()
    #clock.tick(2)
    
pygame.quit()
sys.exit()

    
