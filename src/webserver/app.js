console.log('Server-side code running');

// require packages
var util= require('util');
const utf8Encoder = new util.TextEncoder();
const utf8Decoder = new util.TextDecoder("utf-8", { ignoreBOM: true });
const express = require("express");
const path = require("path");
const sf = require("sf");
const iniparser = require("iniparser");
const bodyParser = require("body-parser")
var mongoose = require("mongoose");

// connect mongo
var config = iniparser.parseSync(path.join(__dirname, '..', 'config.ini'));
var uri = sf('mongodb://{0}:{1}@{2}:27017/roomdb?authSource=admin',
              config.MONGO.user, config.MONGO.pw, config.MONGO.ip);
mongoose
  .connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Successfully connected to mongodb'))
  .catch(e => console.error(e));
const UserSchema = new mongoose.Schema({
  email: String,
  cafe: String,
  theme: String,
  untilMonth: Number,
}, {collection:'user'});
const User = mongoose.model("User", UserSchema);

// declare app
const app = express();
const port = 3001;
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());

app.listen(port, () => {
  console.log("Listening on", port)
});

app.get('/', (req, res) => {
  res.sendFile('public/index.html');
});

// register
app.post('/register', function(req, res){
  console.log("registered start");
  var checkUser = JSON.parse(JSON.stringify(req.body));
  delete checkUser['untilMonth'];

  User
  .findOne(checkUser)
  .then(output =>{
    if(output){
      User.updateOne(output, {untilMonth: req.body.untilMonth})
          .then(() => console.log("update 완료"));
      return res.status(404).json();
    }

    var user = new User(req.body);
    user.save().then(() => {
      console.log("register 완료")
      return res.status(200).json();
    });
  })
  .catch(err => {
    res.status(500).json();
  });
});

// delete
app.post('/delete', function(req, res){
  console.log("delete start");
  var checkUser = JSON.parse(JSON.stringify(req.body));
  delete checkUser['untilMonth'];

  User
  .findOne(checkUser)
  .then(output =>{
    if(!output)
      return res.status(404).json();

    User.deleteOne(output).then(()=>{
      console.log("Delete 완료")
      res.status(200).json();
    });
  })
  .catch(err => {
    res.status(500).json();
  });
});
