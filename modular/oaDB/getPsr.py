from modular import mapper
from modular.common.SqlChangeFormat import  list_to_str

find_psr = """   SELECT
        
          psr.ProductShiftRequestCode AS productShiftRequestCode,
        psr.ProductID AS productId,
        ISNULL(psr.PropertyID, 0) AS propertyId,
        psr.Quantity AS quantity,
        psr.SourceProcessCenterID AS originProcessCenterId,
        psr.ProcessCenterID AS targetProcessCenterId,
        psr.ShipType AS shipType,
        ISNULL(
        pop.PropertyCode,
        p.ProductCode
        ) AS baseProductCode,
        psr.PriorityLevel AS priorityLevel,
        ISNULL(psr.shipmentId, '') AS shipmentId,
        psr.GoodsType AS goodsType,
        ISNULL(psr.DeliveryProductCode, '') AS deliveryProductCode,
        psr.IsSelfPacked AS isSelfPacked,
        psr.IsFullBox AS isFullBox,
        psr.BoxQuantity AS boxQuantity,
        CAST(psr.ModifyTimeStamp AS BIGINT) AS modifyTimeStamp,
        CASE psr.GoodsType
        WHEN 4 THEN
        ISNULL(
        aisp.DestinationFulfillmentCenterId,
        ''
        )
        ELSE
        ISNULL(psr.StorageCode, '')
        END storageCode,
        ISNULL(psr.AmazonShop, '') AS amazonShop,
        ISNULL(psr.AmazonCustomerLabel, '') AS amazonCustomerLabel,
        psr.CreateDate,
        psr.AuditTime,
        psr.LastUpdateTime,
        ISNULL((SELECT 1 FROM Product_RelatedPdcLabel prpl WHERE prpl.ProductID = psr.ProductID AND prpl.ProductLabel_ID = 163 AND prpl.IsDeleted = 0), 0) AS goodsSize

        FROM
        SellerCube.dbo.ProductShiftRequest psr
        INNER JOIN SellerCube.dbo.Product p ON p.ProductID = psr.ProductID
        LEFT JOIN SellerCube.dbo.ProductOptionProperty pop ON p.ProductID = pop.ProductID
        AND pop.PropertyID = ISNULL(psr.PropertyID, 0)
        LEFT JOIN SellerCube.dbo.ShiftRequestToAmazonShipment sras ON psr.ShiftRequestID = sras.ShiftRequestID
        LEFT JOIN SellerCube.dbo.AmazonInboundShipmentPlan aisp ON aisp.ShipmentId = sras.ShipmentId
        WHERE  1=1

        and psr.ProductShiftRequestCode in ({0});"""

update_process_by_psr = """ update  SellerCube.dbo.ProductShiftRequest set ProcessCenterID={process} where ProductShiftRequestCode in ({psr_codes})"""

find_psr_targeprocess = """select ProcessCenterID from  SellerCube.dbo.ProductShiftRequest where   ProductShiftRequestCode = ('{psr_code}') """

class PsrMessage():

    def __init__(self):
        self.cursor = mapper.connect_sqlserve()

    def findPsrMessage(self, psr_codes):
        """
        根据调拨请求单号查询数据库获取生成源单所需参数，
        sql从以下接口逻辑获取
        http://172.16.11.39:9996/oa-sync-server/syncapi/productshift-request/queryProductShiftRequestToWsp?modifyTimeStamp=
        :param psr_codes:
        :return: 返回生成调拨申请源单数据
        """
        psr_code_str = list_to_str(psr_codes)
        sql = find_psr.format(psr_code_str)
        psr_message = self.cursor.fetchall(sql)
        return psr_message

    def getPsrCodeByGoodsType(self,goods_type):
        sql = "select ProductShiftRequestCode from ProductShiftRequest where  GoodsType=17 order by ProductShiftRequestCode desc ;".format(goods_type)
        psr_message = self.cursor.fetchone(sql)
        return psr_message['ProductShiftRequestCode']

    def findTargeProcess(self,psr_code):

        sql = find_psr_targeprocess.format(psr_code=psr_code)
        targe_process_id = self.cursor.fetchone(sql)['ProcessCenterID']
        return targe_process_id
    def updatePsrTargeProcess(self, psr_codes, process):
        """
        变更调拨请求目标处理中心， 初始设计原因，wps生成pck根据oa调拨请求目标处理中心进行不同处理，需要变更为不需要生成文件的处理中心，
        减少无法生成pck的情况
        :param psr_codes: 需要变更调拨请求单号
        :param process:  变更处理中心值
        :return:
        """
        psr_code_str = list_to_str(psr_codes)
        sql = update_process_by_psr.format(process=process, psr_codes=psr_code_str)
        self.cursor.execute(sql)
        self.cursor.commit()

    def updatePsrBstatus(self,top_num):
        """
        更新调拨请求状态，符合正常下发流程，
        :param top_num:
        :return: 返回更新后的调拨请求单号
        """
        select_psr = 'select top {num} ShiftRequestID,ProductShiftRequestCode  from ProductShiftRequest where bStatus=0 order by CreateDate desc'
        psrs = self.cursor.fetchall(select_psr.format(num=top_num))
        psr_ids = ''
        psr_codes = []
        count = 0
        for psr in psrs:
            psr_codes.append(psr['ProductShiftRequestCode'])
            psr_id = str(psr['ShiftRequestID'])
            psr_ids = psr_ids + psr_id + ','
        psr_ids = psr_ids.strip(',')
        # updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in (select top 10 ShiftRequestID from ProductShiftRequest order by ShiftRequestID desc ); '
        updateSql = 'update ProductShiftRequest set bStatus=1 , AuditState=2 where ShiftRequestID in ({0}); '.format(
            psr_ids)
        self.cursor.execute(updateSql)
        self.cursor.commit()
        print('修改状态，能正常下发wsp的调拨请求{0}'.format(psr_codes))
        return psr_codes

if __name__=="__main__":

    get_Psr=PsrMessage()
    b=['PSR-A0-20190327-0642','PSR-A0-20190327-0658']
    # get_Psr.findPsrMessage(b)
    get_Psr.updatePsrBstatus(10)


