function unfold_upload(){
    $('#board #upload-window').fadeIn();
}

function fold_upload(){
    $('#board #upload-window').fadeOut();
    upload_files = new FormData();
    file_num = 0;
    $('#zbasic p').remove();
}

function upload(){
    console.log(upload_files[0]);
    $.ajax({
        url: '/problem/upload/',
        data: upload_files,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
            alert('업로드 되었습니다.');
            fold_upload();
        }
    });
}

function handleFileSelect(evt){
    var files = evt.target.files;
    var length = files.length;
    for(i=0;i<length;i++){
        upload_files.append('file-'+file_num,files[i]);
        var zbasic = $('#zbasic');
        var p = $('<p>').text(files[i].name);
        p.appendTo(zbasic);
        file_num++;
    }
    $('#zbasic input[type=file]').val('')
}

function onDragEnter(event){
    console.log(1);
    console.log(event);
}
function onDrop(event){
    console.log(2);
    console.log(event);
}
