var ipUrl = "kns.cnki.net";//此处的ip是Krs发布机器的ip地址  ，外网发布时则修改为域名。
var indexArray = ["http://www.cnki.net"];
var ISIE;

$(function () {
    RecommendFun();
});
function RecommendFun() {
    ISIE = navigator.userAgent.indexOf("MSIE") != -1 && !window.opera;

    //设置cookie（GUID）
    SetCookie("cnkiUserKey", SetNewGuid(), 3650);

    //进入首页之后，设置cookie则，直接跳出去。
    if (document.URL.toLocaleLowerCase().indexOf(indexArray[0]) > -1) {
        return;
    }

    var userName="";

    if (window.parent.$("#klogin_isPersonal").val() == "1") {
        userName = window.parent.$("#klogin_userName").val();
    }
    else if ($("#klogin_isPersonal").val() == "1") {
        userName = $("#klogin_userName").val();
    }


    var cnkiUserKey = GetCookie("cnkiUserKey");

    //记录检索关键词(brief/brief.aspx)
    WriteKeyWord(userName, cnkiUserKey,window.location);

    //写行为记录
    WriteActionLog(userName, cnkiUserKey, window.location, document.referrer);
}

function WriteActionLog(curUrl, referUrl)
{
    var userName = "";
    if (window.parent.$("#klogin_isPersonal").val() == "1") {
        userName = window.parent.$("#klogin_userName").val();
    }
    else if ($("#klogin_isPersonal").val() == "1") {
        userName = $("#klogin_userName").val();
    }
    var cnkiUserKey = GetCookie("cnkiUserKey");
    WriteActionLog(userName, cnkiUserKey, curUrl, referUrl);
}

//每个记录的页面开始调用这个函数()   记录操作日志文件
function WriteActionLog(userName, cnkiUserKey, curUrl, referUrl) {
    if (curUrl == "") {
        return;
    }
    var turnpage = GetQueryStringByName(curUrl, "turnpage");
    var param = GetQueryStringByName(curUrl, "Param");
    var sorttype = GetQueryStringByName(curUrl, "sorttype");

    if (turnpage != null || param != null || sorttype != null) {
        return;
    }

    if (IsSimFileRequest(curUrl)) {
        return;//有重复记录
    }

    var serverUrl = "http://" + ipUrl + "/KRS/KRSWriteHandler.ashx";
    var geturl = serverUrl + "?curUrl=" + escape(curUrl) + "&referUrl=" + escape(referUrl) + "&cnkiUserKey=" + escape(cnkiUserKey) + "&action=file" + "&userName=" + escape(userName);
    var CoreDomainClass = new CoreDomainLoadJson();
    CoreDomainClass.Load(geturl, function () { });
}
//判断是否在同一天有同样的请求操作文献
function IsSimFileRequest(curUrl) {
    var dbCode = GetQueryStringByName(curUrl, "dbcode");
    var filename = GetQueryStringByName(curUrl, "filename");
    var action = "";
    if (curUrl.toString().indexOf("download.aspx") > -1) {
        action = "download";
    }
    if (curUrl.toString().indexOf("detail.aspx") > -1) {
        action = "view";
    }
    if (curUrl.toString().indexOf("catalogviewpage.aspx") > -1 || curUrl.toString().indexOf("viewpage.aspx") > -1) {
        action = "read";
    }
    if (curUrl.toString().indexOf("share.ashx") > -1) {
        action = "share";
    }

    var actionID = GetActionID();
    var cnkiUserKey = GetCookie("cnkiUserKey");
    var curRecord = cnkiUserKey + actionID + filename + action;

    //先判断是不是今天的时间，不是则全部清空。再判断本次行为有没有操作过。操作过则不需要再次访问
    if (window.localStorage)//本地支持用localStorage
    {
        if (localStorage.getItem("myCnkiTime") != actionID) {
            localStorage.setItem("myCnkiTime", actionID);
            localStorage.removeItem("myCnkiFile");
            localStorage.removeItem("myCnkiKeyWord");
        }
        var recordTodayAll = localStorage.getItem("myCnkiFile");
        if (recordTodayAll != null) {
            var recordItem = recordTodayAll.split('|');
            var type = true;
            for (var i = 0; i < recordItem.length; i++) {
                if (recordItem[i] == curRecord) {
                    type = false;
                    break;
                }
            }
            if (type) {
                localStorage.setItem("myCnkiFile", recordTodayAll + "|" + curRecord);
                return false;//继续记录
            }
            else {
                return true;//不继续记录行为
            }
        }
        else
        {
            localStorage.setItem("myCnkiFile", curRecord);
            return false;//继续记录
        }
    }
}

//记录检索关键词
function WriteKeyWord(userName, cnkiUserKey, curUrl) {
    if (curUrl == "") {
        return;
    }
    var turnpage = GetQueryStringByName(curUrl, "turnpage");
    var param = GetQueryStringByName(curUrl, "Param");
    var sorttype = GetQueryStringByName(curUrl, "sorttype");

    if (turnpage != null || param != null || sorttype != null) {
        return;
    }
    var keyValue = GetQueryStringByName(curUrl, "keyValue");
    if (keyValue == null) {
        return;
    }

    if (IsSimKeyWordRequest(keyValue,cnkiUserKey)) {
        return;
    }
    var serverUrl = "http://" + ipUrl + "/KRS/KRSWriteHandler.ashx";
    var geturl = serverUrl + "?keyWord=" + keyValue + "&cnkiUserKey=" + escape(cnkiUserKey) + "&action=keyWord&userName=" + escape(userName) ;

    var CoreDomainClass = new CoreDomainLoadJson();
    CoreDomainClass.Load(geturl, function () { });
}

//判断关键词记录是否重复
function IsSimKeyWordRequest(keyValue,cnkiUserKey) {
    var actionID = GetActionID();
    var curKeyWord = cnkiUserKey + actionID + keyValue;
    if (window.localStorage)//本地支持用localStorage
    {
        if (localStorage.getItem("myCnkiTime") != actionID) {
            localStorage.setItem("myCnkiTime", actionID);
            localStorage.removeItem("myCnkiKeyWord");
            localStorage.removeItem("myCnkiFile");
        }
        var todayAllKeyWord = localStorage.getItem("myCnkiKeyWord");
        if (todayAllKeyWord != null) {
            var keyWordItem = todayAllKeyWord.split('|');
            var type = true;
            for (var i = 0; i < keyWordItem.length; i++) {
                if (keyWordItem[i] == curKeyWord) {
                    type = false;
                    break;
                }
            }
            if (type) {
                localStorage.setItem("myCnkiKeyWord", todayAllKeyWord + "|" + curKeyWord);
                return false;//继续记录
            }
            else {
                return true;//不继续记录行为
            }
        }
        else {
            localStorage.setItem("myCnkiKeyWord", curKeyWord);
            return false;//继续记录
        }
    }
}

function GetActionID()
{
    var myDate = new Date();
    var year = myDate.getFullYear().toString();
    var month = (myDate.getMonth() + 1).toString();
    var day = myDate.getDate().toString();
    if (month.length == 1) {
        month = "0" + month;
    }
    if (day.length == 1) {
        day = "0" + day;
    }
    var actionID = year + month + day;
    return actionID;
}
   
//获取url参数
function GetQueryStringByName(query, name) {
    if (query && name) {
        var result = query.toString().match(new RegExp("[\?\&]" + name + "=([^\&]+)", "i"));
        if (result == null || result.length < 1) {
            return null;
        }
        return result[1];
    }
    return null;
}

//取url参数值
function getUrlParam(url, name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = url.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return r[2]; return null; //返回参数值
}

//异步获取跨域站点服务内容
function J(C) {
    return document.createElement(C)
}
//添加监听事件
function O(G, U, C) {
    if (ISIE) {
        if (U == "load") {
            G.onreadystatechange = function () {
                if (this.readyState == "loaded") {
                    C();
                }
            }
        }
        else
            G.attachEvent("on" + U, (function (V) { return function () { C.call(V) } })(G))
    }
    else {
        G.addEventListener(U, C, false)
    }
}
function CoreDomainLoadJson() {
    this.C;
    this.J = J;
    this.O = O;
    this.Load = function (src, onJsonLoaded, id) {
        var oldscript = document.getElementById(id);
        if (oldscript) {
            document.body.removeChild(oldscript);
        }
        this.C = J("SCRIPT");
        if (typeof id == "string" && id.length > 0) {
            this.C.id = id;
        }
        else {
            this.C.id = "callScriptE";
        }
        this.C.src = src + "&td=" + (new Date()).getTime();
        this.C.charset = "utf-8";
        document.body.appendChild(this.C);
        O(this.C, "load", onJsonLoaded);
    }
}

//设置cookie
function SetCookie(name, value, expiredays) {
    if (GetCookie(name) == "" || GetCookie(name) == null) {
        var exdate = new Date()
        exdate.setDate(exdate.getDate() + expiredays)
        document.cookie = name + "=" + escape(value) +
        //本地使用
        //((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()) + "; path=/";
        //外网使用
        ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()) + "; path=/;" + "domain=cnki.net";
    }
}

//读取cookies
function GetCookie(name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(name + "=")
        if (c_start != -1) {
            c_start = c_start + name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}

//设置新的GUID
function SetNewGuid() {
    var guid = "";
    for (var i = 1; i <= 32; i++) {
        var n = Math.floor(Math.random() * 16.0).toString(16);
        guid += n;
        if ((i == 8) || (i == 12) || (i == 16) || (i == 20))
            guid += "-";
    }
    return guid;
}


//收集导出和分析记录
function SubmitExportAnaly(action, fileNameItems) {
    var sjson = { action: action, cnkiUserKey: GetCookie("cnkiUserKey"), fileNameItems: fileNameItems};
    $.ajax({
        type: "post",
        url: "http://" + ipUrl + "/KRS/ExportAnal.aspx",
        data: sjson,
        success: function () {
        }
    });
}
