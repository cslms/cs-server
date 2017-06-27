var webpack = require('webpack');
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');


module.exports = {
    entry: {
        main: './assets/index.js',
        latex: './assets/index-latex.js',
        ace: './assets/index-ace.js',
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'static')
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    use: 'css-loader'
                })
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    use: ['css-loader', 'fast-sass-loader']
                })
            },
            {
                test: /\.vue$/,
                use: 'vue-loader',
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                query: {
                    name: 'img/[name].[ext]'
                }
            },
            {
                test: /\.(ttf|woff2)$/,
                loader: 'file-loader',
                query: {
                    name: 'fonts/[name].[ext]'
                }
            },
            {
                test: /\.elm$/,
                exclude: [/elm-stuff/, /node_modules/],
                loader: 'elm-hot!elm-webpack'
            }
        ],
    },
    plugins: [
        new ExtractTextPlugin("[name].css")
    ],
    resolve: {
        extensions: ['.js', '.ts', '.vue'],
        alias: {
            'ace': 'brace/index.js',
            'vue': 'vue/dist/vue.common.js',
            'jquery': 'jquery/dist/jquery.js'
        }
    },
    devServer: {
        historyApiFallback: true,
        noInfo: true
    },
    //devtool: '#eval-source-map'
};


if (process.env.NODE_ENV === 'production' && false) {
    module.exports.devtool = '#source-map'

    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = module.exports.plugins.concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new ClosureCompilerPlugin({
            compiler: {
                language_in: 'ECMASCRIPT6',
                language_out: 'ECMASCRIPT5',
                compilation_level: 'SIMPLE'/*,
                 create_source_map: true*/
            },
            concurrency: 3
        })
    ])
}
