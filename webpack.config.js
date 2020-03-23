var path = require('path')
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    entry: './src/js/index.js',
    output: {
        path: path.resolve(__dirname, 'static/bundles'),
        filename: "[name]-[hash].js",
    },
    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' }),

    ],
      module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
        
      },
      {
          test:/\.css$/,
          use:[
           'style-loader',
           'css-loader',
          ]
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }
}
// also multiple entry point and output point