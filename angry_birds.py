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
    
    def draw(self):
        pygame.draw.rect(screen,(255,192,203),self.rect)

    def react_to_keyboard(self, key):
        if key == pygame.K_UP:
            self.rect = self.rect.move(0, -10)
        if key == pygame.K_DOWN:
            self.rect = self.rect.move(0,10)

bird1 = Bird(100,100,100,100)
bird2 = Bird(200,200,50,50)

isRunning = True
while isRunning:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            bird1.react_to_keyboard(event.key)
            bird2.react_to_keyboard(event.key)

    bird1.draw()
    bird2.draw()
    
    pygame.display.update()

pygame.quit()