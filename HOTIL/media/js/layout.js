function autoHeight(){
    var height = parseInt($(window).outerHeight() - $('#header').outerHeight() - $('#footer').outerHeight());
    var container_height = parseInt($('#container').outerHeight());
    if(container_height < height)
        $('#container').css('height', height+'px');
}
