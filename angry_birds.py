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

screen_width, screen_height = background.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0.0, -200.0
space.damping = 0.9

fps = 60
dt = 1.0 / fps
width = 50
height = 50

def convert_to_pymunk(x: int, y: int):
    return float(x), float(screen_height - y)

def convert_to_pygame(x: float, y: float):
    return int(x), int(screen_height - y)

class Earth():
    def __init__(self, init_y):
        self.earth_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.earth_shape = pymunk.Segment(self.earth_body, (0.0, init_y), (screen_width, init_y), 4.0)
        self.earth_shape.friction = 0.7
        self.earth_shape.elasticity = 0.8
        space.add(self.earth_body, self.earth_shape)

class Bird():
    def __init__(self, x: float, y: float):
        self.image = sprites.subsurface(513,913,75,75)
        self.rect = pygame.Rect(0, 0, 75, 75)
        self.rect.center = convert_to_pygame(x, y)
        
        # Launcher
        self.launcher_front = sprites.subsurface(0,0,40,200)
        self.launcher_front_rect = self.launcher_front.get_rect()
        self.launcher_front_rect.center = convert_to_pygame(x + 5.0, y - 50.0)
        
        self.launcher_back = sprites.subsurface(0,840,45,130) 
        self.launcher_back_rect = self.launcher_back.get_rect()
        self.launcher_back_rect.bottomright = convert_to_pygame(x, y - 70.0)
        
        
        # Coordinates and accelarations
        self.bird_body = pymunk.Body()
        self.bird_body.position = x, y
        
        #self.bird_shape = pymunk.Circle(self.bird_body, 37.0)
        self.bird_shape = pymunk.Poly.create_box(self.bird_body, (74.0, 74.0))
        self.bird_shape.friction = 0.2
        self.bird_shape.elasticity = 0.8
        self.bird_shape.density = 1.0
        
        self.init_x, self.init_y = convert_to_pygame(x,y)
        self.radius = 150
            
        # Status
        self.status = Status.NOTMOVING
    
    def draw(self):
        screen.blit(self.launcher_back,self.launcher_back_rect)
        screen.blit(self.image, self.rect)
        screen.blit(self.launcher_front, self.launcher_front_rect)

    def react(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.status = Status.ATTACHED_MOUSE 
        if event.type == pygame.MOUSEBUTTONUP:
            if self.status == Status.ATTACHED_MOUSE:
                x, y = self.rect.center
                dist = ((x - self.init_x)**2 + (y - self.init_y)**2)**0.5
                if dist <= 30.0:
                    self.status = Status.NOTMOVING
                else:
                    vel_x = -3.3*float(x - self.init_x)
                    vel_y = 3.3*float(y - self.init_y)
                    self.bird_body.velocity = vel_x, vel_y
                    space.add(self.bird_body, self.bird_shape)
                    self.status = Status.FREE_FLY
    
    def check_status(self):
        if self.status == Status.NOTMOVING:
            self.bird_body.position = convert_to_pymunk(self.init_x, self.init_y)
            
        if self.status == Status.ATTACHED_MOUSE:
            x,y = pygame.mouse.get_pos()
            dist = ((x - self.init_x)**2 + (y - self.init_y)**2)**0.5
            if dist**2 < self.radius**2:
                self.bird_body.position = convert_to_pymunk(x, y)
            else:
                x2 = self.init_x + (x - self.init_x) * self.radius / dist
                y2 = self.init_y + (y - self.init_y) * self.radius / dist
                self.bird_body.position = convert_to_pymunk(x2, y2)
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
            pass
        
        if self.status == Status.ON_EARTH:
            self.acc_x = 0
            self.acc_y = 0
            self.vel_y = 0
            self.vel_x = 0
    
    def update(self):  
        self.check_status() 
        
        x, y = self.bird_body.position                  
        self.rect.center = convert_to_pygame(x, y)
        
# Bird is created in physics coordinates
bird = Bird(200.0, 300.0)
earth = Earth(130.0)

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