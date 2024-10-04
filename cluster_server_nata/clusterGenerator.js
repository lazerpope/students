const { exec } = require("child_process");


module.exports.generate = async function () {
    console.log('Begin CLUSTER  GENERATION');
    let data = ''
    let req = `python \"${__dirname}\\main.py\"`
    exec(req, async (error, stdout, stderr) => {
        if (error) {
            console.log(`ERROR ${error.message}`);

            return;
        }
        if (stderr) {
            console.log(`ERROR PIC ${stderr.message}`);

            return;
        }
        if (stdout.indexOf('1')!= '-1') {
            console.log('DONE CLUSTER  GENERATION');
        }        
    });   
}