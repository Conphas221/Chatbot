let brain = require('brain.js');
let fs = require('fs');
let keywords = require('./keywords');

let questionNet = new brain.recurrent.LSTM();
let helpNet = new brain.recurrent.LSTM();

// parses the trained data for the neural network
let parseNetwork = (network, file) => {
    let buffer = fs.readFileSync(file);

    if (buffer) {
        // file is readable, parse contents!
        let data = JSON.parse(buffer);

        // parse neural network data
        network.fromJSON(data);
    }
};

let express = require('express');
let bodyParser = require('body-parser');

// Finds keywords in a statement, finds if a statement is a question and if the user needs help
let handleStatement = statement => {
    let response = {};

    statement = statement.toLowerCase();

    response.keywords = keywords.find(statement);
    response.needsHelp = helpNet.run(statement) == 'True' ? true : false;
    response.isQuestion = questionNet.run(statement) == 'Question' ? true : false;

    // testing purposes
    console.log(response);

    return response;
};

let main = () => {
    // parse neural networks
    parseNetwork(questionNet, 'nn/question_network.json');
    parseNetwork(helpNet, 'nn/help_network.json');

    // handleStatement('I love playing with python libraries');
    // handleStatement('Do you love me?');

    // HTTP API
    let app = express();
    app.use(bodyParser.json());
    app.post('/analyse', (req, res) => {
        try {
            let sentence = req.body.data;

            // handle statement
            let response = handleStatement(sentence);

            // send response
            res.send(response);
        } catch (err) {
            res.sendStatus(400);
            console.log(err);
        }
    });
    app.listen(5000, () => console.log('HTTP API running on port 5000'));
};

// start the application
main();
