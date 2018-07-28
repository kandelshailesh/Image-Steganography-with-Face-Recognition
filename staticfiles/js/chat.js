var text_box_send = '<div class="row"><div class="col-sm-6"></div><div class="col-sm-6"><div style=" padding:10px; color: black; overflow-wrap:break-word; border-radius: 5px;  background-color: #EEE;">'+'{message}'+'</div></div>';


var image_insert_send='<div class="row"><div class="col-sm-6"></div><div class="col-sm-6"> <img src="/static/second/{message}" id="/static/second/{message1}"  width=300px; height=300px;/> <button id="{message2}" onclick="decoded(this.id)" style="display:hidden; width:50px; height:50px; border-radius:25px; background-color:#00ACE9; font-size:20px; color:black;">D</button></div></div>';

var image_insert_receiver='<div class="row"><div class="col-sm-6"> <img  style="order:-1;" id="/static/second/{message}" src="/static/second/{message1}" width=300px; height=300px;/> <button id="{message2}" onclick="decoded(this.id)" style="display:hidden; width:50px; height:50px; border-radius:25px; background-color:#00ACE9; font-size:20px; color:black;">D</button></div><div class="col-sm-6"></div></div>';

var text_box_receive='<div class="row"><div class="col-sm-6"> <div style=" padding:10px; color: white; overflow-wrap:break-word; border-radius: 5px;  background-color: blue;">'+'{message}'+'</div></div><div class="col-sm-6"></div></div>';

var image_box= '<input type="text" value="{image_mess}">';

var web_host='<div class="dialog" id="{x.id}" style=" height:70px; border-bottom: 1px solid #EEE;"><a style="text-decoration:none; color:black; " href="/chat/{request.user.id}/{x.id}" id="user{x.id}"><img style="width:30px; height:30px; border-radius:10px; " src="https://frontend-1.adjust.com/new-assets/images/site-images/interface/user.svg"> <span class="title" style="position:relative; top:-10px; font-weight: bolder;">'+'{username}'+'</span><p style="margin-left:30px; max-width: 90%; max-height: 20px;">'+'{message}'+'</p></a></div>';

function scrolltoend() {
    console.log("HEllo");
    $('.chatlogs').stop().animate({
       scrollTop: $('.chatlogs')[0].scrollHeight
    }, 100);
}

function decoded(iden){
    m="/static/second/"+iden;
    // m=document.getElementById('identity').src;
    // m=$('#images').attr('src');
    console.log(m)
    $.ajax({
        url:'/decoded',
        type:'post', 
        data: { message:m,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
        dataType:'text',
        success:function(data)
            {
            alert(data);
            console.log(data);
        }
    });
}

function send(sender, receiver, message) {
    $.post('/api/messages', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        source="/static/second/"+message
        var ext = message.split('.').pop();
        '{% load staticfiles %}'
    if(ext === "jpg" || ext==="jpeg" || ext==="png") 
    {
     var box= image_insert_send.replace('{message}',message);
     var box= box.replace('{message1}',message);
     var box= box.replace('{message2}',message);
     $('.chatlogs').append(box);
    }
    else
    {
    console.log("Yes")
     var  box = text_box_send.replace('{message}', message);
     $('.chatlogs').append(box);
        
    }
    // var aSound = document.createElement('audio');
    // aSound.setAttribute('src','/static/beep.wav');
    // aSound.play();
        // $('#board').append(box);

        scrolltoend();
    })
    checkmessage();
}

function receive() {
    $.get('/api/messages/'+ sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        console.log("OK");
        if (data.length !== 0)
        {
            for(var i=0;i<data.length;i++) {
                console.log(data[i]);
                var ext = data[i].message.split('.').pop();
                // var box = text_box.replace('{sender}', data[i].sender);
                 '{% load staticfiles %}'
                if( ext === "jpg" || ext==="jpeg" || ext==="png") 
                {
                    var box = image_insert_receiver.replace('{message}', data[i].message);
                    var box = box.replace('{message1}',data[i].message);
                    var box= box.replace('{message2}',data[i].message);
                   
                }
                else
                {
                 var box= text_box_receive.replace('{message}',data[i].message);
                }
                $('.chatlogs').append(box);
                var aSound = document.createElement('audio');
                aSound.setAttribute('src','/static/beep.wav');
                aSound.play();
                scrolltoend();
               
            }
        }
    })
     checkmessage();
     checknewmessage();
}


function checkmessage()
{   
     
    $.get('/apis/messages/'+ sender_id + '/' + receiver_id, function (data) {
        console.log("checkmessage");
        console.log(data);
        console.log("OK");
        if (data.length !== 0)
        { 
            
            for(var i=0 ; i<1;i++)
            {
            console.log("Shailesh");
            console.log(data.sender);
            var hold= data.message;
            var box= web_host.replace('{request.user.id}',receiver_id);
            var box= box.replace('{x.id}',sender_id);
            var box=box.replace('{username}',data.sender);
            var box=box.replace('{message}',data.message);

                            
}
}
if(document.getElementById(sender_id)===null)
{
$('.scrolling').prepend(box);
}
else
{
var messageid= "message".concat(sender_id);
document.getElementById(messageid).textContent=hold;
var findname= document.getElementById(sender_id);
// document.getElementById(sender_id).remove();
$('.scrolling').prepend(findname);
}
})
}

function checknewmessage() {
     $.get('/apis/messages/'+ receiver_id, function (data) {
        console.log("entry to the game");
        console.log(data);
        if (data.length !== 0)
        { 
            
            for(var i=0 ; i<1;i++)
            {
            console.log("Shailesh");
            console.log(data.sender);
            var hold= data.message;
            var holdid=data.sender_id;
            var box= web_host.replace('{request.user.id}',receiver_id);
            var box= box.replace('{x.id}',data.sender_id);
            var box=box.replace('{username}',data.sender);
            var box=box.replace('{message}',data.message);

                            
}
// if(document.getElementById(holdid)===null)
// {
// $('.scrolling').prepend(box);
// }
// else
// {
// var messageid= "message".concat(holdid);
// document.getElementById(messageid).textContent=hold;
// var findname= document.getElementById(holdid);
// // document.getElementById(sender_id).remove();
// $('.scrolling').prepend(findname);
// }
}

})

}
function register(username, password) {
    $.post('/api/users', '{"username": "'+ username +'", "password": "'+ password +'"}',
        function (data) {
        console.log(data);
        window.location = '/';
        }).fail(function (response) {
            $('#id_username').addClass('invalid');
        })
}