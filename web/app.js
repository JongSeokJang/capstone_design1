const express = require('express');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const app = express();
const exec = require('child_process').exec;
const pug = require('pug');
const fs = require('fs');
const Promise = require('bluebird');
const mysql = require('mysql');
const lexrank = require('lexrank');

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '1q2w3e4r',
  database : 'newsData'
});

connection.connect();


//set view engine
app.set('view engine', 'pug');
app.set('views','./views');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

const execAsync = (cmd) => {
  return new Promise((resolve, reject) => {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve(stdout);
      }
    });
  });
};

app.get('/', (req, res) => {
    res.render('main');
})
app.get('/index', (req, res) => {
  res.redirect('/news');
});
//keyword engine
app.get('/keyword', (req, res)=>{
  res.render('keyword');
})

app.post('/keyword', (req, res, next) => {
  const text = req.body.content;
  const filename = crypto.randomBytes(16).toString('hex');

  fs.writeFile(`/tmp/${filename}`, text, (err) => {
    if (err) {
      next(err);
    } else {
      Promise.all([
        execAsync(`python3 keyword.py /tmp/${filename}`),
      ])
        .spread((keywords) => {
          fs.unlink(`/tmp/${filename}`, (err) => {
            if (err) {
              next(err);
            } else {
              keywords = JSON.parse(keywords);
              res.render('keyword', {
                'keywords': keywords
              });
            }
          });
        })
        .catch((err) => {
          console.log(err);
          res.end();
        });
    }
  });
});
app.get('/englishSentiment', (req, res)=>{
  res.render('englishSentiment');
})
app.post('/englishSentiment', (req, res, next) => {
  const text = req.body.content;
  const filename = crypto.randomBytes(16).toString('hex');

  fs.writeFile(`/tmp/${filename}`, text, (err) => {
    if (err) {
      next(err);
    } else {
      Promise.all([
        execAsync(`python3 englishSentiment.py /tmp/${filename}`),
      ])
        .spread((result) => {
          fs.unlink(`/tmp/${filename}`, (err) => {
            if (err) {
              next(err);
            } else {
              result = result.split('\n');
              var posNeg = result[0];
              var polarity = result[1];
              res.render('englishSentiment', {
                'polarity': polarity, 'posNeg':posNeg
              });
            }
          });
        })
        .catch((err) => {
          console.log(err);
          res.end();
        });
    }
  });
});

app.get('/summarize', (req, res) => {
  res.redirect('http://ai.sgcslab.com');
})
app.get('/sentiment', (req, res) => {
  res.render('sentiment');
})



app.post('/sentiment', (req, res, next) => {
  const text = req.body.content;
  const filename = crypto.randomBytes(16).toString('hex');

  fs.writeFile(`/tmp/${filename}`, text, (err) => {
    if (err) {
      next(err);
    } else {
      Promise.all([
        execAsync(`python3 sentiment.py /tmp/${filename}`),
      ])
        .spread((result) => {
          fs.unlink(`/tmp/${filename}`, (err) => {
            if (err) {
              next(err);
            } else {
              result = result.split('\n');
              var posNeg = result[0];
              var polarity = result[1];
              res.render('sentiment', {
                'polarity': polarity, 'posNeg':posNeg
              });
            }
          });
        })
        .catch((err) => {
          console.log(err);
          res.end();
        });
    }
  });
});



app.get('/deeplearning', (req, res)=> {
    res.render('deeplearning');
})
app.post('/deeplearning', (req, res, next) => {
  const text = req.body.content;
  const filename = crypto.randomBytes(16).toString('hex');

  fs.writeFile(`/tmp/${filename}`, text, (err) => {
    if (err) {
      next(err);
    } else {
      Promise.all([
        execAsync(`python3 deeplearning.py /tmp/${filename}`),
      ])
        .spread((keywords) => {
          fs.unlink(`/tmp/${filename}`, (err) => {
            if (err) {
              next(err);
            } else {
              res.render('deeplearning', {
                'keywords': keywords
              });
            }
          });
        })
        .catch((err) => {
          console.log(err);
          res.end();
        });
    }
  });
});

app.get('/news', (req, res) => {
  var querys = req.query.query;
  var mid = req.query.mid
  if (querys && !mid){
    var queryList = querys.split(' ');
    
    
    var sql = "SELECT * from mediaNews WHERE ";
    for(var i = 0; i<queryList.length -1; i++){
      sql = sql + "CONENT LIKE '%" + queryList[i] + "%'" + " AND ";
    }
    sql = sql + "CONTENT like '%" + queryList.pop() + "%'";
    sql = sql + " ORDER BY id DESC limit 9";
    
    
    connection.query(sql, (err, rows, fields) => {
      if(err) {
        res.render('news');
      }
      else if(!rows){
        res.render('news');
      }
      else{
      //console.log(rows);
      // console.log(rows.length);
      mid = rows[rows.length-1];
      mid = mid['id'];
      res.render('news', {'rows' : rows, 'mid' : mid, 'querys': querys});
      }
    });
  }
  else if(querys && mid){
    var queryList = querys.split(' ');
    
    
    var sql = "SELECT * from mediaNews WHERE ";
    for(var i = 0; i<queryList.length -1; i++){
      sql = sql + "CONENT LIKE '%" + queryList[i] + "%'" + " AND ";
    }
    sql = sql + "CONTENT like '%" + queryList.pop() + "%'" + " AND id < "+ mid.toString();
    sql = sql + " ORDER BY id DESC limit 9";
    connection.query(sql, (err, rows, fields) => {
      if(err) {
        res.render('news');
      }
      else if(!rows){
        res.render('news');
      }
      else{
      //console.log(rows);
      // console.log(rows.length);
      mid = rows[rows.length-1];
      mid = mid['id'];
      res.render('news', {'rows' : rows, 'mid' : mid, 'querys': querys});
      }
    });
  }
  else{
    console.log('no querys!');
    res.render('news');
  }
});




app.get('/collocation', (req, res) => {
    res.render('collocation');
})
app.get('/getWords', (req, res) => {
    word = req.query.word;
    exec(`python3 word2vecRun.py "${word}"`, (err, stdout, stderr)=>{
        if (err){
            words = ""
       }
        else{
            words = stdout;
            words = JSON.parse(words);
            res.render('collocation', {'words':words});
        }
    })

})


app.get('/admin', (req, res) => {
  var sql = "SELECT mediaName,COUNT(*) as count FROM mediaNews GROUP BY mediaName ORDER BY count DESC";
  connection.query(sql, (err, rows, fields) => {
    if(err) throw err;

    res.render('admin', {'rows' : rows});
  })
})

app.get('/englishSum', (req, res) => {
  res.render('englishSum');
});

app.post('/englishSUm', (req, res => {
  var content = req.body.content;
  lexrank.summarize(content, 4, (err, toplines, text) => {
    var summarized = text;
    res.render('enlighSum', {'text':text});
  })
}))



app.listen(80, ()=>{
    console.log('server running on port 3000!!');
})
