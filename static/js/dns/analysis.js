/**
 * Created by wupeiqi on 15/8/13.
 */
$(function () {
    $('#left_menu_zone').addClass('active');
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
更新资产（退出编辑状态;获取资产中变更的字段；提交数据；显示状态）
*/
function Save(){

    if($('#edit_mode_target').hasClass('btn-warning')){
        $.TableEditMode('#edit_mode_target','#table-body');
    }
    var target_status = '#handle_status';
    //get update data
    var updateData = [];
    // get new data
    var newData = [];

    var error_list = [];
    var error_flag = false;

    $('#table-body').children().each(function(i){
        var $tr = $(this);
        var is_new = $(this).attr('create');
        $tr.removeClass('danger');

        if(is_new){
            var row={};
            $(this).find('input[type="text"],select').each(function(){
                var name = $(this).attr('name');
                var value = $(this).val();
                if(!value){
                    $tr.addClass('danger');
                    error_flag = true;
                }else{
                    row[name] = value;
                }
            });

            newData.push(row);

        }else{
            var flag = false;
            var rows = {};
            var id = $(this).attr('auto-id');
            var num = $(this).attr('num');
            $(this).children('td[edit-enable="true"]').each(function(){
                var editType = $(this).attr('edit-type');
                if(editType == 'input'){
                    var origin = $(this).attr('origin');
                    var newer = $(this).text();
                    var name = $(this).attr('name');
                    if(newer && newer.trim() && origin != newer){
                        rows[name] = newer;
                        flag = true;
                    }
                }else{
                    var origin = $(this).attr('origin');
                    var newer = $(this).attr('new-value');
                    var name = $(this).attr('name');

                    if(newer && newer.trim() && origin != newer){
                        rows[name] = newer;
                        flag = true;
                    }
                }

            });
            if(flag){
                rows["id"] = id;
                rows["num"] = num;
                updateData.push(rows);
            }
        }

    });

    if(error_flag){
        return;
    }else if(newData.length<1 && updateData.length<1){
        return;
    }

    //submit data
    newData = JSON.stringify(newData);
    updateData = JSON.stringify(updateData);
    $.Show('#shade,#loading');
    var nid = $('#zone_file_name').attr('nid');
    $.ajax({
        url:'/dns/analysis_modify/',
        type:'POST',
        traditional:true,
        data:{nid:nid ,create :newData, update:updateData},
        success: function (callback) {

            callback = $.parseJSON(callback);

            if(callback.status){
                //success
                SuccessHandleStatus(target_status, callback.message, callback.data);
                Refresh();
            }else{
                // part error
                ErrorHandleStatus(target_status,callback.message,callback.data);
            }
            $.Hide('#shade,#loading');
        },
        error:function(){
            alert('请求错误.');
            //Refresh();
            $.Hide('#shade,#loading');
        }
    });
}


/*
聚合搜索条件
*/
function AggregationSearchCondition(conditions){
    var ret = {};
    var nid = $('#zone_file_name').attr('nid');
    ret['zone__id'] = [nid];
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

        ret['record__contains'] = valList;
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
        url:'/dns/analysis_list/',
        type:'POST',
        traditional:true,
        data:{'condition':conditions,'page':page},
        success:function(callback){

            callback = $.parseJSON(callback);

            //create global variable
            InitGlobalDict(callback);

            //embed table
            EmbedIntoTable(callback.lists, callback.start, "#table-body");


            //ResetSort()
            $.ResetTableSort('#table-head',"#table-body");

            //pager
            CreatePage(callback.pager,'#pager');

            //bind function and event
            $.BindTableSort('#table-head','#table-body');
            $.BindDoSingleCheck('#table-body');
            $.Hide('#shade,#loading');

        },
        error:function(){
            $.Hide('#shade,#loading');
        }
    })

}


/*
初始化字典到全局变量，以便Select中的选项使用
 */
function InitGlobalDict(callback){
    window.window_relation_type = callback.relation_type_choice.data;
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
        $.each(response.data,function(key,value){
            var tds = [];
            tds.push($.CreateTd({},{},$.CreateInput({'type':'checkbox'},{})));
            tds.push($.CreateTd({},{},startNum + key + 1));

            tds.push($.CreateTd({'edit-enable':'true','edit-type':'input','name':'host_record','origin':value.host_record},{}, value.host_record));
            var type_text = TypeToText(value.relation_type);
            tds.push($.CreateTd({'edit-enable':'true','edit-type':'select','value_key':'0','text_key':1,'name':'relation_type','origin':value.relation_type,'edit-option':'relation_type','options':'window_relation_type'},{}, type_text));

            tds.push($.CreateTd({'edit-enable':'true','edit-type':'input','name':'record','origin':value.record},{}, value.record));

            var tr = $.CreateTr({'auto-id':value.id,'num':startNum + key + 1, 'nid': value.zone_id},{},tds);

            $(body).append(tr);

        })

    }
}


/*
将类型码 0 或1 转换成文字
 */
function TypeToText(value){
    var text = '';
    $.each(window['window_relation_type'], function (k, v) {
        if(v[0] == value){
            text = v[1];
            return
        }
    });
    return text;
}

/*
创建分页信息
*/
function CreatePage(data,target){
    $(target).empty().append(data);
}


/*
更新资产错误，显示错误信息
 */
function ErrorHandleStatus(target,content,detailDict){

    $(target).attr('data-toggle','popover');

    var detailStr = '';
    $.each(detailDict,function(k,v){
        if(v.status){
            var parentStr = "<div class='popover-block'><i class='fa fa-info-circle text-success'></i><span class='row-title'>" + v.data + '</span></div>';
        }else{
            var parentStr = "<div class='popover-block'><i class='fa fa-info-circle text-danger'></i><span class='row-title'>" + v.data + '</span></div>';
        }
        $.each(v.message,function(key,value){
            parentStr = parentStr + "<div class='popover-detail'>"+ value.num +"： "+ value.message +"</div>";
        });
        detailStr = detailStr + parentStr;

    });

    $(target).attr('data-content',detailStr);
    $(target).popover();

    var msg = "<i class='fa fa-info-circle'></i>" + content;
    $(target).empty().removeClass('btn-success').addClass('btn-danger').html(msg);

}

/*
更新资产成功，显示更新信息
 */
function SuccessHandleStatus(target,content,detailDict){

    $(target).attr('data-toggle','popover');

    var detailStr = '';
    $.each(detailDict,function(k,v){
        detailStr = detailStr + "<div class='popover-block'><i class='fa fa-info-circle text-success'></i><span class='row-title'>" + v.data + '</span></div>';
    });

    $(target).attr('data-content',detailStr);
    $(target).popover();

    var msg = "<i class='fa fa-check'></i>" + content;
    $(target).empty().removeClass('btn-danger').addClass('btn-success').html(msg);
    //setTimeout(function(){ $(target).empty().removeClass('btn-success btn-danger'); },5000);

}


/*
删除资产
*/
function DoDelete(){
    var target_status = '#handle_status';
    var table_body = '#table-body';
    var rows = [];

    $(table_body).find('input:checked').each(function(){
        var id = $(this).parent().parent().attr('auto-id');
        var num = $(this).parent().parent().attr('num');
        rows.push({'id':parseInt(id),'num':parseInt(num)});
    });

    rows = JSON.stringify(rows);
    var nid = $('#zone_file_name').attr('nid');
    $.Show('#shade,#loading');
    $.ajax({
        url: '/dns/analysis_del/',
        type: 'POST',
        traditional: true,
        data: {'nid':nid,'rows': rows},
        success:function(callback){
            $.Hide('#shade,#modal_delete');
            callback = $.parseJSON(callback);
            if(callback.status == 1){
                //success
                SuccessHandleStatus(target_status,callback.message,  callback.data);
            }else{
                ErrorHandleStatus(target_status, callback.message, callback.data);
            }
            Refresh();
        },
        error:function(){
            alert('请求错误.');
            $.Hide('#shade,#loading');
        }
    });
}

/*
添加VLAN-取消
*/
function CancelModal(container){
    $("#do_add_form").find('input').val('');
    $('#do_add_modal').modal('hide')
}

/*
添加VLAN-提交
*/
function SubmitModal(formId,statusId){
    var data_dict = {};
    $(formId).find('input[type="text"]').each(function(){
        var name = $(this).attr('name');
        var val =  $(this).val();
        data_dict[name] = val
    });
    ClearLineError(formId,statusId);
    $.ajax({
        url: '/dns/zone_add/',
        type: 'POST',
        traditional: true,
        data: data_dict,
        success:function(callback){
            callback = $.parseJSON(callback);
            if(callback.status){
                CancelModal();

            }else{
                if(callback.summary){
                    SummaryError(callback.summary,statusId);
                }
                if(callback.error){
                    LineError(callback.error,formId);
                }

            }
            Refresh();
        }
    });
}

/*
清除所有行下的错误信息
 */
function ClearLineError(formId,statusId){
    $(statusId).empty();
    $(formId).find('div[class="form-error"]').remove();
}

/*
添加行错误信息
 */
function LineError(errorDict,formId){
    //find all line，add error
    $.each(errorDict,function(key,value){
        var errorStr = '<div class="form-error">'+ value[0]['message'] +'</div>';
        $(formId).find('input[name="'+key+'"]').after(errorStr);
    });
}
/*
添加整体错误信息
 */
function SummaryError(errorStr,statusId){
    $(statusId).text(errorStr);
}

/*
监听是否已经按下control键
*/
window.globalCtrlKeyPress = false;
window.onkeydown = function(event){
    if(event && event.keyCode == 17){
        window.globalCtrlKeyPress = true;
    }
};

/*
按下Control，联动表格中正在编辑的select
 */
function MultiSelect(ths){
    if(window.globalCtrlKeyPress){
        var index = $(ths).parent().index();
        var value = $(ths).val();
        $(ths).parent().parent().nextAll().find("td input[type='checkbox']:checked").each(function(){
            $(this).parent().parent().children().eq(index).children().val(value);
        });
    }
}


function AddRow(body){
    var tds = [];
    tds.push($.CreateTd({},{},$.CreateInput({'type':'checkbox'},{})));
    tds.push($.CreateTd({},{},"新建"));

    tds.push($.CreateTd({'class':'padding-3'},{},$.CreateInput({'name':'host_record', 'type':'text', 'value':'', 'class':'padding-tb-5 form-control '}, {'width':'100%'})));
    tds.push($.CreateTd({'class':'padding-3'},{},$.CreateSelect({'name':'relation_type', 'class':'padding-tb-5 form-control','onchange':'MultiSelect(this)'}, {'width':'100%'}, window['window_relation_type'], ' ', 0,1)));

    var input = $.CreateInput({'name':'record', 'type':'text', 'value':'','class':'padding-tb-5 form-control '}, {'width':'80%','display':'inline-block'});
    var cancle = $.CreateA({'href':'javascript:void(0);','onclick':"RemoveRow(this)",'class':'remove-row'},{},'<i class="fa fa-times-circle"></i>');

    tds.push($.CreateTds({'class':'padding-3'},{},[input, cancle],''));

    var tr = $.CreateTr({'auto-id':0,'num':0, 'create':true},{},tds);

    $(body).prepend(tr);
}


function RemoveRow(ths){
    $(ths).parent().parent().remove();
}