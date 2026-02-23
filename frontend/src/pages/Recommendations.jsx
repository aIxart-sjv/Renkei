import { useEffect, useState } from "react";
import api from "../services/api";

import StudentCard from "../components/StudentCard";
import MentorCard from "../components/MentorCard";
import StartupCard from "../components/StartupCard";

import "../App.css";

export default function Recommendations() {
  const [data, setData] = useState({
    students: [],
    mentors: [],
    alumni: [],
    startups: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Replace with actual logged-in student ID later
  const studentId = 1;

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);

      // Backend endpoint:
      // GET /recommendations/{student_id}
      const response = await api.get(`/recommendations/${studentId}`);

      setData(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load recommendations.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <h2>Recommendations</h2>
        <p>Loading AI recommendations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <h2>Recommendations</h2>
        <p className="error">{error}</p>
      </div>
    );
  }

  return (
    <div className="page-container">

      {/* Header */}
      <div className="page-header">
        <h2>AI Recommendations</h2>
        <p className="page-subtitle">
          Personalized matches based on skills, interests, and network analysis.
        </p>
      </div>

      {/* Students */}
      <section className="section">
        <h3>Recommended Students</h3>

        {data.students.length === 0 ? (
          <p>No student recommendations available.</p>
        ) : (
          <div className="card-grid">
            {data.students.map((student) => (
              <StudentCard
                key={student.student_id}
                student={student}
              />
            ))}
          </div>
        )}
      </section>

      {/* Mentors */}
      <section className="section">
        <h3>Recommended Mentors</h3>

        {data.mentors.length === 0 ? (
          <p>No mentor recommendations available.</p>
        ) : (
          <div className="card-grid">
            {data.mentors.map((mentor) => (
              <MentorCard
                key={mentor.mentor_id}
                mentor={mentor}
              />
            ))}
          </div>
        )}
      </section>

      {/* Alumni */}
      <section className="section">
        <h3>Recommended Alumni</h3>

        {data.alumni.length === 0 ? (
          <p>No alumni recommendations available.</p>
        ) : (
          <div className="card-grid">
            {data.alumni.map((alumni) => (
              <MentorCard
                key={alumni.alumni_id}
                mentor={alumni}
              />
            ))}
          </div>
        )}
      </section>

      {/* Startups */}
      <section className="section">
        <h3>Recommended Startups</h3>

        {data.startups.length === 0 ? (
          <p>No startup recommendations available.</p>
        ) : (
          <div className="card-grid">
            {data.startups.map((startup) => (
              <StartupCard
                key={startup.startup_id}
                startup={startup}
              />
            ))}
          </div>
        )}
      </section>

    </div>
  );
}