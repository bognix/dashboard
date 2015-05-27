define('dashboard', ['jquery', 'screen'], function($, screen){
    'use strict';

    var config = $('#mainContainer').data('config'),
        screens = config['screens'],
        screensIdList = [],
        activeScreen;

    function create() {
        var screensCount,
            screenConfig,
            i;

        showScreen(config['screens'][0]['id']);

        if (screens) {
            screensCount = config['screens'].length;
        }

        for (i=0; i<screensCount; i++) {
            screenConfig = config['screens'][i];
            screen.createScreen(screenConfig);
            screensIdList.push(screenConfig['id']);
        }

    }

    function showScreen(id) {
        if (activeScreen) {
            document.getElementById(activeScreen).classList.add('hidden');
        }

        document.getElementById(id).classList.remove('hidden');
        activeScreen = id;
    }

    function showNextScreen() {
        var currentIndex = screensIdList.indexOf(activeScreen);

        if (currentIndex + 1 < screensIdList.length) {
            showScreen(screensIdList[currentIndex+1]);
        } else {
            showScreen(screensIdList[0]);
        }
    }

    function switchOnScreenRotation() {
        setInterval(showNextScreen, 10000)
    }

    return {
        create: create,
        switchOnScreenRotation: switchOnScreenRotation
    }
});