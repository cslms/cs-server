var ExtractTextPlugin = require("extract-text-webpack-plugin");
//var ModernizrWebpackPlugin = require('modernizr-webpack-plugin');
var webpack = require("webpack");

module.exports = {
    entry: {
        main: "./static_src/entry.js",
        ace: "./static_src/entry-ace.js",
        //wagtailadmin: "./static_src/entry-wagtail.js",
        //wagtailpageeditor: "./static_src/entry-wagtail-page-editor.js",
        //wagtailhome: "./static_src/entry-wagtail-home_url.js"
    },
    output: {
        path: './static/',
        filename: "[name].js",
        chunkFilename: "[id].js"
    },
    module: {
        loaders: [
            // transpile es6 code to es5 code.
            //{
            //    test: /.js$/,
            //    loader: 'babel-loader',
            //    exclude: [/node_modules/],
            //    query: {
            //      presets: ['es2015', 'stage-2']
            //    }
            //},
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract("style-loader", "css-loader", {publicPath: '../'})
            },
            {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract("style-loader", "css-loader!sass-loader", {publicPath: '../'})
            },
            {
                test: /\.png$/,
                loader: "url?mimetype=image/png"
            },
            {
                test: /\.svg$/,
                loader: 'url?limit=65000&mimetype=image/svg+xml&name=public/fonts/[name].[ext]'
            },
            {
                test: /\.woff$/,
                loader: 'url?limit=65000&mimetype=application/font-woff&name=public/fonts/[name].[ext]'
            },
            {
                test: /\.woff2$/,
                loader: 'url?limit=65000&mimetype=application/font-woff2&name=public/fonts/[name].[ext]'
            },
            {
                test: /\.[ot]tf$/,
                loader: 'url?limit=65000&mimetype=application/octet-stream&name=public/fonts/[name].[ext]'
            },
            {
                test: /\.eot$/,
                loader: 'url?limit=65000&mimetype=application/vnd.ms-fontobject&name=public/fonts/[name].[ext]'
            },
            {
                test: /\.modernizrrc$/,
                loader: "modernizr"
            },
            {
                test: /\.js$/,
                loader: 'exports-loader'
            }
        ]
    },
    plugins: [
        //new ModernizrWebpackPlugin({
        //    'feature-detects': [
        //        'input',
        //        'canvas',
        //        'css/resize'
        //    ]
        //}),
        new ExtractTextPlugin("css/[name].css"),
            //new webpack.optimize.UglifyJsPlugin({
            //    compress: {
            //        warnings: false
            //    },
            //    minimize: true
            //})
    ],
    resolve: {
        modulesDirectories: ['node_modules/'],
        alias: {
            'ace': 'ace-editor-builds/src-min/ace.js',
            'dialog-polyfill-js': 'dialog-polyfill/dialog-polyfill.js',
            'dialog-polyfill-css': 'dialog-polyfill/dialog-polyfill.css',
            'mdl-js': 'material-design-lite/material.min.js',
            'mdl-css': 'material-design-lite/material.min.css',
            'riot': 'riot/riot.min.js',
            'webcomponents.js': 'webcomponents.js/webcomponents-lite.js'
        }
    }
};
