function cnVideoBlock (runtime, element){
    var iframe = $('.cnvideo iframe'),
        player = $f(iframe[0]),
        watched_count = $('.cnvideo .watched_tracker .watched_count')
    
    console.log("Initialiazed cnVideoBlock !")
    function onFinish (video) {
        $.ajax({
            type : 'POST',
            url : runtime.handlerUrl(element, 'mark_as_watched'),
            data : JSON.stringify({watched:true}),
            success : function (result) {
                watched_count.text(result.watched_count)
            }
        })
    }
    
    player.addEvent('ready', function () {
        player.addEvent('finish', onFinish)
    })
}


