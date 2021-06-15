# hud.py
# 这个模块用于维护屏幕右侧的信息显示.

import pygame
from utility import globe


class Hud(object):
    def __init__(self, blood=None):
        # 构造定位点, 声明字体
        self.picture = globe.destiny.rsManager.image["front00"]
        self.dot = self.picture.subsurface(339, 33, 6, 6)
        self.posi = []
        self.posi.append((32, 0, 384, 16))
        self.posi.append((32, 464, 384, 16))
        self.posi.append((0, 0, 32, 480))
        self.posi.append((416, 0, 224, 480))
        self.posi.append((432, 50, 64, 40))
        self.posi.append((432, 105, 64, 40))
        self.im = []
        self.im.append(self.picture.subsurface(0, 480, 384, 16))
        self.im.append(self.picture.subsurface(0, 496, 384, 16))
        self.im.append(self.picture.subsurface(0, 0, 32, 480))
        self.im.append(self.picture.subsurface(32, 0, 224, 480))
        self.im.append(self.picture.subsurface(256, 0, 64, 40))
        self.im.append(self.picture.subsurface(256, 40, 64, 40))
        self.num = []
        for i in range(0, 10):
            self.num.append(self.picture.subsurface(335 + 16 * i, 0, 16, 20))
        self.dot = self.picture.subsurface(339, 33, 6, 6)
        self.star = self.picture.subsurface(496, 3, 16, 14)
        self.bouns = self.picture.subsurface((267, 100, 221, 28))
        self.fb = 0  # b: bonus
        self.failed = self.picture.subsurface((267, 387, 138, 28))
        self.ff = 0  # f: fail

        self.blood = blood
        self.blood_show = False
        self.font_bimini = pygame.font.Font(globe.destiny.rsManager.font["bimini"], 19)

        self.bonusCnt = 1

    def create_bonus(self, fp=60):
        # 创建"get spell card bonus"字样
        self.fb = fp
        self.ff = 0

    def create_failed(self, fp=60):
        # 创建"bonus fail"字样
        self.ff = fp
        self.fb = 0

    def change_blood(self, blo_bool):
        # 转移血量数据
        self.blood_show = blo_bool

    def draw(self, screen):
        for i in range(0, 6):
            screen.blit(self.im[i], self.posi[i])
        # 绘制基础元素

        score = globe.scgame.score
        hiscore = globe.scgame.hiscore
        if globe.hiscore > hiscore:
            hiscore = globe.hiscore
            globe.scgame.hiscore = globe.hiscore

        if hiscore > 999999999:
            hiscore = 999999999
        if score > 999999999:
            score = 999999999
        # 分数不能溢出
        if hiscore < score:
            hiscore = score
            globe.scgame.hiscore = globe.scgame.score

        if score/500000 >= self.bonusCnt:
            globe.scgame.player.life += 1
            globe.destiny.msManager.play_SE("extend")
            globe.scgame.blManager.clear_enbl()
            globe.scgame.itManager.getitem()
            self.bonusCnt += 1

        if globe.hiscore < globe.scgame.hiscore:
            globe.hiscore = globe.scgame.hiscore
        # 更新最高分

        life = globe.scgame.player.life
        power = globe.scgame.player.power

        for i in range(0, 9):
            screen.blit(self.num[int(hiscore / (10 ** (8 - i))) % 10], (500 + 15 * i, 50))
        for i in range(0, 9):
            screen.blit(self.num[int(score / (10 ** (8 - i))) % 10], (500 + 15 * i, 70))
        for i in range(0, life):
            screen.blit(self.star, (500 + i * 16, 111))

        screen.blit(self.dot, (500 + 15, 125 + 13))

        screen.blit(self.num[int(power / 100)], (500, 125))
        screen.blit(self.num[int(power % 100 / 10)], (518, 125))
        screen.blit(self.num[int(power % 10)], (532, 125))
        # 将数字元素绘制到屏幕上

        if self.fb > 0:
            self.fb -= 1
            screen.blit(self.bouns, (115, 116))

        if self.ff > 0:
            self.ff -= 1
            screen.blit(self.failed, (156, 131))
        # 处理上文提到的"bonus"的两种字样

        if self.blood_show:
            max_heal_card = self.blood.max_heal_card  # 符卡最大血量上限
            now_heal_card = self.blood.now_heal_card  # 现在符卡血量
            max_heal_nosc = self.blood.max_heal_nosc  # 非符最大血量上限
            now_heal_nosc = self.blood.now_heal_nosc  # 现在非符血量

            card_per = self.blood.card_per  # 符卡百分比 <1
            nosc_per = self.blood.nosc_per  # 非符百分比 <1

            len1 = globe.playrc.width * card_per * now_heal_card / max_heal_card
            len2 = globe.playrc.width * nosc_per * now_heal_nosc / max_heal_nosc

            if len2 < 0:
                len2 = 0

            d = 32 + int(len1)
            pygame.draw.line(screen, (255, 0, 0), (32, 16), (d, 16))
            # 符卡血量为红色, 处于左侧位置
            pygame.draw.line(screen, (255, 255, 255), (d, 16), (d + int(len2), 16))
            # 非符血量为白色, 处于右侧位置
        # 在boss战中的显示元素: boss进度

        font = self.font_bimini
        grz = str(globe.scgame.graze)
        gzimg = font.render("Graze  " + grz, True, (255, 255, 255))
        rc = gzimg.get_rect()
        rc.bottomleft = (444, 170)
        globe.destiny.screen.blit(gzimg, rc)
