var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser');

router.use(bodyParser.urlencoded({extended:true}));
router.use(bodyParser.json());

var khmerload_items = require('./newsItem').model('khmerload');
var post_items = require('./newsItem').model('posts');

// RETURNS ALL THE USERS IN THE DATABASE
router.get('/api', function (req, res) {
    console.log(req.query);
        post_items.find({magazine:req.query.magazine,category:req.query.category},(err,docs)=>{
        if(err) return res.status(500).send("problem");
        if(!docs) return res.status(404).send("no news found");
        res.status(200).send(docs);
    })
});

// router.get('/api/:magazine/:category',(req,res)=>{
//     post_items.find({magazine:req.params.magazine,category:req.params.category},(err,docs)=>{
//         if(err) return res.status(500).send("problem");
//         if(!docs) return res.status(404).send("no news found");
//         res.status(200).send(docs);
//     })
// })

// router.get('/api/:magazine',(req,res)=>{
//     post_items.find({magazine:req.params.magazine},(err,docs)=>{
//         if(err) return res.status(500).send("problem");
//         if(!docs) return res.status(404).send("no news found");
//         res.status(200).send(docs);
//     })
// })

// router.get('/api/:category',(req,res)=>{
//     post_items.find({category:req.params.category},(err,docs)=>{
//         if(err) return res.status(500).send("problem");
//         if(!docs) return res.status(404).send("no news found");
//         res.status(200).send(docs);
//     })
// })

module.exports = router;
