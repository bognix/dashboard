define('iframe', ['jquery', 'spinner', 'mustache'], function($, spinner, mustache) {
	var template = $('#iframeResult').html();

	function createIframe(config) {
		var rendered = mustache.render(template, {
				url: config.url
			}),
			container = $(document.getElementById(config['id']));

			container.html(rendered);
	}

	return {
		createIframe: createIframe
	}
})