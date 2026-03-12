import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import ArxivDaily from "./pages/ArxivDaily";
import KnowledgeGraph from "./pages/KnowledgeGraph";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ArxivDaily />} />
          <Route path="graph" element={<KnowledgeGraph embedded />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
