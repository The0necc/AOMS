# -*- coding: utf-8 -*- 
# @Time    : 2019/12/9 17:26 
# @Author  : p0st
# @Site    :  
# @File    : __init__.py
# @Software: PyCharm
import importlib
from django.conf import settings
def process_info(info,host_obj):
    """
    处理中控汇报资产信息
    :return:
    """
    # for key,path in settings.CMDB_PLUGINS_DICT.items():
    #         module_path,class_name = path.rsplit('.',maxsplit=1)
    #         module = importlib.import_module(module_path)
    #         obj = getattr(module,class_name)()
    #         obj.process(info[key],host_obj)

    # 第二种方法会比上面减少实例化的过程
    for key in info:
        if settings.CMDB_PLUGINS_DICT.get(key):
            module_path, class_name = settings.CMDB_PLUGINS_DICT.get(key).rsplit('.', maxsplit=1)
            module = importlib.import_module(module_path)
            obj = getattr(module, class_name)(key)
            obj.process(info[key], host_obj)

            # obj.process(info, host_obj)
            # info = {'board':
            # {'status': True,
            #       'data': {'manufacturer': 'Bochs', 'model': 'Bochs', 'sn': '4c5b8c7f-7c5f-4bcd-b8a6-5584a718b4dd'},
            #       'error': None
            #    },
            # 'cpu':
            #       {'status': True,
            #       'data': {'cpu_count': 1, 'cpu_physical_count': 1, 'cpu_model': ' Intel(R) Xeon(R) CPU E5-26xx v4'},
            #       'error': None
            #       }
            # }