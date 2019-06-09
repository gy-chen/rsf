import BFS from './BFS';
import Graph from './Graph';

class DistanceCalculator {

    private graph: Graph;

    constructor(graph: Graph) {
        this.graph = graph;
    }

    distance(targets: number[], sources: number[]) {
        const sourcesBFS = new BFS(this.graph, ...sources);
        const targetBFS = new BFS(this.graph, ...targets);
        let shortestVertexDistance = Infinity;
        for (let v = 0; v < this.graph.getVertexNumber(); v++) {
            if (sourcesBFS.isConnected(v) && targetBFS.isConnected(v)) {
                const distance = sourcesBFS.distanceTo(v) + targetBFS.distanceTo(v);
                if (distance < shortestVertexDistance) {
                    shortestVertexDistance = distance;
                }
            }
        }
        return shortestVertexDistance;
    }
}

export default DistanceCalculator;