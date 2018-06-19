let fs = require('fs');

class Keywords {
    constructor() {
        this.keywords = [];
        this.parse();
    }

    parse() {
        if (fs.existsSync('nn/keywords.json')) {
            let data = fs.readFileSync('nn/keywords.json');
            if (data) {
                this.keywords = JSON.parse(data);
            } else {
                console.log(`An error occured while parsing keywords: ${err}`);
            }
        }
    }

    find(statement) {
        let tokens = statement.toLowerCase().split(' ');
        let foundKeywords = [];

        for (let i = 0; i < tokens.length; i++) {
            if (this.keywords.indexOf(tokens[i]) !== -1) {
                foundKeywords.push(tokens[i]);
            }
        }

        return foundKeywords;
    }
}

module.exports = new Keywords();
