#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 09:54:31 2023

@author: shurik
"""
import pygame
import pymunk

pygame.init()

screen = pygame.display.set_mode((600, 400))

clock = pygame.time.Clock()
fps = 60

space = pymunk.Space()
space.gravity = 0.0, -10.0

ball = pymunk.Body()
ball.position = (100.0,300.0)
ball_shape = pymunk.Circle(ball, 30.0)
ball_shape.density = 1.0

earth = pymunk.Body(body_type = pymunk.Body.STATIC)
earth_shape = pymunk.Segment(earth, (0.0, 100.0), (600.0, 100.0), 5.0)

space.add(ball, ball_shape, earth, earth_shape)

isRunning = True
while isRunning:
    screen.fill((100, 100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
    x, y = ball.position
    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 30)
    
    clock.tick(fps)
    space.step(1.0 / fps)
    pygame.display.update()

pygame.quit()
