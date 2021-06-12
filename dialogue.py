# dialogue.py
# 维护对话

import pygame
from pygame.locals import *
import sys
import globe

global globaltext

global globaltext

# 对话文本
globaltext = [
    ['みんなー！', 'チルノのさんすう教室はじまるよー！'],
    ['あたいみたいな天才目指して、', 'がんばっていってね！'],
    "showright",
    ['１＋１に等しい?'],
    "showleft",
    ['⑨!!'],
    "showright",
    ['馬鹿!']
]


class TextPlayer(object):
    def __init__(self):
        self.texts = globaltext
        self.index = 0
        self.lpic = globe.destiny.rsManager.image["cirno"]
        self.rpic = globe.destiny.rsManager.image["reimu"]
        self.lpic_av = False
        self.rpic_av = False

        # pygame自带字体无法渲染日文
        self.font = pygame.font.Font(globe.destiny.rsManager.font["JAP1"], 15)

        # 对话框
        self.rc = pygame.Rect(globe.playrc.left, globe.playrc.bottom - 100, globe.playrc.width - 128, 100)

    def command(self, cm=None):
        if cm == "next":
            self.index += 1
        else:
            cm = self.texts[self.index]
            if cm == "showleft":
                self.lpic_av = True
                self.rpic_av = False
                self.index += 1
            elif cm == "showright":
                self.rpic_av = True
                self.lpic_av = False
                self.index += 1

    def update(self):
        if self.index < len(self.texts):
            self.command()
        else:
            globe.scgame.time += 1
            globe.scgame.tstart()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 点Z进入下一句话
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.command("next")

    def draw(self, screen):
        if globe.scgame.timestop:
            if not self.lpic_av:
                screen.fill((200, 200, 200), self.rc, BLEND_RGB_ADD)
                if type(self.texts[self.index]) == str:
                    # 基于文字生成用于渲染的图像
                    txtimg = self.font.render(self.texts[self.index], True, (255, 0, 0))
                    screen.blit(txtimg, self.rc.topleft)
                elif type(self.texts[self.index]) == list:
                    for i in range(len(self.texts[self.index])):
                        txtimg = self.font.render(self.texts[self.index][i], True, (255, 0, 0))
                        screen.blit(txtimg, (self.rc.left, self.rc.top + i * 40))
                if self.rpic_av:  # 句子在右边显示
                    tprc = self.rpic.get_rect()
                    tprc.bottomleft = self.rc.bottomright
                    screen.blit(self.rpic, tprc)
                elif self.lpic_av:  # 句子在左边显示
                    tprc = self.lpic.get_rect()
                    tprc.bottomright = self.rc.bottomleft
                    screen.blit(self.lpic, tprc)

            else:
                tp = self.rc.copy()
                tp.left += 128
                screen.fill((200, 200, 200), tp, BLEND_RGB_ADD)

                if type(self.texts[self.index]) == str:
                    txtimg = self.font.render(self.texts[self.index], True, (255, 0, 0))
                    screen.blit(txtimg, tp.topleft)
                elif type(self.texts[self.index]) == list:
                    for i in range(len(self.texts[self.index])):
                        txtimg = self.font.render(self.texts[self.index][i], True, (255, 0, 0))
                        screen.blit(txtimg, (tp.left, tp.top + i * 40))
                if self.rpic_av:
                    tprc = self.rpic.get_rect()
                    tprc.bottomleft = tp.bottomright
                    screen.blit(self.rpic, tprc)
                elif self.lpic_av:
                    tprc = self.lpic.get_rect()
                    tprc.bottomright = tp.bottomleft
                    screen.blit(self.lpic, tprc)
