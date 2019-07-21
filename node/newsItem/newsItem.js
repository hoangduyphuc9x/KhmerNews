var mongoose = require('mongoose');

Khmerload_collection = "Khmerload";
posts_collection = "posts";


var NewsSchema = new mongoose.Schema({
  magazine:String,
  title:String,
  date:String,
  category:String,
  url:String
});

mongoose.model('khmerload',NewsSchema,Khmerload_collection);
mongoose.model('posts',NewsSchema,posts_collection);


module.exports = mongoose.model('khmerload');
module.exports = mongoose.model('posts');