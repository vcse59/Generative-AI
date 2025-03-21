const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: './index.web.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
    },
    module: {
        rules: [
            // Rule to handle JavaScript, JSX, TypeScript, and TSX files
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules\/(?!react-native-markdown-display)/, // Exclude most node_modules except for specific cases
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            '@babel/preset-env', // Transpiles ES6+ to ES5
                            '@babel/preset-react', // Handles JSX
                        ],
                        plugins: ['@babel/plugin-transform-runtime'], // Optimizes Babel helpers
                    },
                },
            },
            // Rule to handle images (png, jpg, gif)
            {
                test: /\.(png|jpe?g|gif)$/i,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[path][name].[ext]',
                        },
                    },
                ],
            },
            {
                test: /postMock.html$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                    },
                },
            },
        ],
    },
    resolve: {
        alias: {
            'react-native$': 'react-native-web', // Ensures React Native components are resolved to web equivalents
            // Mock Platform module for web usage
            'react-native/Libraries/Utilities/Platform': path.resolve(__dirname, 'src/platform-web.js')
        },
        extensions: ['.web.js', '.js', '.json', '.jsx'], // Support for JSX files
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html', // Webpack HTML template
        }),
    ],
    devServer: {
        static: {
            directory: path.join(__dirname, 'public'),
        },
        port: 8080, // Port for dev server
    },
};
