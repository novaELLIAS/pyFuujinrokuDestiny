# menu_confirm.py
# 这个模块用于处理暂停界面的二级菜单, 选项确认界面

import pygame
from pygame.locals import *
import sys
from utility import globe
from process.scene import title


class PauseMenu_Confirm(object):

	def __init__(self):

		self.button_rect = []
		self.rs = globe.destiny.rsManager.image
		self.confirm_title = self.rs["confirm_title"]

		self.button_rect.append([170, 240])  # "Yes"按键位置
		self.button_rect.append([170, 280])  # "No"按键位置

		self.image = []
		self.image.append(self.rs["Yes"])  # 0
		self.image.append(self.rs["No"])   # 1

		self.index = 3       # 初始化高亮按键: 默认为无定义
		self.choose = False  # 初始化按键选定状态

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
							if event.key == K_UP:
								self.index = 0
							elif event.key == K_DOWN:
								self.index = 1
							self.button_rect[self.index][0] -= 5      # 按键微移
							self.image[self.index].set_alpha(1000)    # 选中项高亮显示
						else:
							self.index ^= 1
							self.button_rect[self.index][0] -= 5      # 按键微移
							self.image[self.index].set_alpha(1000)    # 选中项高亮显示
							self.button_rect[self.index ^ 1][0] += 5  # 按键微移
							self.image[self.index ^ 1].set_alpha(90)  # 重置透明度
						globe.destiny.msManager.play_SE("select")
					if event.key == K_z and self.index ^ 3:
						self.choose = True
						globe.destiny.msManager.play_SE("select")
					if event.key == K_ESCAPE:
						self.replace()
						globe.scene_menu_choose = False
						globe.destiny.back()
		else:
			if self.index == 0:
				if globe.scene_menu_flag == 1:
					self.replace()
					globe.destiny.call(title.Scene_Title)
				elif globe.scene_menu_flag == 2:
					self.replace()
					globe.scene_menu_choose = False
					globe.scgame.__init__()
					globe.scgame.update()
					globe.destiny.back()
					globe.destiny.back()
			if self.index == 1:
				self.replace()
				globe.scene_menu_choose = False
				# 消除原有选项
				globe.destiny.screen.blit(globe.game_active_bg_blured, (30, 14))
				globe.destiny.back()

	def draw(self, screen):
		screen.blit(globe.game_active_bg_blured, (30, 14))
		screen.blit(self.confirm_title, (160, 180))
		for i in range(0, 2):
			screen.blit(self.image[i], self.button_rect[i])


class Scene_Menu_Confirm(object):
	# 暂停页面的确认页面

	def __init__(self):
		self.rs = globe.destiny.rsManager
		self.menu = PauseMenu_Confirm()
		self.fade = pygame.Surface(globe.destiny.screen.get_size())
		self.imtmp = globe.destiny.screen.subsurface(Rect(30, 14, 388, 452)).copy()

	def update(self):
		self.menu.update()

	def draw(self, screen):
		self.menu.draw(screen)

	def start(self):
		pass

	def stop(self):
		pass
