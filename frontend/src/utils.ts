import {
  Node,
  Edge, Position
} from "reactflow";

let node_counter = 0;
let edge_counter = 0;

const getNodeId = () => `randomnode_${node_counter++}`;
const getEdgeId = () => `randomedge_${edge_counter++}`;

type Argument = {
  [key: string]: Argument | null;
};

/**
 * Parse JSON string to nodes and edges that Reactflow can understand.
 *
 * @param jsonString A JSON string.
 * @returns Nodes and edges.
 */
export function jsonToFlow(
  content: string,
  jsonData: Argument | null
): [Node[], Edge[]] {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  const node: Node = {
    id: getNodeId(),
    position: { x: 0, y: 0 },
    data: {
      label: content,
    },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  };

  if (jsonData != null) {
    for (const key in jsonData) {
      const [ns, es] = jsonToFlow(key, jsonData[key]);
      if (ns.length != 0) {
        const edge: Edge = {
          id: getEdgeId(),
          source: node.id,
          target: ns[0].id,
        };
        es.unshift(edge);
      }
      nodes.unshift(...ns);
      edges.unshift(...es);
    }
  }
  nodes.unshift(node);

  return [nodes, edges];
}
