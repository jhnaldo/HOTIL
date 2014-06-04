function autoHeight(){
    var window_height = parseInt($(window).outerHeight());
    var height = parseInt(window_height - $('#header').outerHeight() - $('#footer').outerHeight());
    var container_height = parseInt($('#container').outerHeight());
    if(container_height < height){
        $('#container').css('height', height+'px');
    }

    $('#background').css('height', parseInt($('body').outerHeight())+'px');
    centerLoginWindow();
}

function loginDialog(){
    var body = $('body');
    var background = $('<div>',{'id':'background'});
    background.appendTo(body);

    var login_div = $('<div>',{'id':'login'});
    login_div.appendTo(body);

    var exit = $('<img>',{'src':'/media/image/x.png','id':'exit','onclick':'closeLogin()'});
    exit.appendTo(login_div);

    var login_content = $('<div>', {'id':'login-content'});
    login_content.appendTo(login_div);
    login_content.load('/media/html/login.html',autoHeight);
}

function closeLogin(){
    $('#background').remove();
    $('#login').remove();
}

function centerLoginWindow(){
    var body_height = parseInt($('body').outerHeight());
    var header_width = parseInt($('#header').outerWidth());
    $('#login').css('margin-left', (header_width-500)/2+'px');
    $('#login').css('margin-top', (body_height-300)/2+'px');
}

function ajaxLogout(){
    $.ajax({
        url: '/logout/',
        type: 'POST',
        dataType : 'json',
        success:function(result){
            alert('로그아웃 되었습니다.');
            window.location='/';
        },
        error:function(e){
            console.log(e);
        }
    });
}

function ajaxLogin(){
    var id = document.getElementsByName('id')[0].value;
    var passwd = document.getElementsByName('password')[0].value;

    var data = {'id':id, 'passwd':passwd};

    $.ajax({
        url: '/login/',
        type: 'POST',
        dataType : 'json',
        data: data,
        success:function(result){
            switch(result){
                case -1:
                    alert('잘못된 입력입니다.');
                    break;
                case 0:
                    alert('존재하지 않는 아이디 혹은 잘못된 비밀번호입니다.');
                    break;
                case 1:
                    window.location='/';
                    break;
            }
        },
        error:function(e){
            console.log('[ERROR] '+e);
        }
    });
}

function unfold_setting(){
    $('#float #black').css('height', '182px');
    setting_fold = false;
}

function fold_setting(){
    $('#float #black').css('height', '0px');
    setting_fold = true;
}
