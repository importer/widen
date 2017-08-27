$(document).ready(function(){
	var now_id=0
	var obj_lis=$("#adds li").length;
	console.log(obj_lis);

	$("#adds li").click(function(){
	if (obj_lis>now_id){
		addhtml="<"+now_id+">@"+$(this).text();
		$(this).text(addhtml);
		$(this).attr("id",now_id);
		console.log($(this).text());
		$(this).css("color", "red");
		now_id++;
	} else
	{
		console.log("id upp!!");
	}
});
	//点击提交
	$("#add").click(function(){
  	// var obj_lis=$("#adds li");
  	// var data = new Array();;
  	var params = $("#adds li");  
  		console.log("params:");
  		console.log(params);
         var values = {};  
         for (i = 0; i < params.length; i++) {  
  			console.log(params[i].id+":"+params[i].innerText);
  			values[params[i].id] = [params[i].innerText.split('>@')[1],params[i].title];
  			if (params[i].innerText.split('>@')[1]==null){
  				values[params[i].id] = [params[i].innerText,params[i].title];
  			}
              
         }  
         var data = JSON.stringify(values);  
  	console.log(data);
	// var url="http://127.0.0.1:8000/wechat/checkbox/";
	var url="http://widen-zhouzw.rhcloud.com/wechat/checkbox/";
	$.post(url, {"csrfmiddlewaretoken":csrfmiddlewaretoken,"data":data}, function (data) {alert(data);window.close();});
	// $.post(url, {"csrfmiddlewaretoken":getCookie('csrftoken')}, function (data) {alert(data);});
  });
});

//获取 csrf
function getCookie(sName){ 
	var aCookie=document.cookie.split("; "); 
	for(var i=0;i<aCookie.length;i++){ 
		var aCrumb=aCookie[i].split("="); 
		if(sName==aCrumb[0])
			console.log(sName+":"+aCrumb[1]);
			return (aCrumb[1]); 
} return null;} 