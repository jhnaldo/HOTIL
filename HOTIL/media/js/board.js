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
    $.ajax({
        url: '/problem/upload/',
        data: upload_files,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function(data){
            if(data==-1){
                alert('잘못된 파일입니다.');
            }else{
                alert('업로드 되었습니다.');
            }
            fold_upload();
            pagenum=1;
            page_load();
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
    $('#zbasic').css('border-color','rgb(240,144,70)');
}

function onDragOver(event){
    $('#zbasic').css('border-color','rgb(240,144,70)');
}

function onDragLeave(event){
    $('#zbasic').css('border-color','rgb(82,82,82)');
}

function onDrop(event){
    $('#zbasic').css('border-color','rgb(82,82,82)');
}

function page_load(){
    $('.problem_tr').remove();
    $('.block_tr').remove();
    $('#page-contain').remove();

    conditions={'pagenum':pagenum};
    $.ajax({
        url: '/problem/page/',
        type: 'POST',
        data: conditions,
        dataType : 'json',
        success:function(result){
            var num = result.num;
            var problems = result.problems;
            var k=(num-pagenum)*15+result.remain;
            problems.forEach(function(p){
                add_problem(k,p);
                k--;
            });

            var remain = 15-problems.length;
            for(i=0;i<remain;i++){
                var table = $('#question-list')[0];
                var tr = $('<tr>',{'class':'block_tr'});
                var td1 = $('<td>');
                var td2 = $('<td>');
                var td3 = $('<td>');
                var td4 = $('<td>');
                td1.appendTo(tr);
                td2.appendTo(tr);
                td3.appendTo(tr);
                td4.appendTo(tr);
                tr.appendTo(table);
            }

            var board = $('#board')[0];
            var page_div = $('<div>',{'id':'page-contain'});
            page_div.appendTo(board);
            for(i=1;i<=num;i++){
                if(i==pagenum){
                    var p = $('<p>').text(i);
                    p.appendTo(page_div);
                }else{
                    var p = $('<p>',{'class':'page','onclick':'pagenum='+i+';page_load();'}).text(i);
                    p.appendTo(page_div);
                }
            }
            page_div.css('margin-left',(1000-page_div.width())/2+'px');
        },
    });
}

function add_problem(k,p){
    var table = $('#question-list')[0];
    var tr = $('<tr>',{'class':'problem_tr', 'onclick':'window.location=\'/problem/show/?id='+p.id+'\';'});
    tr.appendTo(table);

    var num_td = $('<td>');
    $('<p>').text(k).appendTo(num_td);
    num_td.appendTo(tr);

    var title_td = $('<td>');
    $('<p>').text(p.title).appendTo(title_td);
    title_td.appendTo(tr);

    var writer_td = $('<td>');
    $('<p>').text(p.writer).appendTo(writer_td);
    writer_td.appendTo(tr);

    var created_td = $('<td>');
    $('<p>').text(p.created).appendTo(created_td);
    created_td.appendTo(tr);
}

function del_problem(id){
    if(confirm('Do you want to delete this problem?')){
        conditions={'id':id};
        $.ajax({
            url: '/problem/delete/',
            type: 'POST',
            data: conditions,
            dataType : 'json',
            success:function(result){
                window.location='/problem/';
            }
        });
    }
}
