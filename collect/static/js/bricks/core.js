var bricks = (function ($) {
    var json = bricks$json;
    var actions = bricks$actions;
    var util = bricks$util;
    var byId = util.byId;

    // Main entry point
    function bricks() {
        return bricks_call(arguments, {
            program: true,
            converter: function (x) {
                return x.result
            }
        });
    }


    // The synchronous version of the bricks() function.
    bricks.sync = function () {
        return bricks_call(arguments, {
            async: false,
            program: true,
            converter: function (x) {
                return x.result
            }
        });
    };


    // Like the regular bricks function, but it does not run any program
    // returned by the server.
    bricks.call = function () {
        return bricks_call(arguments, {
            program: false,
            converter: function (x) {
                return x.result
            }
        });
    };


    // Consumes and execute javascript
    bricks.js = function () {
        return bricks_call(arguments, {
            method: 'js',
            converter: function (x) {
                return x.data
            }
        }).then(processProgram);
    };


    /**
     Retrieve HTML data from a registered bricks template by passing the
     given arguments.

     In Django, functions are registered using the @bricks.html decorator::

     .. code:: python
     import bricks

     @bricks.html
     def js_maker(request, arg1, arg2, arg3, ...):
     return string_of_html_source()

     */
    bricks.html = function (api) {
        return bricks_call(arguments, {
            bricks: 'html',
            converter: function (x) {
                return x.data
            }
        });
    };


    /**
     Similar to bricks.html. However, the second argument is a CSS selector
     for the elements that will receive the resulting html code.
     */
    bricks.htmlTo = function () {
        var selector = arguments[2];
        arguments.splice(1, 1);

        return bricks.html.apply(this, arguments).then(function (html) {
            $(selector).html(html);
        });

    };

    /**
     Form processing using bricks: the form is converted into the arguments
     passed to a bricks function which is then executed.
     */
    bricks.form = function (api, form) {
        var args = getFormData(form);
        if (args.__pending !== undefined) {
            var pending = args.__pending;
            var send = function () {
                if (pending.__size === 0) {
                    delete args.__pending;
                    return bricks(api, args);
                } else {
                    setTimeout(send, 50);
                }
            };
            setTimeout(send, 50);
        } else {
            return bricks(api, args);
        }
    };

    /**
     Bind api element to form submit event.
     */
    bricks.bindForm = function (api, form) {
        $(form).submit(function (event) {
            event.preventDefault();
            bricks.form(api, this);
        });
    };

    bricks.bindClick = function (api, elem) {
        $(elem).click(function (event) {
            event.preventDefault();
            bricks.click(api, this);
        })
    };

    bricks.bind = function (api, elem, event) {
        if (event == undefined) {
            return bindAuto(api, elem);
        }

        // We map event names to events
        return {
            form: bricks.bindForm,
            click: bricks.bindClick
        }[event](api, elem);
    };

    function bindAuto(api, element) {
        var query;
        if (element === undefined) {
            query = $('[bricks-bind]');
        } else {
            query = $('[bricks-bind]', element);
        }
        bindForms(api, query);
        bindClickable(api, query);
    }

    // Bind all bricks form elements to the submit event
    function bindForms(api, query) {
        query.filter('form').each(function () {
            if (api === undefined) {
                api = $(this).attr('bricks-bind');
            }
            var transform = getBoundTransform(this);
            bricks.bindForm(api, this, transform);
        });
    }

    // Bind all clickable elements to bricks
    function bindClickable(api, query) {
        query.filter('a, button, input[type=button]').each(function () {
            if (api == undefined) {
                api = $(this).attr('bricks-bind');
            }
            var transform = getBoundTransform(this);
            bricks.bindClick(api, this, transform);
        });
    }

    function getBoundTransform(elem) {
        var data = $(elem).attr('bricks-transform');
        return undefined;
    }


    function getFormData(form) {
        var files = {};
        var pending = {__size: 0};
        var formData = {fileData: files, __pending: pending};
        var params = $(form).serializeArray();

        // We add all files in the array as a text file. Maybe in the future we
        // will add support for binary data
        $(form).find('input[type=file]').each(function (i, item) {
            var itemFileList = [];
            formData[item.name] = itemFileList;

            for (var i = 0; i < item.files.length; i++) {
                var file = item.files[i];
                var reader = new FileReader();
                pending[file.name] = true;
                itemFileList[itemFileList.length] = file.name;
                pending.__size += 1;
                reader.readAsText(file);
                reader.onloadend = function () {
                    files[file.name] = reader.result;
                    delete pending[file.name];
                    pending.__size -= 1;
                };
            }
        });
        if (pending.__size === 0) {
            delete formData.__pending;
        }

        // Convert array into dictionary. We iterate backwards to preserve the
        // first occurrence of a given name.
        for (var i = params.length - 1; i >= 0; i--) {
            var item = params[i];
            formData[item.name] = item.value;
        }
        return formData;
    }


    // Workhorse implementation for bricks(), bricks.call(), etc.
    bricks.rpc = function (args) {
        // Initialize parameters
        args = $.extend({
            api: undefined,
            params: {},
            async: true,
            program: true,
            errors: true,
            timeout: 5,
            bricks: 'api',
            converter: function (x) {
                return x
            }
        }, args);

        // Check consistency
        if (args.api === undefined) {
            throw TypeError('must define an api function');
        }

        // Create the payload
        var payload = json.dumps({
            jsonrpc: '2.0',
            method: args.api,
            params: args.params,
            id: Math.random(),
        });

        // Create ajax promise object
        var promise = $.ajax({
            url: args.api,
            data: payload,
            contentType: 'application/json',
            dataType: 'json',
            async: args.async,
            method: 'POST',
            converters: {
                "text json": function (x) {
                    var raw = $.parseJSON(x);
                    var data = json.decode(raw);
                    args.errors && processErrors(data.error);
                    if (data.result.constructor == json.JsAction) {
                        processProgram(data.result.js);
                        data.result = data.result.result;
                    }
                    return args.converter(data.result);
                }
            }
        });

        return (args.async) ? promise : promise.responseJSON;
    };

    function processProgram(program) {
        if (program !== undefined) {
            Function(program)();
        }
    }


    function processErrors(error) {
        if (error !== undefined) {
            var errormsg = error.error + ': ' + error.message + '\n\n' + error.traceback;
            bricks.dialog({html: errormsg});
            throw Error(errormsg);
        }
    }

    // Auxiliary function used to normalize input arguments to many bricks
    // methods.
    function bricks_call(args, options) {
        var api_url = args[0];
        args = Array.prototype.slice.call(args, 1);

        if (api_url[api_url.length - 1] === '*') {
            kwargs = {}
        } else if (args.length == 0) {
            args = [];
            kwargs = {};
        } else if (args.length == 1 && args[0] instanceof Object) {
            kwargs = args[0];
            args = [];
        } else {
            kwargs = {};
        }

        // Normalize api name
        if (api_url[api_url.length - 1] !== '/') {
            api_url = api_url + '/';
        }

        // Create promise and attach value() method
        if (args.length != 0) {
            kwargs['*args'] = args
        }
        var promise = bricks.rpc($.extend({
            api: api_url,
            params: kwargs,
        }, options));

        return promise;
    }

    // Support CSRF protection for AJAX requests in Django.
    // This recipe was taken from Django's documentation.
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    // Configure bricks function and register it in jQuery.
    $.bricks = bricks;
    bricks.bricksURI = '/api/';
    bricks.do = bricks$actions;
    bricks.json = json;
    return bricks;
})(jQuery);


// Bind all [bricks-bind] elements in the bubbling phase of document load.
window.addEventListener('load', function () {
    bricks.bind();
}, false);