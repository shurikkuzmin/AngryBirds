#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:49:54 2022

@author: shurik
"""

import pygame

pygame.init()

screen = pygame.display.set_mode((1500, 800))

clock = pygame.time.Clock()

fps = 60
dt = 1.0 / fps
width = 50
height = 50

class Bird():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.init_x = float(x)
        self.init_y = float(y)
        self.x = self.init_x
        self.y = self.init_y
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.acc_x = 0.0
        self.acc_y = 0.0

        self.radius = 150
        self.attached_to_mouse = False
        self.start_movement = False
        self.attached_to_spring = False
    
    def draw(self):
        pygame.draw.rect(screen,(255,192,203),self.rect)

    def react_to_keyboard(self, key):
        if key == pygame.K_UP:
            self.rect = self.rect.move(0, -10)
        if key == pygame.K_DOWN:
            self.rect = self.rect.move(0,10)
    def react_to_mouse(self, buttons):
        if buttons[0] == True:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.attached_to_mouse = True
                
    def detach_from_mouse(self):
        if self.attached_to_mouse == True:
            self.attached_to_mouse = False
            self.start_movement = True
            
    def update(self):
        x, y = pygame.mouse.get_pos()
            
        if self.attached_to_mouse == True:
            dist = ((x - self.init_x)**2 + (y - self.init_y)**2)**0.5
            if dist**2 < self.radius**2:
                self.x = float(x)
                self.y = float(y)
            else:
                self.x = self.init_x + (x - self.init_x) * self.radius / dist
                self.y = self.init_y + (y - self.init_y) * self.radius / dist
                
        if self.start_movement == True:
            dist = ((self.x - self.init_x)**2 + (self.y - self.init_y)**2)**0.5
      
            if dist < 5:
                self.attached_to_mouse = False
                self.start_movement = False
                self.acc_y = 100
            else:    
                self.acc_x = -5.0 * (self.x - self.init_x)
                self.acc_y = -5.0 * (self.y - self.init_y)
            
        self.vel_x = self.vel_x + self.acc_x * dt
        self.vel_y = self.vel_y + self.acc_y * dt
        self.x = self.x + self.vel_x * dt
        self.y = self.y + self.vel_y * dt
            
        self.rect.center = int(self.x), int(self.y)
            

bird = Bird(200,500,30,30)

isRunning = True
while isRunning:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            bird.react_to_keyboard(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            bird.react_to_mouse(pygame.mouse.get_pressed())
        if event.type == pygame.MOUSEBUTTONUP:
            bird.detach_from_mouse()
    bird.update()
    bird.draw()
    
    clock.tick(fps)
    pygame.display.update()

pygame.quit()