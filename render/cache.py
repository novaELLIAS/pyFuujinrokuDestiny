# cache.py
# 缓存(处理)页面内容的变化

import pygame
from pygame.locals import *

global image
global hue


def cache_init():
    global image
    global hue
    image = {}
    hue = {}


def cache_rotate(img, theta, flag=False):
    # 处理旋转. 图像, 旋转角, 是否存储生成
    global image

    if img not in image:
        cache_buffer(img)

    if theta in image[img][0]:
        # 如果有贴图, 则返回贴图
        return image[img][0][theta]
    else:
        if flag:
            # 存储生成的旋转贴图
            image[img][0][theta] = pygame.transform.rotate(img, theta)
            return image[img][0][theta]
        else:
            # 不存储生成的旋转贴图
            return pygame.transform.rotate(img, theta)


def cache_inter_change_alpha(img, alpha):
    # 逐像素更改透明度
    tmp = pygame.Surface(img.get_size()).convert_alpha()
    tmp.lock()
    for i in range(tmp.get_width()):
        for j in range(tmp.get_height()):
            cl = img.get_at((i, j))
            if cl.a != 0:
                cl.a = alpha
            tmp.set_at((i, j), cl)
    tmp.unlock()
    return tmp


def cache_set_alpha(img, alpha, flag=False):
    # 直接设定透明度, flag定义以及后续操作与上文类似
    global image
    if img not in image:
        cache_buffer(img)
    if alpha in image[img][1]:
        return image[img][1][alpha]
    else:
        if flag:
            image[img][1][alpha] = cache_inter_change_alpha(img, alpha)
            image[img][1][alpha].fill((100, 0, 100, 40), None, BLEND_RGB_ADD)
            return image[img][1][alpha]
        else:
            return cache_inter_change_alpha(img, alpha)


def cache_flip(img, flag=False):
    # 翻转
    global image
    if img not in image:
        cache_buffer(img)
    if image[img][2] is not None:
        return image[img][2]
    else:
        if not flag:
            tp = pygame.transform.flip(img, True, False)
            return tp
        else:
            image[img][2] = pygame.transform.flip(img, True, False)
            return image[img][2]


def cache_create_mask(img, color):
    # 创建遮罩
    img.fill(color, None, BLEND_RGB_ADD)


def cache_buffer(img):
    # 新建实例
    global image
    if img in image:
        return
    else:
        image[img] = [{}, {}, None]
        # 旋转, 透明度, 镜像翻转


def cache_set_mask(img, color, flag=False):
    # 应用遮罩
    if img not in hue:
        hue[img] = {}
    if color not in hue[img]:
        if flag:
            hue[img][color] = img.copy()
            hue[img][color].fill(color, None, BLEND_RGB_ADD)
            return hue[img][color]
        else:
            tp = img.copy()
            tp.fill(color, None, BLEND_RGB_ADD)
            return tp
    else:
        return hue[img][color]
