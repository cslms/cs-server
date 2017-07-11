var srvice = (function ($) {
    var json = srvice$json;
    var actions = srvice$actions;
    var util = srvice$util;
    var byId = util.byId;

    /**
     * Main entry point
     */
    function srvice() {
        return srvice_call(arguments, {
            program: true,
            converter: function (x) {
                return x.result
            }
        });
    }


    /**
     * The synchronous version of the srvice() function.
     */
    srvice.sync = function () {
        return srvice_call(arguments, {
            async: false,
            program: true,
            converter: function (x) {
                return x.result
            }
        });
    };


    /**
     Like the regular srvice function, but will not run any program returned by
     the server.

     .. code:: python
     import srvice

     @srvice.program
     def program(client, arg1, arg2, ...):
     if client.request.user is None:
     raise PermissionError

     client.alert("this will trigger a js alert in the client!")
     client.jquery('div').hide()
     client.js('console.log("foo bar")')
     return 42

     This function will only handle the 42 result.
     */
    srvice.call = function () {
        return srvice_call(arguments, {
            program: false,
            converter: function (x) {
                return x.result
            }
        });
    };

    /**
     Execute the javascript source code in the given API point in an
     isolated namespace.

     In Django, functions are registered using the @srvice.js decorator::

     .. code:: python
     import srvice

     @srvice.js
     def js_maker(request, arg1, arg2, arg3, ...):
     return string_of_javascript_code()

     */
    srvice.js = function () {
        return srvice_call(arguments, {
            method: 'js',
            converter: function (x) {
                return x.data
            }
        }).then(processProgram);
    };


    /**
     Retrieve HTML data from a registered srvice template by passing the
     given arguments.

     In Django, functions are registered using the @srvice.html decorator::

     .. code:: python
     import srvice

     @srvice.html
     def js_maker(request, arg1, arg2, arg3, ...):
     return string_of_html_source()

     */
    srvice.html = function (api) {
        return srvice_call(arguments, {
            srvice: 'html',
            converter: function (x) {
                return x.data
            }
        });
    };


    /**
     Similar to srvice.html. However, the second argument is a CSS selector
     for the elements that will receive the resulting html code.
     */
    srvice.htmlTo = function () {
        var selector = arguments[2];
        arguments.splice(1, 1);

        return srvice.html.apply(this, arguments).then(function (html) {
            $(selector).html(html);
        });

    };

    /**
     Form processing using srvice: the form is converted into the arguments
     passed to a srvice function which is then executed.
     */
    srvice.form = function (api, form) {
        var args = getFormData(form);
        if (args.__pending !== undefined) {
            var pending = args.__pending;
            var send = function () {
                if (pending.__size === 0) {
                    delete args.__pending;
                    return srvice(api, args);
                } else {
                    setTimeout(send, 50);
                }
            };
            setTimeout(send, 50);
        } else {
            return srvice(api, args);
        }
    };

    /**
     Bind api element to form submit event.
     */
    srvice.bindForm = function (api, form) {
        $(form).submit(function (event) {
            event.preventDefault();
            srvice.form(api, this);
        });
    };

    srvice.bindClick = function (api, elem) {
        $(elem).click(function (event) {
            event.preventDefault();
            srvice.click(api, this);
        })
    };

    srvice.bind = function (api, elem, event) {
        if (event == undefined) {
            return bindAuto(api, elem);
        }

        // We map event names to events
        return {
            form: srvice.bindForm,
            click: srvice.bindClick
        }[event](api, elem);
    };

    function bindAuto(api, element) {
        var query;
        if (element === undefined) {
            query = $('[srvice-bind]');
        } else {
            query = $('[srvice-bind]', element);
        }
        bindForms(api, query);
        bindClickable(api, query);
    }

    // Bind all srvice form elements to the submit event
    function bindForms(api, query) {
        query.filter('form').each(function () {
            if (api === undefined) {
                api = $(this).attr('srvice-bind');
            }
            var transform = getBoundTransform(this);
            srvice.bindForm(api, this, transform);
        });
    }

    // Bind all clickable elements to srvice
    function bindClickable(api, query) {
        query.filter('a, button, input[type=button]').each(function () {
            if (api == undefined) {
                api = $(this).attr('srvice-bind');
            }
            var transform = getBoundTransform(this);
            srvice.bindClick(api, this, transform);
        });
    }

    function getBoundTransform(elem) {
        var data = $(elem).attr('srvice-transform');
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


    srvice.rpc = function (args) {
        /**
         The workhorse behind srvice(), srvice.run(), srvice.js() and
         srvice.html() functions. It receives a single dictionary argument
         that understands the following parameters:

         api:
         Api name of the called function/program
         args:
         List of positional arguments to be passed to the calling function.
         kwargs:
         An object with all the named arguments.
         server:
         Override the default server root. Usually srvice will open the URL
         at http://<localdomain>/srvice/api-function-name.
         async:
         If true, returns a promise. Otherwise, it blocks execution and
         returns the result of the function call.
         method:
         Can be any of 'api', 'program', 'js', or 'html'.
         program:
         If true (default), execute any received programmatic instructions.
         error:
         If true (default), it will raise any exceptions raised by the remote
         call.
         result:
         If given, will determine the result value of the function call.
         timeout:
         Maximum amount of time (in seconds) to wait for a server response.
         Default to 30.0.
         converter:
         A function that process the resulting JSON result and convert it
         to the desired value.
         */

            // Initialize parameters
        args = $.extend({
            api: undefined,
            args: [],
            kwargs: {},
            async: true,
            program: true,
            errors: true,
            timeout: 5,
            method: 'POST',
            srvice: 'api',
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
            api: args.api,
            args: args.args,
            kwargs: args.kwargs,
            srvice: args.srvice
        });

        // Create ajax promise object
        var promise = $.ajax({
            url: args.api,
            data: payload,
            type: args.method,
            dataType: 'json',
            async: args.async,
            converters: {
                "text json": function (x) {
                    var data = json.loads(x);
                    console.log(data);
                    args.errors && processErrors(data.error);
                    args.program && processProgram(data.program);
                    return args.converter(data);
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
            srvice.dialog({html: errormsg});
            throw Error(errormsg);
        }
    }

    // Auxiliary function used to normalize input arguments to many srvice
    // methods.
    function srvice_call(args, options) {
        var api = args[0];
        args = Array.prototype.slice.call(args, 1);

        if (api[api.length - 1] === '*') {
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
        if (api[api.length - 1] !== '/') {
            api = api + '/';
        }

        // Create promise and attach value() method
        var promise = srvice.rpc($.extend({
            api: api,
            args: args,
            kwargs: kwargs
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


    // Configure srvice function and register it in jQuery.
    $.srvice = srvice;
    srvice.srviceURI = '/api/';
    srvice.do = srvice$actions;
    srvice.json = json;
    return srvice;
})(jQuery);


// Bind all [srvice-bind] elements in the bubbling phase of document load.
window.addEventListener('load', function () {
    srvice.bind();
}, false);