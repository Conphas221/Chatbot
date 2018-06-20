let fs = require('fs');

class Keywords {
    constructor() {
        this.keywords = [];
        this.parse();
    }

    parse() {
        // parses the relevant keywords from a json file
        if (fs.existsSync('nn/keywords.json')) {
            let data = fs.readFileSync('nn/keywords.json');
            if (data) {
                this.keywords = JSON.parse(data);
            } else {
                console.log(`An error occured while parsing keywords: ${err}`);
            }
        }
    }

    // finds all keywords in a sentence
    find(statement) {
        // splits the sentence into tokens
        let tokens = statement.toLowerCase().split(' ');
        let foundKeywords = [];

        // searches all tokens in the parsed keyword array
        for (let i = 0; i < tokens.length; i++) {
            if (this.keywords.indexOf(tokens[i]) !== -1) {
                foundKeywords.push(tokens[i]);
            }
        }

        // returns found keywords
        return foundKeywords;
    }
}

module.exports = new Keywords();
