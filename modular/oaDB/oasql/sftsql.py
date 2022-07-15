


sql_get_sft_to_instorage="""SELECT top 10
        psi.ProductShitItemCode AS originCode,
        psi.OriginCode AS productShitItemOriginCode,
        ps.ProductID AS productId,
        ISNULL(ps.PropertyID, 0) AS propertyId,
        ISNULL(psbi.Quantity, ps.Quantity) AS quantity,
        s.ProcessCenterID AS originProcessCenterId,
        ss.ProcessCenterID AS targetProcessCenterId,
        ISNULL(
        pop.PropertyCode,
        p.ProductCode
        ) AS baseProductCode,
        psi.ShipType AS shipType,
        psi.GoodsType  AS goodsType,
        ISNULL(psb.Length, 0) AS length,
        ISNULL(psb.Width, 0) AS width,
        ISNULL(psb.Height, 0) AS height,
        ISNULL(psb.Weight, 0) AS weight,
        psi.ModifyDate AS modifyTimeStamp,
        ISNULL(asp.DestinationFulfillmentCenterId, '') AS storageCode,
        ISNULL(ps.DeliveryProductCode, '') AS deliveryProductCode,
        ISNULL(ps.AmazonShop, '') AS amazonShop,
        (CASE WHEN psb.OriginBoxCode IS NOT NULL AND psb.OriginBoxCode != '' THEN psb.OriginBoxCode ELSE ISNULL(psb.ProductShiftBoxCode, '') END) AS productShiftBoxCode,
        ISNULL(ps.DetailLabel, '') AS detailLabel,
        ISNULL(psb.IsFull, ps.IsFull) AS ful,
        ISNULL(psi.RelativeCode, '') AS relativeCode,
        psi.traceID AS traceCode,
        psl.LogId AS logId,
        psi.GoodsSize as goodsSize,
        isnull(psbi.OriginCode,'') as  fboxItemOriginCode,
        p.Platform as type
       FROM
        SellerCube..ProductShiftItem (NOLOCK) psi
        INNER JOIN SellerCube..ProductShift (NOLOCK) ps ON ps.ProductShiftItemID = psi.ID
        INNER JOIN SellerCube..ProductShiftLog psl ON psi.ID = psl.ShiftID AND psl.ToStatus = '6'
        INNER JOIN SellerCube..Storage s ON psi.FromStorageID = s.StorageID
        INNER JOIN SellerCube..Storage ss ON psi.ToStorageID = ss.StorageID
        INNER JOIN SellerCube..Product p ON p.ProductID = ps.ProductID
        LEFT JOIN SellerCube..ProductShiftBoxItem psbi ON ps.ShiftID = psbi.ShiftID AND psbi.ProductID =
        ps.ProductID AND psbi.PropertyID = ISNULL(ps.PropertyID, 0) AND psbi.Status <> -1
        LEFT JOIN SellerCube..ProductShiftBox psb ON psbi.ProductShiftBoxId = psb.ProductShiftBoxId AND psb.Status <> -1
        LEFT JOIN SellerCube..ProductOptionProperty pop ON pop.PropertyID = ps.PropertyID
        LEFT JOIN SellerCube.dbo.AmazonInboundShipmentPlan asp on asp.ShipmentId = ps.AmazonShipmentID
        WHERE
       -- psi.LastTraceStatus = 6
        -- AND 
        psi.ProductShitItemCode in ( {sft_codes})
        -- AND ps.Deleted = 0
        -- AND ps.Complete = 0
        -- AND ps.CompleteQuantity = 0
        -- AND psi.Status = 1
        AND psi.Deleted = 0;
"""