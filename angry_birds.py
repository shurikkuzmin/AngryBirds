#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:49:54 2022

@author: shurik
"""

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

width = 50
height = 50

class Bird():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.init_x = x
        self.init_y = y
        self.radius = 150
        self.attached_to_mouse = False
    
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
            
    def update(self):
        if self.attached_to_mouse == True:
            x, y = pygame.mouse.get_pos()
            if (x - self.init_x)**2 + (y - self.init_y)**2 < self.radius**2:
                self.rect.center = (x, y)

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
    
    pygame.display.update()

pygame.quit()