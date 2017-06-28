/*
 * 3rd party libs
 */
// Material design lite
import 'material-design-lite/material';
import * as mdl from 'material-design-lite/material.css';
componentHandler = mdl.componentHandler;

// Dialog polyfill
import 'dialog-polyfill/dialog-polyfill.css';
import * as dialogPolyfill from 'dialog-polyfill/dialog-polyfill';

// Javascript libs
import * as jQuery from 'jquery';
global.$ = jQuery;
global.jQuery = jQuery;


/*
 * Codeschool libs and resources
 */
import './scss/main.scss';
