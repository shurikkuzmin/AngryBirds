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

class Bird():
    def __init__(self, x: float, y: float):
        self.image = sprites.subsurface(513,913,75,75)
        self.rect = pygame.Rect(0, 0, 75, 75)
        self.rect.center = convert_to_pygame(x, y)
        
        # Coordinates and accelarations
        self.bird_body = pymunk.Body()
        self.bird_body.position = x, y
        
        self.bird_shape = pymunk.Circle(self.bird_body, 37.0)
        self.bird_shape.friction = 1.0
        self.bird_shape.elasticity = 0.8
        
        self.init_x, self.init_y = convert_to_pygame(x,y)
        self.radius = 150
            
        # Status
        self.status = Status.NOTMOVING
    
    def draw(self):
        screen.blit(bird.image, self.rect)

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
        
        x, y = self.bird_body.position                  
        self.rect.center = convert_to_pygame(x, y)
        
# Bird is created in physics coordinates
bird = Bird(200.0,200.0)

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