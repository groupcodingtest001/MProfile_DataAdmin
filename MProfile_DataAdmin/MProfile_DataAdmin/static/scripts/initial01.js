function dataload01() {
    var result
    $.ajax({
        type: "GET",
        url: '/ready',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        async: false,
        success: function (result1) {
            result=result1
        }
    }).fail(function (msg) {
        alert(msg.responseText);
    });
    return result
}

function refresh(ds) {
    $('#table_list_1').empty();
    $('#pager_list_l').empty();
    $('#pager_list_t').empty();
    $('#ttcnt01_val').empty();
    $.jgrid.defaults.styleUI = "Bootstrap";
    $("#table_list_1").jqGrid({
        data: ds,
        datatype: 'local',
        height: 'auto',
        autowidth: true,
        shrinkToFit: true,
        scrollOffset: 0,
        rowNum: 8,
        colNames: ["Segment ID", "Segment Name", "Advertiser", "Size", "Create Time", "Status", "[m]insights", "T-DMP", "UP", "TD", "UD", "Action"],
        colModel: [
            { name: "segmentid", index: "segmentid", width: 110, align: "center" },
            { name: "segmentname", index: "segmentname", width: 290, align: "center" },
            { name: "advertiser", index: "advertiser", width: 130, align: "center" },
            { name: "size", index: "size", width: 110, align: "center" },
            { name: "createtime", index: "createtime", width: 200, align: "center" },
            { name: "status", index: "status", width: 90, align: "center" },
            { name: "minsights", index: "minsights", width: 120, align: "center" },
            { name: "tdmp", index: "tdmp", width: 70, align: "center" },
            { name: "up", index: "up", width: 60, align: "center" },
            { name: "td", index: "td", width: 60, align: "center" },
            { name: "ud", index: "ud", width: 60, align: "center" },
            {
                name: "action", index: "action", width: 150, align: "center",
                formatter: function (cellvalue, options, rowObject) { return "<a name='upl' href='#'><img src='/static/img/upload.png' width='25' /></a><span>&nbsp; &nbsp;</span><a name='dwl' href='#'><img src='/static/img/Excel.png' width='25' /></a>"; }
            }
        ],
        pager: "#pager_list_1",
        viewrecords: true,
        hidegrid: true,
        rowattr: function (rd) {
            return { "data-id": rd.segmentid };
        },
        gridComplete: function () {
            $("#table_list_1").closest(".ui-jqgrid-bdiv").css({ "overflow-x": "hidden" });
            $("#table_list_1").closest(".ui-jqgrid-bdiv").css({ "overflow-y": "hidden" });
            $("#pager_list_1").hide();
        }
    });

    var rowNum = $("#table_list_1").jqGrid('getGridParam', 'rowNum');
    var totalNum = $("#table_list_1").jqGrid('getGridParam', 'records');
    
    if (totalNum > 0) {
        $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
        $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
        if (Math.ceil(totalNum / rowNum) >= 5) {
            var pagecnts = 5;
        } else {
            var pagecnts = Math.ceil(totalNum / rowNum);
        }
        for (var i = 0; i < pagecnts; i++) {
            if (i == 0) {
                $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + (i + 1) + "</a></li>");
            }
            else {
                $('ul#pager_list_t').append("<li><a href='#'>" + (i + 1) + "</a></li>");
            }
        }
        $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
        $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
    }
    else {
        $('ul#pager_list_t').append("<li><a href='#'>&laquo;</a></li>");
        $('ul#pager_list_t').append("<li><a href='#'>&lsaquo;</a></li>");
        $('ul#pager_list_t').append("<li class='active'><a href='#'>1</a></li>");
        $('ul#pager_list_t').append("<li><a href='#'>&rsaquo;</a></li>");
        $('ul#pager_list_t').append("<li><a href='#'>&raquo;</a></li>");
    }
    $('#ttcnt01_val').append("共" + totalNum + "条记录");
}



$(document).ready(function () {
    var ds = dataload01();
    refresh(ds);
});

$(function () {
    
    $('#divdate1').datetimepicker(
        {
            startView: 2,
            minView: "month",
            format: "yyyy-mm-dd",
            autoclose: true,
            todayBtn: true,
            startDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 365),
            endDate: new Date(new Date() + 1000 * 60 * 60 * 24 * 30)
        }
    );
    
});


$('ul#pager_list_t').on("click", "li", function () {
    var rowNum   = $("#table_list_1").jqGrid('getGridParam', 'rowNum');
    var totalNum = $("#table_list_1").jqGrid('getGridParam', 'records');
    var ttpages = Math.ceil(totalNum / rowNum);
    var prenode = $(this).siblings(".active")
    var premaxpage = parseInt(prenode.text());    
    if (parseInt($(this).text()) > 0) {
        $('ul#pager_list_t li').removeClass("active");
        $(this).addClass("active");
        var pageclick = parseInt($(this).text());
        $("#table_list_1").trigger("reloadGrid", [{ page: pageclick }]);
    }
    else if (this.id == "nxt") {        
        if (premaxpage != ttpages) {
            $('ul#pager_list_t li').removeClass("active");
            if (premaxpage % 5 != 0) {
                prenode.next().addClass("active");
                var pageclick = parseInt(prenode.next().text());
                $("#table_list_1").trigger("reloadGrid", [{ page: pageclick }]);
            }
            else {
                if ((premaxpage / 5) + 1 == Math.ceil(ttpages / 5)) {
                    $('ul#pager_list_t').empty("");
                    $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
                    for (var i = premaxpage + 1; i <= ttpages; i++) {
                        if (i == premaxpage + 1) {
                            $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + i + "</a></li>");
                        }
                        else {
                            $('ul#pager_list_t').append("<li><a href='#'>" + i + "</a></li>");
                        }
                    }
                    $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
                }
                else {
                    $('ul#pager_list_t').empty("");
                    $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
                    for (var i = premaxpage+1; i <= premaxpage + 5; i++) {
                        if (i == premaxpage+1) {
                            $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + i + "</a></li>");
                        }
                        else {
                            $('ul#pager_list_t').append("<li><a href='#'>" + i  + "</a></li>");
                        }
                    }
                    $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
                    
                }
                $("#table_list_1").trigger("reloadGrid", [{ page: premaxpage + 1 }]);
            }
          }
        
    }
    else if (this.id == "pvs") {
        if (premaxpage != 1) {
            $('ul#pager_list_t li').removeClass("active");
            if (premaxpage % 5 != 1) {
                prenode.prev().addClass("active");
                var pageclick = parseInt(prenode.prev().text());
                $("#table_list_1").trigger("reloadGrid", [{ page: pageclick }]);
            }
            else {
                $('ul#pager_list_t').empty("");
                $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
                $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
                for (var i = premaxpage - 5; i <= premaxpage - 1; i++) {
                    if (i == premaxpage - 1) {
                        $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + i + "</a></li>");
                    }
                    else {
                        $('ul#pager_list_t').append("<li><a href='#'>" + i + "</a></li>");
                    }
                }
                $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
                $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");                
                $("#table_list_1").trigger("reloadGrid", [{ page: premaxpage - 1 }]);
            }
        }
    }
    else if (this.id == "lst") {
        if (premaxpage != ttpages) {
            $('ul#pager_list_t').empty("");
            $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
            $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
            for (var i = 5* (Math.ceil(ttpages/5)-1)+1; i <= ttpages; i++) {
                if (i == ttpages) {
                    $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + i + "</a></li>");
                }
                else {
                    $('ul#pager_list_t').append("<li><a href='#'>" + i + "</a></li>");
                }
            }
            $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
            $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
            $("#table_list_1").trigger("reloadGrid", [{ page: ttpages }]);

        }

    }
    else if (this.id == "fst") {
        if (premaxpage != 1) {
            $('ul#pager_list_t li').removeClass("active");
            $('ul#pager_list_t').empty("");
            $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
            $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
            if (ttpages >= 5) {
                var pagecnts = 5;
            } else {
                var pagecnts = ttpages;
            }
            for (var i = 0; i < pagecnts; i++) {
                if (i == 0) {
                    $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + (i + 1) + "</a></li>");
                }
                else {
                    $('ul#pager_list_t').append("<li><a href='#'>" + (i + 1) + "</a></li>");
                }
            }
            $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
            $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
            $("#table_list_1").trigger("reloadGrid", [{ page: 1 }]);
        }
    }
});

$("#find_btn").click(function () {
    var sid = $("input#id").val()
    var adv = $("input#adv").val()
    var idate = $("input#idate").val()
    var stts = $("#stts").val()
    if (!stts && typeof (stts) != "undefined" && stts != 0) {
        stts = "";
    }    
    $.ajax({
            type: "GET",
            url: '/filter01?sid=' + sid + '&adv=' + adv +'&idate='+ idate +'&stts='+stts,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            async: true,
            success: function (result1) {
                $('#table_list_1').jqGrid('clearGridData');
                $('#table_list_1').jqGrid('setGridParam', { data: result1 });
                $('#table_list_1').trigger('reloadGrid');

                var rowNum = $("#table_list_1").jqGrid('getGridParam', 'rowNum');
                var totalNum = $("#table_list_1").jqGrid('getGridParam', 'records');

                $('ul#pager_list_t').empty();
                $('#ttcnt01_val').empty();
                $('#ttcnt01_val').append("共" + totalNum + "条记录");
                if (totalNum > 0) {
                    $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
                    if (Math.ceil(totalNum / rowNum) >= 5) {
                        var pagecnts = 5;
                    } else {
                        var pagecnts = Math.ceil(totalNum / rowNum);
                    }
                    for (var i = 0; i < pagecnts; i++) {
                        if (i == 0) {
                            $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + (i + 1) + "</a></li>");
                        }
                        else {
                            $('ul#pager_list_t').append("<li><a href='#'>" + (i + 1) + "</a></li>");
                        }
                    }
                    $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
                    $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
                }
                else {
                    $('ul#pager_list_t').append("<li><a href='#'>&laquo;</a></li>");
                    $('ul#pager_list_t').append("<li><a href='#'>&lsaquo;</a></li>");
                    $('ul#pager_list_t').append("<li class='active'><a href='#'>1</a></li>");
                    $('ul#pager_list_t').append("<li><a href='#'>&rsaquo;</a></li>");
                    $('ul#pager_list_t').append("<li><a href='#'>&raquo;</a></li>");
                }
            }
        });
});


/*new*/
function selectFile() {
    if ($("#chsfile01").attr("name") == "chsfile01_1") {
        $("#file").trigger("click");
        var str = "<table id='file_tb01'  class='table' ><thead><tr><th style='width:100px;'>File #</th><th id='fname01'>File Name</th></tr></thead><tbody>";
        $("#file").on("change", function () {
            var obj = document.getElementById("file");
            var length = obj.files.length;
            for (var i = 0; i < length; i++) {
                var temp = obj.files[i].name;
                var temp_size = obj.files[i].size/1024;
                if (temp.substring(temp.lastIndexOf("."), temp.length).toUpperCase() == ".XLS" && temp_size < 10240) {
                    str += "<tr><td style='width:100px;'>" + (i + 1) + "</td><td>" + temp + "</td><tr>";
                }
                else {
                    alert("Unidesk file should be with '.xls' format and less than 10M in size!");
                    //$('div#start1').modal('toggle');
                    return;                    
                }
            }
            str += "</tbody></table>"

            $("#filedisplay01").removeClass("modal_files");
            $("#filedisplay01").empty();            
            $("#filedisplay01").append(str);
            $("#chsfile01").attr("name", "chsfile01_2");
            $("#chsfile01").text("Upload UniDesk File");
        });
    }
    else {
        var idv = $("#modalLabel").attr("name");
        var fdata01 = new FormData()
        fdata01.append('file01', $("#file")[0].files[0]);
        $.ajax({
            type: "POST",
            url: '/up_00?bid=1&idv=' + idv,
            data: fdata01,
            contentType: false,
            processData: false,
            success: function (msg) {
                //alert(JSON.stringify(msg));
                $("#chsfile01").hide();
                $("#fname01").empty();
                $("#fname01").append("File Name Uploaded");
                if ($("#chsfile02").attr("name") == "chsfile02_2") {
                    $("#dsubm01").show();
                }
            }
        });
    }
}

function selectFile02() {
    if ($("#chsfile02").attr("name") == "chsfile02_1") {        
        $("#file02").trigger("click");
        var str = "<table id='file_tb02'  class='table' ><thead><tr><th style='width:100px;'>File #</th><th id='fname02'>File Name</th></tr></thead><tbody>";
        $("#file02").on("change", function () {
            var obj = document.getElementById("file02");
            var length = obj.files.length;
            for (var i = 0; i < length; i++) {
                var temp = obj.files[i].name;
                var temp_size = obj.files[i].size / 1024;
                if (temp.substring(temp.lastIndexOf("."), temp.length).toUpperCase() == ".HTML"&& temp_size < 10240) {
                    str += "<tr><td style='width:100px;'>" + (i + 1) + "</td><td>" + temp + "</td><tr>";
                }
                else {
                    alert("Tencent DMP file should be with '.html' format and less than 10M in size!");
                    //$('div#start1').modal('toggle');
                    return;
                }
            }
            str += "</tbody></table>"

            $("#filedisplay02").removeClass("modal_files");
            $("#filedisplay02").empty();
            $("#filedisplay02").append(str);
            $("#chsfile02").attr("name", "chsfile02_2");
            $("#chsfile02").text("Upload Tencent Files");
        });
    }
    else {
        var idv = $("#modalLabel").attr("name");
        var fdata02 = new FormData()
        var files = $("#file02").get(0).files;
        for (var i = 0; i < files.length; i++) {
            fdata02.append("file02", files[i]);
        }

        $.ajax({
            type: "POST",
            url: '/up_00?bid=2&idv=' + idv,
            data: fdata02,
            contentType: false,
            processData: false,
            success: function (msg) {
                //alert(JSON.stringify(msg));
                $("#chsfile02").hide();
                $("#fname02").empty();
                $("#fname02").append("File Name Uploaded");
                if ($("#chsfile01").attr("name") == "chsfile01_2") {
                    $("#dsubm01").show();
                }
            }
        });
    }
}



$("table#table_list_1").on("click", "a[name='upl']", function () {    
    var idv = $(this).parent().parent().find("td").html()
    var sechtml1_1 = "Please Select Unidesk File";   
    var sechtml1_2 = "<input type='file' id='file' style='filter:alpha(opacity=0);opacity:0;width: 0;height: 0;' /><button id='chsfile01' name='chsfile01_1' class='btn btn-primary' onclick='selectFile();'>Select</button>";
    var sechtml2_1 = "Please Select Tencent Files";
    var sechtml2_2 = "<input type='file' id='file02' multiple='multiple' style='filter:alpha(opacity=0);opacity:0;width: 0;height: 0;' /><button id='chsfile02' name='chsfile02_1' class='btn btn-primary' onclick='selectFile02();'>Select</button>";
    var sechtml3_1 = "<div id='dsubm01' class='col-lg-offset-2 col-lg-2' style='display:none;'><button id='submit01' class='btn btn-primary'>Submit</button></div><div><button id='cancel1' type='button' class='btn btn-default' onclick='cancel1()'>Cancel</button></div>";
    //before initialization
    $("#filedisplay01").empty();
    $("#filedisplay01").removeClass('modal_files');
    $("#filedbtn01").empty();
    $("#filedisplay02").empty();
    $("#filedisplay02").removeClass('modal_files');
    $("#filedbtn02").empty();
    $("#footer01").empty();
    //elements loading
    $("#filedisplay01").append(sechtml1_1);
    $("#filedisplay01").addClass('modal_files');
    $("#filedbtn01").append(sechtml1_2);
    $("#filedisplay02").append(sechtml2_1);
    $("#filedisplay02").addClass('modal_files');
    $("#filedbtn02").append(sechtml2_2);
    $("#footer01").append(sechtml3_1);
    /*
    $('div#start1').empty("");
    var boxhtml = "";
    boxhtml = "<div id='question_answer' class='modal-dialog' name='" + idv + "'>";
    boxhtml = boxhtml + "<div class='modal-content'><div class='modal-header' align='center'><h4><b>Loading For Segment ID " + idv + "</b></h4></div><div class='modal-body' style='max-height:300px;overflow-y:auto;'>";
    boxhtml = boxhtml + "<div class='form-horizontal'><div class='form-group'><div class='col-md-6'  ><input type='file' id='file' style='filter:alpha(opacity=0);opacity:0;width: 0;height: 0;'/><button id='chsfile01' name='chsfile01_1' class='btn btn-primary' onclick='selectFile();'>Select UniDesk File</button><div id='notice01' style='display:none;font-family:Georgia, Times, serif;' ><b>UniDesk File Uploaded</b> </div>  </div>   <div id='display_sec' class='col-md-6' ></div>        </div></div>"
    boxhtml = boxhtml + "<div class='form-horizontal'><div class='form-group'><div class='col-md-6'  > <input type='file' id='file02' multiple='multiple' style='filter:alpha(opacity=0);opacity:0;width: 0;height: 0;'/><button  id='chsfile02' name='chsfile02_1' class='btn btn-primary' onclick='selectFile02();'>Select Tencent File</button><div id='notice02' style='display:none;font-family:Georgia, Times, serif;' ><b>Tencent Files Uploaded</b> </div> </div><div id='display_sec02'  class='col-md-6' ></div>   </div></div>"
    boxhtml = boxhtml + "</div><div class='modal-footer'><div class='form-group' align='center'><div id='dsubm01' class='col-lg-offset-2 col-lg-2' style='display:none;'><button id='submit01' class='btn btn-primary' >Submit</button></div><div><button id='cancel1' type='button' class='btn btn-default' onclick='cancel1()'>Cancel</button></div></div></div></div></div>"

    $('div#start1').append(boxhtml);
    $('div#start1').modal('toggle');
    */
    //$('#modalLabel').attr("text", "Loading For Segment ID ");


    $('#modalLabel').attr("name", "");
    $('#modalLabel').attr("name", idv);
    $('div#start1').modal('toggle');
    $('button#submit01').click(function () {
        $.ajax({
            type: "PUT",
            url: '/stsup01?sid=' + idv,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            async: true,
            success: function (msg) {
                $('div#start1').modal('toggle');                
                $.ajax({
                    type: "POST",
                    url: '/submit01?sid=' + idv,
                    contentType: "application/json; charset=utf-8",
                    dataType: 'json',
                    async: true,
                    success: function (msg) {
                        $('div#start1sts').modal('toggle');

                        /* reload table*/
                        var ds = dataload01();
                        $('#table_list_1').jqGrid('clearGridData');
                        $('#table_list_1').jqGrid('setGridParam', { data: ds });
                        $('#table_list_1').trigger('reloadGrid');
                        var rowNum = $("#table_list_1").jqGrid('getGridParam', 'rowNum');
                        var totalNum = $("#table_list_1").jqGrid('getGridParam', 'records');
                        $('ul#pager_list_t').empty();
                        $('#ttcnt01_val').empty();
                        if (totalNum > 0) {
                            $('ul#pager_list_t').append("<li id='fst'><a href='#'>&laquo;</a></li>");
                            $('ul#pager_list_t').append("<li id='pvs'><a href='#'>&lsaquo;</a></li>");
                            if (Math.ceil(totalNum / rowNum) >= 5) {
                                var pagecnts = 5;
                            } else {
                                var pagecnts = Math.ceil(totalNum / rowNum);
                            }
                            for (var i = 0; i < pagecnts; i++) {
                                if (i == 0) {
                                    $('ul#pager_list_t').append("<li class='active'><a href='#'·>" + (i + 1) + "</a></li>");
                                }
                                else {
                                    $('ul#pager_list_t').append("<li><a href='#'>" + (i + 1) + "</a></li>");
                                }
                            }
                            $('ul#pager_list_t').append("<li id='nxt'><a href='#'>&rsaquo;</a></li>");
                            $('ul#pager_list_t').append("<li id='lst'><a href='#'>&raquo;</a></li>");
                        }
                        else {
                            $('ul#pager_list_t').append("<li><a href='#'>&laquo;</a></li>");
                            $('ul#pager_list_t').append("<li><a href='#'>&lsaquo;</a></li>");
                            $('ul#pager_list_t').append("<li class='active'><a href='#'>1</a></li>");
                            $('ul#pager_list_t').append("<li><a href='#'>&rsaquo;</a></li>");
                            $('ul#pager_list_t').append("<li><a href='#'>&raquo;</a></li>");
                        }
                        $('#ttcnt01_val').append("共" + totalNum + "条记录");
                    }
                });
            }
        });
    });

});