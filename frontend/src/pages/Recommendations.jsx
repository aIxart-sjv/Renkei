// frontend/src/pages/Recommendations.jsx

import { useEffect, useState } from "react";
import "./Recommendations.css";

import { getRecommendations } from "../api/recommendations";
import Card from "../components/common/Card";

const Recommendations = () => {

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      // assuming logged-in user id = 1 for now
      const data = await getRecommendations(1);
      setRecommendations(data);
    } catch (err) {
      console.error("Recommendation fetch failed");
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return <div className="rec-loading">Generating AI matches...</div>;

  return (
    <div className="recommendations-page">

      <h1 className="rec-title">
        AI Collaboration Recommendations
      </h1>

      <p className="rec-subtitle">
        Ranked connections optimized for innovation impact
      </p>

      <div className="recommendation-grid">

        {recommendations.map((rec, index) => (

          <Card key={index}>

            <div className="rec-card">

              {/* Rank */}
              <div className="rec-rank">
                #{index + 1}
              </div>

              {/* Name */}
              <h3>{rec.name}</h3>

              <p className="rec-role">
                {rec.type}
              </p>

              {/* Score */}
              <div className="score-section">

                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{
                      width: `${rec.score * 100}%`
                    }}
                  />
                </div>

                <span className="score-text">
                  {(rec.score * 100).toFixed(1)}% Match
                </span>

              </div>

              {/* Reason */}
              <p className="rec-reason">
                {rec.reason || "High innovation compatibility"}
              </p>

              <button className="collab-btn">
                Collaborate
              </button>

            </div>

          </Card>

        ))}

      </div>

    </div>
  );
};

export default Recommendations;