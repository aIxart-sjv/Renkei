// frontend/src/pages/Startups.jsx

import { useEffect, useState } from "react";
import "./Startups.css";

import { getStartups } from "../api/startups";
import Card from "../components/common/Card";

const Startups = () => {

  const [startups, setStartups] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStartups();
  }, []);

  const loadStartups = async () => {
    try {
      const data = await getStartups();
      setStartups(data);
    } catch (err) {
      console.error("Failed to fetch startups");
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return <div className="startup-loading">Loading startups...</div>;

  return (
    <div className="startups-page">

      <h1 className="startup-title">
        Innovation Startups
      </h1>

      <p className="startup-subtitle">
        Emerging ventures inside the Renkei ecosystem
      </p>

      <div className="startup-grid">

        {startups.map((startup) => (

          <Card key={startup.id}>

            <div className="startup-card">

              <h3>{startup.name}</h3>

              <p className="startup-domain">
                {startup.domain || "General Innovation"}
              </p>

              <p className="startup-description">
                {startup.description || "No description available"}
              </p>

              {/* Innovation Score */}
              <div className="innovation-section">

                <span>Innovation Score</span>

                <div className="innovation-bar">
                  <div
                    className="innovation-fill"
                    style={{
                      width: `${startup.innovation_score * 10}%`
                    }}
                  />
                </div>

              </div>

              {/* Meta Info */}
              <div className="startup-meta">

                <span>
                  👥 Team: {startup.team_size || "N/A"}
                </span>

                <span>
                  🧠 Industry: {startup.industry || "Unknown"}
                </span>

              </div>

              <div className="startup-links">

                {startup.website && (
                  <a href={startup.website} target="_blank">
                    Website
                  </a>
                )}

                {startup.github_url && (
                  <a href={startup.github_url} target="_blank">
                    GitHub
                  </a>
                )}

              </div>

            </div>

          </Card>

        ))}

      </div>

    </div>
  );
};

export default Startups;