#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:49:54 2022

@author: shurik
"""

import pygame
import pymunk

from enum import Enum

class Status(Enum):
    NOTMOVING = 1
    ATTACHED_MOUSE = 2
    ATTACHED_SPRING = 3
    FREE_FLY = 4
    ON_EARTH = 5

pygame.init()

background = pygame.image.load("background.jpg")
sprites = pygame.image.load("sprites.png")

screen = pygame.display.set_mode(background.get_size())
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0.0, -200.0
space.damping = 0.9

fps = 60
dt = 1.0 / fps
width = 50
height = 50

class Bird():
    def __init__(self, x, y):
        self.image = sprites.subsurface(513,913,75,75)
        self.rect = pygame.Rect(0, 0, 75, 75)
        self.rect.center = (x, y)
        
        # Coordinates and accelarations
        self.bird_body = pymunk.Body()
        self.bird_body.position = float(x), float(y)
        
        self.bird_shape = pymunk.Circle(self.bird_body, 37.0)
        self.bird_shape.friction = 1.0
        self.bird_shape.elasticity = 0.8
        
        self.init_x = float(x)
        self.init_y = float(y)
        self.radius = 150
        
        #self.x = self.init_x
        #self.y = self.init_y
        #self.vel_x = 0.0
        #self.vel_y = 0.0
        #self.acc_x = 0.0
        #self.acc_y = 0.0

        
        # Status
        self.status = Status.NOTMOVING
    
    def draw(self):
        screen.blit(bird.image, self.rect)
        #pygame.draw.rect(screen,(255,192,203),self.rect)

    def react(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.status = Status.ATTACHED_MOUSE 
        if event.type == pygame.MOUSEBUTTONUP:
            if self.status == Status.ATTACHED_MOUSE:
                dist = ((self.x - self.init_x)**2 + (self.y - self.init_y)**2)**0.5
                if dist <= 30.0:
                    self.status = Status.NOTMOVING
                else:
                    self.status = Status.ATTACHED_SPRING
    
    def check_status(self):
        if self.status == Status.NOTMOVING:
            self.x = self.init_x
            self.y = self.init_y
            self.acc_x = 0
            self.acc_y = 0
            self.vel_y = 0
            self.vel_x = 0
            
        if self.status == Status.ATTACHED_MOUSE:
            x,y = pygame.mouse.get_pos()
            dist = ((x - self.init_x)**2 + (y - self.init_y)**2)**0.5
            if dist**2 < self.radius**2:
                self.x = float(x)
                self.y = float(y)
            else:
                self.x = self.init_x + (x - self.init_x) * self.radius / dist
                self.y = self.init_y + (y - self.init_y) * self.radius / dist
                
        if self.status == Status.ATTACHED_SPRING:
            if self.x > self.init_x:
                self.status = Status.NOTMOVING
            else:
                dist = ((self.x - self.init_x)**2 + (self.y - self.init_y)**2)**0.5
                if dist <= 5.0:
                    self.status = Status.FREE_FLY
                self.acc_x = -5.0 * (self.x - self.init_x)
                self.acc_y = -5.0 * (self.y - self.init_y)
        
        if self.status == Status.FREE_FLY:
            self.acc_x = 0.0
            self.acc_y = 130.0
            if self.y > background.get_size()[1]-175:
                self.status = Status.ON_EARTH
        if self.status == Status.ON_EARTH:
            self.acc_x = 0
            self.acc_y = 0
            self.vel_y = 0
            self.vel_x = 0
    
    def update(self):  
        self.check_status()
        
        #self.vel_x = self.vel_x + self.acc_x * dt
        #self.vel_y = self.vel_y + self.acc_y * dt
        #self.x = self.x + self.vel_x * dt
        #self.y = self.y + self.vel_y * dt
            
        x, y = self.bird_body.position
        self.rect.center = int(x), background.get_height()-int(y)  
            

bird = Bird(200,300)

isRunning = True
while isRunning:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        bird.react(event)

    bird.update()
    bird.draw()
    
    space.step(1.0 / fps)
    clock.tick(fps)
    pygame.display.update()

pygame.quit()