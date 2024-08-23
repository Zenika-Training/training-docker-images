module.exports = {
  devServer: {
    disableHostCheck: true,
    proxy: "http://127.0.0.1:5000"
  },
  publicPath: '/app/'
}
