define('jenkins', ['jquery', 'spinner', 'mustache'], function($, spinner, mustache) {
    'use strict';

    var jenkinsName;

    function getRequest(groupName) {
        return $.ajax({
            url: 'jenkins_results/' + jenkinsName + '/' + groupName,
            dataType: 'json'
        });
    }

    function createItems(screenConfig, cb) {
        var $screen = $(document.getElementById(screenConfig['id'])),
            items = screenConfig['screen_items'],
            updateInterval = screenConfig['update_interval'],
            templateID = screenConfig.template || 'jenkinsResult',
            template;

        jenkinsName = screenConfig['data_source'];
        template = $(document.getElementById(templateID)).html();

        if (items) {
            for (var i=0; i<items.length; i++) {
                createItem(items[i], $screen, updateInterval, template, cb);
            }
        }
    }

    function createItem(item, $screen, updateInterval, template, cb) {
        var request = getRequest(item);

        request.done(function(jenkinsBuildData) {
            var rendered = mustache.render(template, jenkinsBuildData),
                $dashboardItem, $counter, failedCount;

            failedCount = Array.isArray(jenkinsBuildData['failed_runs']) ? jenkinsBuildData['failed_runs'].length : 0;
            $dashboardItem = $screen.find('#' + jenkinsBuildData['name']);
            spinner.hideSpinner(jenkinsBuildData['name']);
            $dashboardItem.html(rendered);

            $counter = $($dashboardItem.find('.results-counter')[0]);
            if (jenkinsBuildData['child_runs_count'] > 0) {
                $counter.text(failedCount + '/' + jenkinsBuildData['child_runs_count']);
            } else {
                $($dashboardItem.find('.pie')[0]).hide();
            }

            if (jenkinsBuildData['status'] === 'FAILURE' || jenkinsBuildData['status'] === 'UNSTABLE') {
                $dashboardItem.find('h2').addClass('failed');
            } else {
                $dashboardItem.find('h2').addClass('success');
            }
            cb();
        });

        setInterval(function() {
            spinner.showSpinner(item);
            var request = getRequest(item);
            request.done(function(jenkinsBuildData) {
                var rendered = mustache.render(template, jenkinsBuildData),
                    $dashboardItem, $counter, failedCount;

                failedCount = Array.isArray(jenkinsBuildData['failed_runs']) ? jenkinsBuildData['failed_runs'].length : 0
                $dashboardItem = $screen.find('#' + jenkinsBuildData['name']);
                spinner.hideSpinner(jenkinsBuildData['name']);
                $dashboardItem.html(rendered);

                $counter = $($dashboardItem.find('.results-counter')[0]);
                if (jenkinsBuildData['child_runs_count'] > 0) {
                    $counter.text(failedCount + '/' + jenkinsBuildData['child_runs_count']);
                } else {
                    $($dashboardItem.find('.pie')[0]).hide();
                }

                if (jenkinsBuildData['status'] === 'FAILURE' || jenkinsBuildData['status'] === 'UNSTABLE') {
                    $dashboardItem.find('h2').addClass('failed');
                } else {
                    $dashboardItem.find('h2').addClass('success');
                }
                cb();
            });
        }, updateInterval)
    }

    return {
        createItems: createItems
    }
});
