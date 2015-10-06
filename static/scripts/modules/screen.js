define('screen', ['jquery', 'jenkins', 'spinner', 'mustache', 'pie-chart'], function($, jenkins, spinner, mustache, pieChart) {
    'use strict';

    function createScreen(screenConfig) {
        switch (screenConfig['data_source']) {
            case 'jenkins':
            case 'jenkins-api':
                jenkins.createItems(screenConfig, pieChart.drawPies);
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
