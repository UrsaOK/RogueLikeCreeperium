# -*- coding: utf-8 -*-

import libtcodpy as libtcod


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
                def tyhja(): libtcod.console_put_char(0, x_screen, y_screen, " ", libtcod.BKGND_NONE)
                if x < 0 or y < 0:
                    tyhja()
                    continue
                try:
                    libtcod.console_put_char(0, x_screen, y_screen, self.taso.kartta[x,y].merkki, libtcod.BKGND_NONE)
                except IndexError:
                    tyhja()
    def offset(self):
        return -self.centerx + self.x, -self.centery + self.y
