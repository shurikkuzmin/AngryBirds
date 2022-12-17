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
    def __init__(self, x, y):
        self.x = x
        self.y = y


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    pygame.draw.rect(screen, (255,0,0), (width, height, 100, 100))

    pygame.display.update()

pygame.quit()