import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Network from "./pages/Network";
import Startups from "./pages/Startups";

function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/network" element={<Network />} />
        <Route path="/startups" element={<Startups />} />
      </Routes>
    </>
  );
}

export default App;