import random
from numpy import floor
from perlin_noise import PerlinNoise


class Generation:
    def __init__(self, massive):
        self.translate = {0: 'water', 1: 'sand', 2: 'flower', 3: 'forest', 4: 'stone', 5: 'snow'}
        self.procent = list()
        self.masbiom = list()
        self.masive = massive
        self.coord_objects = list()
        self.select_cord_objects = list()
        for i in range(massive):
            prom = list()
            for j in range(massive):
                prom.append(0)
            self.procent.append(prom)
        for i in range(massive):
            prom = list()
            for j in range(massive):
                prom.append(0)
            self.masbiom.append(prom)

    def add_on_world(self, klak, llack, chance, instx, insty, name):
        if random.randint(1, chance) == 1:
            random_x = random.randint(70, 130)
            random_y = random.randint(30, 150)
            klak.append([(instx + random_x, insty + random_y), name, random.randint(0, 1)])
            llack.append([(instx - 50 + random_x, insty - 200 + random_y), name])
        else:
            klak.append([(0, 0), 'None'])
            llack.append([(0, 0), 'None'])

    def xy_objects(self):
        for i in range(len(self.masbiom)):
            prom = list()
            prom2 = list()
            for j in range(len(self.masbiom[i])):
                this_biom = self.masbiom[i][j]
                instx = j * 180
                insty = i * 180
                klak = list()
                llack = list()
                if this_biom == 'forest':
                    self.add_on_world(klak, llack, 4, instx, insty, 'tree')
                elif this_biom == 'stone':
                    self.add_on_world(klak, llack, 9, instx, insty, random.choice(['stone', 'stone', 'stone_pink']))
                else:
                    klak.append([(0, 0), 'None'])
                    llack.append([(0, 0), 'None'])
                prom.append(klak)
                prom2.append(llack)
            self.coord_objects.append(prom)
            self.select_cord_objects.append(prom2)
        return [self.coord_objects, self.select_cord_objects]

    def weathering(self):
        for i in range(1, len(self.masbiom) - 1):
            for j in range(1, len(self.masbiom[i]) - 1):
                close = [self.masbiom[i - 1][j - 1], self.masbiom[i - 1][j], self.masbiom[i - 1][j + 1],
                         self.masbiom[i][j - 1], self.masbiom[i][j + 1], self.masbiom[i + 1][j - 1],
                         self.masbiom[i + 1][j], self.masbiom[i + 1][j + 1]]
                if 'water' in close and self.masbiom[i][j] != 'water' and self.masbiom[i][j] != 'forest':
                    self.masbiom[i][j] = 'sand'

    def add_barier(self, size):
        for i in range(self.masive + size * 2):
            if i < size:
                self.masbiom.insert(0, ['water'] * (self.masive + size * 2))
            elif i >= self.masive + size:
                self.masbiom.append(['water'] * (self.masive + size * 2))
            else:
                self.masbiom[i] = ['water'] * size + self.masbiom[i] + ['water'] * size
        return self.masbiom

    def get_key(self, z):
        if z < -6:
            return 0
        elif z in range(-6, -5):
            return 1
        elif z in range(-5, -4):
            return 2
        elif z in range(-4, 2):
            return 3
        elif z in range(1, 7):
            return 4
        else:
            return 5

    def generation(self):
        seed = random.randint(1000, 9000)
        noise = PerlinNoise(octaves=7, seed=seed)
        amp = 14
        period = 100
        landscale = [[0 for _ in range(self.masive)] for _ in range(self.masive)]
        for position in range(self.masive ** 2):
            x = floor(position / self.masive)
            z = floor(position % self.masive)
            y = floor(noise([x / period, z / period]) * amp)
            landscale[int(x)][int(z)] = self.get_key(int(y))
        for i in range(self.masive):
            for j in range(self.masive):
                self.masbiom[i][j] = self.translate[landscale[i][j]]
        return self.masbiom
