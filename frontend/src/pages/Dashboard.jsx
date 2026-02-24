import { useEffect, useState } from "react";
import "./Dashboard.css";

import Navbar from "../components/Navbar";
import StudentCard from "../components/StudentCard";
import MentorCard from "../components/MentorCard";
import StartupCard from "../components/StartupCard";
import AchievementsCard from "../components/AchievementsCard";
import GraphView from "../components/GraphView";

const API_BASE = "http://127.0.0.1:8000";

export default function Dashboard() {
  const [students, setStudents] = useState([]);
  const [mentors, setMentors] = useState([]);
  const [startups, setStartups] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [graphData, setGraphData] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // -----------------------------
  // Fetch helper
  // -----------------------------
  const fetchData = async (endpoint, setter) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch ${endpoint}`);
      }

      const data = await response.json();
      setter(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // -----------------------------
  // Load dashboard data
  // -----------------------------
  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true);

      await Promise.all([
        fetchData("/students", setStudents),
        fetchData("/mentors", setMentors),
        fetchData("/startups", setStartups),
        fetchData("/achievements", setAchievements),
        fetchData("/graph", setGraphData),
      ]);

      setLoading(false);
    };

    loadDashboard();
  }, []);

  // -----------------------------
  // Loading State
  // -----------------------------
  if (loading) {
    return (
      <>
        <Navbar />
        <div className="dashboard-loading">
          Loading dashboard...
        </div>
      </>
    );
  }

  // -----------------------------
  // Error State
  // -----------------------------
  if (error) {
    return (
      <>
        <Navbar />
        <div className="dashboard-error">
          Error: {error}
        </div>
      </>
    );
  }

  // -----------------------------
  // Dashboard UI
  // -----------------------------
  return (
    <>
      <Navbar />

      <div className="dashboard-container">

        {/* Graph Section */}
        <section className="dashboard-section">
          <h2>Innovation Network</h2>
          {graphData && <GraphView data={graphData} />}
        </section>

        {/* Students */}
        <section className="dashboard-section">
          <h2>Students</h2>
          <div className="card-grid">
            {students.map((student) => (
              <StudentCard
                key={student.id}
                student={student}
              />
            ))}
          </div>
        </section>

        {/* Mentors */}
        <section className="dashboard-section">
          <h2>Mentors</h2>
          <div className="card-grid">
            {mentors.map((mentor) => (
              <MentorCard
                key={mentor.id}
                mentor={mentor}
              />
            ))}
          </div>
        </section>

        {/* Startups */}
        <section className="dashboard-section">
          <h2>Startups</h2>
          <div className="card-grid">
            {startups.map((startup) => (
              <StartupCard
                key={startup.id}
                startup={startup}
              />
            ))}
          </div>
        </section>

        {/* Achievements */}
        <section className="dashboard-section">
          <h2>Achievements</h2>
          <div className="card-grid">
            {achievements.map((achievement) => (
              <AchievementsCard
                key={achievement.id}
                achievement={achievement}
              />
            ))}
          </div>
        </section>

      </div>
    </>
  );
}