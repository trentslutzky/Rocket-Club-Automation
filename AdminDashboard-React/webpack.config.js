const webpack = require('webpack');

module.exports = {
    mode: 'development',

    entry: './src/index.jsx',

    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader'],
            },

            {
                test: /\.(woff|woff2)$/,
                use: ['url-loader'],
            },

            {
                test: /\.(jpg|jpeg|png|pdf|svg|gif)$/,
                use: ['file-loader'],
            }
        

        ]
    },

    output: {
        path: __dirname + '/public',
        filename: 'bundle.js'
    },

    plugins:[
        new webpack.HotModuleReplacementPlugin()
    ],


}
