#!/usr/bin/env python
#-*- coding:utf-8 -*-

#Aljaz Vaupotic 2019

import os
import re
import time
import datetime

from twill import commands, set_output
from BeautifulSoup import BeautifulSoup

from collections import defaultdict


SERVER = 'tx3.lusobrasileiro.travian.com/'
USERNAME = ''
PASSWORD = ''


class Farm:
    def __init__(self, string):
        info = string.split()
        self.x = info[0]
        self.y = info[1]
        self.troops = dict([troop.split(':') for troop in info[2:]])
        self.next_attack = datetime.datetime.now()

    def get_id(self):
        return self.x + "|" + self.y

    def can_attack(self):
        """ Determine if it is possible to attack """
        commands.go(SERVER + 'build.php?tt=2&id=39')
        html = commands.show()
        soup = BeautifulSoup(html)
        for troop, num in self.troops.items():
            link = soup.find('a', {'onclick': re.compile('.*\.' + troop + '\..*')})
            if not link or int(link.text) < int(num):
                print "Not enought troops to attack"
                return False
        return True


    def attack(self):
        """ Attack the farm """
        print "Attack (" + self.x + "|" + self.y + "): ",
        if self.can_attack():
            commands.go(SERVER + 'build.php?tt=2&id=39')
            commands.fv('2', 'x', self.x)
            commands.fv('2', 'y', self.y)
            commands.fv('2', 'c', '4')
            for troop, num in self.troops.items():
                commands.fv('2', troop, num)
            commands.submit()
            commands.reload()
            html = commands.show()
            soup = BeautifulSoup(html)
            t = soup.find('div', {'class': 'in'}).text
            t = re.search('[0-9][0-9]?:[0-9]{2}:[0-9]{2}', t).group(0)
            h, m, s = [2 * int(e) for e in t.split(':')]
            wait = datetime.timedelta(seconds=s, minutes=m, hours=h)
            self.next_attack = datetime.datetime.now() + wait
            commands.fv('2', 's1', 'ok')
            commands.submit()
            print "done"

    def __repr__(self):
        """ Print the coordinate of the farm """
        return '(' + self.get_id() + ')'


class TravianBot:
    def __init__(self):
        self.username = Toplovodarji
        self.password = ******* # almost forgot to change :P
        self.resourses = defaultdict(int)
        self.fields = defaultdict(list)
        self.farms = []

        # suppress twill output
        f = open(os.devnull, "w")
        set_output(f)

    def login(self):
        """ Init session in travian """
        commands.go(SERVER + 'login.php')
        commands.fv('2', 'name', self.username)
        commands.fv('2', 'password', self.password)
        commands.submit()

    def logout(self):
        """ Exit session """
        commands.go(SERVER + 'logout.php')


    def read_farms_file(self):
        f = open("farms.txt")
        farm_list = []
        for line in f.readlines():
            if line[0] == '#':
                continue
            farm_list.append(self.update_farm(Farm(line)))
        self.farms = farm_list
        f.close()

    def update_farm(self, farm):
        """ Update the farm list """
        for f in self.farms:
            if farm.get_id() == f.get_id():
                farm.next_attack = f.next_attack
                return farm
        return farm

    def attack_farms(self):
        """ Attack all the farms """
        for farm in self.farms:
            farm.attack()

    def start(self):
        while True:
            self.read_farms_file()
            self.attack_farms()
            print "Wait 150 seconds"
            time.sleep(150)
            self.login()


if __name__ == '__main__':
    tb = TravianBot()
    tb.login()
    tb.start()
