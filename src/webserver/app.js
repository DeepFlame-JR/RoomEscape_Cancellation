console.log('Server-side code running');

const express = require("express");
var path = require("path");

const app = express();
const port = 3001;

app.use(express.static(__dirname + '/public'));

app.listen(port, () => {
  console.log("Listening on", port)
});

app.get('/', (req, res) => {
  res.sendFile('public/index.html');
});

// module.exports = app;
