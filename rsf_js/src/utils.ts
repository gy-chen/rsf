export const sigmoid = (x: number): number => {
    return 1. / (1 + Math.pow(Math.E, -x));
}

export const softmax = (x: number[]): number[] => {
    let denom = 0;
    for (const j of x) {
        denom += Math.pow(Math.E, j);
    }
    const result: number[] = [];
    for (const n of x) {
        result.push(Math.pow(Math.E, n) / denom);
    }
    return result;
}

export const getDefaultEncodedWords = () => {
    const fs = require('fs');
    const path = require('path');
    const encodedWordsPath = path.resolve(__dirname, 'encodedWords.json');
    const encodedWordsContent = fs.readFileSync(encodedWordsPath);
    return JSON.parse(encodedWordsContent.toString());
};