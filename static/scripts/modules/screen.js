define('screen', ['jquery', 'jenkins', 'jenkins-api', 'spinner', 'mustache', 'pie-chart'], function($, jenkins, jenkinsApi, spinner, mustache, pieChart) {
    'use strict';

    function createScreen(screenConfig) {
        switch (screenConfig['data_source']) {
            case 'jenkins':
                jenkins.createItems(screenConfig, pieChart.drawPies);
                break;
            case 'jenkins-api':
                jenkinsApi.createItems(screenConfig, pieChart.drawPies);
                break;
            default:
                throw new Error('Wrong data source provided');
                break;
        }
    }

    return {
        createScreen: createScreen
    }
});
