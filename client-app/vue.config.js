//TODO: on server change here
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: './',
  transpileDependencies: true,
  devServer: {
    host: 'localhost',
    port: 8080,
  }
})
