define('jenkins', ['jquery', 'spinner', 'mustache'], function($, spinner, mustache) {
    'use strict';

    var template, jenkinsName;

    function getRequest(groupName, type) {
        return $.ajax({
            url: 'jenkins_results/' + jenkinsName + '/' + groupName + '/' + (type || '') ,
            dataType: 'json'
        });
    }

    function createItems(screenConfig, cb) {
        var $screen = $(document.getElementById(screenConfig['id'])),
            items = screenConfig['screen_items'],
            updateInterval = screenConfig['update_interval'],
            templateID;

        switch (screenConfig.type) {
            case 'grouped':
                templateID = 'jenkinsResult';
                break;
            case 'single':
                templateID = 'jenkinsReslutSingle';
                break;
            default:
                templateID = 'jenkinsResult';
                break;
        }

        jenkinsName = screenConfig['data_source'];
        template = $(document.getElementById(templateID)).html();

        if (items) {
            for (var i=0; i<items.length; i++) {
                createItem(items[i], $screen, updateInterval, screenConfig.type, cb);
            }
        }
    }

    function createItem(item, $screen, updateInterval, type, cb) {
        var request = getRequest(item, type);

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
