# gameover.py
# 这个模块用于维护游戏结束画面

import pygame
from pygame.locals import *
import sys

from utility import globe

from process.scene import game, loading, title
from PIL import Image, ImageFilter


class PauseMenu(object):
	# 选单界面

	def __init__(self):
		self.rs = globe.destiny.rsManager.image
		self.button_rect = []

		self.button_rect.append([100, 220])  # "To_Title_Start"按键位置
		self.button_rect.append([90, 260])   # "Retry_Start"按键位置

		self.image = []
		self.image.append(self.rs["To_Title_Start"])  # 0
		self.image.append(self.rs["Retry_Start"])     # 1
		self.index = 3  # 选项标识符, 默认为不可用
		self.choose = False

	def replace(self):
		if self.index ^ 3:
			self.image[self.index].set_alpha(90)
		self.index = 3

	def update(self):

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
						if self.index == 3:
							self.index = 1
						self.index ^= 1
						self.button_rect[self.index][0] -= 5
						self.image[self.index].set_alpha(1000)
						self.button_rect[self.index ^ 1][0] += 5
						self.image[self.index ^ 1].set_alpha(90)
						globe.destiny.msManager.play_SE("select")
					if event.key == K_z and self.index ^ 3:
						self.choose = True
						globe.destiny.msManager.play_SE("select")
					if event.key == K_ESCAPE:
						self.index = 0
						self.choose = True
		else:
			if self.index == 0:
				# To title
				self.replace()
				globe.destiny.navigate_to = title.Scene_Title
				globe.destiny.sync_flag = ["sync", "getrank"]
				globe.destiny.goto(loading.Scene_Loading)
			if self.index == 1:
				# Replay
				self.replace()
				globe.destiny.navigate_to = game.Scene_Game
				globe.destiny.sync_flag = ["sync"]
				globe.destiny.goto(loading.Scene_Loading)

	def draw(self, screen):

		for i in range(0, 2):
			screen.blit(self.image[i], self.button_rect[i])


class Scene_GameOver(object):

	def __init__(self):
		self.rs = globe.destiny.rsManager.image
		self.myfont = pygame.font.SysFont(None, 60)
		self.menu = PauseMenu()
		self.imgtmp = globe.destiny.screen.subsurface(Rect(30, 14, 388, 452)).copy()

		globe.destiny.msManager.stop()

		# 参考menu.py
		for i in range(0, 3):
			raw_str = pygame.image.tostring(self.imgtmp, "RGBA", False)
			image = Image.frombytes("RGBA", self.imgtmp.get_size(), raw_str)
			imgblur = image.filter(ImageFilter.BLUR)
			raw_str = imgblur.tobytes("raw", "RGBA")
			imgblur_pygame = pygame.image.fromstring(raw_str, imgblur.size, "RGBA")
			self.imgtmp = imgblur_pygame

		globe.scgame.score += globe.scgame.player.life * 500 * (1 + globe.scgame.player.power)

		if globe.scgame.player.life < 0:
			# 满身疮痍
			globe.destiny.msManager.play_BGM("gameover")
			self.title = self.rs["Dead"]
		else:
			# 演目终演
			globe.destiny.msManager.play_BGM("win")
			self.title = self.rs["Clear"]

	def start(self):
		pass

	def stop(self):
		pass

	def update(self):
		self.menu.update()

	def draw(self, screen):
		screen.blit(self.imgtmp, (30, 14))
		screen.blit(self.title, (160, 140))
		self.menu.draw(screen)
		globe.scgame.hud.draw(screen, False)
