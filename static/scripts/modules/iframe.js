define('iframe', ['jquery', 'spinner', 'mustache'], function($, spinner, mustache) {
    var template = $('#iframeResult').html();

    function createIframe(config) {
        var rendered = mustache.render(template, {
                url: config.url
            }),
            container = $(document.getElementById(config['id']));

            container.html(rendered);
            console.log(config['update_interval']);
            setInterval(function() {
                rendered = mustache.render(template, {
                    url: config.url
                }),
                container = $(document.getElementById(config['id']));
                container.html(rendered);
            }, config['update_interval'])
    }

    return {
        createIframe: createIframe
    }
})