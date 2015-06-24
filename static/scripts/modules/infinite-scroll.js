define('infinite-scroll', function() {
    'use strict';

    function addInfiniteScrollToElement($element) {
        var scrollDuration = 5000,
            intervalID;

        intervalID = setInterval(function() {
            //Scroll down
            $element.animate({
                scrollTop: $element.height()
            }, scrollDuration);

            //Scroll up
            $element.animate({
                scrollTop: 0
            }, scrollDuration)
        }, 2 * scrollDuration + 5000);

        return intervalID;
    }

    function removeInfiniteScrollByIntervalID(intervalID) {
        window.clearInterval(intervalID);
    }

    return {
        addInfiniteScrollToElement: addInfiniteScrollToElement,
        removeInfiniteScrollByIntervalID: removeInfiniteScrollByIntervalID
    }
});
