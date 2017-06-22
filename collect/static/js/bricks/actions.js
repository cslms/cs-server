(function($) {
    /**
     * Go to the given url as if following a click.
     *
     * @param url
     * @param replace
     */
    bricks.go = function (url, link) {
        if (link) {
            window.location.href = url;
        } else {
            window.location.replace(url);
        }
    };
})(jQuery);