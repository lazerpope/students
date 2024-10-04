
const PDFDocument = require('pdfkit');
const fs = require('fs');
module.exports.generate = async function (data) {
    let articles = readJson('./articles.json')
    let clusters = readJson('./clusters.json')
    let response
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
    let text = ""
    let i = 0
    response.forEach(group => {
        i++
        text = `Кластер ${i}`
        pdfDoc.font('./Times New Roman Regular.ttf').text(text, { underline: true })
        group.forEach(article => {
            text = `    Название: ${article.title} `
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
            text = `    Тема: ${article.mark}`
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
        });
        pdfDoc.font('./Times New Roman Regular.ttf').text(' ')
    });
    pdfDoc.end();


    pdfDoc = new PDFDocument;
    pdfDoc.pipe(fs.createWriteStream('Mini batch K-means.pdf'));
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
    text = ""
    i = 0
    response.forEach(group => {
        i++
        text = `Кластер ${i}`
        pdfDoc.font('./Times New Roman Regular.ttf').text(text, { underline: true })
        group.forEach(article => {
            text = `    Название: ${article.title} `
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
            text = `    Тема: ${article.mark}`
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
        });
        pdfDoc.font('./Times New Roman Regular.ttf').text(' ')
    });
    pdfDoc.end();


    pdfDoc = new PDFDocument;
    pdfDoc.pipe(fs.createWriteStream('Agglomerative clustering.pdf'));
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
    text = ""
    i = 0
    response.forEach(group => {
        i++
        text = `Кластер ${i}`
        pdfDoc.font('./Times New Roman Regular.ttf').text(text, { underline: true })
        group.forEach(article => {
            text = `    Название: ${article.title} `
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
            text = `    Тема: ${article.mark}`
            pdfDoc.font('./Times New Roman Regular.ttf').text(text)
        });
        pdfDoc.font('./Times New Roman Regular.ttf').text(' ')
    });
    pdfDoc.end();


    pdfDoc = new PDFDocument;
    pdfDoc.pipe(fs.createWriteStream('All methods.pdf'));
    for (let m = 0; m < 3; m++) {
        if (m==0) {
            text = `K-means`
        }
        if (m ==1) {
            text = `Mini batch K-means`
        }
        if (m == 2) {
            text = `Agglomerative clustering`
        }
        pdfDoc.font('./Times New Roman Regular.ttf').text(text, { underline: true })

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
        text = ""
        i = 0
        response.forEach(group => {
            i++
            text = `Кластер ${i}`
            pdfDoc.font('./Times New Roman Regular.ttf').text(text, { underline: true })
            group.forEach(article => {
                text = `    Название: ${article.title} `
                pdfDoc.font('./Times New Roman Regular.ttf').text(text)
                text = `    Тема: ${article.mark}`
                pdfDoc.font('./Times New Roman Regular.ttf').text(text)
            });
            pdfDoc.font('./Times New Roman Regular.ttf').text(' ')
        });
        pdfDoc.font('./Times New Roman Regular.ttf').text(' ')
    }
    pdfDoc.end();
}
function readJson(path) {
    let data = fs.readFileSync(path, "utf8");
    return JSON.parse(data)
}