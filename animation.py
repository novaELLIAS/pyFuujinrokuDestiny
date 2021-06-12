# animation.py
# 这个模块用于维护页面上的所有动画和单帧素材.

class Anime(object):

	def __init__(self, anime, pos, fps=1):
		self.anime = anime
		self.frame = len(anime)
		self.fps = fps
		self.now_frame = 0
		self.now_pic = 0
		self.pos = pos
		# 参数定义:
		# anime: 动画列表
		# frame: 帧计数
		# fps: 帧率
		# pos: 放映位置


class AnimeManager(object):

	def __init__(self):
		self.La = []
		# La(List of animation): 存储动画
		self.Lf = []
		# Lf(List of frame): 单帧存储
		self.frame = 0
		# 维持帧数

	def create_anime(self, anime, pos, fps=1):
		self.La.append(Anime(anime, pos, fps))
		# 素材名, 放映位置, 剩余帧数
		# 这里有一个bug, 如果帧数不+1的话第一帧就无法播放, 目前没找到原因.
		# 在实际测试中发现pos为tuple和rect都是可行的.

	def create_pic(self, pic, frame, pos):
		self.Lf.append([pic, frame, pos, 0])
		# 素材名, 帧数, 放映位置

	def update(self):
		# 动画列表更新.
		# 维护动画和单帧的生命周期.zz
		for i in self.La:
			i.now_frame += 1
			if i.now_frame % i.fps == 0:
				i.now_pic += 1
				if i.now_pic >= i.frame:
					self.La.remove(i)
		for i in self.Lf:
			if i[3] >= i[1]:
				self.Lf.remove(i)
		self.frame += 1

	def draw(self, screen):
		# 将所有动画绘制到屏幕上.
		for i in self.La:
			screen.blit(i.anime[i.now_pic], i.pos)
		for i in self.Lf:
			screen.blit(i.pic, i.pos)
