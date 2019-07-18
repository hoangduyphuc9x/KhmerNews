var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');

router.use(bodyParser.urlencoded({extended:true}));
router.use(bodyParser.json());

var khmerload_items = require('./newsItem').model('khmerload');

// RETURNS ALL THE USERS IN THE DATABASE
router.get('/', function (req, res) {
    khmerload_items.find({}, function (err, users) {
        if (err) return res.status(500).send("There was a problem finding the users.");
        res.status(200).send(users);
    });
});

router.get('/:category',(req,res)=>{
    // khmerload_items.findById(req.params.id, function (err, user) {
    //     if (err) return res.status(500).send("There was a problem finding the user.");
    //     if (!user) return res.status(404).send("No user found.");
    //     res.status(200).send(user);
    // });
    khmerload_items.find({category:req.params.category},(err,docs)=>{
        if(err) return res.status(500).send("PROBLEM!");
        if(!docs) return res.status(404).send("no newsItem found");
        res.status(200).send(docs);
    })
})
module.exports = router;
