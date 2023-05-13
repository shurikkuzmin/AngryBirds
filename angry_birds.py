#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 09:49:54 2022

@author: shurik
"""

import pygame
import pymunk
import numpy

from enum import Enum

class Status(Enum):
    NOTMOVING = 1
    ATTACHED_MOUSE = 2
    ATTACHED_SPRING = 3
    FREE_FLY = 4

pygame.init()

background = pygame.image.load("background.jpg")
sprites = pygame.image.load("sprites.png")
explosion = pygame.image.load("explosion.png")

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

#pole_size = 200.0
#pole_width = 30.0

def convert_to_pymunk(x: int, y: int):
    return float(x), float(screen_height - y)

def convert_to_pygame(x: float, y: float):
    return int(x), int(screen_height - y)

class Pole():
    def __init__(self, type: str,  init_x: float, init_y: float):
        image = pygame.image.load("wood.png")
        image = image.subsurface((160,1),(23,169))
        self.image = pygame.transform.scale(image, (12, 85))
        
        if type == "Horizontal":
            self.image = pygame.transform.rotate(self.image, 90)

        self.body = pymunk.Body()
        self.body.position = init_x, init_y
        
        if type == "Vertical":
            self.shape = pymunk.Poly.create_box(self.body,(12, 85))
        else:
            self.shape = pymunk.Poly.create_box(self.body,(85, 12))

        self.shape.density = 0.5
        self.shape.friction = 0.8
        self.shape.elasticity = 0.5
        self.shape.collision_type = 3
                
        space.add(self.body, self.shape)
        
    def update(self):
        pass
        
    def draw(self):
        # To properly draw the segment, the information is here: 
        # https://stackoverflow.com/questions/70320642/python-code-problem-displaying-a-polygon-in-pygame-using-a-polygon-modeled-in-py
        x, y = self.body.position
        image_rotated=pygame.transform.rotate(self.image, self.body.angle / numpy.pi * 180.0)
        rect = image_rotated.get_rect()
        rect.center = convert_to_pygame(x,y)
        screen.blit(image_rotated, rect)


class Earth():
    def __init__(self, init_y: float):
        self.earth_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.earth_shape = pymunk.Segment(self.earth_body, (-5.0*screen_width, init_y), (5.0*screen_width, init_y), 4.0)
        self.earth_shape.friction = 0.7
        self.earth_shape.elasticity = 0.8
        space.add(self.earth_body, self.earth_shape)

class Pig():
    def __init__(self, x: float, y: float):
        self.pig_body = pymunk.Body()
        self.pig_body.position = x, y
        self.pig_shape = pymunk.Poly.create_box(self.pig_body, (45, 45))
        self.pig_shape.density = 0.1
        self.pig_shape.friction = 0.5
        self.pig_shape.elasticity = 0.8
        self.pig_shape.collision_type = 2
        image1 = sprites.subsurface(279, 744, 119, 107)
        image2 = sprites.subsurface(164, 848, 119, 107)
        image3 = sprites.subsurface(281, 845, 119, 107)
        images = [image1, image2, image3]
        images = [pygame.transform.scale(image, (60, 54)) for image in images]
        
        explosion_images = []
        for i in range(5):
            explosion_images.append(explosion.subsurface(320*3, 230 * i, 320, 230))
        self.explosion_images = [pygame.transform.scale(image, (60, 54)) for image in explosion_images]
        
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.total_energy_lost = 0.0
        
        space.add(self.pig_body, self.pig_shape)
    
    def update(self):
        x, y = self.pig_body.position
        self.rect.center = convert_to_pygame(x, y)
        if self.total_energy_lost < 4000000.0:
            self.image = self.images[0]
        elif self.total_energy_lost < 8000000.0:
            self.image = self.images[1]
        elif self.total_energy_lost < 1200000.0:
            self.image = self.images[2]
        else:
            self.image = self.explosion_images[2]
            
    def draw(self):
        screen.blit(self.image, self.rect)


class Bird():
    def __init__(self, x: float, y: float):
        image1 = sprites.subsurface(517,913,65,55)
        image2 = sprites.subsurface(585,913,65,55)
        image3 = sprites.subsurface(651,913,65,55)
        image4 = sprites.subsurface(530,842,65,55)
        self.images = [image1, image2, image3, image4]
        #self.image = sprites.subsurface(513,913,70,55)
        self.image = self.images[0]
        
        self.rect = pygame.Rect(0, 0, 65, 55)
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
        self.bird_shape = pymunk.Poly.create_box(self.bird_body, (70.0, 55.0))
        self.bird_shape.friction = 0.2
        self.bird_shape.elasticity = 0.8
        self.bird_shape.density = 1.0
        self.bird_shape.collision_type = 1
        
        self.init_x, self.init_y = convert_to_pygame(x,y)
        self.radius = 150
            
        self.collision = False
        # Status
        self.status = Status.NOTMOVING
    
    def draw(self):
        screen.blit(self.launcher_back,self.launcher_back_rect)
        
        xback, yback = self.launcher_back_rect.topright
        yback = yback + 30
        xback = xback - 30
        xbottom, ybottom = self.rect.bottomleft
        xbottom = xbottom + 15
        ybottom = ybottom - 5
        
        if self.status == Status.FREE_FLY:
            xbottom = self.init_x
            ybottom = self.init_y
        pygame.draw.line(screen, (59, 30, 8), (xbottom, ybottom), 
                         (xback, yback), 10)
        
        screen.blit(self.image, self.rect)
        screen.blit(self.launcher_front, self.launcher_front_rect)
        
        xfront, yfront = self.launcher_front_rect.topright
        yfront = yfront + 30
        xfront = xfront - 10
        xbottom, ybottom = self.rect.bottomleft
        xbottom = xbottom + 15
        ybottom = ybottom - 5
        if self.status == Status.FREE_FLY:
            xbottom = self.init_x
            ybottom = self.init_y
        
        pygame.draw.line(screen, (59, 30, 8), (xbottom, ybottom), 
                         (xfront, yfront), 10)

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
            self.image = self.images[0]
            
        if self.status == Status.ATTACHED_MOUSE:
            x,y = pygame.mouse.get_pos()
            dist = ((x - self.init_x)**2 + (y - self.init_y)**2)**0.5
            if dist**2 < self.radius**2:
                self.bird_body.position = convert_to_pymunk(x, y)
            else:
                x2 = self.init_x + (x - self.init_x) * self.radius / dist
                y2 = self.init_y + (y - self.init_y) * self.radius / dist
                self.bird_body.position = convert_to_pymunk(x2, y2)
            self.image = self.images[1]
            
        if self.status == Status.ATTACHED_SPRING:
            if self.x > self.init_x:
                self.status = Status.NOTMOVING
            else:
                dist = ((self.x - self.init_x)**2 + (self.y - self.init_y)**2)**0.5
                if dist <= 5.0:
                    self.status = Status.FREE_FLY
                self.acc_x = -5.0 * (self.x - self.init_x)
                self.acc_y = -5.0 * (self.y - self.init_y)
            self.image = self.images[1]
        
        if self.status == Status.FREE_FLY:
            self.image = self.images[2]
            if self.collision == True:
                self.image = self.images[3]
            
    def update(self):  
        self.check_status() 
        
        x, y = self.bird_body.position                  
        self.rect.center = convert_to_pygame(x, y)

def collision_bird_wood(arb, space, data):
    bird.collision = True
    return True

def collision_bird_pig(arb, space, data):
    shapes = arb.shapes
    for i in range(2):
        if pigs[i].pig_shape == shapes[1]:
            pigs[i].collision = True
            print("Pig " + str(i + 1))
    bird.collision = True
    return True

def postcollision_bird_pig(arb, space, data):
    shapes = arb.shapes
    for i in range(2):
        if pigs[i].pig_shape == shapes[1]:
            pigs[i].total_energy_lost = pigs[i].total_energy_lost + arb.total_ke
            print(pigs[i].total_energy_lost)

handler_bird_wood = space.add_collision_handler(1, 3)
handler_bird_wood.begin = collision_bird_wood

handler_bird_pig = space.add_collision_handler(1, 2)
handler_bird_pig.begin = collision_bird_pig
handler_bird_pig.post_solve = postcollision_bird_pig

# Bird is created in physics coordinates
pole1 = Pole("Vertical", 740.0, 185.0)
pole2 = Pole("Vertical", 830.0, 185.0)
pole3 = Pole("Horizontal", 785.0, 250.0)
bird = Bird(200.0, 300.0)
earth = Earth(130.0)
pig1 = Pig(785.0, 170.0)
pig2 = Pig(785.0, 250.0)
pigs = [pig1, pig2]
#pig3 = Pig(800.0,450.0)
#pig4 = Pig(800.0,550.0)
#pig5 = Pig(600.0,250.0)

objects = [bird, pole1, pole2, pole3, pig1, pig2] #, pig2, pig3, pig4, pig5]

isRunning = True
while isRunning:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        bird.react(event)

    for obj in objects:
        obj.update()
        obj.draw()
    
    space.step(1.0 / fps)
    clock.tick(fps)
    pygame.display.update()

pygame.quit()