function cnVideoEditBlock (runtime, element) {
    console.log("initializing video edit block")
    $(element).find('.save-button').bind('click', function () {
        var handlerUrl = runtime.handlerUrl(element, 'studio_save');
        var data = {
            href: $(element).find('input[name=href]').val(),
        };
        runtime.notify('save', {state: 'start'});
        $.post(handlerUrl, JSON.stringify(data)).done(function(res){
            console.log("video saved !", res);
            runtime.notify('save', {state: 'end'});
        });
    });
    
    $(element).find('.cancel-button').bind('click', function(){
        runtime.notify('cancel', {});
    });
}
