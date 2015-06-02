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
                failedCount = jenkinsBuildData['failed_runs'].length, $dashboardItem, $counter;

            $dashboardItem = $screen.find('#' + jenkinsBuildData['name']);
            spinner.hideSpinner(jenkinsBuildData['name']);
            $dashboardItem.html(rendered);

            $counter = $($dashboardItem.find('.results-counter')[0]);
            if (jenkinsBuildData['child_runs_count'] > 0) {
                $counter.text(failedCount + '/' + jenkinsBuildData['child_runs_count']);

                if (failedCount > 0) {
                    $counter.addClass('failed');
                } else {
                    $counter.addClass('success');
                }
            }

            if (jenkinsBuildData['status'] === 'FAILURE') {
                $dashboardItem.find('h2').addClass('failed');
            }
        });
    }

    return {
        createItems: createItems
    }
});
