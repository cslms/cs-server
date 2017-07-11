srvice$dialog = (function($) {
    byId = srvice$util.byId;

    function _asDialog(elem) {
        if (elem.showModal === undefined) {
            dialogPolyfill.registerDialog(elem);
        }
        return elem;
    }

    function _getDialog(args, action) {
        args = args || {};
        var dialog = args.dialog || byId(args.dialogId || 'dialog');
        var content = args.dialogContent || byId(args.dialogContentId || 'dialog-content');

        if (dialog === undefined) {
            dialog = document.createElement('DIALOG');
            dialog.id = 'dialog';
            document.body.appendChild(dialog);
        }
        if (content === undefined) {
            content = document.createElement('DIV');
            content.id = 'dialog-content';
            dialog.appendChild(content);
        }

        // Add content from html element, if given
        var html = args.html;
        if (args.sourceId) {
            html = (html || '') + byId(args.sourceId).innerHTML;
            srvice.bind(dialog);
        }

        if (args.url) {
            // Append html from  url
            var promise = $.ajax(args.url, {
                method: 'GET',
                dataType: 'text',
                async: true
            }).then(function (data) {
                $(content).html((html || '') + data);
                action(dialog);
            });

            return promise;
        }
        else {
            if (html !== undefined) {
                $(content).html(html);
            }
            action(dialog);
        }
        var deferred = $.Deferred();
        deferred.resolve(html, 'success', null);
        return deferred.promise();
    }

    /**
     Show dialog with some content.

     It accept the following named arguments.

     Keyword Args:
         dialog:
            The dialog element.
         dialogId:
            The id for the dialog element. The default is 'dialog'. It creates
            a new dialog and appends to body if no dialog is set.
         dialogContent:
            A child element of dialog that should hold the html content.
         dialogContentId:
             The id for dialogContent. The default is 'dialog-content'. If no
             dialog content is specified, it creates a <div id="dialog-content">
             and append to the dialog.
         html:
            The inner HTML text for the dialog-content.
         sourceId:
             If given, represents the id from an html element whose innerHTML
             should be copied to dialogContent element.
         url:
             If given, represents the url that will be used to fetch html data
             and insert in the dialogContent innerHTML.

     Return:
        This function is executed async and return a promise object. The
        chained functions receive a string with the html content inserted into
        the dialog.

     */
    srvice.dialog = function (options) {
        return _getDialog(options, function (dialog) {
            _asDialog(dialog).showModal();
        });
    };

    /**
     * Hide dialog.
     *
     * Accept the same arguments as the dialog() function.
     */
    srvice.closeDialog = function (options) {
        return _getDialog(options, function (dialog) {
            _asDialog(dialog).close();
        });
    };

    /**
     * Toggle dialog visibility.
     *
     * Accept the same arguments as the dialog() function.
     */
    srvice.toggleDialog = function (options) {
        return _getDialog(options, function (dialog) {
            dialog = _asDialog(dialog);
            if (dialog.open) {
                dialog.close()
            }
            else {
                dialog.showModal();
            }
        });
    };
}(jQuery));