global data_poa, data1
data_poa = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "17", "priorityLevel": "0", "shipType": "4", "processCenterId": "1078",
         "sourceProcessCenterId": "1040", "remark": "fbc", "sourceProcessCenterName": "广州处理中心",
         "processCenterName": "法国赛斯塔FBC处理中心", "quantity": "3", "productId": 1004320, "propertyId": 2000346,
         "storageQuantity": 37, "originStorageId": 370, "originStorageName": "广州发货仓库", "productCode": "SKU654734",
         "productName": "XXX", "propertyCode": "POA1989947", "transferPrice": 0, "amazonShop": "UNIQUE V",
         "shopId": "662344609522913280", "deliveryProductCode": "3282926120193"}]

}

data_sku1 = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "17", "priorityLevel": "0", "shipType": "3", "processCenterId": "1078",
         "sourceProcessCenterId": "1040", "remark": "fbc", "sourceProcessCenterName": "广州处理中心",
         "processCenterName": "法国赛斯塔FBC处理中心", "quantity": "3", "productId": 1425194, "propertyId": "",
         "storageQuantity": 37, "originStorageId": 370, "originStorageName": "广州发货仓库", "productCode": "SKU986500",
         "productName": "XXX", "propertyCode": "", "transferPrice": 0, "amazonShop": "PROMORE",
         "shopId": "662344609522913280", "deliveryProductCode": "6414970632538"}]

}

data_sku = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "17", "priorityLevel": "0", "shipType": "3", "processCenterId": "1078",
         "sourceProcessCenterId": "1040", "remark": "fbc", "sourceProcessCenterName": "香港处理中心",
         "processCenterName": "法国赛斯塔FBC处理中心", "quantity": "3", "productId": 1488131,
         "storageQuantity": 37, "originStorageId": 370, "originStorageName": "广州发货仓库", "productCode": "SKU654734",
         "productName": "XXX", "transferPrice": 0, "amazonShop": "PROMORE",
         "shopId": "662344609522913280", "deliveryProductCode": "6472063406343"}]

}


def return_api_FBC_data(is_poa):
    if is_poa:
        return_data = data_poa
    else:
        return_data = data_sku1

    return return_data


if __name__ == "__main__":
    print((17))
