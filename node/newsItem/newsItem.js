var mongoose = require('mongoose');

Khmerload_collection = "Khmerload";


var NewsSchema = new mongoose.Schema({
  magazine:String,
  title:String,
  date:String,
  category:String,
  url:String
});

mongoose.model('khmerload',NewsSchema,Khmerload_collection);

module.exports = mongoose.model('khmerload');