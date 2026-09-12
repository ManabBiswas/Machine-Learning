import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import Home from "./pages/Home";
import Assess from "./pages/Assess";
import Insights from "./pages/Insights";
import About from "./pages/About";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Home />} />
          <Route path="/assess" element={<Assess />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
