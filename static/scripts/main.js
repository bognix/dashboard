require.config({
    baseUrl: 'static/scripts/modules',
    paths: {
        main: '../main',
        jquery: '../external/jquery/dist/jquery',
        mustache: '../external/mustache/mustache'
    }
});

requirejs(['dashboard'], function(dasboard) {
    dasboard.create();
    dasboard.switchOnScreenRotation();
});