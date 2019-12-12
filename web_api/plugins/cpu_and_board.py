# -*- coding: utf-8 -*- 
# @Time    : 2019/12/9 17:28 
# @Author  : p0st
# @Site    :  
# @File    : cpu_and_board.py
# @Software: PyCharm
from web_cmdb import models
from .base import BasePlugins
class CPUAndBoard(BasePlugins):
    # {'status': True, 'data': {'cpu_count': 1, 'cpu_physical_count': 1, 'cpu_model': ' Intel(R) Xeon(R) CPU E5-26xx v4'}
    def process(self, info, host_obj):
        if not info['status']:
            print('采集资产错误',info['error'])
            return
        cpu_info = info['data']
        recode_msg_list = []
        for key,new_value in cpu_info.items():
            old_value = getattr(host_obj.server,key)
            verbose_name = models.Server._meta.get_field(key).verbose_name
            if new_value != old_value:
                setattr(host_obj.server,key,new_value)
                if self.key == 'cpu':
                    msg = "【更新CPU】%s 由%s变更为%s"%(verbose_name,old_value,new_value)
                else:
                    msg = "【更新主板】%s 由%s变更为%s" % (verbose_name, old_value, new_value)
                recode_msg_list.append(msg)
        if recode_msg_list:
            models.EventLog.objects.create(asset=host_obj,detail="\n".join(recode_msg_list),user_id=1)
            host_obj.server.save()



