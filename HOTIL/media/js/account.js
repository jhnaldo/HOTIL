function signup(){
    var user_id = document.getElementsByName('id')[0].value;
    var passwd= document.getElementsByName('password')[0].value;
    var re_passwd = document.getElementsByName('re-password')[0].value;
    var name = document.getElementsByName('name')[0].value;

    if(user_id.length < 6){
        alert('아이디는 최소 6자리로 해주세요.');
        return;
    }

    if(passwd.length < 6){
        alert('비밀번호는 최소 6자리로 해주세요.');
        return;
    }

    if(passwd != re_passwd){
        alert('비밀번호가 일치하지 않습니다.');
        return;
    }

    if(name.length < 3){
        alert('이름은 최소 세 자리로 해주세요.');
        return;
    }

    var data = {'id':user_id};

    $.ajax({
        url: '/id_check/',
        type: 'POST',
        dataType : 'json',
        data: data,
        success:function(result){
            if(result<1){
                alert('회원가입이 완료되었습니다.');
                $('#signup-form').submit();
            }else{
                alert('이미 존재하는 아이디 입니다.');
            }
        },
        error:function(e){
            console.log('[ERROR] '+e);
        }
    });
}
