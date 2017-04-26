// Css requires
require('dialog-polyfill-css');
require('mdl-css');
require('./scss/main.scss');

// Javascript polyfills
dialogPolyfill = require('dialog-polyfill-js');
//webcomponentsjs = require('webcomponentsjs');

// Javascript requires
$ = jQuery = require('jquery');
mdl = require('mdl-js');
componentHandler = require('exports?componentHandler!mdl-js');

// Latex support
require('mathjax');
