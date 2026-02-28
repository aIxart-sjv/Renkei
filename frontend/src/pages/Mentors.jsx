// frontend/src/pages/Mentors.jsx

import { useEffect, useState } from "react";
import "./Mentors.css";

import { getMentors } from "../api/mentors";
import Card from "../components/common/Card";

const Mentors = () => {

  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMentors();
  }, []);

  const loadMentors = async () => {
    try {
      const data = await getMentors();
      setMentors(data);
    } catch (err) {
      console.error("Failed to fetch mentors");
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return <div className="mentor-loading">Loading mentors...</div>;

  return (
    <div className="mentors-page">

      <h1 className="page-title">
        Mentor Network
      </h1>

      <div className="mentor-grid">

        {mentors.map((mentor) => (
          <Card key={mentor.id}>

            <div className="mentor-card">

              <div className="mentor-header">
                <h3>{mentor.full_name}</h3>
                <span className="mentor-domain">
                  {mentor.domain || "General"}
                </span>
              </div>

              <p className="mentor-bio">
                {mentor.bio || "No bio available"}
              </p>

              <div className="mentor-meta">

                <div>
                  <strong>Experience</strong>
                  <p>{mentor.experience_years || 0} yrs</p>
                </div>

                <div>
                  <strong>Industry</strong>
                  <p>{mentor.industry || "N/A"}</p>
                </div>

              </div>

              <button className="connect-btn">
                Connect
              </button>

            </div>

          </Card>
        ))}

      </div>

    </div>
  );
};

export default Mentors;