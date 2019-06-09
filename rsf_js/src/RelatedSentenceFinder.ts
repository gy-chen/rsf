import Dictionary from './Dictionary';
import Graph from './Graph';
import DistanceCalculator from './DistanceCalculator';
import { sigmoid, softmax } from './utils';

class RelatedSentenceFinder {

    private dictionary: Dictionary;
    private sentences: string[];
    private sentenceWords: number[][];
    private graph: Graph;
    private distanceCalculator: DistanceCalculator;

    constructor(dictionary: Dictionary, ...sentences: string[]) {
        this.dictionary = dictionary;
        this.sentences = sentences;
        this.sentenceWords = [];
        for (const sentence of sentences) {
            this.sentenceWords.push(this.buildSentenceWords(dictionary, sentence));
        }
        this.graph = this.buildGraph(dictionary);
        this.distanceCalculator = new DistanceCalculator(this.graph);
    }

    addSentence(sentence: string) {
        this.sentences.push(sentence);
        this.sentenceWords.push(this.buildSentenceWords(this.dictionary, sentence));
    }

    searchRelatedSentence(sentence: string): string {
        let distances = [];
        const sentenceIds = this.buildSentenceWords(this.dictionary, sentence);
        if (sentenceIds.length === 0) {
            return this.randomChoose(this.sentences);
        }
        const defaultDistance = this.dictionary.count();
        for (const wordIds of this.sentenceWords) {
            let distance = Math.min(this.distanceCalculator.distance(sentenceIds, wordIds), defaultDistance);
            distances.push(Math.pow(1 - sigmoid(distance - 5), 2));
        }
        distances = softmax(distances);
        const resultIndex = this.randomChooseFromSoftmax(distances);
        return this.sentences[resultIndex];
    }

    private randomChoose(arr: any[]): any {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    private randomChooseFromSoftmax(arr: number[]): number {
        const r = Math.random();
        let acc = 0;
        for (let i = 0; i < arr.length; i++) {
            const p = arr[i];
            acc += p;
            if (r < acc) {
                return i;
            }
        }
        throw new Error("randomChooseFromSoftmax error, input is not applied softmax?")
    }

    private buildSentenceWords(dictionary: Dictionary, sentence: string): number[] {
        const wordIds: number[] = [];
        for (const word of dictionary.getWords()) {
            if (sentence.indexOf(word) !== -1) {
                wordIds.push(dictionary.getWordId(word));
            }
        }
        return wordIds;
    }

    private buildGraph(dictionary: Dictionary): Graph {
        const graph = new Graph(dictionary.count());
        for (const word of dictionary.getWords()) {
            const wordId = dictionary.getWordId(word);
            for (const relatedWordId of dictionary.getRelatedWordIds(word)) {
                graph.connect(wordId, relatedWordId);
            }
        }
        return graph;
    }
}

export default RelatedSentenceFinder;