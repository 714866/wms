

sql_get_PPL_to_instorage = """
select 
        pk.PackageID,
        ISNULL(pk.FPLCode, pk.PackageCode) AS packageCode,
        pp.PurchaseCenterID AS OriginProcessCenterId,
        ppi.ProcessCenterID AS TargetProcessCenterId,
        pk.Quantity ,
        pk.CreateUserID,
        pk.CreateTime,
        pk.LastUpdateUserID,
        pk.LastUpdateTime,
        (CASE
        WHEN ppi.ShipType = 'Airfreight' THEN 1
        WHEN ppi.ShipType = 'Airlift' THEN 2
        WHEN ppi.ShipType = 'General' THEN 3
        WHEN ppi.ShipType = 'Seaway' THEN 4
        WHEN ppi.ShipType = 'Sample' THEN 5
        WHEN ppi.ShipType = 'MoveStorage' THEN 6
        WHEN ppi.ShipType = 'Railway' THEN 7
        WHEN ppi.ShipType = 'Ground' THEN 8
        WHEN ppi.ShipType = 'Vessel' THEN 9
        WHEN ppi.ShipType = 'ExpressGround' THEN 10
        ELSE 3
        END
        ) AS ShipType,
        ppi.ProductID,
        ISNULL(ppi.PropertyID, 0) AS PropertyID,
        (
        CASE WHEN ppi.IsTestPass IS NOT NULL AND ppi.IsTestPass = 1 THEN 0 ELSE ISNULL(p.isTest, 0) END
        ) AS IsTest,
        ppi.AmazonShop,
        ppi.ProductBarCode as deliveryProductCode ,
        pc.Type processCenterType,
        0 AS GoodsType ,
        asp.DestinationFulfillmentCenterId as storageCode,
        ppi.IsDrawback AS isDrowback,ppi.IsShiftCosting,
        (
			CASE
			WHEN EXISTS(SELECT 1 FROM Product_RelatedPdcLabel prpl WHERE prpl.ProductLabel_ID = 194 AND prpl.ProductID = ppi.ProductID)
			OR
			(p.Platform IN (1, 24) AND p.BaseType = 2 AND NOT EXISTS(SELECT 1 FROM Product_RelatedPdcLabel prpl WHERE prpl.ProductLabel_ID = 195 AND prpl.ProductID = ppi.ProductID))
			OR
			(p.Platform IN (1, 24) AND EXISTS(SELECT 1 FROM ProductCategoryMapping pcm WHERE pcm.CategoryID = 405 AND pcm.ProductCode = p.ProductCode) AND NOT EXISTS(SELECT 1 FROM Product_RelatedPdcLabel prpl WHERE prpl.ProductLabel_ID = 195 AND prpl.ProductID = ppi.ProductID))
			THEN 1
			ELSE 0
			END
		) AS vacuumPacking,
		p.Platform as salePlatform,
		(CASE WHEN ppi.PurchaseType IN(13,14) THEN 1 ELSE 0 END) AS goodsSize,
		ISNULL(
		pk.ShipmentId,
		'') AS shipmentId,
        (CASE
        WHEN ppi.Speed = 0 THEN '普通'
        WHEN ppi.Speed = 1 THEN '紧急'
        WHEN ppi.Speed = 18 THEN '平急'
        WHEN ppi.Speed = 19 THEN '特急'
        WHEN ppi.Speed = 20 THEN '正常'
        WHEN ppi.Speed = 21 THEN 'fba紧急'
        WHEN ppi.Speed = 22 THEN 'fba平急'
        WHEN ppi.Speed = 23 THEN 'fba正常'
        WHEN ppi.Speed = 24 THEN 'fba特急'
        ELSE ''
        END
        ) AS speed
FROM PurchasePackage pk
        INNER JOIN ProductPurchaseItem ppi ON pk.PurchaseItemID = ppi.ItemID
        INNER JOIN ProductPurchase pp ON ppi.PurchaseID = pp.PurchaseID
        INNER JOIN Product p ON ppi.ProductID = p.ProductID
        LEFT JOIN ProductOptionProperty pop ON ppi.PropertyID = pop.PropertyID
        INNER JOIN SellerCube.dbo.ProcessCenter pc ON ppi.ProcessCenterID = pc.ProcessCenterID
        INNER JOIN SellerCube.dbo.ProductPurchase ppk ON ppk.PurchaseID= ppi.PurchaseID
        LEFT JOIN SellerCube.dbo.AmazonInboundShipmentPlan asp on asp.ShipmentId = pk.ShipmentId
        WHERE 
--               pk.Status IN (1,2,3,4)
--  AND 
              pk.PackageCode IN ({0});
"""