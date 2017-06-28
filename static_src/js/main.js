// Utility functions
function bindPaperTabs(element) {
    var tabs = element.querySelector('paper-tabs');
    var pages = element.querySelector('iron-pages');
    tabs.selected = tabs.selected && 0;
    pages.selected = pages.selected && 0;

    tabs.addEventListener('iron-select', function () {
        pages.selected = tabs.selected;
    })
}


$.fn.submitWith = function (data) {
    var select;
    form = this[0];

    for (var k in data) {
        select = $(form).find('[name=%s]'.replace('%s', k))[0];
        select.value = data[k];
    }

    return $(form).submit();
};

var $styles = $(function () {
    var apply_styles = true;
    var elements = $();
    componentHandler.upgradeDom();

    // Apply material style to all form elements
    // if (apply_styles) {
    //    var buttons = $('button, input[type=button], input[type=reset], input[type=submit], .button');
    //    buttons.addClass('mdl-button mdl-js-button mdl-js-ripple-effect');
    //    buttons.filter('.primary, [raised]').addClass('mdl-shadow--4dp mdl-button--raised');
    //    buttons.filter(':not(.flat)').addClass('mdl-button--raised');
    //    elements = elements.add(buttons);
    //}

    // Make open=False for main dialog
    $('#dialog, dialog').each(function (i, el) {
        el.open = false;
    });

    if (apply_styles) {
        elements.each(function (idx, elem) {
            componentHandler.upgradeElement(this);
        });
    }

});


$(function () {
    // Make sortable-js understand the sync-api and sync-id attributes when
    // sorting
    $('sortable-js').on('update', function () {
        var state = this.sortable.toArray();
        var api_url = (this.attributes['sync-api'] || {}).nodeValue;
        var api_id = (this.attributes['sync-id'] || {}).nodeValue;

        if (api_url) {
            if (('' + this.__array_state) === ('' + state)) {
                return;
            }
            this.__array_state = state;
        }
        $.srvice(api_url, {owner_ref: api_id || null, order: state});
    });

    // Enable the remove button from sortable-remove classes
    $('sortable-js .sortable-remove')
        .fadeTo(1, 0.1)
        .hover(
            function () {
                $(this).fadeTo(0.1, 1)
            },
            function () {
                $(this).fadeTo(1, 0.1)
            }
        )
        .click(function () {
            var sortable = this.parentNode;
            var parent = this;
            while (sortable.nodeName !== 'SORTABLE-JS') {
                parent = sortable;
                sortable = sortable.parentNode;
            }
            parent.remove();
            sortable.fire('update');
        });
});