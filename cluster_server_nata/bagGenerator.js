const fs = require("fs");
const mongoDB = require('./mongoDBmodule');
const porter = require("./stemmerPorter");


module.exports.generate = async function () {
    let articles = await mongoDB.ReadDB()
    articles = trimExcesses(articles)
    articles = stem(articles)
    let data = []
    let ids = []
    for (let i = 0; i < articles.length; i++) {
        data.push(articles[i].stemmed)
        ids.push(articles[i]._id)
    }
    fs.writeFileSync("./preparedArticles.json", JSON.stringify(data), () => { });
    fs.writeFileSync("./preparedIds.json", JSON.stringify(ids), () => { });
}
function stem(articles) {
    for (let i = 0; i < articles.length; i++) {
        articles[i].stemmed = articles[i].article.split(" ")
    }

    for (let i = 0; i < articles.length; i++) {
        let h = 0
        let stemmed = []
        articles[i].stemmed.forEach(word => {
            h += 1
            if (word) {

            }
            try {
                stemmed.push(porter.stem(word))
            } catch (error) {
            }

        });
        articles[i].stemmed = stemmed.join()

    }
    return articles
}

function trimExcesses(articles) {
    let stopWords = readJson('./stopwords.json')
    let excessSymbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '“', '”', '-', '–', '\r', '\.', ',', ':', ';', '?', '!', '...', '—', '"', '(', ')', '/', '№', '$', '%', '*', '&', '`', '~', '#', '@', '+', '»', '«']
    let spaces = ['  ', '   ', '    ', '     ', '      ', '       ']
    let letters = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю']
    for (let i = 0; i < articles.length; i++) {
        articles[i].article = articles[i].article.toLowerCase()
        //удаление лишних символов
        excessSymbols.forEach(mark => {
            while (articles[i].article.indexOf(mark) != -1) {
                articles[i].article = articles[i].article.replace(mark, ' ')
            }
        })
        //удаление стоп - слов
        stopWords.forEach(mark => {
            while (articles[i].article.indexOf(" " + mark + " ") != -1) {
                articles[i].article = articles[i].article.replace(" " + mark + " ", ' ')
            }
        })
        articles[i].article = articles[i].article.trim()

        letters.forEach(mark => {
            while (articles[i].article.indexOf(" " + mark + " ") != -1) {
                articles[i].article = articles[i].article.replace(" " + mark + " ", ' ')
            }
        })
        articles[i].article = articles[i].article.trim()
        spaces.forEach(mark => {
            while (articles[i].article.indexOf(mark) != -1) {
                articles[i].article = articles[i].article.replace(mark, ' ')
            }
        })

    }  
    return articles
}

function readJson(path) {
    let data = fs.readFileSync(path, "utf8");
    return JSON.parse(data)
}
