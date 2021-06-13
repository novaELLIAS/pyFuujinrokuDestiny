# database.py
# 用于处理数据库操作

import globe
import leancloud
import win32con,win32api
import threading

globe.online = False  # 在线标志(是否登录)


class DatabaseManager:

    def __init__(self):
        leancloud.init(globe.appid, globe.appkey)
        self.user = leancloud.User()

    def asyncprocess(self):
        # 供外部调用的流程
        if not globe.logonflag:
            self.logon()
        if not globe.online:
            globe.getrankflag = True
            globe.updateflag = True
            globe.logonflag = True
            return
        if not globe.updateflag and globe.online:
            t1 = threading.Thread(target=self.update)
            t1.start()
        if not globe.getrankflag and globe.online:
            t2 = threading.Thread(target=self.getrank)
            t2.start()

    def message(self, content, title):
        # 消息对话框
        win32api.MessageBox(0, content, title, win32con.MB_OK)

    def isUserExist(self) -> bool:
        # 检测用户是否存在
        user_query = leancloud.Object.extend("_User")
        query = user_query.query
        query.equal_to("username", globe.username)
        useronline = query.find()
        if useronline:
            return True
        else:
            return False

    def logon(self):
        # 用户登录
        if globe.username == "":
            self.message("Logon Fail.\nusername missing.", "ERROR")
            globe.online = False
            globe.logonflag = True
            return
        try:
            if self.isUserExist():
                self.user.login(globe.username, globe.password)
            else:
                self.register()
                self.user.login(globe.username, globe.password)
            globe.online = True
        except Exception as e:
            self.message("Logon Fail.\nUsing offline mode.", "ERROR")
            globe.online = False
            globe.logonflag = True
            print(e)
        globe.logonflag = True

    def logout(self):
        self.user.logout()

    def register(self):
        # 用户注册
        try:
            self.user.set_username(globe.username)
            self.user.set_password(globe.password)
            self.user.set_email(globe.useremail)
            self.user.sign_up()
        except Exception as e:
            self.message("Register Fail.\nUsing offline mode.", "ERROR")
            print(e)

    def getscore(self) -> int:
        # 查询在线分数
        scoreframe = leancloud.Object.extend("score")
        query = scoreframe.query
        query.equal_to("username", globe.username)
        scorelist = query.find()
        if not scorelist:
            self.score = scoreframe()
            self.score.set("username", globe.username)
            self.score.set("score", globe.hiscore)
            self.user.login(globe.username, globe.password)
            self.score.save()
        else:
            self.score = scorelist[0]
        return self.score.get("score")

    def update(self):
        if not globe.online:
            pass
        # 更新在线成绩
        onlinebest = self.getscore()
        if globe.hiscore > onlinebest:
            self.score.set("score", globe.hiscore)
            self.user.login(globe.username, globe.password)
            self.score.save()
        else:
            globe.hiscore = onlinebest
        globe.updateflag = True

    def getrank(self):
        if not globe.online:
            pass
        # 查询前1000名
        scoreframe = leancloud.Object.extend("score")
        query = scoreframe.query
        query.descending("score")
        query.limit(1000)
        ranklist = query.find()
        listret = list()
        cnt = 0
        for i in ranklist:
            # 格式化返回值
            cnt += 1
            listret.append({"username": i.get("username"), "score": i.get("score"), "rank": cnt})
        globe.ranklist = listret
        print(globe.ranklist)
        globe.getrankflag = True
