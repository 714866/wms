global data_poa, data1
data_poa = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "26", "priorityLevel": "0", "shipType": "1", "processCenterId": "1087",
         "sourceProcessCenterId": 7, "remark": "sd", "sourceProcessCenterName": "广州处理中心",
         "processCenterName": "惠州博罗HBA处理中心", "quantity": "2", "productId": 511598, "propertyId": 713343,
         "storageQuantity": 55, "originStorageId": 4, "originStorageName": "广州发货仓库", "productCode": "SKU309964",
         "productName": "xxx", "propertyCode": "POA692034", "transferPrice": 0, "amazonShop": "chengxidianzi01",
         "shopId": "439848661963378688", "deliveryProductCode": "X000UOZH1B2"}]

}

data_sku1 = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "26", "priorityLevel": "0", "shipType": "3", "processCenterId": "1087",
         "sourceProcessCenterId": "1040", "remark": "fbc", "sourceProcessCenterName": "香港处理中心",
         "processCenterName": "惠州博罗HBA处理中心", "quantity": "3", "productId": 1425194, "propertyId": "",
         "storageQuantity": 37, "originStorageId": 370, "originStorageName": "香港发货仓库", "productCode": "SKU986500",
         "productName": "XXX", "propertyCode": "", "transferPrice": 0, "amazonShop": "PROMORE",
         "shopId": "662344609522913280", "deliveryProductCode": "6414970632538"}]

}

data_sku = {
    "productShiftRequestCreateVOS": [
        {"shiftType": "26", "priorityLevel": "0", "shipType": "3", "processCenterId": "1087",
         "sourceProcessCenterId": "1040", "remark": "fbc", "sourceProcessCenterName": "香港处理中心",
         "processCenterName": "惠州博罗HBA处理中心", "quantity": "3", "productId": 1488131,
         "storageQuantity": 37, "originStorageId": 370, "originStorageName": "香港发货仓库", "productCode": "SKU654734",
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
