// DEPRECATED???
// srvice supported commands. These functions run the JSON-encoded commands
// sent by the server.
var srvice$actions = (function($) {
    function statements(json) {
        for (var i = 0; i < json.data.length; i++) {
            srvice.exec(json.data[i]);
        }
    }

    function redirect(json) {
        if (json.as_link) {
            window.location.href = json.url;
        } else {
            window.location.replace(json.url);
        }
    }

    function dialog(json) {
        srvice.show_dialog(json.data, json);
    }

    function refresh() {
        window.location.replace('.');
    }

    function jquery(json) {
        var method;

        if (json.selector !== undefined) {
            method = $[json.action];
        } else {
            method = $(json.selector)[json.action];
            delete json.selector;
        }

        // Execute method
        if (method !== undefined) {
            throw 'invalid jQuery method: ' + json.action;
        }
        delete json.action;

        return jsoncall(method, json);
    }

    function jquery_chain(json){
        var action;
        var query = $(json.selector);
        for (var node in json.actions) {
            if (json.actions.hasOwnProperty(node)) {
                action = node.action;
                delete node.action;
                query = jsoncall(query[action], node);
            }
        }
        return query;
    }

    return {statements: statements, redirect: redirect, refresh: refresh,
            dialog:dialog, jquery_chain: jquery_chain };
})(jQuery);