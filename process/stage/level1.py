# level1.py
# 用于维护stage1流程

from utility import globe
from object import bullet
from render import orbit
from object import item

import random
import time

from process.scene import gameover

global lbltype
global orb
global scgame
global lentype

global boss

htmp = None


class BloodStruct(object):
    def __init__(self, mhsc, nowsc, mhnsc, nownsc, cp, np):
        self.max_heal_card = mhsc
        self.now_heal_card = nowsc
        self.max_heal_nosc = mhnsc
        self.now_heal_nosc = nownsc
        self.card_per = cp
        self.nosc_per = np


def selfsniper(this):
    # 自击狙快速调用
    if this.frame % 12 == 0 and this.frame <= 90:
        tmp = orbit.quickcreate(1, point=this.point, speed=7, bltype=lbltype["bluecircle"])
        scgame.blManager.create_enbl(lbltype["bluecircle"], tmp)


def downrand(this):
    # 随机下落弹快速调用
    if this.frame % 100 == 0:
        tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 180.0 + 90), speed=3,
                                bltype=lbltype["redsword"])
        scgame.blManager.create_enbl(lbltype["redsword"], tmp)
        tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 180.0 + 90), speed=3,
                                bltype=lbltype["blueball"])
        scgame.blManager.create_enbl(lbltype["blueball"], tmp)


def roundrand(this):
    # 随机大玉快速调用
    if this.frame % 16 == 0:
        tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 360.0), speed=0.8,
                                bltype=lbltype["orangerice"])
        scgame.blManager.create_enbl(lbltype["orangerice"], tmp)


def roundrand2(this):
    if this.frame % 16 == 0:
        if random.random() > 0.25:
            tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 180.0), speed=0.8,
                                    bltype=lbltype["orangerice"])
            scgame.blManager.create_enbl(lbltype["orangerice"], tmp)
        else:
            tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 360.0), speed=0.8,
                                    bltype=lbltype["orangerice"])
            scgame.blManager.create_enbl(lbltype["orangerice"], tmp)


def p2e1roundrand(this):
    if this.frame % 16 == 0:
        tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 180 - 180), speed=2,
                                bltype=lbltype["redrice"])
        scgame.blManager.create_enbl(lbltype["redrice"], tmp)


def p2e2roundrand(this):
    if this.frame % 10 == 0:
        tmp = orbit.quickcreate(0, point=this.point, theta=int(random.random() * 180), speed=4,
                                bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)


def p3e1roundsnipe(this):
    if this.proc == 1:
        if this.frame % 70 == 0:
            tmp = orbit.quickcreate(1, point=this.point, speed=5.5, bltype=lbltype["greencircle"])
            scgame.blManager.create_enbl(lbltype["bluecircle"], tmp)
            mtheta = tmp.gettheta()
            for i in range(-3, 3):
                if i == 0:
                    continue
                tmp = orbit.quickcreate(0, point=this.point, theta=(mtheta + i * 30), speed=4,
                                        bltype=lbltype["greencircle"])
                scgame.blManager.create_enbl(lbltype["greencircle"], tmp)


def p4e2snipe(this):
    if this.status == globe.enstatus["dead"]:
        if this.frame == this.delay1 + 1:
            tmp = orbit.quickcreate(1, point=this.point, speed=8.5, bltype=lbltype["redround"])
            scgame.blManager.create_enbl(lbltype["redround"], tmp)
            this.mtheta = tmp.gettheta() + random.random() * 4 - 2
        elif this.frame % 2 == 0:
            for i in range(-3, 3):
                tmp = orbit.quickcreate(0, point=this.point, theta=(this.mtheta + i * 45 - 2), speed=8.5,
                                        bltype=lbltype["redround"])
                scgame.blManager.create_enbl(lbltype["redround"], tmp)
                tmp = orbit.quickcreate(0, point=this.point, theta=(this.mtheta + i * 45), speed=8.5,
                                        bltype=lbltype["redround"])
                scgame.blManager.create_enbl(lbltype["redround"], tmp)
                tmp = orbit.quickcreate(0, point=this.point, theta=(this.mtheta + i * 45 + 2), speed=8.5,
                                        bltype=lbltype["redround"])
                scgame.blManager.create_enbl(lbltype["redround"], tmp)


def p5e1roundrand(this):
    if this.proc == 1:
        if this.frame % 2 == 0:
            for i in range(6):
                tmp = orbit.quickcreate(0, point=this.point, theta=(int(this.frame ** 2 / 13) % 360 + i * 60),
                                        speed=4.7, bltype=lbltype["bluerice"])
                scgame.blManager.create_enbl(lbltype["bluerice"], tmp)


def enbossNSC1(this):
    # boss战非符1
    if this.frame % 4 == 0:
        tmp = orbit.quickcreate(0, point=(random.random() * globe.playrc.width + globe.playrc.left, globe.playrc.top),
                                theta=180 + 30 * random.random() - 15, speed=5, bltype=lbltype["blueball"])
        scgame.blManager.create_enbl(lbltype["blueball"], tmp)


def enbossSC1(this):
    # boss战非符2
    tmp = boss.rect
    tmp.centerx = globe.playrc.centerx
    tmp.centery = boss.rect.centery

    pt = [tmp.topleft, (tmp.centerx - 50, tmp.centery + 50), tmp.topright, (tmp.left + 50, tmp.centery + 50)]

    if this.frame % 8 == 0:
        tmp = orbit.quickcreate(0, point=pt[0], theta=(this.frame) / 2, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)
        tmp = orbit.quickcreate(0, point=pt[0], theta=(this.frame) / 2 + 180, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)

        tmp = orbit.quickcreate(0, point=pt[2], theta=(-this.frame) / 2, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)
        tmp = orbit.quickcreate(0, point=pt[2], theta=(-this.frame) / 2 - 180, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)

        tmp = orbit.quickcreate(0, point=pt[1], theta=(this.frame) / 2 + 90, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)
        tmp = orbit.quickcreate(0, point=pt[1], theta=(this.frame) / 2 + 270, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)

        tmp = orbit.quickcreate(0, point=pt[3], theta=(-this.frame) / 2 - 90, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)
        tmp = orbit.quickcreate(0, point=pt[3], theta=(-this.frame) / 2 + 90, speed=4.5, bltype=lbltype["bluerice"])
        scgame.blManager.create_enbl(lbltype["bluerice"], tmp)
        if this.frame % 20 == 0:
            tmp = orbit.quickcreate(1, point=this.point, speed=3, bltype=lbltype["blueball"])
            scgame.blManager.create_enbl(lbltype["blueball"], tmp)


def create_no(point):
    pass


def create_smallp(point):
    scgame.itManager.create(item.SPowerItem, point)


def create_largep(point):
    scgame.itManager.create(item.LPowerItem, point)


def create_pandpoint(point):
    a = random.random()
    if a < 0.5:
        scgame.itManager.create(item.SPowerItem, point)
    else:
        scgame.itManager.create(item.PointItem, point)


def create_life(point):
    scgame.itManager.create(item.LifeItem, point)


def create_point(point):
    scgame.itManager.create(item.PointItem, point)


def create_d_smallp(point):
    scgame.itManager.create(item.SPowerItem, point)


def create_d_point(point):
    scgame.itManager.create(item.PointItem, point)


def init():
    global lbltype
    global lentype
    global orb
    global scgame
    scgame = globe.scgame
    lbltype = {}
    lentype = {}
    orb = {}

    random.seed(int(time.time()))

    # 数据设定
    lbltype["bluecircle"] = bullet.BulletType(scgame.rs.image["bullet1"][3][5], 6)
    lbltype["orangerice"] = bullet.BulletType(scgame.rs.image["bullet1"][4][3], (0, 0, 8, 6))
    lbltype["bluerice"] = bullet.BulletType(scgame.rs.image["bullet1"][4][2], (0, 0, 8, 6))
    lbltype["redrice"] = bullet.BulletType(scgame.rs.image["bullet1"][4][6], (0, 0, 8, 6))
    lbltype["greencircle"] = bullet.BulletType(scgame.rs.image["bullet1"][3][7], 6)

    lbltype["redround"] = bullet.BulletType(scgame.rs.image["bullet1"][2][2], 6)

    lbltype["redsword"] = bullet.BulletType(scgame.rs.image["bullet2"][3][1], (0, 0, 25, 4))

    lbltype["blueball"] = bullet.BulletType(scgame.rs.image["bullet2"][1][3], 12)

    lbltype["bluetama"] = bullet.BulletType(scgame.rs.image["bullet2"][6][1], 18)

    lentype["p1e1"] = globe.entype["maoyu1"].copy()
    lentype["p1e1"].fbuff = create_smallp
    lentype["p1e1"].maxhealth = 3000

    lentype["p1e2"] = globe.entype["maoyu2"].copy()
    lentype["p1e2"].fbuff = create_no
    lentype["p1e1"].maxhealth = 3000

    lentype["p2e1"] = globe.entype["sprite4"].copy()
    lentype["p2e1"].fbuff = create_point
    lentype["p2e1"].maxhealth = 5000

    lentype["p2e2"] = globe.entype["sprite5"].copy()
    lentype["p2e2"].fbuff = create_smallp
    lentype["p2e2"].maxhealth = 6000

    lentype["p3e1"] = globe.entype["sprite7"].copy()
    lentype["p3e1"].fbuff = create_pandpoint
    lentype["p3e1"].maxhealth = 20000

    lentype["p3e2"] = globe.entype["sprite2"].copy()
    lentype["p3e2"].fbuff = create_pandpoint
    lentype["p3e2"].maxhealth = 15000

    lentype["p4e1"] = globe.entype["guihuo2"].copy()
    lentype["p4e1"].bump = True
    lentype["p4e1"].fbuff = create_d_point
    lentype["p4e1"].maxhealth = 6000

    lentype["p4e2"] = globe.entype["guihuo0"].copy()
    lentype["p4e2"].bump = True
    lentype["p4e2"].fbuff = create_d_smallp
    lentype["p4e2"].maxhealth = 6000

    lentype["p5e1"] = globe.entype["butterfly"].copy()
    lentype["p5e1"].bump = True
    lentype["p5e1"].fbuff = create_life
    lentype["p5e1"].maxhealth = 240000

    lentype["ebinto"] = globe.entype["cirno"].copy()
    lentype["ebinto"].bump = True
    lentype["ebinto"].fbuff = create_no
    lentype["ebinto"].maxhealth = 10000

    lentype["eb1NSC"] = globe.entype["cirno"].copy()
    lentype["eb1NSC"].bump = True
    lentype["eb1NSC"].fbuff = create_no
    lentype["eb1NSC"].maxhealth = 560000

    lentype["eb1SC"] = globe.entype["cirno"].copy()
    lentype["eb1SC"].bump = True
    lentype["eb1SC"].fbuff = create_no
    lentype["eb1SC"].maxhealth = 720000

    orb["p1e1"] = orbit.quickcreate(102, p1=(96, 0), p2=(128, 196), speed=3)
    orb["p1e1"].create_bullet = selfsniper

    orb["p1e2"] = orbit.quickcreate(102, p1=(288, 0), p2=(256, 196), speed=3)
    orb["p1e2"].create_bullet = selfsniper

    orb["p1e3"] = orbit.quickcreate(102, p1=(96, globe.playrc.bottom), p2=(128, globe.playrc.bottom - 196), speed=1.5)
    orb["p1e3"].create_bullet = roundrand

    orb["p1e4"] = orbit.quickcreate(102, p1=(288, globe.playrc.bottom), p2=(256, globe.playrc.bottom - 196), speed=1.5)
    orb["p1e4"].create_bullet = roundrand2

    orb["p2e1"] = orbit.quickcreate(101, point=(0, 0), speedx=0, speedy=3)
    orb["p2e1"].create_bullet = p2e1roundrand

    orb["p2e2"] = orbit.quickcreate(101, point=(0, 0), speedx=0, speedy=3)
    orb["p2e2"].create_bullet = p2e2roundrand

    orb["p3e1"] = orbit.quickcreate(103, p1=(0, 0), p2=(1, 1), speed=2, time=600)
    orb["p3e1"].create_bullet = p3e1roundsnipe

    orb["p4e1"] = orbit.quickcreate(104, point=(0, 0), delay1=180, delay2=6)
    orb["p4e1"].create_bullet = p4e2snipe

    orb["p4e2"] = orbit.quickcreate(104, point=(0, 0), delay1=180, delay2=6)
    orb["p4e2"].create_bullet = p4e2snipe

    orb["p5e1"] = orbit.quickcreate(103, p1=(0, 0), p2=(1, 1), speed=2, time=850)
    orb["p5e1"].create_bullet = p5e1roundrand

    orb["ebinto"] = orbit.L1BossRunInto((globe.playrc.centerx + 50, globe.playrc.top), (globe.playrc.centerx, 80), 4, 1)
    orb["ebinto"].create_bullet = create_no

    orb["ebstay"] = orbit.quickcreate(101, point=(globe.playrc.centerx, 80), speedx=0, speedy=0)
    orb["ebstay"].create_bullet = enbossNSC1

    orb["eb1NSC-1SC"] = orbit.L1BossRunInto((globe.playrc.centerx, 80), (globe.playrc.centerx, 150), 4, 1)
    orb["eb1NSC-1SC"].create_bullet = enbossSC1


def update(now_time):
    # 流程控制
    global boss
    if 40 <= now_time <= 240:
        if now_time % 10 == 0:
            scgame.enManager.create_enemy(lentype["p1e1"], orb["p1e1"].copy())

    elif 350 <= now_time <= 560:
        if now_time % 10 == 0:
            scgame.enManager.create_enemy(lentype["p1e1"], orb["p1e2"].copy())

    elif 810 <= now_time <= 1020:
        if now_time % 16 == 0:
            scgame.enManager.create_enemy(lentype["p1e2"], orb["p1e3"].copy())

    elif 1050 <= now_time <= 1260:
        if now_time % 16 == 0:
            scgame.enManager.create_enemy(lentype["p1e2"], orb["p1e4"].copy())

    elif 1500 <= now_time <= 2000:
        if now_time % 20 == 0:
            tmp = orb["p2e1"].copy()
            tmp.point[0] = random.random() * 100 + 48
            scgame.enManager.create_enemy(lentype["p2e1"], tmp)

            tmp = orb["p2e2"].copy()
            tmp.point[0] = globe.playrc.right - (random.random() * 100 + 48)
            scgame.enManager.create_enemy(lentype["p2e2"], tmp)

    elif 2160 <= now_time < 2640:
        if now_time % 45 == 0:
            tmp = None
            if now_time <= 2400:
                tmp = orb["p3e1"].copy()
                tmp.fr = ((now_time - 2160) / 45 * globe.playrc.width / 6, globe.playrc.top)
                tmp.tg = (tmp.fr[0], 100)
                tmp.refresh()
            else:
                if now_time >= 2000:
                    if not now_time % 3:
                        tmp = orb["p4e2"].copy()
                        tmp.point = (
                            (random.random()) * globe.playrc.width + globe.playrc.left,
                            200 + 30 * random.random())
                        tmp.delay1 = 50
                        scgame.enManager.create_enemy(lentype["p4e2"], tmp, bump=False)

                tmp = orb["p3e1"].copy()
                tmp.fr = ((6 - (now_time - 2400) / 45) * globe.playrc.width / 6, globe.playrc.top)
                tmp.tg = (tmp.fr[0], 200)
                tmp.refresh()

                tmp2 = tmp.copy()
                tmp2.fr = (random.random() * (globe.playrc.width - 30) + globe.playrc.left + 20, tmp2.fr[1])
                tmp2.tg = (tmp2.fr[0], 150)
                tmp2.refresh()
                tmp2.create_bullet = downrand
                scgame.enManager.create_enemy(lentype["p3e2"], tmp2, bump=None)

            scgame.enManager.create_enemy(lentype["p3e1"], tmp, wdtime=100, bump=None)

    elif 2880 <= now_time < 3000:
        if now_time % 30 == 0:
            tmp2 = orb["p3e1"].copy()
            tmp2.fr = (random.random() * (globe.playrc.width - 30) + globe.playrc.left + 20, tmp2.fr[1])
            tmp2.tg = (tmp2.fr[0], random.random() * 200 + 50)
            tmp2.refresh()
            tmp2.create_bullet = downrand
            scgame.enManager.create_enemy(lentype["p3e2"], tmp2)

    elif 3200 <= now_time <= 3240:
        if now_time % 5 == 0:
            tmp3 = orb["p4e1"].copy()
            tmp3.point = (random.random() * (globe.playrc.width) + globe.playrc.left, 200 + 20 * random.random())
            tmp3.delay1 -= int((now_time - 3200) * 0.6)
            scgame.enManager.create_enemy(lentype["p4e1"], tmp3, bump=True)

    elif 3480 < now_time <= 3560:
        if now_time % 5 == 0:
            tmp3 = orb["p4e2"].copy()
            tmp3.point = (
                (1 + random.random()) * (globe.playrc.width / 2) + globe.playrc.left, 200 + 30 * random.random())
            tmp3.delay1 -= int((now_time - 3480) * 0.6)
            scgame.enManager.create_enemy(lentype["p4e2"], tmp3, bump=False)

            tmp3 = orb["p4e1"].copy()
            tmp3.point = ((random.random()) * (globe.playrc.width / 2) + globe.playrc.left, 200 + 30 * random.random())
            tmp3.delay1 += 75
            tmp3.delay1 -= int((now_time - 3480) * 0.6)
            scgame.enManager.create_enemy(lentype["p4e1"], tmp3, bump=False)

    elif 3920 <= now_time <= 3980:
        if now_time % 5 == 0:
            tmp3 = orb["p4e2"].copy()
            tmp3.point = (
                (1 + random.random()) * (globe.playrc.width / 2) + globe.playrc.left, 200 + 30 * random.random())
            tmp3.delay1 -= int((now_time - 3920) * 0.6)
            scgame.enManager.create_enemy(lentype["p4e2"], tmp3, bump=True)

            tmp3 = orb["p4e1"].copy()
            tmp3.point = ((random.random()) * (globe.playrc.width / 2) + globe.playrc.left, 200 + 30 * random.random())
            tmp3.delay1 -= int((now_time - 3920) * 0.6)
            tmp3.delay1 += 75
            scgame.enManager.create_enemy(lentype["p4e1"], tmp3, bump=True)

    elif now_time == 4300:
        tmp = orb["p5e1"].copy()
        tmp.fr = (globe.playrc.width / 2 + globe.playrc.left, globe.playrc.top)
        tmp.tg = (globe.playrc.width / 2 + globe.playrc.left, globe.playrc.top + 90)
        tmp.refresh()
        tmp.create_bullet = p5e1roundrand
        tp = lentype["p5e1"].copy()
        tp.maxhealth = 240000
        scgame.enManager.create_enemy(tp, tmp, bump=True, wdtime=400)

    elif now_time == 5400:
        tmp = orb["p5e1"].copy()
        tmp.fr = (-globe.playrc.width / 3 + globe.playrc.right, globe.playrc.top)
        tmp.tg = (-globe.playrc.width / 3 + globe.playrc.right, globe.playrc.top + 90)
        tmp.refresh()
        tmp.create_bullet = p5e1roundrand
        tp = lentype["p5e1"].copy()
        tp.maxhealth = 100000
        scgame.enManager.create_enemy(tp, tmp, bump=True, wdtime=400)

        tmp1 = orb["p5e1"].copy()
        tmp1.fr = (globe.playrc.width / 3 + globe.playrc.left, globe.playrc.top)
        tmp1.tg = (globe.playrc.width / 3 + globe.playrc.left, globe.playrc.top + 90)
        tmp1.refresh()
        tmp1.create_bullet = p5e1roundrand
        tp = lentype["p5e1"].copy()
        tp.maxhealth = 100000
        scgame.enManager.create_enemy(tp, tmp1, bump=True, wdtime=400)

    elif 5400 <= now_time < 6000:
        if not now_time % 50:
            tmp = orb["p4e2"].copy()
            tmp.point = (
                (random.random()) * globe.playrc.width + globe.playrc.left,
                globe.playrc.bottom - 20 - 5 * random.random())
            tmp.delay1 = 50
            scgame.enManager.create_enemy(lentype["p4e2"], tmp, bump=False)

    elif now_time == 6500:
        boss = scgame.enManager.create_enemy(lentype["ebinto"], orb["ebinto"], bump=None, wdtime=100)
        boss.life = 3

    elif now_time == 6560:
        globe.scgame.tstop()

    elif now_time == 6561:
        globe.BOSSING = True
        globe.destiny.msManager.stop()
        globe.destiny.msManager.play_BGM("lv1b")
        globe.scgame.hud.change_blood(True)
        globe.scgame.hud.blood = BloodStruct(720000, 720000, 560000, 560000, 0.3, 0.7)

        boss.crash()

    elif 6561 < now_time < 100000:

        if boss.status == globe.enstatus["normal"]:
            if boss.life == 2:
                if boss.health >= 0:
                    globe.scgame.hud.blood.now_heal_nosc = boss.health
                else:
                    globe.scgame.hud.blood.now_heal_nosc = 0
            elif boss.life == 1:
                if boss.health >= 0:
                    globe.scgame.hud.blood.now_heal_card = boss.health
                else:
                    globe.scgame.hud.blood.now_heal_card = 0

        elif boss.status == globe.enstatus["dead"]:
            boss.life -= 1
            if boss.life == 2:
                boss.__init__(lentype["eb1NSC"], orb["ebstay"], 0, bump=True, wdtime=100)
                boss.status = globe.enstatus["normal"]
                boss.life = 2

            elif boss.life == 1:
                global htmp
                htmp = [globe.scgame.player.life, globe.scgame.player.power]
                globe.scgame.blManager.clear_enbl()
                globe.scgame.bgManager.background_change(True)
                boss.__init__(lentype["eb1SC"], orb["eb1NSC-1SC"], 0, bump=True, wdtime=100)
                boss.life = 1

            else:
                # global htmp
                if htmp[0] != globe.scgame.player.life or htmp[1] != globe.scgame.player.power:
                    globe.scgame.hud.create_failed()
                else:
                    globe.scgame.hud.create_bonus()
                    globe.scgame.score += 100000
                globe.scgame.hud.change_blood(False)
                boss.status = globe.enstatus["del"]
                globe.scgame.bgManager.background_change(False)
                globe.scgame.time = 100000
                globe.scgame.blManager.clear_enbl()
                globe.scgame.anManager.create_anime(globe.destiny.rsManager.anime["bubble"], boss.orbit.point, 15)

    elif now_time >= 100120:
        globe.destiny.call(gameover.Scene_GameOver)
