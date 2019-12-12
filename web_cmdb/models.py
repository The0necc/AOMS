from django.db import models

# Create your models here.
"""全部资产共有数据项"""
class Asset(models.Model):
    """所有资产的共有数据"""
    asset_type_choise = (
        ('server','服务器'),
        ('networkdevice','网络设备'),
        ('storagedevice','存储设备'),
        ('securitydevice','安全设备'),
        ('software','软件资产'),
        ('other','其他'),
    )
    asset_status = (
        (0,'在线'),
        (1,'下线'),
        (2,'未知'),
        (3,'故障'),
        (4,'备用'),
    )
    asset_type = models.CharField(choices=asset_type_choise,max_length=64,default='server',verbose_name='资产类型')
    name = models.CharField(verbose_name='资产名称',unique=True,max_length=64)   # 这是资产的名字，是叫什么，比如服务器a，路由器b，也可以理解为hostname
    asset_nu = models.CharField(verbose_name="资产编号",unique=True,max_length=64) # 企业都会有资产编号，进行集中管理，与服务器的sn号码不同
    department = models.ForeignKey(to='Department',null=True,blank=True,verbose_name="所属部门",on_delete=models.SET_NULL) # 不随着业务线的删除而删除
    status = models.SmallIntegerField(choices=asset_status,default=0,verbose_name="设备状态")
    manufacturer = models.ForeignKey(to='Manufacturer',verbose_name="制造商",blank=True,null=True,on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(unique=True,null=True, blank=True, verbose_name='管理IP') # 有的设备可能有ip，有的可能没有ip，先不写
    tags = models.ManyToManyField(to="Tag",blank=True,null=True,verbose_name="标签")
    admin = models.ForeignKey(to="User",null=True, blank=True, verbose_name='资产管理员', related_name='admin',on_delete=models.SET_NULL) # 使用键查询的时候不用表名小写_set()，而是通过related_name
    idc = models.ForeignKey(to='IDC',null=True,blank=True,verbose_name='所在机房',on_delete=models.SET_NULL)
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='合同', on_delete=models.SET_NULL)
    purchase_day = models.DateField(null=True, blank=True, verbose_name="购买日期")
    expire_day = models.DateField(null=True, blank=True, verbose_name="过保日期")
    price = models.FloatField(null=True, blank=True, verbose_name="价格")
    approved_by = models.ForeignKey(to="User", null=True, blank=True, verbose_name='批准人', related_name='approved_by',on_delete=models.SET_NULL)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    c_status = models.BooleanField(default=True, verbose_name="今日是否采集")


    def __str__(self):
        return '<%s>  %s %s' % (self.get_asset_type_display(), self.name,self.get_status_display())

    class Meta:
        verbose_name = '资产总表'
        ordering = ['-c_time']   # 查询时候的排序方法
        app_label = "web_cmdb"

"""部门"""
class Department(models.Model):

    name = models.CharField(verbose_name='部门',max_length=64,unique=True)
    memo = models.CharField(verbose_name="备注",max_length=64,blank=True,null=True)
    # app_name = models.CharField(verbose_name='应用名',  max_length=32, db_column='app_name2')
    # 指的是在数据库中该字段是怎么显示，django中默认是app名字+类名+字段名

    def __str__(self):
        return self.name

    class Meta:
        # db_table = 'info'  # 在数据库中显示info表的名字，而不是web_cmdb_info
        verbose_name = "部门"
        # verbose_name_plural = "部门" # 复数显示的显示方式，中文一般不做区分
        app_label = "web_cmdb"

"""设备厂商"""
class Manufacturer(models.Model):

    name = models.CharField(verbose_name="设备厂商",max_length=108,unique=True)
    telephone = models.CharField(verbose_name='支持电话',max_length=20,blank=True,null=True)
    memo = models.CharField(verbose_name="备注",max_length=256,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        app_label = "web_cmdb"

"""标签"""
class Tag(models.Model):
    name = models.CharField(verbose_name="标签名",max_length=32,unique=True)
    c_day = models.DateField(verbose_name="创建日期",auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        app_label = "web_cmdb"

"""机房"""
class IDC(models.Model):
    name = models.CharField(verbose_name="机房名称",blank=True,null=True,max_length=64,unique=True)
    c_day = models.DateField(verbose_name="使用开始日期", auto_now_add=True)
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        app_label = "web_cmdb"

"""合同"""
class Contract(models.Model):

    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    memo = models.TextField('备注', blank=True, null=True)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详细', blank=True, null=True)
    start_day = models.DateField('开始日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    license_num = models.IntegerField('license数量', blank=True, null=True)
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        app_label = "web_cmdb"

# # """CPU"""
# class CPU(models.Model):
#
#     asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
#     cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
#     cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1)
#     cpu_core_count = models.PositiveSmallIntegerField('CPU核数', default=1)
#
#     def __str__(self):
#         return self.asset.name + ":   " + self.cpu_model
#
#     class Meta:
#         verbose_name = 'CPU'
#         app_label = "web_cmdb"

"""内存"""
class RAM(models.Model):

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    # sn = models.CharField('SN号', max_length=128, blank=True, null=True)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    # manufacturer = models.CharField('内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField('插槽', max_length=64)
    capacity = models.CharField('内存大小', blank=True, null=True,max_length=32)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        unique_together = ('asset', 'slot')   # 只能有一台机器对应其中的一个槽位，不能出现重复的数据
        app_label = "web_cmdb"

"""硬盘"""
class Disk(models.Model):

    # disk_interface_type_choice = (
    #     ('SATA', 'SATA'),
    #     ('SAS', 'SAS'),
    #     ('SCSI', 'SCSI'),
    #     ('SSD', 'SSD'),
    #     ('unknown', 'unknown'),
    # )

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    # disksn = models.CharField('硬盘SN号', max_length=128)   # 虚拟机不知道为什么获取不到
    slot = models.CharField('所在插槽位', max_length=64, blank=True, null=True)
    model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
    # manufacturer = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
    capacity = models.CharField('磁盘容量(GB)', max_length=64 ,blank=True, null=True)
    interface_type = models.CharField('接口类型', max_length=32, default='unknown')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '硬盘'
        # unique_together = ('asset', 'sn')  # 应该是asset和sn之间时联合唯一，因为在虚拟机里面可能会有相同的硬盘sn
        app_label = "web_cmdb"

"""网卡"""
class NIC(models.Model):

    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)  # 注意要用外键
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    # model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    net_mask = models.CharField('掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s:   %s' % (self.asset.name,  self.mac)

    class Meta:
        verbose_name = '网卡'
        unique_together = ('asset',  'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。
        app_label = "web_cmdb"

"""服务器设备"""
class Server(models.Model):

    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    asset = models.OneToOneField(to='Asset', on_delete=models.CASCADE,blank=True, null=True)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    # hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True, verbose_name="宿主机", on_delete=models.CASCADE)  # 虚拟机专用字段
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')
    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)
    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True,default=None)
    cpu_count = models.PositiveSmallIntegerField('物理CPU个数', default=1,blank=True, null=True)
    cpu_physical_count = models.PositiveSmallIntegerField('CPU核数', default=1,blank=True, null=True)
    board_sn = models.CharField(verbose_name='主板SN号', max_length=64, null=True, blank=True,default=None)
    board_model = models.CharField(verbose_name='主板型号', max_length=64, null=True, blank=True,default=None)
    board_manufacturer = models.CharField(verbose_name='主板厂商', max_length=64, null=True, blank=True,default=None)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.asset_nu)

    class Meta:
        verbose_name = '服务器'
        app_label = "web_cmdb"

"""安全设备,一般需要手工录入"""
class SecurityDevice(models.Model):

    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField(to='Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="安全设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        app_label = "web_cmdb"

"""存储设备,一般需要手工录入"""
class StorageDevice(models.Model):

    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机'),
    )

    asset = models.OneToOneField(to='Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="存储设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='存储设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        app_label = "web_cmdb"

"""网络设备,一般需要手工录入"""
class NetworkDevice(models.Model):

    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")

    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="VLanIP")
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="内网IP")

    model = models.CharField(max_length=128, default='未知型号',  verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="详细配置")

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.asset_nu)

    class Meta:
        verbose_name = '网络设备'
        app_label = "web_cmdb"

"""只保存付费购买的软件,一般需要手工录入"""
class Software(models.Model):

    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="软件类型")
    license_num = models.IntegerField(default=1, verbose_name="授权数量")
    version = models.CharField(max_length=64, unique=True, help_text='例如: RedHat release 7 (Final)',
                               verbose_name='软件/系统版本')
    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        app_label = "web_cmdb"

"""用户表"""
class User(models.Model):
    username = models.CharField(verbose_name="用户名",unique=True,max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)
    department = models.ForeignKey(to="Department",verbose_name="所属部门")
    c_day = models.DateField(verbose_name="创建日期", auto_now_add=True)

    class Meta:
        verbose_name = "用户表"
        app_label = "web_cmdb"

    def __str__(self):
        return self.username

"""日志表"""
class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """
    # name = models.CharField('事件名称', max_length=128)
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=2)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.new_asset

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

"""新资产待审批区"""
class NewAssetApprovalZone(models.Model):

    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField('CPU物理数量', blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField('CPU核心数量', blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_type = models.CharField('系统类型', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本号', max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']