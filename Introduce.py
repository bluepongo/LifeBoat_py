import Role
import Good
import time


# 角色集合
Roles = Role.createRoles()
# 物资集合
Goods = Good.createOneGood()

print('============游戏图鉴============')
# 角色介绍
print('============角色介绍============')
for role in Roles:
    role.showInfo()
    print('-----------------')

# 物资介绍
print('============物资介绍============')
for good in Goods:
    good.showInfo()
    print('-----------------')
time.sleep(1000000)