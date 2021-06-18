# scene::title 标题界面.

import pygame
from pygame.locals import *
import sys
from utility import globe
from process.scene import game, loading


class Title_Menu(object):

    def __init__(self):
        self.rectList = []
        self.rs = globe.destiny.rsManager.image
        self.rectList.append([495, 200])
        self.rectList.append([500, 240])
        self.image = []
        self.image.append(self.rs["startb"])
        self.image.append(self.rs["startd"])
        self.image.append(self.rs["quitb"])
        self.image.append(self.rs["quitd"])

        self.index = 0
        # index==1: 退出, 否则开始

        self.choose = False
        # "已确定"选择状态

        self.flash = 0
        self.mask = pygame.Surface(globe.destiny.screen.get_size())
        self.mask.fill((0, 0, 0))
        # 图像蒙版

        globe.destiny.msManager.stop()
        globe.destiny.msManager.play_BGM("title")

    def update(self):
        # 选择支
        if not self.choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP or event.key == K_DOWN:
                        self.index ^= 1
                        self.rectList[self.index][0] -= 5
                        self.rectList[self.index ^ 1][0] += 5
                        globe.destiny.msManager.play_SE("select")
                    if event.key == K_z:
                        self.choose = True
                        globe.destiny.msManager.play_SE("select")
        else:
            self.flash += 1
            if self.flash >= 20:
                if self.index == 1:
                    # 用户退出登录
                    if globe.online:
                        globe.destiny.dbManager.logout()
                    pygame.quit()
                    sys.exit()
                else:
                    if self.flash >= 40:
                        globe.destiny.msManager.stop()
                        globe.destiny.navigate_to = game.Scene_Game
                        globe.destiny.sync_flag = []
                        globe.destiny.goto(loading.Scene_Loading)

            if self.flash % 2 == 0 and self.flash <= 40:
                # 处理选择后的素材抖动效果
                tmp = self.image[self.index * 2]
                self.image[self.index * 2] = self.image[self.index * 2 + 1]
                self.image[self.index * 2 + 1] = tmp

    def draw(self, screen):
        # 将元素绘制到屏幕上
        screen.blit(self.image[self.index], self.rectList[0])
        screen.blit(self.image[3 - self.index], self.rectList[1])
        if self.flash >= 20:
            self.mask.set_alpha((self.flash - 20) * 12)
            screen.blit(self.mask, (0, 0))


class Scene_Title(object):

    def __init__(self):
        self.rs = globe.destiny.rsManager
        self.menu = Title_Menu()

        # ranklist
        self.imglist = list()
        self.reclist = list()

        myfont15 = pygame.font.Font(globe.destiny.rsManager.font["cour"], 15)
        myfontdb30 = pygame.font.Font(globe.destiny.rsManager.font["courdb"], 30)
        myfontdb18 = pygame.font.Font(globe.destiny.rsManager.font["courdb"], 18)

        # 用户名
        img = myfontdb30.render(globe.username, True, (0, 0, 0))
        rec = img.get_rect()
        rec.topleft = (10, 10)
        self.imglist.append(img)
        self.reclist.append(rec)

        # 历史最高成绩
        img = myfont15.render("score: " + str(globe.hiscore), True, (0, 0, 0))
        rec = img.get_rect()
        rec.topleft = (10, 40)
        self.imglist.append(img)
        self.reclist.append(rec)

        if globe.online:
            # 个人排名
            notlegendflag = True
            for i in globe.ranklist:
                if i.get("username") == globe.username:
                    img = myfont15.render("rank: " + str(i.get("rank")), True, (0, 0, 0))
                    notlegendflag = False
                    break
            if notlegendflag:
                img = myfont15.render("Not on List of Legends.", True, (0, 0, 0))
            rec = img.get_rect()
            rec.topleft = (10, 55)
            self.imglist.append(img)
            self.reclist.append(rec)

            # 英雄榜排名靠前
            index = 1
            nowpos = 75

            img = myfontdb18.render("1.", True, (0, 0, 0))
            rec = img.get_rect()
            rec.topleft = (10, nowpos)
            self.imglist.append(img)
            self.reclist.append(rec)

            img = myfontdb18.render(globe.ranklist[0]["username"], True, (0, 0, 0))
            rec = img.get_rect()
            rec.topleft = (50, nowpos)
            self.imglist.append(img)
            self.reclist.append(rec)

            img = myfontdb18.render(str(globe.ranklist[0]["score"]), True, (0, 0, 0))
            rec = img.get_rect()
            rec.topright = (350, nowpos)
            self.imglist.append(img)
            self.reclist.append(rec)

            for i in range(1, min(len(globe.ranklist), 20)):
                if globe.ranklist[i]["score"] != globe.ranklist[i - 1]["score"]:
                    index += 1

                img = myfontdb18.render(str(index) + '.', True, (0, 0, 0))
                rec = img.get_rect()
                rec.topleft = (10, nowpos + i * 20)
                self.imglist.append(img)
                self.reclist.append(rec)

                img = myfontdb18.render(globe.ranklist[i]["username"], True, (0, 0, 0))
                rec = img.get_rect()
                rec.topleft = (50, nowpos + i * 20)
                self.imglist.append(img)
                self.reclist.append(rec)

                img = myfontdb18.render(str(globe.ranklist[i]["score"]), True, (0, 0, 0))
                rec = img.get_rect()
                rec.topright = (350, nowpos + i * 20)
                self.imglist.append(img)
                self.reclist.append(rec)

    def update(self):
        self.menu.update()

    def draw(self, screen):

        screen.blit(self.rs.image["background"], (0, 0))
        for i in range(0, len(self.imglist)):
            screen.blit(self.imglist[i], self.reclist[i])

        self.menu.draw(screen)
