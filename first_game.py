#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 22:42:55 2017

@author: steve
"""

import pygame

def first_game():
    pygame.init()
    
    
    winsizex = 400
    winsizey = 300
    ftick = 60
    screen = pygame.display.set_mode((winsizex, winsizey))
    done = False
    
    # gameticks
    clock = pygame.time.Clock()
    
    # initial position:
    x=30
    y=30
    
    while not done:
        clock.tick(ftick)
        yprev = y
        xprev = x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
                pygame.quit()
        
        #input checking
        pressed = pygame.key.get_pressed()
        up_key = pressed[pygame.K_UP]
        down_key = pressed[pygame.K_DOWN]
        left_key = pressed[pygame.K_LEFT]
        right_key = pressed[pygame.K_RIGHT]
        if up_key: y-=3
        if down_key: y+=3
        if left_key: x-=3
        if right_key: x+=3
        
        # wrap the screen
        y = y%winsizey
        x = x%winsizex
        
        
        # screen rendering
        # do we need to draw stuff?
        if x!=xprev or y!=yprev:
            # erase previous screen
            screen.fill((0,0,0))  
            # draw stuff
            pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x, y, 60, 60))
        
        # flip the buffer
        pygame.display.flip()
        
first_game()