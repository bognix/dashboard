define('jenkins', ['jquery', 'spinner', 'mustache'], function($, spinner, mustache) {
    'use strict';

    var template = $('#jenkinsResult').html();

    function getRequest(groupName) {
        return $.ajax({
            url: 'jenkins_results/' + groupName,
            dataType: 'json'
        });
    }

    function createItems(screenConfig) {
        var $screen = $(document.getElementById(screenConfig['id'])),
            items = screenConfig['screen_items'];

        if (items) {
            for (var i=0; i<items.length; i++) {
                createItem(items[i], $screen);
            }
        }
    }

    function createItem(item, $screen) {
        var request = getRequest(item);

        request.done(function(jenkinsBuildData) {
            var rendered = mustache.render(template, jenkinsBuildData),
                $dashboardItem;

            $dashboardItem = $screen.find('#' + jenkinsBuildData['name']);
            spinner.hideSpinner(jenkinsBuildData['name']);
            $dashboardItem.html(rendered);

            if (jenkinsBuildData['status'] === 'FAILURE') {
                $dashboardItem.addClass('failed');
            }
        });
    }

    return {
        createItems: createItems
    }
});