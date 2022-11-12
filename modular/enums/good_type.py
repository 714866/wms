import copy
from enum import Enum

class GoodsType(Enum):
    General=0  # 普通
    Sample = 2  # 样品
    StockUp = 3 #备货
    FBA =  4  # FBA调拨
    NewProductForOverSea = 6 # 海外新品调拨
    Wholesale = 7 #批发
    Advertisement = 8 # 广告推广
    StockUpBySeaway = 9 # 海运备货
    StockUpForFBA = 12 # FBA备货
    Material = 13 # 耗材
    ReturnGoodsFromFBA = 14 # FBA退货
    MoveStorage = 15 # 转仓
    FashionOrder = 16 # 红人订单
    FBC = 17 # FBC调拨
    JN = 18 # 捷网调拨
    FBJ = 19 # FBJ调拨
    B2S2C = 20 # 共享仓调拨
    FBW = 21 # FBW
    FBY = 22 # FBY
    JDC = 23 # JDC
    FBL = 24 # FBL
    FBN = 25 # FBN调拨
    HBA = 26 # HBA调拨
    Winit = 27 # 万邑通调拨
    FourthPX = 28 # 递四方调拨
    FBD = 29 # FBD调拨
    FBM = 30 # FBM调拨
    驿川 = 31 # 驿川  枚举名称为中文
    RefundIn = 32 # 退供（入库）
    FBS = 33 # FBS调拨
    WFS = 34 # WFS调拨
    退件调拨 = 35 # 退件调拨
    三方仓调拨 = 36 # 三方仓调拨   为京东调拨类型
    FBE = 37 # FBE调拨
    IML = 38 # 艾姆勒调拨
    GC = 37 # 谷仓调拨
    TM = 38 # 天马调拨
    Alljoy = 41 # 全和悦调拨
    CG = 42 # CG调拨
    NewEgg = 43 # 新蛋调拨
    BC = 45 # 搬仓
    SeaStar = 46 # 海星调拨
    VC = 47 # VC调拨

__goods_type_option = [ str(x.value)+'-'+x.name  for x in GoodsType]

def goods_type_option_enum():


    return copy.deepcopy(__goods_type_option)

# goods_type_option_enum = list_p = [x.name + '-' + str(x.value) for x in GoodsType]
if __name__=="__main__":
    # print(GoodsType.Vessel)
    # print(GoodsType(1).name)
    print(GoodsType['退件调拨'].value)

    print(GoodsType['三方仓调拨'])
    list_p = goods_type_option_enum()
    print(list_p)
    print(GoodsType.驿川.value)
