var express = require('express');
var path = require('path');
var serveStatic = require('serve-static');

app = express();
app.use(serveStatic(__dirname + "/display/police-view/dist"));
app.use(serveStatic(__dirname+'/display/civilian-mobile-app'));

app.get ('/police', function(req,res) {
  res.sendFile(__dirname+'/display/police-view/dist/index.html');
});

app.get ('/civilian', function(req,res) {
  res.sendFile(__dirname+'/display/civilian-mobile-app/index.html');
});

var port = process.env.PORT || 5000;
app.listen(port);
console.log(port);
