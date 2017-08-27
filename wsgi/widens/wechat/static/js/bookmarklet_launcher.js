/**
 * Created by zhouzw on 2017/7/30.
 */
(function(){
    if(window.myBookmarklet!==undefined){
        myBookmarklet();
    }
    else{
        document.body.appendChild(document.createElement('script')).src='http://widen-zhouzw.rhcloud.com/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();