define('screen', ['jquery', 'jenkins', 'spinner', 'mustache', 'pie-chart', 'iframe'], function($, jenkins, spinner, mustache, pieChart, iframe) {
    'use strict';

    function createScreen(screenConfig) {
        switch (screenConfig['data_source']) {
            case 'jenkins':
            case 'jenkins-api':
                jenkins.createItems(screenConfig, pieChart.drawPies);
                break;
            case 'iframe':
                iframe.createIframe(screenConfig);
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
