#!/usr/bin/env python
update={}
class testing():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def house(self):
        global update
        d = self.a + self.b + self.c
        print(d)

        dic={}
        time=""
        f=open('input/availabilities.txt', 'r')
        for l in f:
            k,v = l.strip().split(' ', 1)
            dic[k]=v
        ks=dic.keys()
        ks.sort()
        for k in ks:
            ls=k + " " + dic[k]
            print ls

        if len(update) == 0:
            update = dic

        keys=update.keys()
        keys.sort()
        for k in keys:
            ks=k + " " + update[k]
            print ks

        for k in keys:
            t = k + " " + " ".join(update[k].split()[:2]) + '\n'
            time += t

        print time

if __name__ == "__main__":
    t=testing(1,2,3)
    t.house()
