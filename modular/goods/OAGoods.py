from modular import mapper
import xmltodict
import json

find_sku = 'select ProductID from Product where ProductCode=\'{0}\''

find_poa = 'select pop.PropertyID,p.Productcode,pop.ProductID from Product p inner  join ' \
           'ProductOptionProperty pop on pop.ProductID=p.ProductID' \
           ' where pop.PropertyCode=\'{0}\''

amz_product_user = """SELECT pu.Id,pu.UserType,pu.UserId
 FROM SellerCube.dbo.ProductUser (NOLOCK) pu
 WHERE pu.ProductId = {sku_id} and pu.UserType=1;"""

update_product_amzuser_sql = "update ProductUser set UserId={user_id} where id={id}"

inser_product_amzuser_sql = """INSERT INTO SellerCube.dbo.ProductUser ( ProductId, UserType, UserId ,
                                        OaProductUserName)
VALUES ( {ProductId}, 1, 21488, N'');"""

class goodsSql():
    global find_sku
    global find_poa

    def __init__(self):
        self.cursor = mapper.connect_sqlserve()

    def findOaGoodsBySku(self, sku_code):
        sql = find_sku.format(sku_code)
        oa_sku = self.cursor.fetchone(sql)
        return oa_sku['ProductID']

    def findOaGoodsByPoa(self, poa_code):
        sql = find_poa.format(poa_code)
        oa_poa = self.cursor.fetchone(sql)

        return {'poa_id': oa_poa['PropertyID'], 'sku_code': oa_poa['Productcode'], 'sku_id': oa_poa['ProductID']}

    def updateGoodsAMZ(self,sku_id):
        """
        产品用户表中userid为0，则更新产品用户表userid=21488
        产品用户表为空，则插入用户表
        :param sku_id:
        :return:
        """
        sql = amz_product_user.format(sku_id=sku_id)
        resulst = self.cursor.fetchone(sql)
        if resulst is not None and resulst['UserId']==0:
            """ 处理产品用户表中用户Id为0的"""
            resulst['UserId']=21488
            self.cursor.executeAndcommit(update_product_amzuser_sql.format(user_id=resulst['UserId'],id=resulst['Id']))
        elif resulst is None:
            """无 产品用户表的需插入"""
            self.cursor.executeAndcommit(inser_product_amzuser_sql.format(ProductId=sku_id))

    def inserProcessCenterTransShipPrice(self,source_process_id,targer_process_id,shift_type):
        """
        插入处理中心转运价
        :param source_process_id:
        :param targer_process_id:
        :param shift_type:
        :return:
        """
        inser_price_sql = """INSERT INTO SellerCube.dbo.ProcessCenterTransShipPrice (FromProcessCenterID, ToProcessCenterID, ShipType,
                                                        TransShipmentPrice, CreatedDate, IsDeleted, IsCalcVolume,
                                                        CalcVolumeNumber, BillingModel, BillingWeight,VATTaxRate,IsVAT)
VALUES ({source_process_id}, {targer_process_id}, '{shift_type}', 1.000, GETDATE(), 0, 0, 0.000, 0, 0,0.000000,0 );"""
        self.cursor.executeAndcommit(inser_price_sql.format(source_process_id=source_process_id,targer_process_id=targer_process_id,shift_type=shift_type))
        return True

    def updateCheckProductShiftRequest(self,shiftType):
        sql = "select Detail from SystemConfig where code = 'CheckProductShiftRequest';"
        result = self.cursor.fetchone(sql)
        xml_parse = xmltodict.parse(result['Detail'])
        content = xml_parse['c']['freeGoodsTypeList']['#text'] #获取免兼容货位类型运输方式处理中心配置数据
        dict_content = json.loads(content)
        dict_content.append(int(shiftType))
        xml_parse['c']['freeGoodsTypeList']['#text'] = str(dict_content)

        s = xmltodict.unparse(xml_parse).split('<?xml version="1.0" encoding="utf-8"?>\n')[1]
        update_sql = "update SystemConfig set Detail='{0}' where code = 'CheckProductShiftRequest'".format(s)
        print(update_sql)
        self.cursor.executeAndcommit(update_sql)

        return True

if __name__=="__main__":
    testsql = goodsSql()
    testsql.updateCheckProductShiftRequest(27,2,1130)
