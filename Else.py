# 重复的零散操作

import random
import time

# 游戏最大最小人数
MINPLAYER = 4
MAXPLAYER = 6

# 输入数字
def inputnum(MIN, MAX):
    while 1:
        try:
            while 1:
                num = int(input())
                if num <= MAX and num >= MIN:
                    return num
                else:
                    print('输入有误，请重新输入')
        except:
            print("输入违规，请重新输入")

# 确认操作
def confirm():
    while 1:
        print('是否确认操作？Y/N')
        flag = input()
        if flag == 'Y' or flag == 'y':
            return 0
        elif flag == 'N' or flag == 'n':
            return 1
        else:
            print('输入有误，请重新输入。')

# 确认游戏人数
def playernum():
    conf = 1
    while conf:
        print("请输入游戏人数({}-{}人):".format(MINPLAYER, MAXPLAYER))
        num = inputnum(MINPLAYER, MAXPLAYER)
        conf = confirm()
    return num

# 加载操作
def load(content, dot):
    print(content, end='')
    for i in range(dot):
        time.sleep(0.7)
        print('.', end='')
    print()

# 展示身份及技能
def showNameSkill(name, role):
    print(name, end='')
    role.onlyShowSkill()

# 分配喜爱、憎恨角色
def loverorhater(playernum, me, ai, emotion):
    emo = []
    for i in range(playernum - 1):
        emo.append(ai[i])
    emo.append(me)
    random.shuffle(emo)
    if(emotion == 'lover'):
        for i in range(playernum - 1):
            ai[i].lover = emo[0]
            emo.pop(0)
        me.lover = emo[0]
        print('我喜欢的人是: {}'.format(me.lover.name))
    elif(emotion == 'hater'):
        for i in range(playernum - 1):
            ai[i].hater = emo[0]
            emo.pop(0)
        me.hater = emo[0]
        print('我憎恨的人是: {}'.format(me.hater.name))

# 抽取*船上*活着的人数相等的物资
def extractGoods(Seat, GoodsStack):
    if len(GoodsStack) == 0:
        print('船上物资全部用完了，跳过物资阶段。')
        return
    preGoods = []
    count = 0
    for role in Seat:
        if role.dead == 0 and role.fail == 0:
            count += 1
    if count > len(GoodsStack):
        count = len(GoodsStack)
    for i in range(count):
        preGoods.append(GoodsStack[0])
        GoodsStack.pop(0)
    return preGoods

# 显示当前座位信息
def showSeat(Seat):
    print('=======现在小船座位如下=======')
    print('\\\ ', end='')
    for seat in Seat:
        print(seat.name, end=' ')
    print('//')

# 计算分数
def countScore(Seat):
    for role in Seat:
        # 如果是厌世者
        if role.hater.name == role.name:
            # 如果对自己又爱又恨,生还时仅获得自己的生存分数
            if role.lover.name == role.name:
                if role.dead == 0:
                    role.score += role.suvscore
            # 厌世者，其他角色死亡可以得到其体力分数
            else:
                for el in Seat:
                    if el.dead == 1:
                        role.score += el.hp
        else:
            # 1 角色是否存活
            if role.dead == 0:
                role.score += role.suvscore
            # 2 喜欢的角色是否存活
            for love in Seat:
                if love.name == role.lover.name and love.dead == 0:
                    role.score += love.suvscore
            # 3 憎恨的角色是否存活
            for hate in Seat:
                if hate.name == role.hater.name and hate.dead == 1:
                    role.score += hate.hp

        # 开始计算财产
        money = 0
        jewel = 0
        jscore = 0
        pic = 0
        if role.fail == 0:
            for g in role.hand:
                # 钞票
                if g.name == '一把钞票':
                    money += 1
                # 名画
                elif g.name == '名画':
                    pic += g.score
                # 珠宝
                elif g.name == '珠宝':
                    jewel += 1
            # 计算珠宝分数
            if jewel == 1:
                jscore = 1
            elif jewel == 2:
                jscore = 4
            elif jewel == 3:
                jscore = 8
            # 角色技能
            if role.name == '船长':
                money *= 2
            elif role.name == '史蒂芬先生':
                pic *= 2
            elif role.name == '罗伦小姐':
                jscore *= 2
            # 计算珍品分数
            role.score += money
            role.score += pic
            role.score += jscore
