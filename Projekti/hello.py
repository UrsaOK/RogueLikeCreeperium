# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import random
from collections import defaultdict
from kartta import *

        
class Esine(object):
    def __init__(self, x, y, img, fg=libtcod.white, bg=libtcod.black):
        self.x = x
        self.y = y
        self.merkki = img
        self.fg = fg
        self.bg = bg
    def update(self):
        pass
    def draw(self):
        libtcod.console_put_char_ex(0, self.x, self.y, self.merkki, self.fg, self.bg)


class Liikkuja(Esine):
    def __init__(self, taso, x, y, img):
        super(Liikkuja, self). __init__(x, y, img)
        self.taso = taso
    def liiku(self, suunta):
        self.x += suunta[0]
        self.y += suunta[1]
    def tarkista(self, suunta):
        kohdex = self.x + suunta[0]
        kohdey = self.y + suunta[1]
        print("wasd")
        if self.taso.kartta[kohdex][kohdey].tyhja\
        and len(self.taso.ruudun_sisalto(kohdex, kohdey)) == 0:
            print("qwerty")
            return True
        else:
            print("qwerty")
            return False
    def yrita_likkua(self, suunta):
        if self.tarkista(suunta):
            self.liiku(suunta)
            return True
class Pelaaja(Liikkuja):
    pass


class Kylalaiset(Liikkuja):
    def __init__(self, taso, x, y):
        super(Kylalaiset, self).__init__(taso, x, y, "+")

    def update(self):
        suunta = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0)))
        reitti = self.taso.kartta.path_finding(self.x, self.y, pelaaja.x, pelaaja.y)
        if reitti is None:
            self.yrita_likkua(reitti[0])



class Taso:
    def __init__(self):
        self.kartta = Kartta()
        self.esineet = [Kylalaiset(self, random.randint(1, self.kartta.leveys-2), random.randint(1, self.kartta.korkeus-2)) for _ in range(10)]
    def ruudun_sisalto(self, x, y):
        return [i for i in self.esineet if i.x == x and i.y == y]
    def update(self):
        for i in self.esineet:
            i.update()
    def draw(self):
        self.kartta.draw()
        for i in self.esineet:
            i.draw()






#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
LIMIT_FPS = 15  #20 frames-per-second maximum
 
 
def handle_keys():
    global playerx, playery
 
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        suunta = 0, -1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        suunta = 0, 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        suunta = -1, 0
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        suunta = 1, 0
    else:
        suunta = 0, 0

    pelaaja.yrita_likkua(suunta)


 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Roguelike', False)
libtcod.sys_set_fps(LIMIT_FPS)
taso = Taso()
pelaaja = Liikkuja(taso, 1, 1, "@")
taso.esineet.append(pelaaja)
 
while not libtcod.console_is_window_closed():
 
    libtcod.console_set_default_foreground(0, libtcod.white)
    
    taso.update()
    taso.draw()

    libtcod.console_flush()
 

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
