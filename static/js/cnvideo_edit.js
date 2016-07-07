function cnVideoEditBlock (runtime, element) {
    $(element).find('.save-button').bind('click', function () {
        var handlerUrl = runtime.handlerUrl(element, 'studio_save');
        var data = {
            href: $(element).find('input[name=href]').val(),
            maxwidth: $(element).find('input[name=maxwidth]').val(),
            maxheight: $(element).find('input[name=maxheight]').val(),
        };
        runtime.notify('save', {state: 'start'});
        $.post(handlerUrl, JSON.stringify(data)).done(function(res){
            runtime.notify('save', {state: 'end'});
        });
    });
    
    $(element).find('.cancel-button').bind('click', function(){
        runtime.notify('cancel', {});
    });
}
