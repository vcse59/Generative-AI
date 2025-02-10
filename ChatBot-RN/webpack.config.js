const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    mode: "development",
    entry: "./index.web.js",
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bundle.js",
    },
    module: {
        rules: [
            // Rule to handle JavaScript and JSX files (including node_modules)
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules\/(?!react-native-markdown-display)/, // Only transpile react-native-markdown-display from node_modules
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: [
                            "@babel/preset-env", // Transpiles ES6+ to ES5
                            "@babel/preset-react", // Handles JSX
                            "@babel/preset-typescript", // For TypeScript files, if applicable
                        ],
                        plugins: ["@babel/plugin-transform-runtime"], // Optimizes Babel helpers
                    },
                },
            },
            // Rule to handle images (png, jpg, gif)
            {
                test: /\.(png|jpe?g|gif)$/i,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "[path][name].[ext]",
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
            "react-native$": "react-native-web", // Ensures React Native components are resolved to web equivalents
            // Mock Platform module for web usage
            "react-native/Libraries/Utilities/Platform": path.resolve(__dirname, "src/platform-web.js"),
            'react-native-webview': 'react-native-web-webview'
        },
        extensions: [".web.js", ".js", ".json", ".jsx", ".ts", ".tsx"], // Support for JSX and TypeScript files
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./public/index.html", // Webpack HTML template
        }),
    ],
    devServer: {
        static: {
            directory: path.join(__dirname, "public"),
        },
        port: 8080, // Port for dev server
    },
};
