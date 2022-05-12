from modular import mapper

find_sku = 'select ProductID from Product where ProductCode=\'{0}\''

find_poa = 'select pop.PropertyID,p.Productcode,pop.ProductID from Product p inner  join ' \
           'ProductOptionProperty pop on pop.ProductID=p.ProductID' \
           ' where pop.PropertyCode=\'{0}\''

amz_product_user = """SELECT u.UserName,pu.Id,pu.UserType,pu.UserId
FROM SellerCube.dbo.ProductUser (NOLOCK) pu
         INNER JOIN SellerCube.dbo.Users (NOLOCK) u ON pu.UserId = u.UserID
WHERE pu.ProductId = {sku_id};"""

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

        sql = amz_product_user.format(sku_id=sku_id)