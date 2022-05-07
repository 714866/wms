from modular import mapper

find_psr = """   SELECT
        TOP 10
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
        WHERE
        psr.ShiftStatus = 0
        AND psr.AuditState = 2
        AND psr.bStatus = 1
        AND psr.IsCompleted = 0
        and psr.ProductShiftRequestCode in ({0});"""


class PsrMessage():

    def __init__(self):
        self.cursor = mapper.connect_sqlserve()

    def findPsrMessage(self, psr_codes):
        psr_code_str=''
        for psr_code in psr_codes:
            psr_code_str+='\''+psr_code+'\','
        psr_code_str=psr_code_str.strip(',')
        sql = find_psr.format(psr_code_str)
        psr_message = self.cursor.fetchall(sql)
        return psr_message



if __name__=="__main__":

    get_Psr=PsrMessage()
    b=['PSR-A0-20190327-0642','PSR-A0-20190327-0658']
    get_Psr.findPsrMessage(b)


