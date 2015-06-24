define('jenkins', ['jquery', 'spinner', 'mustache', 'infinite-scroll'], function($, spinner, mustache, infiniteScroll, undefined) {
    'use strict';

    var template = $('#jenkinsResult').html(),
        intervalIDs = {};

    function getRequest(groupName) {
        return $.ajax({
            url: 'jenkins_results/' + groupName,
            dataType: 'json'
        });
    }

    function createItems(screenConfig, cb) {
        var $screen = $(document.getElementById(screenConfig['id'])),
            items = screenConfig['screen_items'],
            updateInterval = screenConfig['update_interval'];

        if (items) {
            for (var i=0; i<items.length; i++) {
                createItem(items[i], $screen, updateInterval, cb);
            }
        }
    }

    function createItem(item, $screen, updateInterval, cb) {
        updateDashboard(item, $screen, cb);

        setInterval(function() {
            spinner.showSpinner(item);
            updateDashboard(item, $screen, cb);
        }, updateInterval)
    }

    function updateDashboard(item, $screen, cb) {
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
            }

            if (jenkinsBuildData['status'] === 'FAILURE') {
                $dashboardItem.find('h2').addClass('failed');
            } else {
                $dashboardItem.find('h2').addClass('success');
            }

            //call callback
            cb();
            updateInfiniteScroll(item);
        });
    }

    function updateInfiniteScroll(item) {
        var $item = $('#' + item),
            $contentHeight = $item.find('.left-column').height(),
            $failedList = $item.find('.failed-list'),
            intervalID;

        if ($item.height() < $contentHeight) {
            $failedList.addClass('too-long');
            intervalID = infiniteScroll.addInfiniteScrollToElement($failedList);
            intervalIDs[item] = intervalID;
        } else {
            $failedList.removeClass('too-long');
            if (intervalIDs[item]) {
                intervalID = intervalIDs[item];
                infiniteScroll.removeInfiniteScrollByIntervalID(intervalID);
                intervalIDs[item] = undefined;
            }
        }
    }

    return {
        createItems: createItems
    }
});
