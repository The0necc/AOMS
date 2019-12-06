/**
 * Created by wupeiqi on 15/8/13.
 */
$(function () {
    $('#left_menu_template').addClass('active');
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
    //get data
    var updateData = [];
    $('#table-body').children().each(function(){
        var rows = {};
        var id = $(this).attr('auto-id');
        var num = $(this).attr('num');
        var flag = false;
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
    });
    if(updateData.length<1){
        return;
    }
    //submit data
    updateData = JSON.stringify(updateData);


    $.ajax({
        url:'/dns/template_modify/',
        type:'POST',
        traditional:true,
        data:{'data':updateData},
        success: function (callback) {
            callback = $.parseJSON(callback);
            if(callback.status == 1){
                //success
                AllSuccessStatus(target_status,callback.data);
            }else{
                PartSuccessStatus(target_status,callback.data,callback.message);
            }
            Refresh();
        },
        error:function(){
            alert('请求错误.');
            Refresh();
        }

    });


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

    // 获取所有搜索条件
    var conditions = JSON.stringify(AggregationSearchCondition('#search_conditions'));
    var $body = $(tBody);
    var searchConditions = {};
    var page = page;

    $.Show('#shade,#loading');
    $.ajax({
        url:'/dns/template_list/',
        type:'POST',
        traditional:true,
        data:{'condition':conditions,'page':page},
        success:function(callback){
            try{
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

            }catch(e){
                alert(e);
            }finally{
                $.Hide('#shade,#loading');
            }
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
    window.window_template_type = callback.type_choice.data;
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

            tds.push($.CreateTd({'edit-enable':'true','edit-type':'input','name':'caption','origin':value.caption},{}, value.caption));

            var d = $.CreateA({'href':'/dns/template_detail/'+value.id +'/','target':'_blank' },{},'详细');
            tds.push($.CreateTds({},{},[d],'<br/>'));

            var tr = $.CreateTr({'auto-id':value.id,'num':startNum + key + 1},{},tds);
            $(body).append(tr);
        })

    }
}


/*
将类型码 0 或1 转换成文字
 */
function TypeToText(value){
    var text = '';
    $.each(window['window_template_type'], function (k, v) {
        if(v[0] == value){
            text = v[1];
            return
        }
    });
    return text
}


/*
创建分页信息
*/
function CreatePage(data,target){
    $(target).empty().append(data);
}

/*
删除
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
    $.ajax({
        url: '/dns/template_del/',
        type: 'POST',
        traditional: true,
        data: {'rows': rows},
        success:function(callback){
            $.Hide('#shade,#modal_delete');
            callback = $.parseJSON(callback);
            if(callback.status == 1){
                //success
                AllSuccessStatus(target_status,callback.data);
            }else{
                PartSuccessStatus(target_status,callback.data,callback.message);
            }
            Refresh();
        }
    });
}


/*
全部成功，显示更新信息
 */
function AllSuccessStatus(target,content){
    $(target).popover('destroy');
    var msg = "<i class='fa fa-check'></i>" + content;
    $(target).empty().removeClass('btn-danger').addClass('btn-success').html(msg);
    setTimeout(function(){ $(target).empty().removeClass('btn-success btn-danger'); },5000);
}


/*
部分成功，显示错误信息
 */
function PartSuccessStatus(target,content,errorList){
    $(target).attr('data-toggle','popover');

    var errorStr = '';
    $.each(errorList,function(k,v){
        errorStr = errorStr + v.num + '. '+ v.message + '</br>';
    });

    $(target).attr('data-content',errorStr);
    $(target).popover();

    var msg = "<i class='fa fa-info-circle'></i>" + content;
    $(target).empty().removeClass('btn-success').addClass('btn-danger').html(msg);

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
