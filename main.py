# main.py
# 程序入口

import pygame
import yaml
from src import resource

from process.scene import loading, title

from utility import globe, database, music
from render import cache


class GameWindow(object):

    def __init__(self):
        # 读取yaml中的设定数据
        globe.logon = False
        f = open("!config.yaml")
        f = yaml.load(f, Loader=yaml.FullLoader)
        globe.username = f["DB"]["user_name"]
        globe.password = f["DB"]["user_password"]
        globe.appid = f["DB"]["appid"]
        globe.appkey = f["DB"]["appkey"]
        globe.useremail = f["DB"]["email"]

    def init(self):
        # 初始化函数, 实测放在__init__中会失效.

        # pygame 页面 时钟 初始化
        pygame.init()
        pygame.mixer.init()
        cache.cache_init()
        self.screen = pygame.display.set_mode([640, 480])
        self.clock = pygame.time.Clock()

        # logo title设定
        logo = pygame.image.load("src\\pic\\magician.ico")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("pyFuujinroku ~Destiny~")

        globe.hiscore = 0

        self.rsManager = resource.ResourceManager()
        self.msManager = music.SoundManager()
        self.dbManager = database.DatabaseManager()
        globe.destiny.navigate_to = title.Scene_Title
        globe.destiny.sync_flag = ["login", "sync", "getrank"]
        self.goto(loading.Scene_Loading)
        self.stack = []

        self.myfont = pygame.font.SysFont(None, 20)

        self.tst = 0

    def goto(self, sc):
        # 直接跳转到指定scene
        self.scene = sc()
        self.scene.update()

    def call(self, sc):
        # 调用scene, 压入栈中
        self.scene.stop()
        self.stack.append(self.scene)
        self.scene = sc()

    def back(self):
        # 从已被调用(call)的scene中返回, 同时退栈
        self.scene.stop()
        self.scene = self.stack.pop()
        self.scene.start()

    def run(self):
        # 维护帧率
        while True:
            self.scene.update()
            # 更新scene
            self.scene.draw(self.screen)
            # 绘制scene

            img = self.myfont.render("fps:" + str(int(self.clock.get_fps() * 100) * 1.0 / 100), True, (255, 255, 255))
            rc = img.get_rect()
            rc.bottomright = (640, 480)
            self.screen.blit(img, rc)
            # 在屏幕右下角展示帧率

            pygame.display.flip()
            self.clock.tick_busy_loop(60)
            self.tst += 1
            # 维护系统时钟


if __name__ == '__main__':
    globe.destiny = GameWindow()
    globe.destiny.init()
    globe.destiny.run()
