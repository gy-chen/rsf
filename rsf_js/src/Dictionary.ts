interface Word {
    id: number;
    word: string;
    related: number[];
}

class Dictionary {

    private words: { [key: string]: Word }

    constructor(words: Word[]) {
        this.words = this.buildWordMappings(words);
    }

    getWords(): string[] {
        return Object.keys(this.words);
    }

    getWordId(word: string): number {
        return this.words[word].id;
    }

    getRelatedWordIds(word: string): number[] {
        return this.words[word].related;
    }

    count(): number {
        return this.getWords().length;
    }

    private buildWordMappings(words: Word[]): { [key: string]: Word } {
        const result: { [key: string]: Word } = {};
        for (const word of words) {
            result[word['word']] = word;
        }
        return result;
    }
}

export default Dictionary; 