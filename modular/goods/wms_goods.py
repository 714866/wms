import copy
import random

from pymysql import IntegrityError

from modular.common.SqlChangeFormat import selectChangeInsert
from modular.common.commonDB import wmsCommonDB,WspCommonDB
from modular.goods.wms_sql import find_not_exict_goods_by_isr_box_id, find_goods_by_id, insert_goods_volume, \
    inset_goods_weight, goods_weight_exist_zero, update_goods_weight_valuse, goods_volume_exist_zero, \
    update_goods_volume_valuse, find_isr_goods_id_by_code, goods_volume_not_exict, goods_weight_not_exict, \
    find_goods_by_code


class WmsGoods(wmsCommonDB):




    def inser_goods_from_wsp_by_goods_code(self,goods_code):
        wsp_cursor = WspCommonDB().cursor
        wsp_goods_info = wsp_cursor.fetchall(find_goods_by_code(goods_code))
        goods_insert_sql = selectChangeInsert('goods', wsp_goods_info)
        print(goods_insert_sql)
        self.cursor.execute(goods_insert_sql)

    def insert_goods_by_wsp(self,isr_box_id):
        """
        查询wsp有产品信息，但wms没有的，对wms进行插入
        :param isr_box_id:
        :return:
        """
        wsp_cursor = WspCommonDB().cursor
        goods_id_list = self.cursor.fetchall(find_not_exict_goods_by_isr_box_id(isr_box_id))
        step = 50
        goods_id_list = [goods_id_list[i:i+step] for i in range(0,len(goods_id_list),step)]
        for goods_ids in goods_id_list:
            goods_ids = [str(i['id']) for i in goods_ids]
            goods_str = ','.join(goods_ids)
            wsp_goods_info = wsp_cursor.fetchall(find_goods_by_id(goods_str))
            goods_insert_sql = selectChangeInsert('goods',wsp_goods_info)
            self.cursor.execute(goods_insert_sql)
        self.cursor.commit()

    def fix_goods_weigth_and_volume(self,code):
        """
        对wms的goods_weigth和goods_volume 体积重数据为0，或者为空的数据进行补充
        :param code: 入库申请单，来源单，分箱号
        :return:
        """

        # sql = """select isrbi.goods_id
        #         from in_storage_request_box_item isrbi where isr_box_id = {0}""".format(1087775178703462400)
        # goods_ids_list = self.cursor.fetchall(sql)

        goods_ids_list = self.cursor.fetchall(find_isr_goods_id_by_code(code))
        #按50个产品分组[[{goods_Id:1}],[]]
        step=50
        goods_ids_list =[goods_ids_list[i:i+step] for i in range(0,len(goods_ids_list),step)]
        #查询产品体积表与重量表数值为0的
        for goods_list in goods_ids_list:
            # goods_id 列表转字符串
            goods_ids = [str(i['goods_id']) for i in goods_list]
            goods_str = ','.join(goods_ids)

            # 查询体重为0的，并且更新
            goods_weight_zero_list = self.cursor.fetchall(goods_weight_exist_zero(goods_str))
            if len(goods_weight_zero_list) > 0:
                goods_weight_id = ','.join([str(i['id']) for i in goods_weight_zero_list ])
                sql1 =  update_goods_weight_valuse(goods_weight_id ,random.randrange(10,100))
                self.cursor.execute(sql1)
            #查询体积有为0的，并且更新
            goods_volume_zero_list = self.cursor.fetchall(goods_volume_exist_zero(goods_str))
            if len(goods_volume_zero_list)>0 :
                goods_volume_id = ','.join([str(i['id']) for i in goods_volume_zero_list ])
                sql2 = update_goods_volume_valuse(goods_volume_id,random.randrange(10,200))
                self.cursor.execute(sql2)
            self.cursor.commit()

        #补充缺少体积重的数据
        for goods_ids in goods_ids_list:
            goods_id_list=[str(i['goods_id']) for i in goods_ids ]
            goods_str = ','.join(goods_id_list)
            exict_weight_goods_id_dict =  self.cursor.fetchall(goods_weight_not_exict(goods_str))
            goods_volume_id_list =  copy.deepcopy(goods_id_list)
            for goods_dict in exict_weight_goods_id_dict:
                if str(goods_dict['goods_id']) in  goods_id_list:
                    goods_id_list.remove(str(goods_dict['goods_id']))
            for goods_id in goods_id_list:
                try:
                    self.cursor.execute(inset_goods_weight(goods_id=goods_id))
                except IntegrityError as a:
                    print("已插入数据{0}".format(list))

            exict_volume_goods_id_dict = self.cursor.fetchall(goods_volume_not_exict(goods_str))
            for  goods_dict in   exict_volume_goods_id_dict:
                if str(goods_dict['goods_id']) in  goods_volume_id_list:
                    goods_volume_id_list.remove(str(goods_dict['goods_id']))
            for goods_id in goods_volume_id_list:
                try:
                    self.cursor.execute(insert_goods_volume(goods_id=goods_id))
                except IntegrityError as a:
                    print("已插入数据{0}".format(list))

                # try:
                #     self.cursor.execute(insert_goods_volume(goods_id=goods_id['goods_id'],type=0))
                # except IntegrityError as a:
                #     print("已插入数据{0}".format(list))
            self.cursor.commit()



if __name__ == '__main__':

    WmsGoods().fix_goods_weigth_and_volume('SFT-T1-20230323-00005')