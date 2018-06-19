let brain = require('brain.js');
let fs = require('fs');

let net = new brain.recurrent.LSTM();

let questionNet = new brain.recurrent.LSTM();
let helpNet = new brain.recurrent.LSTM();

let trainNetwork = (network, trainFile, outFile, iterations) => {
    fs.readFile(trainFile, (err, buffer) => {
        // check if the file is readable
        if (err) {
            console.log(
                `An error occured while parsing neural network test data file ${file}: ${err}`,
            );
        } else {
            console.log(`Training neural network ${trainFile}...`);

            // train the current neural network
            network.train(JSON.parse(buffer), {
                iterations: iterations,
            });

            // save the trained data
            fs.writeFile(outFile, JSON.stringify(network.toJSON()), err => {
                // do something with the error?
            });
        }
    });
};

let main = () => {
    // train the neural networks
    trainNetwork(questionNet, 'train/question_network.json', 'nn/question_network.json', 2000);
    trainNetwork(helpNet, 'train/help_network.json', 'nn/help_network.json', 2000);
};

// start the application
main();
