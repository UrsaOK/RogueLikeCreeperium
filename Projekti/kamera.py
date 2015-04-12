# -*- coding: utf-8 -*-

import libtcodpy as libtcod
from kartta import Kartta
import game


class Kamera:

    centerx = 40
    centery = 25

    def kamera_draw(self):
        startx = -self.centerx + self.x
        starty = -self.centery + self.y
        endx = startx + 80
        endy = starty + 50
        for x_screen, x in enumerate(range(startx, endx)):
            for y_screen, y in enumerate(range(starty, endy)):
                libtcod.console_put_char(0, x_screen, y_screen, self.taso.kartta[x,y].merkki, libtcod.BKGND_NONE)
    def kamera_draw_debug(self):
        startx = -self.centerx + self.x
        starty = -self.centery + self.y
        endx = startx + 80
        endy = starty + 50
        for x_screen, x in enumerate(range(startx, endx)):
            for y_screen, y in enumerate(range(starty, endy)):
                libtcod.console_put_char(0, x_screen, y_screen, self.taso.kartta[x,y].merkki, libtcod.BKGND_NONE)
        if not len(str(game.pelaaja.x)) > 1:
            libtcod.console_put_char(0, 0, 0, str(game.pelaaja.x), libtcod.BKGND_NONE)
        else:
            pituus = len(str(game.pelaaja.x))
            for i in range(pituus):
                libtcod.console_put_char(0, i, 0, str(game.pelaaja.x)[i], libtcod.BKGND_NONE)
        if not len(str(game.pelaaja.y)) > 1:
            libtcod.console_put_char(0, 0, 1, str(game.pelaaja.y), libtcod.BKGND_NONE)
        else:
            pituus = len(str(game.pelaaja.y))
            for i in range(pituus):
                libtcod.console_put_char(0, i, 1, str(game.pelaaja.y)[i], libtcod.BKGND_NONE)
    def offset(self):
        return -self.centerx + self.x, -self.centery + self.y