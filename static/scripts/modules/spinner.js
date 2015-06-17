define('spinner', ['jquery'], function($) {
    "use strict";

    function hideSpinner(groupName) {
        var placeholder = $('#' + groupName);
        placeholder.removeClass('show-spinner');
    }

    function showSpinner(groupName) {
        var placeholder = $('#' + groupName);
        placeholder.addClass('show-spinner');
    }

    return {
        hideSpinner: hideSpinner,
        showSpinner: showSpinner
    }
});
