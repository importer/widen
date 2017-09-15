(function () {
    // function myBookmarklet() {
    //     var url = 'http://127.0.0.1:8000/wechat/checkbox/';
    // var url = 'http://widen-zhouzw.rhcloud.com/wechat/checkbox/';
    var url = window.location.host;
    var allText = '<form name="input" action="' + url + '" method="GET">';
    var imgWindow;
    var arr = document.links;
    var re1 = /http(s)?:\/\//;
    for (var i = 0; i < arr.length; i++) {
        var href = arr[i].href;
        var text = arr[i].text;
        if (re1.test(href)) {
            allText += '<input type="checkbox" name="' + text + '" value="' + href + '" />' + '<a href="' + href + '">' + text + '</a></br>';
        } else {
            allText += '<input type="checkbox" name="' + text + '" value="' + url + href + '" />' + '<a href="' + url + href + '">' + text + '</a></br>';
        }
    }
    allText += '<br /><br /><input type="submit" value="Submit" /></from>';
    imgWindow = window.open('', 'imgWin', 'width=800,height=600');
    imgWindow.document.write(allText);
    imgWindow.document.close();
    // }
    // myBookmarklet()
})();
