const path = require('path');

module.exports = {
  presets: ['module:@react-native/babel-preset'],
  "plugins": [
    ["@babel/plugin-transform-class-properties", { "loose": true }],
    ["@babel/plugin-transform-private-methods", { "loose": true }],
    ["@babel/plugin-transform-private-property-in-object", { "loose": true }],
    ['module:react-native-dotenv', {
      path: path.resolve(__dirname, '../config/.env'),// Custom path to .env file
      allowUndefined: false
    }]
  ]
};
