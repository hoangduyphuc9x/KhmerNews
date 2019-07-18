var express = require('express');
var app = express();

var db = require('./db');

var newsItemController = require('./newsItem/newsItemController');

//Gan 1 middleware vao /test, khi chay /test thi chay newsItemController
app.use('/',newsItemController);

module.exports = app;