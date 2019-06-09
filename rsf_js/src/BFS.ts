import Graph from './Graph';

class BFS {

    private graph: Graph;
    private marked: { [key: number]: boolean };
    private edgeTo: { [key: number]: number };
    private distTo: { [key: number]: number };

    constructor(graph: Graph, ...v: number[]) {
        this.graph = graph;
        this.marked = {};
        this.edgeTo = {};
        this.distTo = {};
        this.bfs(...v);
    }

    private bfs(...v: number[]) {
        const q: number[] = [...v];
        for (const v of q) {
            this.distTo[v] = 0;
            this.marked[v] = true;
        }

        let earlyStop = 0;
        while (q.length !== 0 && earlyStop < 2000) {
            earlyStop += 1;
            const v = q.shift();
            if (v === undefined) {
                continue;
            }
            for (const w of this.graph.adj(v)) {
                if (!this.marked[w]) {
                    this.marked[w] = true;
                    this.edgeTo[w] = v;
                    this.distTo[w] = this.distTo[v] + 1;
                    q.push(w);
                }
            }
        }
    }

    isConnected(w: number): boolean {
        return this.marked[w];
    }

    distanceTo(w: number): number {
        if (!this.isConnected(w)) {
            return Infinity;
        }
        return this.distTo[w];
    }
}

export default BFS;