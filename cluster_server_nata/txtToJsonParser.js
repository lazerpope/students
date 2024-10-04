const fs = require("fs");
const md5 = require('md5');
const articlesFolder = './archive_storage_for_clustering/';
module.exports.parse = async function () {
    console.log("Begin Parsing txt to JSON");
    let files = []
    fs.readdirSync(articlesFolder).forEach(file => {
        let data = fs.readFileSync('./archive_storage_for_clustering/' + file, "utf8");
        files.push(data)
    });
    let parsedArticles = []
    files.forEach(file => {
        let _id = md5(file)
        let fileRows = file.split('\n');
        let title = fileRows[0]
        let mark = fileRows[4]
        let article = ""
        for (let i = 6; i < fileRows.length; i++) {
            article += fileRows[i]
        }
        parsedArticles.push({
            _id,
            title,
            mark,
            article
        })
    })
    let symbols = ["\n", '\t', '\r']
    let articles = parsedArticles
    for (let i = 0; i < articles.length; i++) {
        //удаление лишних символов
        symbols.forEach(mark => {
            while (articles[i].mark.indexOf(mark) != -1) {
                articles[i].mark = articles[i].mark.replace(mark, '')
            }
            while (articles[i].title.indexOf(mark) != -1) {
                articles[i].title = articles[i].title.replace(mark, '')
            }
            while (articles[i].article.indexOf(mark) != -1) {
                articles[i].article = articles[i].article.replace(mark, '')
            }

        })
        articles[i].mark = articles[i].mark.trim()
        articles[i].title = articles[i].title.trim()
        articles[i].article = articles[i].article.trim()
    }

    writeToJson(articles)
    console.log('DONE Parsing txt to JSON');
}

function writeToJson(data) {
    fs.writeFileSync("./articles.json", JSON.stringify(data), () => { });
}

function readArchive() {
    let data = fs.readFileSync("./articles.json", "utf8");
    return JSON.parse(data)
}