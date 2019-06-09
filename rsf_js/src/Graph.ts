
class Graph {

    private bags: { [key: number]: number[] };
    private vertexNumber: number;

    constructor(vertexNumber: number) {
        this.bags = {};
        this.vertexNumber = vertexNumber;
    }

    connect(v: number, w: number) {
        this._connect(v, w);
        // XXX seems make this unigraph will cause problem in BFS (too much connections?)
        // this._connect(w, v);
    }

    adj(v: number): number[] {
        const edges = this.bags[v] || [];
        return edges;
    }

    getVertexNumber(): number {
        return this.vertexNumber;
    }

    private _connect(v: number, w: number) {
        const edges = this.bags[v] || [];
        edges.push(w);
        this.bags[v] = edges;
    }
}

export default Graph;