import random


class Generation:
    def __init__(self, bioms, massive):
        self.bioms = bioms
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
        self.procent[0][0] = 10
        self.masbiom[0][0] = random.choice(self.bioms)

    def smoof_generation(self, count=0, fl1=True, fl2=True, fl3=True):
        for i in range(1, len(self.masbiom) - 1):
            for j in range(1, len(self.masbiom[i]) - 1):
                self.masbiom[i][j] = random.choice(
                    [self.masbiom[i - 1][j], self.masbiom[i + 1][j], self.masbiom[i][j + 1], self.masbiom[i][j - 1]])
        for i in range(1, len(self.masbiom) - 1):
            for j in range(1, len(self.masbiom[i]) - 1):
                spis = [self.masbiom[i - 1][j], self.masbiom[i][j - 1], self.masbiom[i + 1][j], self.masbiom[i][j + 1]]
                if self.masbiom[i - 1][j] == self.masbiom[i][j - 1] and self.masbiom[i + 1][j] == self.masbiom[i][
                    j + 1] and self.masbiom[i + 1][j] == self.masbiom[i - 1][j] and fl1:
                    self.masbiom[i][j] = self.masbiom[i][j - 1]
                elif self.masbiom[i][j] not in [self.masbiom[i - 1][j], self.masbiom[i][j - 1], self.masbiom[i + 1][j],
                                                self.masbiom[i][j + 1]] and fl2:
                    self.masbiom[i][j] = random.choice(spis)
                elif spis.count(max(spis)) > spis.count(min(spis)) and fl3:
                    self.masbiom[i][j] = max(spis)
                elif spis.count(max(spis)) < spis.count(min(spis)) and fl3:
                    self.masbiom[i][j] = min(spis)
        if count == 0:
            return self.masbiom
        return self.smoof_generation(count - 1, fl1, fl2, fl3)

    def reversive_world(self):
        new_world = list()
        print(len(self.masbiom[0]), len(self.masbiom))
        for i in range(len(self.masbiom[0])):
            prom = list()
            for j in range(len(self.masbiom)):
                prom.append(self.masbiom[j][i])
            new_world.append(prom)
        return new_world

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
                    self.add_on_world(klak, llack, 9, instx, insty, 'stone')
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

    def generation(self):
        pr = 5
        for i in range(len(self.masbiom)):
            prom = list()
            for j in range(len(self.masbiom[i])):
                if i == 0 and j != 0:
                    res = self.procent[i][j - 1] > random.randint(1, 10)
                    self.masbiom[i][j] = self.masbiom[i][j - 1] if res else random.choice(self.bioms)
                    self.procent[i][j] = random.randint(self.procent[i][j - 1] - pr, 10) if res else 10
                elif j == 0 and i != 0:
                    res = self.procent[i - 1][j] > random.randint(1, 10)
                    self.masbiom[i][j] = self.masbiom[i - 1][j] if res else random.choice(self.bioms)
                    self.procent[i][j] = random.randint(self.procent[i - 1][j] - pr, 10) if res else 10
                elif i != 0 and j != 0:
                    up_left = True if self.procent[i][j - 1] > self.procent[i - 1][j] else False
                    res = max(self.procent[i][j - 1], self.procent[i - 1][j]) > random.randint(1, 10)
                    if not up_left:
                        self.masbiom[i][j] = self.masbiom[i][j - 1] if res else random.choice(self.bioms)
                    else:
                        self.masbiom[i][j] = self.masbiom[i - 1][j] if res else random.choice(self.bioms)
                    self.procent[i][j] = max(random.randint(self.procent[i][j - 1] - pr, 10),
                                             random.randint(self.procent[i - 1][j] - pr, 10)) if res else 10

        return self.masbiom
