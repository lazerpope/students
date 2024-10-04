const fs = require("fs");
const MongoClient = require('mongodb').MongoClient;
const ObjectId = require('mongodb').ObjectID;
const url = 'mongodb://localhost:27017';
const dbName = 'articlesDB';
const collectionName = 'articles'

const client = new MongoClient(url, { useUnifiedTopology: true });
try {
    client.connect();
    console.log("DB connected successfully.");
}
catch (error) {
    console.error("DB not connected!");
}
let articlesPath = "./articles.json"
const collection = client.db(dbName).collection(collectionName);

module.exports.writeToDB = async function () {
    console.log("Begin Writing to DB");
   
    await collection.deleteMany({});
    console.log('DONE Wiping DB');


    let data = readJson(articlesPath)
    data.forEach(item => {
        collection.insertOne(item)
    });
    console.log('DONE Writing to DB');
}

module.exports.ReadDB = async function () {
    console.log("Begin Reading DB");
    let response = await collection.find({}).toArray()
    console.log('DONE  Reading DB');
    return response;
}

function readJson(path) {
    let data = fs.readFileSync(path, "utf8");
    return JSON.parse(data)
}