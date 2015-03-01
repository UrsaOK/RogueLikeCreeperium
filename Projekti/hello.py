# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import random
from collections import defaultdict
from kartta import *
from kamera import Kamera
import pickle
import math
        
class Esine(object):
    def __init__(self, x, y, img, fg=libtcod.white, bg=libtcod.black):
        self.x = x
        self.y = y
        self.merkki = img
        self.fg = fg
        self.bg = bg
    def etaisyys(self, kohde):
        etaisyysx = abs(kohde.x - self.x)
        etaisyysy = abs(kohde.y - self.y)
        etaisyys = math.sqrt(etaisyysx*etaisyysx + etaisyysy*etaisyysy)
        return etaisyys
    def update(self):
        pass
    def draw(self, offsetx, offsety):
        libtcod.console_put_char_ex(0, self.x - offsetx, self.y - offsety, self.merkki, self.fg, self.bg)


class Liikkuja(Esine):
    def __init__(self, taso, *args):
        super(Liikkuja, self). __init__(*args)
        self.taso = taso
    def liiku(self, suunta):
        self.x += suunta[0]
        self.y += suunta[1]
    def tarkista(self, suunta):
        kohdex = self.x + suunta[0]
        kohdey = self.y + suunta[1]
        if self.taso.kartta[kohdex,kohdey].tyhja\
        and len(self.taso.ruudun_sisalto(kohdex, kohdey)) == 0:
            return True
        else:
            return False
    def yrita_liikkua(self, suunta):
        if self.tarkista(suunta):
            self.liiku(suunta)
            return True

class Pelaaja(Liikkuja, Kamera):
    def yrita_liikkua(self, suunta):
        if not super(Pelaaja, self).yrita_liikkua(suunta):
            for i in self.taso.ruudun_sisalto(self.x+suunta[0], self.y+suunta[1]):
                if isinstance(i, HP):
                    i.damage(1)

class HP:
    def __init__(self, max, current):
        self.current = current
        self.max = max
    def damage(self, damage):
        self.current -= damage
    def heal(self, heal):
        if self.current != self.max:
            self.current += self.heal
        self.current = min(self.current, self.max)
    def is_alive(self):
        return self.current > 0

class Kylalaiset(Liikkuja, HP):
    def __init__(self, taso, x, y, vihainen):
        super(Kylalaiset, self).__init__(taso, x, y, "+", libtcod.sepia)
        HP.__init__(self, 5, 5)
        self.tila = self.vihainen if vihainen else self.rauhallinen
        
    def update(self):
        self.tila()
        if not self.is_alive():
            self.taso.esineet.remove(self)

    def vihainen(self):
        reitti = self.taso.kartta.path_finding(self.x, self.y, pelaaja.x, pelaaja.y, 10)
        if reitti is not None and len(reitti) < 11:
            self.yrita_liikkua(reitti[0])
        else:
            self.yrita_liikkua(self.arvo_suunta())

    def rauhallinen(self):
        self.yrita_liikkua(self.arvo_suunta())

    def arvo_suunta(self):
        return random.choice(((0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)))



class Taso:
    def __init__(self):
        self.kartta = Kartta()
        self.esineet = [Kylalaiset(self, random.randint(1, self.kartta.leveys-2), random.randint(1, self.kartta.korkeus-2), random.choice((True, False))) for _ in range(100)]
    def ruudun_sisalto(self, x, y):
        return [i for i in self.esineet if i.x == x and i.y == y]
    def update(self):
        for i in self.esineet:
            if pelaaja.etaisyys(i) < 85:
                i.update()
    def draw(self):
        pelaaja.kamera_draw()
        offx, offy = pelaaja.offset()
        for i in self.esineet:
            if pelaaja.etaisyys(i) < 85:
                i.draw(offx, offy)


#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
LIMIT_FPS = 15  #20 frames-per-second maximum
 
 
def handle_keys():
    suunta = 0, 0
 
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
    elif libtcod.console_is_key_pressed(libtcod.KEY_UP):
        suunta = 0, -1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        suunta = 0, 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        suunta = -1, 0
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        suunta = 1, 0
    else:
        return handle_keys()

    pelaaja.yrita_liikkua(suunta)


 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Roguelike', False)
libtcod.sys_set_fps(LIMIT_FPS)
taso = Taso()
pelaaja = Pelaaja(taso, 1, 1, "@", libtcod.light_red)
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
