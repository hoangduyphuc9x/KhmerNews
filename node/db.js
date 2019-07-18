var mongoose = require('mongoose');

MONGODB_HOST = "localhost";
MONGODB_PORT = 27017;
MONGODB_DATABASE = "OFFICIAL_DATABASE";

mongoose.connect(`mongodb://${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DATABASE}`,{useNewUrlParser:true});
