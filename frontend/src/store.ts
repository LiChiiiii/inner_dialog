import { create } from 'zustand';
import Dagre from "@dagrejs/dagre";
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';

import { jsonToFlow } from './utils';

export type RFState = {
  nodes: Node[];
  edges: Edge[];
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  getMindMap: (question: string, model: string) => Promise<void>;
  layout: (direction: string) => void;
};

// this is our useStore hook that we can use in our components to get parts of the store and call actions
const useStore = create<RFState>((set, get) => ({
  nodes: [],
  edges: [],
  onNodesChange: (changes: NodeChange[]) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },
  onEdgesChange: (changes: EdgeChange[]) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },
  onConnect: (connection: Connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
  },
  getMindMap: async (question: string, model: string) => {
    try {
      const use_cache = true;
      const force_write_cache = false;
      const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imdlbl9taW5kbWFwIn0._o0YEp70nondUuckGagYUtlYMc5qXWR7LBh8abDQxEg";
      // backend_url: e.g., http:localhost:8113
      // const backend_url: string = import.meta.env.VITE_API_URL;
      const backend_url: string = "http://localhost:8000";
      const apiUrl = `${backend_url}/gen_mindmap/?question=${question}&model=${model}&use_cache=${use_cache}&force_write_cache=${force_write_cache}&token=${token}`;
      const response = await fetch(apiUrl);

      if (response.ok) {
        const jsonData = await response.json();
        const key = Object.keys(jsonData)[0];
        const [nodes, edges] = jsonToFlow(key, jsonData[key]);
        set({ nodes: nodes, edges: edges });
      } else {
        console.error("Error fetching data:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  },
  layout: (direction: string) => {
    const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));

    const getLayoutedElements = (
      nodes: Node[],
      edges: Edge[],
      options: { [key: string]: string }
    ) => {
      g.setGraph({ rankdir: options.direction });

      edges.forEach((edge) => g.setEdge(edge.source, edge.target));
      nodes.forEach((node) => g.setNode(node.id, node));

      Dagre.layout(g);

      return {
        nodes: nodes.map((node) => {
          const { x, y } = g.node(node.id);

          return { ...node, position: { x, y } };
        }),
        edges,
      };
    };

    const layouted = getLayoutedElements(get().nodes, get().edges, { direction });

    set({
      nodes: layouted.nodes,
      edges: layouted.edges,
    })

    // window.requestAnimationFrame(() => {
    //   fitView();
    // });
  }
}));

export default useStore;
