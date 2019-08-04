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
    if(req.query.article != null){
        post_items.
            find({_id:req.query.article}).
            exec((err,result)=>{
                if(err) return res.status(500).send("problem");
                if(!result) return res.status(404).send("no news");
                res.status(200).send(result);
            })
    }
    else{
        if(req.query.page == null){
            req.query.page = 1
        }
        item_per_page = 20;
            post_items.
            find({category:req.query.category}).
            sort({date:-1}).
            skip(item_per_page*(req.query.page-1)).
            limit(item_per_page).
            exec((err,result)=>{
                if(err) return res.status(500).send("problem");
                if(!result) return res.status(404).send("no news");
                res.status(200).send(result)
            })
        }
    }
);

router.get('/api/home',(req,res)=>{
    item_per_page = 20
    console.log(req.query);
    if(req.query.page == null){
        req.query.page = 1
    }
    post_items.find({})
        .sort({date:-1})
        .skip(item_per_page*(req.query.page-1))
        .limit(item_per_page)
        .exec((err,result)=>{
            if(err) return res.status(500).send("problem");
            if(!result) return res.status(404).send("no news");
            res.status(200).send(result)
        })
})

// router.get('/api/id',(req,res)=>{
//     item_per_page = 20
//     console.log(req.query);
//     // if(req.query.id == null){
//     //     req.query.id = 1
//     // }
//     post_items.find({_id})
//         .sort({date:-1})
//         .skip(item_per_page*(req.query.page-1))
//         .limit(item_per_page)
//         .exec((err,result)=>{
//             if(err) return res.status(500).send("problem");
//             if(!result) return res.status(404).send("no news");
//             res.status(200).send(result)
//         })
// })

module.exports = router;
