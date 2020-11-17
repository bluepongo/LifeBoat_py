# 物资
class Good(object):
    score = 0
    describe = ''
    def __init__(self):
        self.id = 0
        self.name = '物资'
        self.special = 0
        self.delete = 0
    # 显示物资名称
    def showName(self):
        print(self.name)
    # 显示物资名称和描述
    def showInfo(self):
        print('{},{}'.format(self.name, self.describe))

# 珍品（物品）
class Treasure(Good):
    def __init__(self):
        self.name = '珍品'
        self.score = 0

# 武器（物品）
class Weapon(Good):
    def __init__(self):
        self.name = '武器'
        self.attack = 0
    def showInfo(self):
        print('{},体力:{}'.format(self.name, self.attack))

# 特殊物品（物品）
class Special(Good):
    def __init__(self):
        self.name = '特殊物品'
    def showInfo(self):
        print('{},'.format(self.name), end='')
        print('(效果)' + self.describe)
    def use(self, role):
        role.equip.append(self)
        role.hand.remove(self)
        print('{} 装备了 {}!'.format(role.name, self.name))

# 水（物品）
class Water(Good):
    def __init__(self):
        self.id = 1
        self.name = '水'
        self.special = 0
        self.describe = '在航海阶段使用，让任何一名角色免于1种口渴所造成的伤害，使用后立即丢弃。'

# 珠宝（珍品）
class Jewel(Treasure):
    def __init__(self):
        self.id = 2
        self.name = '珠宝'
        self.score = 1
        self.special = 0
        self.describe = '珠宝的价值会随持有的张数不同而改变： 1张=1分 2张=4分 3张=8分'

# 一把钞票（珍品）
class Money(Treasure):
    def __init__(self):
        self.id = 3
        self.name = '一把钞票'
        self.score = 1
        self.special = 0
        self.describe = '1分'

# 名画（珍品）
class Picture(Treasure):
    def __init__(self, score):
        self.id = 4
        self.name = '名画'
        self.score = score
        self.special = 0
        self.describe = str(score) + '分'

# 船桨（武器）
class Quant(Weapon):
    def __init__(self):
        self.id = 5
        self.name = '船桨'
        self.attack = 1
        self.special = 0
        self.describe = '可以当做武器使用和(或)在划船时，多选择两个航海决策。'
    def showInfo(self):
        print('{},体力:{}'.format(self.name, self.attack), end='')
        print('(效果)'+self.describe)

# 一记闷棍（武器）
class Stick(Weapon):
    def __init__(self):
        self.id = 6
        self.name = '一记闷棍'
        self.attack = 2
        self.special = 0

# 短刀（武器)
class Knife(Weapon):
    def __init__(self):
        self.id = 7
        self.name = '短刀'
        self.attack = 3
        self.special = 0

# 鱼钩（武器）
class Hook(Weapon):
    def __init__(self):
        self.id = 8
        self.name = '鱼钩'
        self.attack = 4
        self.special = 0

# 信号枪（武器）
class Gun(Weapon):
    def __init__(self):
        self.id = 9
        self.name = '信号枪'
        self.attack = 8
        self.special = 1
        self.describe = '可以当做武器使用，或执行。特殊行动：选择三个航海决策，立即处理海鸥的效应，决策的其他效果全部忽略，若使用这个效果，则马上丢弃此物品，三个航海决策放置末尾。'
    def showInfo(self):
        print('{},体力:{}'.format(self.name, self.attack), end='')
        print('(效果)' + self.describe)
    # 使用信号枪
    def use(self, role, SailStack, Mew):
        print('{} 使用了 信号枪，'.format(role.name), end='')
        for i in range(3):
            if SailStack[0].mew == 1:
                Mew += 1
            elif SailStack[0].mew == -1:
                if Mew != 0:
                    Mew -= 1
            SailStack.append(SailStack[0])
            SailStack.pop(0)
        print('目前为止，已经发现了 {} 只海鸥'.format(Mew))

        # 将信号枪移出游戏
        for g in role.hand:
            if g.name == '信号枪':
                role.hand.remove(g)
        for g in role.equip:
            if g.name == '信号枪':
                role.equip.remove(g)
        return Mew

# 救生圈（特殊物品）
class LifeBell(Special):
    def __init__(self):
        self.id = 10
        self.special = 0
        self.name = '救生圈'
        self.describe = '可以避免落海造成的伤害，也可以丢给落海但仍有意识的角色，但会让他们保留救生圈。'

# 阳伞（特殊物品）
class Umbrella(Special):
    def __init__(self):
        self.id = 11
        self.name = '阳伞'
        self.special = 1
        self.open = 0
        self.describe = '特殊行动：撑开阳伞。阳伞撑开后，你每回合可以避免一种口渴所造成的伤害。'
    # 使用阳伞
    def use(self, role, SailStack, Mew):
        print('{} 使用了 阳伞'.format(role.name))
        role.equip.append(self)
        self.open = 1
        role.hand.remove(self)
        return Mew

# 指南针（特殊物品）
class Compass(Special):
    def __init__(self):
        self.id = 12
        self.special = 0
        self.name = '指南针'
        self.describe = '当你是舵手时，在选择一个航海决策使用之前，从航海决策开头选择一个航海决策加入备选。'


# 物资堆
def createGoods():
    Goods = []
    # 生成多个相同物资（物资名称，数量）
    def CreateMany(good, count):
        for i in range(count):
            Goods.append(good)
    # 创建物资堆
    CreateMany(Water(), 15)
    CreateMany(Money(), 6)
    CreateMany(Picture(2), 1)
    CreateMany(Picture(3), 2)
    CreateMany(Jewel(), 3)
    CreateMany(Quant(), 2)
    CreateMany(Stick(), 1)
    CreateMany(Knife(),1)
    CreateMany(Hook(), 1)
    CreateMany(Gun(), 1)
    CreateMany(LifeBell(), 1)
    CreateMany(Umbrella(), 1)
    CreateMany(Compass(), 1)
    return Goods

# 介绍专用
def createOneGood():
    Goods = []
    # 生成多个相同物资（物资名称，数量）
    def CreateMany(good, count):
        for i in range(count):
            Goods.append(good)
    # 创建物资堆
    CreateMany(Water(), 1)
    CreateMany(Money(), 1)
    CreateMany(Picture(2), 1)
    CreateMany(Picture(3), 1)
    CreateMany(Jewel(), 1)
    CreateMany(Quant(), 1)
    CreateMany(Stick(), 1)
    CreateMany(Knife(),1)
    CreateMany(Hook(), 1)
    CreateMany(Gun(), 1)
    CreateMany(LifeBell(), 1)
    CreateMany(Umbrella(), 1)
    CreateMany(Compass(), 1)
    return Goods