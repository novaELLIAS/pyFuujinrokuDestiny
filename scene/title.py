# scene::title 标题界面.

import pygame
from pygame.locals import *
import sys
import globe
from scene import game, loading


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
                    pygame.quit()
                    sys.exit()
                else:
                    if self.flash >= 40:
                        globe.destiny.msManager.stop()
                        globe.destiny.navigate_to = game.Scene_Game
                        globe.destiny.sync_flag = False
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

    def update(self):
        self.menu.update()

    def draw(self, screen):
        screen.blit(self.rs.image["background"], (0, 0))
        self.menu.draw(screen)
