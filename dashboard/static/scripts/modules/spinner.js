define('spinner', ['jquery'], function($) {
    "use strict";

    function hideSpinner(groupName) {
        var placeholder = $('#' + groupName);
        placeholder.removeClass('show-spinner');
    }

    return {
        hideSpinner: hideSpinner
    }
});