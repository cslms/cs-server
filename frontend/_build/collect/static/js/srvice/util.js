// Utility functions
srvice$util = (function($) {
    /**
     * Apply dialog polyfill to dialog on unsupported browsers and display it
     * afterwards.
     *
     * @param dialog - <dialog> element.
     */
    function dialogShowModal(dialog) {
        if (dialog.showModal === undefined) {
            dialogPolyfill.registerDialog(dialog);
        }
        dialog.showModal();
    }

    /**
     * Shortcut to document.getElementById()
     */
    function byId(x) {
        return document.getElementById(x);
    }

    /**
     * Variadic function call.
     */
    function varcall(func, args) {
        return func.apply(this, args);
    }

    function jsoncall(method, json) {
        // Execute with positional arguments
        if ('args' in json) {
            var args = json.args || [];
            delete json.args;

            if (!$.isEmptyObject(json)) {
                args[args.length] = json;
            }
            return varcall(method, args);
        }

        // Execute with a single object argument
        else {
            return method(json);
        }
    }

    return {byId: byId, varcall: varcall, jsoncall: jsoncall}
})(jQuery);