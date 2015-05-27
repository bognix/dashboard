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
                $dashboardItem, resultsVisualizationRow;

            $dashboardItem = $screen.find('#' + jenkinsBuildData['name']);
            spinner.hideSpinner(jenkinsBuildData['name']);
            $dashboardItem.html(rendered);

            resultsVisualizationRow = $dashboardItem.find('.results-visualization tr')[0];
            for (var i=0; i < jenkinsBuildData['child_runs_count']; i++) {
                var tdElement = document.createElement('td');
                resultsVisualizationRow.appendChild(tdElement);
            }

            var resultsVisualizationCells;
            resultsVisualizationCells = $dashboardItem.find('.results-visualization td');
            for (var i=0; i<jenkinsBuildData['failed_runs'].length; i++) {
                $(resultsVisualizationCells[i]).addClass('failed');
            }
            if (jenkinsBuildData['status'] === 'FAILURE') {
                $dashboardItem.addClass('failed');
            }
        });
    }

    return {
        createItems: createItems
    }
});