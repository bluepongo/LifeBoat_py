import time


# 航海决策
class Sail(object):
    def __init__(self, fail, thirsty, fight, quant, mew):
        self.fail = fail
        self.thirsty = thirsty
        self.fight = fight
        self.quant = quant
        self.mew = mew

    def showInfo(self):
        print('【', end='')
        if self.fail:
            print('-落海:', end='')
            for f in self.fail:
               print(f, end=' ')
        if self.thirsty:
            print('-口渴:', end='')
            for f in self.thirsty:
                print(f, end=' ')
        if self.fight:
            print('-打架', end=' ')
        if self.quant:
            print('-划船', end=' ')
        if self.mew == 1:
            print('-出现一只海鸥', end=' ')
        elif self.mew == -1:
            print('-杀死一只海鸥', end=' ')
        print('】')

    def use(self, Mew, Seat):
        self.showInfo()
        time.sleep(1)
        # 是否可以解除落水状态
        flag = 0
        # 海鸥
        if self.mew == 1:
            Mew += 1

        # 落水
        for r in Seat:
            for name in self.fail:
                if r.name == name:
                    if r.name == '法国佬':
                        flag = 1
                    for g in r.hand:
                        if g.name == '救生圈':
                            g.use(r)
                    for g in r.equip:
                        if g.name == '救生圈':
                            flag = 1
                            break
                    if flag == 1:
                        break
                    r.failInSea()

        # 口渴
        for r in Seat:
            if r.dead == 0:
                flag = 0
                # 划船
                if self.quant == 1 and r.boathurt == 1:
                    r.hurt += 1
                    flag += 1
                    print('{} 因划船受到1点伤害，当前受伤指数为 {} 点'.format(r.name, r.hurt))
                    time.sleep(0.5)
                # 打架
                if self.fight == 1 and r.fighthurt == 1:
                    r.hurt += 1
                    flag += 1
                    print('{} 因打架受到1点伤害，当前受伤指数为 {} 点'.format(r.name, r.hurt))
                    time.sleep(0.5)
                # 口渴名单
                for th in self.thirsty:
                    if r.name == th:
                        r.hurt += 1
                        flag += 1
                        print('{} 因出现在口渴名单上而受到1点伤害，当前受伤指数为 {} 点'.format(r.name, r.hurt))
                        time.sleep(0.5)
                # 判断阳伞
                umb = 0
                for g in r.equip:
                    if g.name == '阳伞':
                        umb = 1
                        break
                if umb == 1 and r.hurt != 0 and flag > 0:
                    r.hurt -= 1
                # 喝水
                if flag > 0:
                    for i in range(flag):
                        r.drink()

        # 判断死亡状态
        for r in Seat:
            r.isDead()

        return Mew


# 创建航海决策堆（落海，口渴，打架，划船，海鸥）
def createSails():
    Sails = []
    def CreateSail(fail, thirsty, fight, quant, mew):
        sail = Sail(fail, thirsty, fight, quant, mew)
        Sails.append(sail)

    CreateSail(['法国佬'], ['船长', '大副', '法国佬', '史蒂芬先生'], 1, 1, 0)
    CreateSail(['小孩'], ['船长', '大副', '法国佬', '罗伦小姐'], 0, 0, 0)
    CreateSail(['小孩'], ['船长', '大副', '法国佬', '小孩'], 1, 0, 0)
    CreateSail(['法国佬'], ['船长', '大副', '小孩'], 0, 1, 0)
    CreateSail(['罗伦小姐'], ['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐'], 0, 1, -1)
    CreateSail(['大副'], ['船长', '大副'], 0, 1, 0)
    CreateSail(['大副'], ['船长', '法国佬'], 1, 1, 0)
    CreateSail(['小孩'], ['船长', '大副', '法国佬', '史蒂芬先生', '小孩'], 1, 1, 1)
    CreateSail(['史蒂芬先生'], ['船长', '史蒂芬先生'], 0, 0, 0)
    CreateSail(['史蒂芬先生'], ['船长', '大副', '法国佬'], 1, 1, 0)
    CreateSail(['史蒂芬先生'], ['船长', '小孩'], 0, 1, 1)
    CreateSail(['法国佬'], ['船长', '大副', '史蒂芬先生'], 0, 0, 1)
    CreateSail([], [], 0, 0, 1)
    CreateSail(['大副'], ['罗伦小姐'], 0, 0, 0)
    CreateSail(['法国佬'], ['船长', '大副', '罗伦小姐'], 1, 0, 0)
    CreateSail(['船长'], ['船长'], 0, 0, 0)
    CreateSail(['船长'], ['法国佬'], 0, 0, 0)
    CreateSail(['小孩'], ['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐'], 0, 1, 0)
    CreateSail(['史蒂芬先生'], ['船长', '罗伦小姐'], 1, 0, 0)
    CreateSail(['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐', '小孩'], ['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐', '小孩'], 1, 0, 0)
    CreateSail(['船长'], ['史蒂芬先生'], 1, 1, 0)
    CreateSail(['船长'], ['大副'], 1, 0, 1)
    CreateSail(['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐', '小孩'], ['船长', '大副', '法国佬', '史蒂芬先生', '罗伦小姐', '小孩'], 1, 1, 1)
    CreateSail(['大副'], ['小孩'], 1, 0, 1)
    return Sails

