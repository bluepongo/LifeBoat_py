# 游戏主函数

import Role
import random
import Else
import time
import operator
import Good
import Sail

# 角色集合
Roles = Role.createRoles()
# 游戏AI
AI = []
# 喜爱的人
Lover = []
# 憎恨的人
Hater = []
# 位置
Seat = []
# 航海决策堆
SailStack = []
# 航海决策预备堆
preSail = []

print('=====欢迎进入LifeBoat=====')

# 确认游戏人数
playernum = Else.playernum()
print('当前游戏人数为 {} 人'.format(playernum))

# 确认标识
confirm = 1
# 选择角色
while confirm:
    print('=======请选择你的角色========')
    i = 1
    for role in Roles:
        # Else.showNameSkill('{}.'.format(i), role)
        print('{}.'.format(i), end='')
        role.showInfo()
        i += 1
    print('==========================')
    number = Else.inputnum(1, i)

    for role in Roles:
        if(role.seat == number):
            print('已选择 {} '.format(role.name))
            confirm = Else.confirm()
            break
# 获取身份
Me = role
# 角色中去掉玩家获取身份，防止出现身份重复的情况
Roles.pop(number - 1)
# 打乱角色集合
random.shuffle(Roles)

# 游戏AI获取身份
for i in range(playernum-1):
    Roles[0].ai = i + 1
    AI.append(Roles[0])
    Roles.pop(0)
# 展示所有人身份
print('==========================')
Else.showNameSkill('我:', Me)
Else.load('正在分配AI角色', 4)
for i in range(playernum-1):
    Else.showNameSkill('AI{}号：'.format(i+1), AI[i])
    time.sleep(0.5)
print('==========================')

# 分配喜爱和憎恨的人
Else.load('正在分配喜爱和憎恨的人', 3)
Else.loverorhater(playernum, Me, AI, 'lover')
time.sleep(0.5)
Else.loverorhater(playernum, Me, AI, 'hater')
print('==========================')
time.sleep(0.5)

Else.load('即将登船', 3)

# 上船分配座位
AI.append(Me)
for ai in AI:
    Seat.append(ai)
cmp = operator.attrgetter('seat')
Seat.sort(key=cmp)
AI.pop(-1)
Else.showSeat(Seat)
print('==========================')

# 生成物资堆
time.sleep(0.5)
GoodsStack = Good.createGoods()
random.shuffle(GoodsStack)
print('物资生成成功！')
time.sleep(0.5)

# 生成航海决策堆
time.sleep(0.5)
SailStack = Sail.createSails()
random.shuffle(SailStack)
print('决策生成成功！')
time.sleep(0.5)

# 初始海鸥数为0
Mew = 0
round = 1
WinMew = 4
print('==========================')
Else.load('做好准备，游戏即将正式开始,当发现 {} 只海鸥时，游戏立刻结束'.format(WinMew), 4)

# 进入正式游戏循环
while Mew < WinMew:
    # 准备阶段
    # 清空所有船上角色的预备伤害、行动标记
    for role in Seat:
        role.boathurt = 0
        role.fighthurt = 0
        role.act = 0
    # A 物资阶段
    print('=======（第{}轮）物资阶段========'.format(round))
    time.sleep(0.5)
    if len(GoodsStack) != 0:
        preGoods = Else.extractGoods(Seat, GoodsStack)
        for role in Seat:
            if role.dead == 0:
                if role.ai == 0:
                    role.playerChooseGoods(preGoods)
                else:
                    role.aiChooseGoods(preGoods)
            elif role.dead == 1 and role.ai == 0:
                print('所选角色已死亡，跳过物资阶段。')
    else:
        print('船上已经没有剩余物资，跳过物资发放阶段。')

    # B 行动阶段
    # 交换座位存在行动顺序问题
    print('=======（第{}轮）行动阶段========'.format(round))
    time.sleep(0.5)
    i = 1
    while i <= len(Seat):
        if Seat[i - 1].dead == 0 and Seat[i - 1].act == 0:
            name = Seat[i - 1].name
            if Seat[i - 1].ai == 0:
                Mew = Seat[i - 1].playerChooseAct(preSail, SailStack, Seat, Mew)
                time.sleep(1)
            else:
                Mew = Seat[i - 1].aiChooseAct(preSail, SailStack, Seat, Mew)
                time.sleep(1)
            if Mew >= WinMew:
                break
            if name != Seat[i - 1].name:
                j = 1
                # 确定被换座人的序号j
                while j <= len(Seat):
                    if name == Seat[j - 1]:
                        break
                    j += 1
                if j > i:
                    i -= 1
        i += 1
    if Mew >= WinMew:
        break
    # C 航海阶段
    print('=======（第{}轮）航海阶段========'.format(round))
    time.sleep(0.5)
    role = None
    # 确定本回合掌舵人
    for r in Seat:
        if r.dead == 0:
            role = r
    if role == None:
        print('全体死亡。')
        time.sleep(0.5)
        break
    # 佩戴指南针
    for g in r.hand:
        if g.name == '指南针':
            g.use(r)
            break

    # 判断角色是否装备指南针
    for g in r.equip:
        if g.name == '指南针':
            preSail.append(SailStack[0])
            SailStack.pop(0)

    # 执行航海决策的指令
    if len(preSail) != 0:
        if role.ai == 0:
            Mew = role.playerSail(preSail, Mew, Seat)
            time.sleep(1)
        else:
            Mew = role.aiSail(preSail, Mew, Seat)
            time.sleep(1)
    else:
        print('这轮没有人划船，跳过航海阶段')
        time.sleep(0.5)

    # 剩余决策重新加入SailStack
    for s in preSail:
        SailStack.append(s)

    # 当前人物状态
    print('=======当前所有人物状态========')
    print('当前已经看到 {} 只海鸥'.format(Mew))
    for r in Seat:
        print('{} 拥有 {} 个物资，体力值为 {} 点，当前受伤 {} 点'.format(r.name, len(r.hand), r.hp, r.hurt), end='')
        if r.dead == 1:
            print(',已死亡。')
        else:
            print('。')

    # 轮次加1
    round += 1

print('=======恭喜！到达目的地！========')
Else.countScore(Seat)
Else.load('分数计算中，请稍后', 4)
print('分数计算完毕！')
time.sleep(0.5)
print('============排行榜=============')
time.sleep(1)
cmp = operator.attrgetter('score')
Seat.sort(key=cmp)
Seat.reverse()
i = 1
for r in Seat:
    sss = '（存活）'
    if r.dead == 1:
        sss = '（死亡）'
    if r.ai == 0:
        print('第 {} 名：我, {}{} ,得分： {}'.format(i, r.name, sss, r.score))
    else:
        print('第 {} 名：AI{}号, {}{} ,得分： {}'.format(i, r.ai, r.name, sss, r.score))
    lll = '（存活）'
    hhh = '（存活）'
    if r.lover.dead == 1:
        lll = '（死亡）'
    if r.hater.dead == 1:
        hhh = '（死亡）'
    print('喜欢的人是： {}{} ,憎恨的人是： {}{}'.format(r.lover.name, lll, r.hater.name, hhh))
    print('手中的物资有：', end='')
    if len(r.hand) == 0:
        print('-', end='')
        print()
    else:
        for g in r.hand:
            print('{}'.format(g.name, g.score), end='')
            if g.score:
                print('({}分) '.format(g.score), end='')
            else:
                print(' ', end='')
        print()
    print('-------------------------')
    time.sleep(1)
    i += 1
r = Seat[0]
if r.ai == 0:
    print('恭喜 我 ，获得胜利！')
else:
    print('恭喜 AI{}号 ，获得胜利！'.format(r.ai))
print('============游戏结束=============')
time.sleep(100)





