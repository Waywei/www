$(document).ready(function(){
  var target = $(".favtopic")
  target.click(function(e){
    e.preventDefault()
    $.ajax({
      type: "POST",
      url: target.attr("href")
    }).done(function( msg ) {
      if(msg.action =="fav"){
        target.removeClass("btn1").addClass("btn2")
        target.find("span").text("取消收藏")
      }else if(msg.action == "unfav"){
        target.removeClass("btn2").addClass("btn1")
        target.find("span").text("收藏话题")
      }else{
        alert("出错了 别乱搞啦")
      }
    });
  })
})


$(document).ready(function(){
  var target = $(".favnode")
  target.click(function(e){
    e.preventDefault()
    $.ajax({
      type: "POST",
      url: target.attr("href")
    }).done(function( msg ) {
      if(msg.action =="fav"){
        target.removeClass("btn1").addClass("btn2")
        target.find("span").text("取消收藏")
      }else if(msg.action == "unfav"){
        target.removeClass("btn2").addClass("btn1")
        target.find("span").text("收藏节点")
      }else{
        alert("出错了 别乱搞啦")
      }
    });
  })
})

$(document).ready(function(){
  var target = $(".favuser")
  target.click(function(e){
    e.preventDefault()
    $.ajax({
      type: "POST",
      url: target.attr("href")
    }).done(function( msg ) {
      if(msg.action =="fav"){
        target.removeClass("btn1").addClass("btn2")
        target.find("span").text("取消关注")
      }else if(msg.action == "unfav"){
        target.removeClass("btn2").addClass("btn1")
        target.find("span").text("特别关注")
      }else{
        alert("出错了 别乱搞啦")
      }
    });
  })
})

$(document).ready(function(){

var geo = $('#getgeo');
geo.click(function(){
  getLocation()
})
function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition);
    }
  else{
    $(".geoerror").html("请升级你的浏览器，暂时把你放在北京了")
    $("#latitude").val(39.9161523)
    $("#longitude").val(116.4470363)
  }
  }
function showPosition(position)
  {
    $("#latitude").val(position.coords.latitude)
    $("#longitude").val(position.coords.longitude)
  }
})


$(document).ready(function(){
  $("#uploads").change(function(){
    $(this).closest('form').trigger('submit');  
  })
})

$(document).ready(function(){
  var comment = $("#comment-content")
  $(".comment-list .item").each(function(i,item){
    var name = $(item).find(".detail .info span").eq(0).text()
    name = name.replace("\n","");
    var reply = $("<i>").addClass("fa").addClass("fa-reply");
    reply.css("cursor","pointer")
    reply.click(function(){
      var text = comment.val()
      comment.val("@"+name+"\n"+text)
    })
    $(item).find(".info").append(reply)
  
  })


})
