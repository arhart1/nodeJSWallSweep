////### WallSweep ###
//COMP-4312
//Austin Hart - Rachel Perry - Vishnu Nair - Alex Petkova
//A web-based program that searches through the Reddit subreddit page 'Wallstreet Bets' and parses through posts talking about stocks,
//then gives them a score based on how positive the post is percieved. You can access the stock data through the website, hosted through
//an AWS EC2 instance.

'use strict';

//Setup web server variables
const express = require('express');
const { disconnect } = require('process');
const app = express()
const port = process.env.port || 3000;
const path = require('path');
const router = express.Router();

const axios = require('axios');

//Setup Reddit API connection
const snoowrap = require('snoowrap');
const vader = require('vader-sentiment');

const calculate = () => {
    const r = new snoowrap({
    userAgent: 'Nearby_Ad_7159',
    clientId: 'WR_qQrJlijkQ9L1f1PiBEg',
    clientSecret: 'djb1S6cc-ENjkCYffe6_b3lBAeEeqQ',
    refreshToken: '656076709479-Og_YQc8dcnpLqGT9CQ61ScmHr8R5tw'
    });

    //Load stocks from json file
    var data = require("./stocks_list.json");
    const { keyBy, indexOf } = require('lodash');
    const { post } = require('request');

    //Setup framework for how posts will be saved
    var posts_dict = {"Title": [], "Post Text": [],
                "ID": [], "Score": [],
                "Total Comments": [], "Post URL": []
                };

    var locate_dict = {"Title": [], "Post URL":[], "Stock":[], "Score":[], "ID":[], "Post Text":[]};

    var stocksUsed = [];
    var counter = 0;

    const postAmount = {limit: 1000};
    

    return new Promise((resolve, reject) => {
        try {
            //Pull the top 1000 posts
            r.getSubreddit("wallstreetbets").getHot(postAmount).then(posts => {
                //For every post add it to a dictionary called posts_dict
                posts.forEach(post => {
                    posts_dict["Title"].push(post.title);
                    posts_dict["Post Text"].push(post.selftext);
                    posts_dict["ID"].push(post.id);
                    posts_dict["Score"].push(post.score);
                    posts_dict["Total Comments"].push(post.num_comments);
                    posts_dict["Post URL"].push(post.url);

                    //Read through stocks from data file
                    data.forEach(stock => {
                        counter = counter + 1;
                        var stk = stock['stock'];
                        var full = stock['full'];

                        //Check if post title or selftext contains the stock
                        if (((post.title.includes(' ' + stk + ' ')) || (post.title.includes('$' + stk)) || (post.title.includes(stk + ' ')) || (post.selftext.includes(' ' + stk + ' ')) || (post.selftext.includes('$' + stk)) || (post.selftext.includes(stk + ' '))
                            || post.title.includes(full) || post.selftext.includes(full)) && !locate_dict.ID.includes(post.id)){
                            locate_dict["Title"].push(post.title);
                            locate_dict["Post URL"].push(post.url);
                            locate_dict["Stock"].push(stk);
                            locate_dict["Score"].push(0);
                            locate_dict["ID"].push(post.id);
                            locate_dict['Post Text'].push(post.selftext);

                            //Add to the list of used stocks if its not already in it
                            if (!stocksUsed.includes(stk)){
                                stocksUsed.push(stk);
                            }
                        }
                    });
                });
            }).then(() => {  
                var sentimentArr = [];
                var cnt = 0;

                //Read through posts and determine how positive they are from -1 to 1
                locate_dict.Title.forEach(row =>{
                    sentimentArr.push(vader.SentimentIntensityAnalyzer.polarity_scores(row));
                    locate_dict.Score[cnt] = sentimentArr.at(cnt)['compound'];
                    cnt++;
                });

                const sorted = [];

                //Place the posts into a display array and sorted array
                for (let i = 0; i < locate_dict.Title.length; i++){
                    sorted.push({'Title': locate_dict.Title[i], 'Score': locate_dict.Score[i], 'Stock': locate_dict.Stock[i], 'Text': locate_dict['Post Text'][i]});
                }

                //Sort the array by score from low-high
                sorted.sort((a,b) => a.Score - b.Score);

                const allTitles = [];
                const allScores = [];
                const allStocks = [];
                const allText = [];

                //Adjust the array to make it easy to send to the web page
                for (let i = 0; i <sorted.length; i++){
                    allTitles.push(sorted[i].Title);
                    allScores.push(sorted[i].Score);
                    allStocks.push(sorted[i].Stock);
                    allText.push(sorted[i].Text);
                }

                var stockScores = [];
                ////Calculate stocks and their scores
                //Make new dict for Stocks and their Scores
                for(let i = 0; i < stocksUsed.length; i++){
                    stockScores.push({'Stock': stocksUsed[i], 'Score': 0, 'Count': 0});
                }

                //Add all scores from posts
                for(let i = 0; i <stockScores.length; i++){
                    sorted.forEach(post =>{
                        if(post.Stock == stockScores[i].Stock){
                            //Add the post score to corresponding Stock and increase count by 1
                            stockScores[i].Score += post.Score;
                            stockScores[i].Count += 1;
                        }
                    })
                }  

                //Calculate average scores
                for(let i = 0; i<stockScores.length;i++){
                    stockScores[i].Score =(stockScores[i].Score / stockScores[i].Count).toFixed(4);
                }

                //Sort the stocks by their avg scores
                stockScores.sort((a,b) => a.Score - b.Score);
                resolve([stockScores, sorted]);
            });
        } catch (err) {
            reject(err);
        }
    });
}

////Webpage handling
//Set web as pug, pull from /views directory
app.set("view engine", "pug");
app.set("views", path.join(__dirname, "views"));
app.use(express.static('views'));

//Send two webpages and their variables, sweep and index
router.get('/', (req, res) =>{ 
    res.render("home");
});
router.get('/search', async (req, res) =>{
    const cal = await calculate();
    console.log(cal);
    res.render("search", {Sorted: cal[1], name: 'Austin', stocks: cal[0]});
});
app.use('/', router);
//Notify server of successful connection
app.listen(port, () => {
    console.log(`WallSweep app listening on port ${port}`)
});






