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
        url:'/configration/order_list/',
        type:'POST',
        traditional:true,
        data:{'condition':conditions,'page':page},
        success:function(callback){

            callback = $.parseJSON(callback);

                       //create global variable
            //InitGlobalDict(callback);

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
            tds.push($.CreateTd({'edit-enable':'false','edit-type':'input','name':'name','origin':value.name},{}, value.name));

            tds.push($.CreateTd({'edit-enable':'false','edit-type':'input','name':'summary','origin':value.summary},{}, value.summary));

            var d = $.CreateA({'href':'/configration/order_detail/'+value.id +'/','target':'_blank' },{},'详细');
            tds.push($.CreateTds({},{},[d],'<br/>'));

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


