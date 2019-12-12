# -*- coding: utf-8 -*- 
# @Time    : 2019/12/10 16:29 
# @Author  : p0st
# @Site    :  
# @File    : disk.py
# @Software: PyCharm
from web_cmdb import models
from .base import BasePlugins

class Disk(BasePlugins):

    def process(self, info, host_obj):
        if not info['status']:
            print('采集资产错误', info['error'])
            return
        disk_info = info['data']
        # 获取原数据库中的数据，将槽位也变成集合
        old_db = models.Disk.objects.filter(asset=host_obj)
        # {"0":obj,"1":obj}
        old_db_dict = {obj.slot: obj for obj in old_db}
        old_db_slot_set = set(old_db_dict.keys())
        # 获取新汇报过来数据的槽位，变成集合
        new_db_slot_set = set(disk_info.keys())

        # 根据新的集合-旧的集合=新增的槽位集合
        create_slot_set = new_db_slot_set - old_db_slot_set
        # 根据旧的集合-新的集合=删除的槽位集合
        remove_slot_set = old_db_slot_set - new_db_slot_set
        # 根据新的集合&旧的集合=更新的槽位集合，里面可能有更新，也可能没有更新
        update_slot_set = old_db_slot_set & new_db_slot_set

        # 新增操作，
        recode_msg_list = []  # 操作记录的列表
        msg_dict = {}
        create_object_list = []  # 将所有的新增数据添加到列表中，一次性提交到数据库
        for slot in create_slot_set:
            # models.DiskInfo.objects.create(**disk_info[slot],host=host_obj)
            create_object_list.append(models.Disk(**disk_info[slot], asset=host_obj))
            msg_dict[slot] = disk_info[slot]['capacity']
        # bluck_create:是一次性操作，不用多次连接数据库，batch_size一次新增10条
        if create_slot_set:  # 判断create_slot_set有值才是新增
            models.Disk.objects.bulk_create(create_object_list, batch_size=10)
            for item in msg_dict:
                msg = "【新增硬盘】在%s槽位新增了容量为%sG的硬盘" % (item, msg_dict[item])
                recode_msg_list.append(msg)

        # 删除操作
        if remove_slot_set:
            models.Disk.objects.filter(slot__in=remove_slot_set, asset=host_obj).delete()
            for item in remove_slot_set:
                msg = "【删除硬盘】在%s槽位删除了容量为%sG的硬盘" % (item, old_db_dict[item].capacity)
                recode_msg_list.append(msg)

        # 更新操作
        for slot in update_slot_set:  # 将老数据和新数据一样的槽位的数据取出来进行比对
            temp = []
            old_dict = old_db_dict[slot]
            net_dict = disk_info[slot]
            for key, value in net_dict.items():
                if value != getattr(old_dict, key):  # 通过反射将对象的值取出来
                    msg = "%s由%s变更为%s" % (key, getattr(old_dict, key), value)
                    temp.append(msg)
                    setattr(old_dict, key, value)  # 通过setattr将新值赋值，并保存
            if temp:
                slot_msg = "【更新硬盘】槽位%s：%s" % (slot, ",".join(temp))
                recode_msg_list.append(slot_msg)
                old_dict.save()
        if recode_msg_list:
            models.EventLog.objects.create(asset=host_obj, detail="\n".join(recode_msg_list))
        # print(recode_msg_list)
        # 为什么更新操作要这么麻烦那？
        # 因为我们需要服务器的修改记录，要保存历史
        """
        if not status:
            print(status)   # 获取硬盘信息的状态，是成功还是失败，如果失败，则返回失败信息

        else: # 成功则写入数据库
            disk_data = disk_info['data']
            # disk_info = {'status': True, 'data': {'0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'}, '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'}, '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}}, 'error': None}
            # disk_data = {'0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'}, '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'}, '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}}
            for slot,slot_info in disk_data.items():
                # print(slot,slot_info)
                models.DiskInfo.objects.create(**slot_info,host=host_obj)
            print("写入成功~")
        """