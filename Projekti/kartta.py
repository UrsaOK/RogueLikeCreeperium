# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import random
from collections import defaultdict
import pickle
import game

class Ruutu(object):
    def __init__(self, merkki, tyhja):
        self.merkki = merkki
        self.tyhja = tyhja

OVI = Ruutu(".", True)
TYHJA = Ruutu(" ", True)
SEINA = Ruutu("#", False)
SUPERSEINA = Ruutu("?", False)

class MapData(defaultdict):
    def __init__(self):
        super(MapData, self).__init__(lambda: TYHJA)

class Kartta(MapData):
    def __init__(self):
        super(Kartta, self).__init__()
        self.leveys = 80
        self.korkeus = 50

        global playerx, playery
        playerx, playery = self.huone()
        for i in range(6):
            self.huone()
        self.tee_seinat(0, 0, self.leveys, self.korkeus, SUPERSEINA)
        OvienTekija(self)

    def huone(self):
        leveys = random.randint(5, 20)
        korkeus = random.randint(5, 20)
        x = random.randint(0, self.leveys - leveys)
        y = random.randint(0, self.korkeus - korkeus)
        self.tee_seinat(x, y, leveys, korkeus, SEINA)
        return x+1, y+1

    def tee_seinat(self, x, y, leveys, korkeus, merkki):
        for x2 in range(x, x + leveys):
            self[x2,y] = merkki
            self[x2,y + korkeus - 1] = merkki
        for y2 in range(y, y + korkeus):
            self[x,y2] = merkki
            self[x + leveys - 1,y2] = merkki

    def draw(self):
        for x in range(self.leveys):
            for y in range(self.korkeus):
                libtcod.console_put_char(0, x, y, self[x,y].merkki, libtcod.BKGND_NONE)

    def path_finding(self, x, y, kohdex, kohdey, maxdist=100000):
        jono = []
        jono.append((x, y, []))
        kaydyt = set()
        suunnat = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while not len(jono) == 0:
            x, y, reitti = jono.pop(0)
            if len(reitti) > maxdist:
                continue
            if x == kohdex and y == kohdey:
                return reitti

            if self[x,y].tyhja != True or (x, y) in kaydyt:
                continue
                
            kaydyt.add((x, y))
            for xmod, ymod in suunnat:
                jono.append((x+xmod, y+ymod, reitti + [(xmod, ymod)]))
class Chunk():
    def __init__(self, taso, rectangle):
        self.taso = taso
        self.rectangle = rectangle
        self.onko_ladattu = False
    def lataa(self):
        self.generoi()
        self.onko_ladattu = True
    def poista(self):
        pass
    def generoi(self):
        for i in range(6):
            self.taso.kartta.huone()
        OvienTekija(self.taso.kartta)
class OvienTekija(object):
    def __init__(self, kartta):
        self.alueet = [[0]*kartta.korkeus for _ in range(kartta.leveys)]
        self.kartta = kartta
        self.selvita_alueet()
        self.tee_ovet()

    def selvita_alueet(self):
        numero = 1
        for x in range(self.kartta.leveys):
            for y in range(self.kartta.korkeus):
                if self.kartta[x,y].tyhja and self.alueet[x][y] == 0:
                    self.flood_fill(x, y, numero)
                    numero += 1

    def flood_fill(self, x, y, numero):

        jono = [(x, y)]
        
        while len(jono) != 0:
            x, y = jono.pop(0)

            if self.alueet[x][y] != 0 or not self.kartta[x,y].tyhja:
                continue

            self.alueet[x][y] = numero
            
            jono.append((x + 1, y))
            jono.append((x - 1, y))
            jono.append((x, y - 1))
            jono.append((x, y + 1))
    def tee_ovet(self):
        parit = []
        for x in range(1, self.kartta.leveys - 1):
            for y in range(1, self.kartta.korkeus - 1):
                parit.append((x, y))

        random.shuffle(parit)
        yhteydet = defaultdict(lambda: 0)

        def yrita_lisata(x, y, a, b):
            avain = (min(a, b), max(a, b))
            if yhteydet[avain] < 1:
                self.kartta[x,y] = OVI
                yhteydet[avain] += 1

        for x, y in parit:
            up = self.alueet[x][y-1]
            down = self.alueet[x][y+1]
            left = self.alueet[x-1][y]
            right = self.alueet[x+1][y]
            if up != 0 and down != 0 and up != down:
                yrita_lisata(x, y, up, down)  
            if left != 0 and right != 0 and left != right:
                yrita_lisata(x, y, left, right)
