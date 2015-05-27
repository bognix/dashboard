define('screen', ['jquery', 'jenkins', 'spinner', 'mustache'], function($, jenkins, spinner, mustache) {
    'use strict';

    function createScreen(screenConfig) {

        switch (screenConfig['data_source']) {
            case 'jenkins':
                jenkins.createItems(screenConfig);
                break;
            //case 'iframe':
            //    iframe.displayPage(screenConfig);
            //    break;
            default:
                throw new Error('Wrong data source provided');
                break;
        }
    }

    return {
        createScreen: createScreen
    }
});