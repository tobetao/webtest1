(function(){
    function getNews() {
        $.ajax({
            'type': 'GET',
            'url': '/getnews/',
            'data': {
            },
            success: function (html) {
                $('#news-block').html(html);
                $('#news-block .news-tooltip').each(function(){
                    var _id = $(this).data('id');
                    var content = $('#content-'+ _id).html();
                    $(this).tooltipster({
                        content: content,
                        delay: 0,
                        offsetY: -20,
                        position: 'bottom',
                        theme: 'tooltipster-shadow',
                        trigger: 'hover'
                    });
                });
            }
        })

    }

    function initSettings() {
        $('#save-setting-btn').on('click', function(){
            var data = {};
            $(this).parents('.modal').find('table tr').each(function(){
                var key = $(this).find('input[name=category]').val();
                var value = $(this).find('input[name=keywords]').val();
                if(key && value) {
                    data[key] = value;
                }
            });
            console.log(data);
            $.ajax({
                'type': 'POST',
                'url': '/category/',
                'data': data,
                success: function (html) {
                    $('#setting-modal').modal('hide');
                }
            });
            return false;
        });
    }

    $(function(){
        initSettings();
        getNews();
        setInterval(getNews, 10000)
    });

})();
