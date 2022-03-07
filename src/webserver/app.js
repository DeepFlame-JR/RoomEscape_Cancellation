console.log('Server-side code running');

// require packages
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

app.post('/clicked', function(req, res){
  var user = new User(req.body);
  user.save()
      .then(() => console.log("user information is added"))
      .catch((err) => console.log(err));
});
