const express = require('express');
const app = express();
const request = require('request');
const {exec} = require('child_process');


app.get('/blogapi', (req, res) => {
  var searchQuery = req.query.query;
  exec(`python3 blog.py ${searchQuery}`, (err, stdout, stderr) => {
    if(err) {
      console.log(err);
      return ;
    }
    var result = stdout;
    console.log(result);
    result = JSON.parse(result);
    res.send(result);
  });
  
});

app.listen(4500, () => {
  console.log("server running on port 4500!");
});
