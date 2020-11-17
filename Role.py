# 角色类
import random
import Else
import time

class Role(object):
    # 初始化一个角色
    def __init__(self, name, hp, suvscore, seat, describe):
        self.name = name   # 角色姓名
        self.hp = hp    # 体力值
        self.suvscore = suvscore    # 生存分数
        self.seat = seat    # 位置
        self.describe = describe    # 技能描述
        self.ai = 0     # 是否是AI
        self.lover = None   # 喜爱的人
        self.hater = None   # 憎恨的人
        self.dead = 0   # 死亡状态
        self.fail = 0   # 落海状态
        self.hand = []  # 手牌
        self.equip = []    # 装备
        self.score = 0  # 最终分数
        self.fail = 0   # 落海状态
        self.boathurt = 0    # 划船预备伤害
        self.fighthurt = 0     # 打架预备伤害
        self.hurt = 0   # 已受伤害
        self.act = 0    # 行动标记

    def __str__(self):
        pass

    def str(self):
        print('name', self.name)
        print('hand', end=' ')
        for g in self.hand:
            print(g.name, end=' ')
        print()
        print('equip', end=' ')
        for e in self.equip:
            print(e.name, end=' ')
        print()

    # 查看角色信息
    def showInfo(self):
        print('姓名:{}'.format(self.name))
        print('  体力:{}'.format(self.hp))
        print('  生存分数:{}'.format(self.suvscore))
        print('  技能:{}'.format(self.describe))

    # 只查看角色技能
    def onlyShowSkill(self):
        print(self.name, self.describe)

    # 玩家选择物资
    def playerChooseGoods(self, preGoods):
        if len(preGoods) == 0:
            print('已经没有物资了。')
            return
        print('请从以下选择一份你需要的物资：')
        i = 1
        for good in preGoods:
            print('{}.'.format(i), end='')
            good.showInfo()
            i += 1
        number = Else.inputnum(1, i)
        self.hand.append(preGoods[number - 1])
        preGoods.pop(number - 1)

    # AI选择物资
    def aiChooseGoods(self, preGoods):
        random.shuffle(preGoods)
        self.hand.append(preGoods[0])
        preGoods.pop(0)

    # 查看当前手中物资
    def checkGoods(self):
        print('{},'.format(self.name), end='')
        for good in self.hand:
            good.showName()

    # 玩家执行行动
    def playerChooseAct(self, preSail, SailStack, Seat, Mew):
        num = 0
        self.act = 1
        while num < 1 or num > 5:
            if self.dead == 1:
                print('-------------------------------')
                print('您已死亡，即将跳过行动阶段')
                time.sleep(0.5)
                break
            confirm = 1
            while confirm:
                print('-------------------------------')
                print('请从以下行动中选择一个：\n1.划船\n2.换座位\n3.抢夺物资\n4.特殊行动\n5.什么都不做\n6.查看我的装备和物资')
                num = Else.inputnum(1, 6)
                confirm = Else.confirm()
                if confirm:
                    continue
                if num == 1:
                    print('我 选择了 划船')
                    time.sleep(0.5)
                    self.playerBoat(preSail, SailStack)
                    break
                elif num == 2:
                    print('我 选择了 换座位')
                    time.sleep(0.5)
                    self.askPlayerSeat(Seat)
                    break
                elif num == 3:
                    print('我 选择了 抢夺物资')
                    time.sleep(0.5)
                    f = self.askPlayerLoot(Seat)
                    if f == 0:
                        print('该玩家没有可以抢夺的物资')
                        confirm = 1
                    elif f == 1:
                        break
                elif num == 4:
                    print('我 选择了 特殊行动')
                    time.sleep(0.5)
                    f, Mew= self.playerSpecial(SailStack, Mew)
                    if f == 0:
                        print('没有可以进行特殊行动的物资')
                        confirm = 1
                    elif f == 1:
                        break
                elif num == 5:
                    print('我 选择了 什么都不做')
                    time.sleep(0.5)
                    break
                elif num == 6:
                    print('物资：', end='')
                    if len(self.hand) == 0:
                        print('-', end='')
                    else:
                        for g in self.hand:
                            print(g.name, end=' ')
                    print()
                    print('装备：', end='')
                    if len(self.equip) == 0:
                        print('-', end='')
                    else:
                        for g in self.equip:
                            print(g.name, end=' ')
                    print()
                    time.sleep(0.5)
                    confirm = 1
        return Mew

    # AI执行行动
    def aiChooseAct(self, preSail, SailStack, Seat, Mew):
        num = random.randint(1, 5)
        self.act = 1
        print('-------------------------------')
        while self.dead == 0:
            if num == 1:
                print('{} 选择了 划船 '.format(self.name))
                time.sleep(0.5)
                self.aiBoat(preSail, SailStack)
                break
            elif num == 2:
                print('{} 选择了'.format(self.name), end='')
                self.askAISeat(Seat)
                break
            elif num == 3:
                f = self.askAILoot(Seat)
                if f == 1:
                    break
                elif f == 0:
                    num = random.randint(1, 5)
                    continue
            elif num == 4:
                print('{} 选择了 特殊行动'.format(self.name))
                time.sleep(0.5)
                f, Mew = self.aiSpecial(SailStack, Mew)
                if f == 0:
                    num = random.randint(1, 5)
                    print('但是失败了')
                    continue
                elif f == 1:
                    break
            elif num == 5:
                print('{} 选择了 什么都不做'.format(self.name))
                time.sleep(0.5)
                break
        return Mew

    # 玩家划船
    def playerBoat(self, preSail, SailStack):
        self.boathurt = 1
        count = 2
        for g in self.equip:
            if g.id == 5:
                count += 1
                break
        confirm = 1
        while confirm:
            print('请从以下航海决策中选择一个加入最终选择：')
            for i in range(count):
                print('{}.'.format(i + 1), end='')
                SailStack[i].showInfo()
            num = Else.inputnum(1, count)
            confirm = Else.confirm()
        # 从决策中选择一个加入最终决策
        preSail.append(SailStack[num - 1])
        SailStack.pop(num - 1)
        # 将剩余决策防止决策底部
        for i in range(count - 1):
            SailStack.append(SailStack[0])
            SailStack.pop(0)

    # AI划船
    def aiBoat(self, preSail, SailStack):
        self.boathurt = 1
        count = 2
        for g in self.equip:
            if g.id == 5:
                count += 1
                break
        num = random.randint(1, count)
        # 从决策中选择一个加入最终决策
        preSail.append(SailStack[num])
        SailStack.pop(num)
        # 将剩余决策防止决策底部
        for i in range(count - 1):
            SailStack.append(SailStack[0])
            SailStack.pop(0)

    # 询问玩家
    def askPlayer(self):
        while self.dead == 0:
            print('{} 是否同意？Y/N'.format(self.name))
            flag = input()
            if flag == 'Y' or flag == 'y':
                return 1
            elif flag == 'N' or flag == 'n':
                return 0
            else:
                print('输入有误，请重新输入。')
        return 1

    # 询问AI
    def askAI(self):
        if self.dead == 0:
            num = random.randint(0, 1)
            if num == 0:
                print('{} 不同意'.format(self.name))
                time.sleep(0.5)
            elif num == 1:
                print('{} 同意了'.format(self.name))
                time.sleep(0.5)
            return num
        else:
            return 1

    # 询问玩家战斗
    def askPlayerFight(self, atk, defc):
        while self.dead == 0:
            print('进攻方 {} ,防守方 {} ,是否参与战斗？（1.进攻方，2.防守方，3.不参与战斗）'.format(atk.name, defc.name))
            flag = Else.inputnum(1, 3)
            if flag == 1:
                return 1
            elif flag == 2:
                return 2
            elif flag == 3:
                return 3
            else:
                print('输入有误，请重新输入。')

    # 询问ai战斗
    def askAIFight(self):
        if self.dead == 0:
            flag = random.randint(1, 3)
            if flag == 1:
                return 1
            elif flag == 2:
                return 2
            elif flag == 3:
                return 3

    # 装备武器
    def equipWeapon(self):
        flag = 0
        i = 0
        while i < len(self.hand):
            if self.hand[i].id >= 5 and self.hand[i].id <= 9:
                for e in self.equip:
                    if e.id == self.hand[i].id:
                        flag = 1
                if flag == 0:
                    self.equip.append(self.hand[i])
                    print('{} 装备了 {} !'.format(self.name, self.hand[i].name))
                    time.sleep(0.5)
                    self.hand.remove(self.hand[i])
                    i -= 1
            i += 1

    # 战斗（进攻方获胜返回1，防守方获胜返回0）
    def fight(self, enemy, Seat):
        print('=========战斗开始=========')
        # 创建进攻方和防守方
        atk = [self]
        defc = [enemy]
        atkpoint = 0
        defcpoint = 0

        # 创建询问队列
        ask = []
        for r in Seat:
            if r.dead == 0:
                ask.append(r)
        for r in ask:
            if self.name == r.name:
                ask.remove(r)
        for r in ask:
            if enemy.name == r.name:
                ask.remove(r)

        # 建立进攻方、防守方
        for r in ask:
            if r.ai == 0:
                agree = r.askPlayerFight(self, enemy)
            else:
                agree = r.askAIFight()
            if agree == 1:
                atk.append(r)
            elif agree == 2:
                defc.append(r)

        print('进攻方：', end=' ')
        for r in atk:
            print(r.name, end=' ')
        print()
        print('防守方：', end=' ')
        for r in defc:
            print(r.name, end=' ')
        print()

        # 装备武器
        for r in atk:
            r.fighthurt = 1
            r.equipWeapon()
        for r in defc:
            r.fighthurt = 1
            r.equipWeapon()

        # 计算进攻指数
        for r in atk:
            for g in r.equip:
                if g.id >= 5 and g.id <= 9:
                    atkpoint += g.attack
            atkpoint += r.hp

        # 计算防守指数
        for r in defc:
            for g in r.equip:
                if g.id >= 5 and g.id <= 9:
                    defcpoint += g.attack
            defcpoint += r.hp

        # 显示战斗结果
        Else.load('战斗中', 3)
        print('=========战斗总结=========')
        time.sleep(1)
        print('进攻方体力值共计 {} 点，防守方体力值共计 {} 点'.format(atkpoint, defcpoint), end=',')
        if atkpoint > defcpoint:
            print('进攻方获胜！')
            time.sleep(0.5)
            print('=========战斗结束=========')
            return 1
        else:
            print('防守方获胜！')
            time.sleep(0.5)
            print('=========战斗结束=========')
            return 0

    # 玩家换座
    def askPlayerSeat(self, Seat):
        print('请选择你要和谁交换座位：')
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            print('{}. {}'.format(i, r.name), end='')
            if r.dead == 1:
                print('（死亡）', end='')
            print()
            i += 1
        num = Else.inputnum(1, i - 1)
        # 确认要交换座位的对象
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            if num == i:
                target = r
                break
            i += 1
        if target.dead == 1:
            self.changeSeat(target, Seat)
        elif target.dead == 0:
            if target.ai == 0:
                res = target.askPlayer()
            else:
                res = target.askAI()
            if res == 0:
                res = self.fight(target, Seat)
            if res == 1:
                self.changeSeat(target, Seat)

    # AI换座
    def askAISeat(self, Seat):
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            i += 1
        num = random.randint(1, i - 1)
        # 确认要交换座位的对象
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            if num == i:
                target = r
                break
            i += 1
        print('和 {} 交换座位'.format(target.name))
        time.sleep(0.5)
        if target.dead == 1:
            self.changeSeat(target, Seat)
        elif target.dead == 0:
            if target.ai == 0:
                Else.showSeat(Seat)
                res = target.askPlayer()
            else:
                res = target.askAI()
            if res == 0:
                res = self.fight(target, Seat)
            if res == 1:
                self.changeSeat(target, Seat)

    # 换座位
    def changeSeat(self, target, Seat):
        for r in Seat:
            if self.name == r.name:
                a = Seat.index(r)
            if target.name == r.name:
                b = Seat.index(r)
        Seat[a], Seat[b] = Seat[b], Seat[a]
        print('{} 和 {} 交换座位'.format(self.name, target.name))
        time.sleep(0.5)
        Else.showSeat(Seat)
        return Seat

    # 询问玩家抢夺物资
    def askPlayerLoot(self, Seat):
        print('请选择你抢夺谁的物资：')
        i = 1
        for r in Seat:
            if r.name == self.name or r.dead == 1:
                continue
            print('{}. {}'.format(i, r.name))
            i += 1
        num = Else.inputnum(1, i - 1)
        # 确认要抢夺的对象
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            if num == i:
                target = r
                break
            i += 1
        if len(target.hand) != 0 or len(target.equip) != 0:
            if self.name == '小孩':
                # 抢夺物资
                self.playerLoot(target)
            elif target.dead == 0:
                if target.ai == 0:
                    res = target.askPlayer()
                else:
                    res = target.askAI()
                if res == 0:
                    res = self.fight(target, Seat)
                if res == 1:
                    # 抢夺物资
                    self.playerLoot(target)
            return 1
        else:
            return 0

    # 询问AI抢夺物资
    def askAILoot(self, Seat):
        i = 1
        for r in Seat:
            if r.name == self.name or r.dead == 1:
                continue
            i += 1
        num = random.randint(1, i - 1)
        # 确认要抢夺物资的对象
        i = 1
        for r in Seat:
            if r.name == self.name:
                continue
            if num == i:
                target = r
                break
            i += 1
        print('{} 选择抢夺 {} 的物资'.format(self.name, target.name))
        time.sleep(0.5)
        if len(target.hand) != 0 or len(target.equip) != 0:
            if self.name == '小孩':
                self.aiLoot(target)
            elif target.dead == 0:
                if target.ai == 0:
                    res = target.askPlayer()
                else:
                    res = target.askAI()
                if res == 0:
                    res = self.fight(target, Seat)
                if res == 1:
                    self.aiLoot(target)
            return 1
        else:
            print('但是失败了')
            return 0

    # 玩家抢夺物资
    def playerLoot(self, target):
        #
        i = 1
        if len(target.equip) != 0:
            print('对方有以下装备：')
            for g in target.equip:
                print('{}. {},{}'.format(i, g.name, g.describe))
                i += 1
        if len(target.hand) == 0:
            print('从对方装备中掠夺物资')
            print('选择哪件装备？（输入装备序号）')
            n = Else.inputnum(1, i - 1)
            j = 1
            for g in target.equip:
                if n == j:
                    self.hand.append(g)
                    target.equip.pop(j - 1)
                    print('{} 抢到了 {} 的 {}'.format(self.name, target.name, g.name))
                    if g.name == '阳伞':
                        g.open = 0
                j += 1
        elif len(target.equip) == 0:
            print('从对方手中随机掠夺物资')
            j = len(target.hand)
            k = random.randint(1, j)
            l = 1
            for g in target.hand:
                if l == k:
                    self.hand.append(g)
                    target.hand.pop(l - 1)
                    print('{} 抢到了 {} 的 {}'.format(self.name, target.name, g.name))
                    if g.name == '阳伞':
                        g.open = 0
                l += 1
        else:
            print('要从哪里掠夺物资？（1.装备，2.手中随机抢夺）')
            num = Else.inputnum(1, 2)
            if num == 1:
                print('选择哪件装备？（输入装备序号）')
                n = Else.inputnum(1, i - 1)
                j = 1
                for g in target.equip:
                    if n == j:
                        self.hand.append(g)
                        target.equip.pop(j - 1)
                        print('{} 抢到了 {} 的 {}'.format(self.name, target.name, g.name))
                        if g.name == '阳伞':
                            g.open = 0
                    j += 1
            elif num == 2:
                j = len(target.hand)
                k = random.randint(1, j)
                l = 1
                for g in target.hand:
                    if l == k:
                        self.hand.append(g)
                        target.hand.pop(l - 1)
                        print('{} 抢到了 {} 的 {}'.format(self.name, target.name, g.name))
                        if g.name == '阳伞':
                            g.open = 0
                    l += 1

    # ai抢夺物资
    def aiLoot(self, target):
        if len(target.hand) == 0:
            n = random.randint(1, len(target.equip))
            j = 1
            for g in target.equip:
                if n == j:
                    self.hand.append(g)
                    target.equip.pop(j - 1)
                    print('{} 抢夺了 {} 的 {}'.format(self.name, target.name, g.name))
                    if g.name == '阳伞':
                        g.open = 0
                j += 1
        elif len(target.equip) == 0:
            j = len(target.hand)
            k = random.randint(1, j)
            l = 1
            for g in target.hand:
                if l == k:
                    self.hand.append(g)
                    target.hand.pop(l - 1)
                    print('{} 抢夺了 {} 的 {}'.format(self.name, target.name, g.name))
                    if g.name == '阳伞':
                        g.open = 0
                l += 1
        else:
            num = random.randint(1, 2)
            if num == 1:
                n = random.randint(1, len(target.equip))
                j = 1
                for g in target.equip:
                    if n == j:
                        self.hand.append(g)
                        target.equip.pop(j - 1)
                        print('{} 抢夺了 {} 的 {}'.format(self.name, target.name, g.name))
                        if g.name == '阳伞':
                            g.open = 0
                    j += 1
            elif num == 2:
                j = len(target.hand)
                k = random.randint(1, j)
                l = 1
                for g in target.hand:
                    if l == k:
                        self.hand.append(g)
                        target.hand.pop(l - 1)
                        print('{} 抢夺了 {} 的 {}'.format(self.name, target.name, g.name))
                        if g.name == '阳伞':
                            g.open = 0
                    l += 1

    # 玩家进行特殊行动
    def playerSpecial(self, SailStack, Mew):
        flag = 0
        pre = []
        for g in self.hand:
            if g.special == 1:
                flag = 1
                pre.append(g)
        for g in self.equip:
            if g.special == 1 and g.name != '阳伞':
                flag = 1
                pre.append(g)
        if flag == 0:
            return 0, Mew
        i = 1
        print('选择将要使用的物品：')
        for g in pre:
            print('{}. {},{}'.format(i, g.name, g.describe))
            i += 1
        num = Else.inputnum(1, i)
        Mew = pre[num - 1].use(self, SailStack, Mew)
        return 1, Mew

    # ai进行特殊行动
    def aiSpecial(self, SailStack, Mew):
        flag = 0
        pre = []
        for g in self.hand:
            if g.special == 1:
                flag = 1
                pre.append(g)
        for g in self.equip:
            if g.special == 1 and g.name != '阳伞':
                flag = 1
                pre.append(g)
        if flag == 0:
            return 0, Mew
        num = random.randint(1, len(pre))
        Mew = pre[num - 1].use(self, SailStack, Mew)
        return 1, Mew

    # 玩家使用航海决策
    def playerSail(self, preSail, Mew, Seat):
        i = 1
        print('请从以下航海决策中选择一个：')
        for sail in preSail:
            print('{}.'.format(i), end='')
            sail.showInfo()
            i += 1
        num = Else.inputnum(1, i - 1)
        print('{} 选择的航海决策是：'.format(self.name))
        time.sleep(1)
        Mew = preSail[num - 1].use(Mew, Seat)
        preSail.pop(num - 1)

        return Mew

    # ai使用航海决策
    def aiSail(self, preSail, Mew, Seat):
        num = random.randint(1, len(preSail))
        print('{} 选择的航海决策是：'.format(self.name))
        time.sleep(1)
        Mew = preSail[num - 1].use(Mew, Seat)
        preSail.pop(num - 1)

        return Mew

    # 喝水
    def drink(self):
        if self.dead == 0:
            i = 1
            while i <= len(self.hand):
                if self.hurt > 0 and self.hand[i - 1].name == '水':
                    self.hurt -= 1
                    self.hand.remove(self.hand[i - 1])
                    print('{} 喝掉了一份水，当前受伤指数为 {} 点'.format(self.name, self.hurt))
                    time.sleep(0.5)
                    i -= 1
                i += 1

    # 落海
    def failInSea(self):
        if self.dead == 0:
            self.hurt += 1
            self.equip = []
            # 如果没死就还可以爬回岸上
            self.fail = 0
        print('{} 落水了,当前受伤指数为 {} 点'.format(self.name, self.hurt))
        time.sleep(0.5)

    # 判断死亡
    def isDead(self):
        if self.hurt >= self.hp:
            self.dead = 1
            print('{} 死亡了。'.format(self.name))
            time.sleep(0.5)


# 生成每个角色的实例对象
def createRoles():
    Rolen = Role('罗伦小姐', 4, 8, 1, '珠宝的分数加倍')
    Steve = Role('史蒂芬先生', 5, 7, 2, '名画的分数加倍')
    Captain = Role('船长', 7, 5, 3, '一把钞票的分数加倍')
    Mate = Role('大副', 8, 4, 4, '就是力气大')
    France = Role('法国佬', 6, 6, 5, '游技绝佳，落海不会造成伤害')
    Child = Role('小孩', 3, 9, 6, '当你从别人那里偷取物资时，别人无法拒绝')
    Roles = [Rolen, Steve, Captain, Mate, France, Child]
    return Roles