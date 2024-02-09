import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import Authorization from "./pages/authorization";
import Join from "./pages/join";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/authenticate" element={<Authorization />} />
        <Route path="/join/:room" element={<Join />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
