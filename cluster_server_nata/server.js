const express = require('express');
const app = express();
const txtParse = require('./txtToJsonParser')
const mongoDB = require('./mongoDBmodule')
const baggenerator = require('./bagGenerator')
const cluster = require('./clusterGenerator')
const pdf = require('./pdfWriter')
const fs = require("fs");

app.use(express.static(__dirname + '/public')); // для статических страниц
app.use(express.json()); // разрешаем обмен в формате JSON
app.use(express.urlencoded({ extended: false })); // обработка AJAX-запроса
var cors = require('cors');
app.use(cors());

let bag = []

async function startArticlesPreparation() {
  console.log('Begin PREPARATON');
  await txtParse.parse()
  await mongoDB.writeToDB()
  bag = await baggenerator.generate()
  cluster.generate()
  pdf.generate()
  console.log('DONE PREPARATON');
}

startArticlesPreparation()


app.get('/test', async (req, res) => {
  res.send({ response: "res" });



});



app.get('/getarticles', async (req, res) => {
  console.log(`Request type ${req.query.type} at ${new Date}`);
  let articles = readJson('./articles.json')
  let clusters = readJson('./clusters.json')
  let response
  switch (req.query.type) {
    case 'kmeans':
      response = clusters[0]
      for (let i = 0; i < response.length; i++) {
        for (let j = 0; j < response[i].length; j++) {
          articles.forEach(article => {
            if (article._id == response[i][j]) {
              response[i][j] = article
            }
          });
        }
      }

      let textToPrint=""
      let pdfDoc = new PDFDocument;

      pdfDoc.pipe(fs.createWriteStream('K-means.pdf'));
      response = clusters[0]
      for (let i = 0; i < response.length; i++) {
        for (let j = 0; j < response[i].length; j++) {
          articles.forEach(article => {
            if (article._id == response[i][j]) {
              response[i][j] = article
            }
          });
        }
      }

      res.send({ response: { kmeans: response } });
      break;
    case 'mbk':
      response = clusters[1]
      for (let i = 0; i < response.length; i++) {
        for (let j = 0; j < response[i].length; j++) {
          articles.forEach(article => {
            if (article._id == response[i][j]) {
              response[i][j] = article
            }
          });
        }
      }
      res.send({ response: { mbk: response } });
      break;
    case 'agglo':
      response = clusters[2]
      for (let i = 0; i < response.length; i++) {
        for (let j = 0; j < response[i].length; j++) {
          articles.forEach(article => {
            if (article._id == response[i][j]) {
              response[i][j] = article
            }
          });
        }
      }
      res.send({ response: { agglo: response } });
      break;
    case 'all_methods':
      let responseAll = []
      for (let m = 0; m < 3; m++) {
        response = clusters[m]
        for (let i = 0; i < response.length; i++) {
          for (let j = 0; j < response[i].length; j++) {
            articles.forEach(article => {
              if (article._id == response[i][j]) {
                response[i][j] = article
              }
            });
          }
        }
        responseAll.push(response)
      }
      res.send({
        response: {
          kmeans: responseAll[0],
          mbk: responseAll[1],
          agglo: responseAll[2],
        }
      });
      break;

    default:
      res.send({ response: "err" })
  }
  console.log(`Response type ${req.query.type} at ${new Date}`);
});





app.listen(3000, () => {
  console.log('App listening on port: 3000!');
});

function readJson(path) {
  let data = fs.readFileSync(path, "utf8");
  return JSON.parse(data)
}