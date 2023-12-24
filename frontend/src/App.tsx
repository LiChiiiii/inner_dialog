import ReactFlow, {
  Background,
  Controls,
  BackgroundVariant,
  ReactFlowProvider,
} from "reactflow";
import "reactflow/dist/style.css";
import { shallow } from "zustand/shallow";
import useStore, { RFState } from "./store";
import QuestionInput from "./QuestionInput";

const selector = (state: RFState) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
});

function App() {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect } = useStore(
    selector,
    shallow
  );

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
        <QuestionInput />
      </ReactFlow>
    </div>
  );
}

function AppWithProvider() {
  return (
    <ReactFlowProvider>
      <App />
    </ReactFlowProvider>
  );
}

export default AppWithProvider;
