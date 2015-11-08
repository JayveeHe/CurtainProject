﻿function sleep(numberMillis) {
    var now = new Date();
    var exitTime = now.getTime() + numberMillis;
    while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
            return;
    }
}
//

function shoot_bullet(start_right, start_top, content, total_time) {
    //$('body').css({overflow: 'hidden'});
    var temp_time = new Date().getTime();
    $("body").append("<div id='bullet" + temp_time + "'>" + content + "</div>");
    var bullet = $("#bullet" + temp_time);
    bullet.css({
        'font-size': '35px',
        overflow: 'hidden',
        height: '35px',
        top: start_top,
        'z-index': '100000',
        position: 'fixed',
        left: window.innerWidth - start_right,
        color: '#' + Math.floor(Math.random() * 0xFFFFFF).toString(16)
    });
    console.log("before animate====" + bullet.css('left'));
    console.log(-bullet.width());
    bullet.animate({left: -$(this).width()}, total_time, "linear", function () {
        console.log($(this), 'remove');
        $(this).remove();
    });
    console.log(bullet + "animated");
}

function machine_gun(bullets, scroll_time) {
    var last_timestamp = bullets[0].timestamp;
    for (var i = 0; i < bullets.length; i++) {
        var content = bullets[i].content;
        console.log(bullets[i]);
        var timestamp = bullets[i].timestamp;
        setTimeout("shoot_bullet(-100, "
            + Math.random() * SCREEN_HEIGHT / 2 + ",'"
            + content + "', "
            + scroll_time + ")",
            timestamp - last_timestamp);
        last_timestamp = timestamp;
    }
}

function get_bullets(page_url, user_id) {
    $.post("/getData", {
            page: page_url,
            userID: user_id
        },
        function (data, status) {
            var jsonroot = JSON.parse(data);
            machine_gun(jsonroot.contents, 8000);
            //for (var i = 0; i < jsonroot.contents.length; i++) {
            //    var text = $("<p></p>");
            //    $("body").append(text);
            //    $(text).text(jsonroot.contents[i].content);
            //}
        });
}

var SCREEN_HEIGHT = window.innerHeight;
var SCREEN_WIDTH = window.innerWidth;
//var current_url = window.location.href;
var user_id = 'hehe';
var current_url ='testPage';


var bullets = [{content: "fuckfuckfuck", timestamp: 500},
    {content: "123123123", timestamp: 2500},
    {content: "hahahahahha", timestamp: 3900},
    {content: "卧槽", timestamp: 5000}];
//machine_gun(bullets, 8000);

setInterval(function () {
    get_bullets(current_url, user_id);
    //machine_gun(bullets, 8000);
}, 5000);

//setTimeout("shoot_bullet(-100,100, '测试文本1', 8000)", 0);//延迟500ms执行该语句
//setTimeout("shoot_bullet(-100,200, '啊哈哈哈哈打算放大维纳斯达芙妮撒旦法到哪里可忘记了空位了空间啊蝶恋蜂狂就', 8000)", 1000);
