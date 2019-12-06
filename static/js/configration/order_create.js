/**
 * Created by wupeiqi on 15/8/13.
 */
$(function () {
    $('#left_menu_order').addClass('active');
    Initialize('#table-body',1);
});


/*
刷新页面
*/
function Refresh(){
    //get current page
    var currentPage = GetCurrentPage('#pager');
    Initialize('#table-body',currentPage);
}

/*
获取当前页码（根据分页css）
 */
function GetCurrentPage(pager) {
    var page = $(pager).find("li[class='active']").text();
    return page;
}

/*
搜索提交
*/
function SearchSubmit(){
    Initialize('#table-body',1);
}

/*
*页面跳转
*/
function ChangePage(page){
    Initialize('#table-body',page);
}

/*
聚合搜索条件
*/
function AggregationSearchCondition(conditions){
    var ret = {};
    var $condition = $(conditions).find("input[is-condition='true']");
    var name = $condition.attr('name');
    var value = $condition.val();
    if(!$condition.is('select')){
        name = name + "__contains";
    }
    if(value) {
        var valList = $condition.val().trim().replace('，', ',').split(',');
        if (ret[name]) {
            ret[name] = ret[name].concat(valList);
        } else {
            ret[name] = valList;
        }
    }
    return ret;
}

/*
页面初始化（获取数据，绑定事件）
*/
function Initialize(tBody,page){
    $.Show('#shade,#loading');
    // 获取所有搜索条件

    var conditions = JSON.stringify(AggregationSearchCondition('#search_conditions'));
    var $body = $(tBody);
    var searchConditions = {};
    var page = page;

    $.ajax({
        url:'/asset/get_lists/',
        type:'POST',
        traditional:true,
        data:{'condition':conditions,'page':page},
        success:function(callback){

            callback = $.parseJSON(callback);

            //embed table
            EmbedIntoTable(callback.asset, callback.start, "#table-body");

            //ResetSort()
            $.ResetTableSort('#table-head',"#table-body");

            //pager
            CreatePage(callback.pager,'#pager');

            //bind function and event
            $.BindTableSort('#table-head','#table-body');

            $.Hide('#shade,#loading');

        },
        error:function(){
            $.Hide('#shade,#loading');
        }
    })

}

/*
将后台ajax数据嵌套到table中
*/
function EmbedIntoTable(response,startNum,body){
    if(!response.status){
        alert(response.message);
    }else{
        //清除table中原内容
        $(body).empty();
        var checked_host = FetchCheckServer();

        $.each(response.data,function(key,value){
            var ii = checked_host.indexOf(value.id);
            var tds = [];
            if(value.server__init_status){
                if(checked_host.indexOf(value.id) != -1){
                    var check_box = $.CreateInput({'type':'checkbox', 'checked':'checked', 'onclick': 'ChoiceServer(this,'+ value.id +',"'+ value.server__manage_ip +'");'},{});
                }else{
                    var check_box = $.CreateInput({'type':'checkbox', 'onclick': 'ChoiceServer(this,'+ value.id +',"'+ value.server__manage_ip +'");'},{});
                }

            }else{
                var check_box = $.CreateInput({'type':'checkbox', 'disabled': 'true'},{});
            }
            tds.push($.CreateTd({},{},check_box));
            tds.push($.CreateTd({},{},startNum + key + 1));
            tds.push($.CreateTd({'edit-enable':'false','edit-type':'input','name':'manage_ip','origin':value.server__manage_ip},{}, value.server__manage_ip));
            tds.push($.CreateTd({'edit-enable':'false','edit-type':'input','name':'init_status','origin':value.server__init_status},{}, value.server__init_status));

            var tr = $.CreateTr({'auto-id':value.id,'num':startNum + key + 1},{},tds);

            $(body).append(tr);

        })

    }
}


/*
创建分页信息
*/
function CreatePage(data,target){
    $(target).empty().append(data);
}


function ChoiceServer(ths, nid, idrac){
    // 获取当前name
    // 将name和id添加头部

    if($(ths).prop('checked')){
        // add
        var str = '<div class="server-item" nid="'+ nid +'" onclick="DelChoiceServer(this);" > <span class="cont">'+ idrac +'</span> <i class="fa fa-times"></i> </div>';
        $('#choice_server_region').append(str);

    }else{
        // remove
        $('#choice_server_region').find('div[nid="'+ nid +'"]').remove();
    }
}

function DelChoiceServer(ths){
    var nid = $(ths).attr('nid');
    $(ths).remove();
    $('#table-body').find('tr[auto-id="'+nid+'"]').find(':checkbox').prop('checked', false);
}


function FetchCheckServer(){
    var checked_host = [];
    $('#choice_server_region').children().each(function(){
        var nid = $(this).attr('nid');
        checked_host.push(parseInt(nid));
    });

    return checked_host;
}


/*
提交步骤一
 */
function FirstNext(){
    $.Show('#shade,#loading');
    var checkedHosts = FetchCheckServer();
    $('#handle_status').empty();
    if(checkedHosts.length<1){
        $.Hide('#shade,#loading');
        $('#handle_status').html('<span>请选择服务器</span>');
        return;
    }else{
        FetchInstallInfo(checkedHosts);
    }
    // show step 2

    // 获取选中的服务器id
    // ajax 获取id的Mac
}

function FetchInstallInfo(checkedHosts){
    var nid_list = JSON.stringify(checkedHosts);
    $.ajax({
        url: '/configration/fetch_install_info/',
        type: 'GET',
        data: {nid_list: nid_list},
        traditional:true,
        success: function(callback){
            callback = $.parseJSON(callback);
            $('#pre_install_region').empty().append(callback.data);
            $.Hide('#shade,#loading');

            $('#first_step').addClass('hide');
            $('#second_step').removeClass('hide');
        },
        error: function(){
            $.Hide('#shade,#loading');
            $('#handle_status').html('<span>请求异常，请联系管理员！</span>');
        }
    });
}

function ChangeVlanList(ths){

    var vlan_id = $(ths).val();
    if(vlan_id == 0){
        ClearIpList(ths);
        return;
    }
    $.ajax({
        url: '/configration/fetch_ip_list/',
        type: 'GET',
        data: {vlan_id: vlan_id},
        success: function(callback){
            callback = $.parseJSON(callback);
            if(callback.status){
                UpdateIpList(ths, callback.data);
            }
        },
        error: function(){
            alert('请求错误');
        }
    })
}


function ClearIpList(vlan_ths){
    var $ipaddr = $(vlan_ths).parent().parent().next().find('select[name="ipaddr_id"]');
    $ipaddr.find('option[value!="0"]').remove();
}

function UpdateIpList(vlan_ths, data_list){
    var $ipaddr = $(vlan_ths).parent().parent().next().find('select[name="ipaddr_id"]');

    $.each(data_list, function(key, value){

        var voption = $.CreateOption({'value': value.id,'getway':value.getway, 'mask':value.mask},{}, value.ipaddr);
        $ipaddr.append(voption);

    });
}

/*
    步骤二：返回上步
 */
function SecondPre(){

    $('#first_step').removeClass('hide');
    $('#second_step').addClass('hide');
    // remove install list
    $('#pre_install_region').empty();
}

/*
    步骤二：提交
 */
function SecondNext(){
    // submit: create record,create ks,reboot server,update ip and server in installing
    // get input,select,radio
    $.Show('#shade,#loading');
    var pre_install_info = GatherInstallInfo();
    $('.form-error').remove();
    $.ajax({
        url: "/configration/submit_install/",
        type: "POST",
        data: pre_install_info,
        traditional:true,
        success: function(callback){
            callback = $.parseJSON(callback);
            $.Hide('#shade,#loading');

            if(callback.status == 1){
                window.location.href = '/configration/order_detail/' + callback.order_id + '/';
            }else if(callback.status == 2){
                try{
                    var error_detail = callback.message;
                    console.log(error_detail);
                    $.each(error_detail, function(key,value){
                        if(key == 'order_name'){
                            $('#create_order_name').after('<div class="form-error no-margin">'+ value +'</div>');
                        }
                        if(key == 'detail'){
                            $.each(value, function(index,detail){
                                var $row = $('#pre_install_region').children().eq(index);
                                $.each(detail, function(name,msg) {
                                    $row.find('[name="' + name + '"]').after('<div class="form-error">'+ msg +'</div>');
                                })
                            })
                        }
                    });
                }catch(e){

                }

            }else if(callback.status == 3){
                var msg = '<span>'+ callback.message +'</span>';
                $('#handle_status').html(msg);
            }
        },
        error: function(){
            $.Hide('#shade,#loading');
        }
    });
}

function GatherInstallInfo(){
    var ret = {};

    // order_name
    var order_name = $('#create_order_name').val();

    var pre_install_list = [];
    // order_install_list
    $('#pre_install_region').children().each(function(index){
        var $row = $(this);
        var row_dict = {'index':index };
        $row.find('input[type="text"],select,:radio:checked').each(function(){
            var name = $(this).attr('name');
            var val = $(this).val();
            var is_fetch_content =  $(this).attr('fetch-content');
            if(name){
                row_dict[name] = val;
            }
            if(is_fetch_content){
                var content_key =  $(this).attr('content-key');
                var text = $(this).find('option[value="'+ val +'"]').text();
                row_dict[content_key] = text;
                var getway = $(this).find('option[value="'+ val +'"]').attr('getway');
                var mask = $(this).find('option[value="'+ val +'"]').attr('mask');
                if(getway && mask){
                    row_dict["getway"] = getway;
                    row_dict["mask"] = mask;
                }
            }
        });
        pre_install_list.push(row_dict);
    });

    ret['order_name'] = order_name;
    ret['pre_install_list'] =  JSON.stringify(pre_install_list);

    return ret;
}