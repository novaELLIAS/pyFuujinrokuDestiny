# enemy.py
# 用于维护敌机

import pygame
from pygame.locals import *
import globe

global entype


class EnemyType(object):
    # 敌机类, 存储敌机信息

    def __init__(self, anime, maxhealth, fbuff=None):
        # 动画类型, 最大生命值, 特殊效果(函数指针)
        self.anime = anime
        self.maxhealth = maxhealth
        self.fbuff = fbuff

    def copy(self):
        return EnemyType(self.anime, self.maxhealth, self.fbuff)

    def buff(self, point):
        if self.fbuff is not None:
            self.fbuff(point)


class Enemy(object):
    def __init__(self, entype, orbit, oristatus, bump=False, wdtime=0):
        # 敌机类型, 轨迹, 初始状态, 是否抗撞, 无敌时间

        self.entype = entype
        self.orbit = orbit
        self.status = oristatus

        self.health = self.entype.maxhealth
        # 数据类型自适应
        if type(self.entype.anime) == dict:
            self.image = self.entype.anime["stay"][0]
            self.rect = self.image.get_rect()
            self.rect.center = orbit.point
        elif type(self.entype.anime) == pygame.Surface:
            self.image = self.entype.anime
            self.rect = self.image.get_rect()
            self.rect.center = orbit.point
        self.frame = 0

        self.bump = bump

        self.wdtime = wdtime
        # 更新无敌时间
        if wdtime > 0:
            self.wudi = True
        else:
            self.wudi = False

    def crash(self):
        # 敌机被击破
        if not self.wudi:
            if self.health <= 0 and self.status == globe.enstatus["normal"]:
                # 追加效果
                self.entype.buff(self.orbit.point)
            self.status = globe.enstatus["dead"]

    def tishu(self):
        # 体术
        if not self.bump:
            # 如果不抗撞, 被撞坠机
            self.health = 0
            self.crash()
        elif self.bump:
            # 如果抗撞, 将自机撞落
            globe.scgame.player.hit()
        elif self.bump is None:
            pass


class Boss(object):  # BOSS类
    def __init__(self, entypes, orbits, oristatus, life=2, bump=True, wdtime=0):
        # 敌机类型, 轨迹, 初始状态, 符卡数量, 是否抗撞, 无敌时间
        self.life = life
        self.entypes = entypes
        self.orbits = orbits
        self.status = oristatus
        self.bump = bump
        self.wdtime = wdtime

        self.entype = entypes[0]
        self.orbit = orbits[0]
        self.index = 0

        self.frame = 0

        if type(self.entype.anime) == dict:
            self.image = self.entype.anime["stay"][0]
            self.rect = self.image.get_rect()
            self.rect.center = self.orbit.point
        elif type(self.entype.anime) == pygame.Surface:
            self.image = self.entype.anime
            self.rect = self.image.get_rect()
            self.rect.center = self.orbit.point

        if wdtime > 0:
            self.wudi = True
        else:
            self.wudi = False
        self.health = self.entype.maxhealth

    def crash(self):
        if not self.wudi:
            if self.health <= 0 and self.status == globe.enstatus["normal"]:
                self.entype.buff(self.orbit.point)
            if self.life > 0:
                # 符卡超时, 判定为全避, 切换符卡
                self.frame = 0
                self.index += 1
                self.entype = self.entypes[self.index]
                self.orbit = self.orbits[self.index]
                self.health = self.entype.maxhealth


class EnemyManager(object):

    def __init__(self):
        self.frame = 0

        enstatus = {"normal": 0, "wudi": 1, "dead": 2, "del": 3}
        # 通常状态, 无敌状态, 被击破, 超出界面被消除
        globe.enstatus = enstatus

        self.enemy = []

        global entype

        rs = globe.destiny.rsManager.anime
        entype = {}
        for i in range(8):
            tp = "sprite" + str(i)
            anime = {"stay": rs["enemy"][i][0], "toright": rs["enemy"][i][1], "right": rs["enemy"][i][2],
                     "toleft": rs["enemy"][i][3], "left": rs["enemy"][i][4]}
            # 停止, 右转, 右行, 左转, 左行
            entype[tp] = EnemyType(anime, 6000)
        anime = {"stay": rs["enemy"][8]}
        entype["butterfly"] = EnemyType(anime, 60000)
        for i in range(4):
            tp = "maoyu" + str(i)
            # 毛玉
            entype[tp] = EnemyType(rs["enemy"][9 + i], 6000)

        for i in range(4):
            tp = "guihuo" + str(i)
            # 鬼火
            anime = {"stay": rs["enemy2"][i]}
            entype[tp] = EnemyType(anime, 6000)

        anime = {"stay": rs["cirno"][0], "toleft": rs["cirno"][1], "toright": rs["cirno"][2]}
        entype["cirno"] = EnemyType(anime, 0)
        # boss

        globe.entype = entype

    def create_enemy(self, entype, orbit, oristatus=0, bump=False, wdtime=0):
        # 创建敌机(对外接口)
        tp = Enemy(entype, orbit, oristatus, bump, wdtime)
        self.enemy.append(tp)
        return tp

    def create_boss(self, entypes, orbits, oristatus=0, life=2, bump=True, wdtime=0):
        # 创建boss(对外接口)
        tp = Boss(entypes, orbits, oristatus, life, bump, wdtime)
        self.enemy.append(tp)
        return tp

    def update(self):

        # 根据自机火力判断伤害
        if globe.scgame.player.power >= 500:
            damage = 120
        else:
            damage = 100 + int((globe.scgame.player.power % 100) / 5)
            # 100基础伤害, 阴阳玉伤害累加
        for i in self.enemy:
            if i.orbit.update is not None:
                # 维护轨迹
                i.orbit.update(i)
            if i.wudi:
                # 维护无敌时间
                i.wdtime -= 1
                if i.wdtime <= 0:
                    i.wudi = False
            if i.status == globe.enstatus["normal"]:
                if i.rect.collidepoint(globe.scgame.player.point):
                    i.tishu()  # 撞上
                else:
                    for j in globe.scgame.blManager.plbullet:
                        if j[0].colliderect(i.rect) and i.status == globe.enstatus["normal"]:
                            # 被自机击中
                            globe.scgame.blManager.plbullet.remove(j)
                            globe.destiny.msManager.play_SE("damage")
                            globe.scgame.score += damage
                            if not i.wudi:
                                i.health -= damage
                                if i.health <= 0:
                                    i.crash()
        self.frame += 1
        for i in self.enemy:
            # 飞出去, 被清除
            if i.status == globe.enstatus["del"]:
                self.enemy.remove(i)

    def draw(self, screen):
        for i in self.enemy:
            if i.status != globe.enstatus["del"] and i.status != globe.enstatus["dead"]:
                screen.blit(i.image, i.rect)
