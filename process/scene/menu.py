# menu.py
# 维护暂停界面

import pygame
from pygame.locals import *
import sys
from utility import globe
from process.scene import menu_confirm
from PIL import Image, ImageFilter


class Pause_Menu(object):
    # 暂停页面

    def __init__(self):
        self.button_rect = []
        self.rs = globe.destiny.rsManager.image
        self.pause_title = self.rs["menu_title"]
        self.confirm_title = self.rs["confirm_title"]

        self.button_rect.append([100, 220])  # Resume_Start
        self.button_rect.append([100, 260])  # To_Title_Start
        self.button_rect.append([90, 300])  # Retry_Start

        self.image = []
        self.image.append(self.rs["Resume_Start"])  # index: 0
        self.image.append(self.rs["To_Title_Start"])  # index: 1
        self.image.append(self.rs["Retry_Start"])  # index: 2

        self.index = 3
        globe.scene_menu_choose = False  # 按键状态
        # 为全局变量是便于二级菜单对状态的重置

    def replace(self):
        if self.index ^ 3:
            self.image[self.index].set_alpha(90)
        self.index = 3

    def update(self):
        if not globe.scene_menu_choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_UP:
                        if self.index == 3:
                            self.index = 1
                        if self.index != 0:
                            self.index -= 1
                            self.button_rect[self.index][0] -= 5      # 按键微移
                            self.image[self.index].set_alpha(1000)    # 增大透明度, 突出显示
                            self.button_rect[self.index + 1][0] += 5  # 按键微移
                            self.image[self.index + 1].set_alpha(90)  # 重置透明度
                            globe.destiny.msManager.play_SE("select")
                        else:
                            self.index = 2
                            self.button_rect[self.index][0] -= 5
                            self.image[self.index].set_alpha(1000)
                            self.button_rect[0][0] += 5
                            self.image[0].set_alpha(90)
                            globe.destiny.msManager.play_SE("select")
                    if event.key == K_DOWN:
                        if self.index == 3:
                            self.index = 2
                        if self.index != 2:
                            self.index += 1
                            self.button_rect[self.index][0] -= 5
                            self.image[self.index].set_alpha(1000)
                            self.button_rect[self.index - 1][0] += 5
                            self.image[self.index - 1].set_alpha(90)
                            globe.destiny.msManager.play_SE("select")
                        else:
                            self.index = 0
                            self.button_rect[self.index][0] -= 5
                            self.image[self.index].set_alpha(1000)
                            self.button_rect[2][0] += 5
                            self.image[2].set_alpha(90)
                            globe.destiny.msManager.play_SE("select")

                    if event.key == K_z and self.index ^ 3:
                        globe.scene_menu_choose = True
                        globe.destiny.msManager.play_SE("select")
                    if event.key == K_ESCAPE:
                        self.replace()
                        globe.destiny.msManager.unpause()
                        globe.destiny.back()
        else:
            if self.index == 0:  # 返回游戏
                self.replace()
                globe.destiny.back()
                globe.destiny.msManager.unpause()
            if self.index == 1:  # 选择了选单第一项, 跳转到确认页面
                self.replace()
                globe.scene_menu_flag = 1
                globe.destiny.call(menu_confirm.Scene_Menu_Confirm)
            if self.index == 2:  # 选择了选单第二项, 跳转到确认页面
                self.replace()
                globe.scene_menu_flag = 2
                globe.destiny.call(menu_confirm.Scene_Menu_Confirm)

    def draw(self, screen):
        screen.blit(self.pause_title, (160, 140))
        for i in range(0, 3):
            screen.blit(self.image[i], self.button_rect[i])

    def start(self):
        pass

    def stop(self):
        pass


class Scene_Menu(object):
    # 游戏背景糊化类

    def __init__(self):
        self.rs = globe.destiny.rsManager
        self.menu = Pause_Menu()
        self.count = 0
        self.fade = pygame.Surface(globe.destiny.screen.get_size())
        self.imgtmp = globe.destiny.screen.subsurface(Rect(30, 14, 388, 452)).copy()

        # 使用枕头库模糊化游戏窗口
        for i in range(0, 3):
            # 转换PyGame图像为pillow图像
            raw_str = pygame.image.tostring(self.imgtmp, "RGBA", False)
            image = Image.frombytes("RGBA", self.imgtmp.get_size(), raw_str)
            imgblur = image.filter(ImageFilter.BLUR)
            # 转换pillow图像为PyGame图像
            raw_str = imgblur.tobytes("raw", "RGBA")
            imgblur_pygame = pygame.image.fromstring(raw_str, imgblur.size, "RGBA")
            self.imgtmp = imgblur_pygame
            globe.game_active_bg_blured = imgblur_pygame

    def update(self):
        self.menu.update()

    def draw(self, screen):
        screen.blit(self.imgtmp, (30, 14))
        self.menu.draw(screen)

    def start(self):
        pass

    def stop(self):
        pass
