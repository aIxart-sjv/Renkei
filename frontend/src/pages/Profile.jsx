import { useEffect, useState } from "react";
import "../App.css";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const API_BASE = "http://localhost:8000";

  // In production this should come from auth context / JWT
  const userId = localStorage.getItem("user_id") || 1;

  useEffect(() => {
    fetchProfile();
    fetchAchievements();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await fetch(`${API_BASE}/students/${userId}`);

      if (!res.ok) throw new Error("Failed to load profile");

      const data = await res.json();
      setProfile(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAchievements = async () => {
    try {
      const res = await fetch(
        `${API_BASE}/achievements/student/${userId}`
      );

      if (!res.ok) throw new Error("Failed to load achievements");

      const data = await res.json();
      setAchievements(data);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading)
    return (
      <div className="page-container">
        <div className="loading">Loading profile...</div>
      </div>
    );

  if (error)
    return (
      <div className="page-container">
        <div className="error">{error}</div>
      </div>
    );

  if (!profile)
    return (
      <div className="page-container">
        <div className="error">Profile not found</div>
      </div>
    );

  return (
    <div className="page-container">

      <h1 className="page-title">My Profile</h1>

      <div className="profile-container">

        {/* Profile Card */}
        <div className="profile-card">

          <div className="profile-header">
            <div className="profile-avatar">
              {profile.name?.charAt(0).toUpperCase()}
            </div>

            <div>
              <h2>{profile.name}</h2>
              <p className="profile-email">{profile.email}</p>
            </div>
          </div>

          <div className="profile-section">
            <h3>Innovation Score</h3>
            <div className="innovation-score">
              {profile.innovation_score?.toFixed(2) || "0.00"}
            </div>
          </div>

          <div className="profile-section">
            <h3>Skills</h3>
            <div className="tag-container">
              {profile.skills?.map((skill, index) => (
                <span key={index} className="tag skill-tag">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="profile-section">
            <h3>Interests</h3>
            <div className="tag-container">
              {profile.interests?.map((interest, index) => (
                <span key={index} className="tag interest-tag">
                  {interest}
                </span>
              ))}
            </div>
          </div>

        </div>

        {/* Achievements Section */}
        <div className="profile-card">

          <h3>Achievements</h3>

          {achievements.length === 0 ? (
            <p className="empty-text">No achievements yet</p>
          ) : (
            <div className="achievement-list">
              {achievements.map((achievement) => (
                <div
                  key={achievement.id}
                  className="achievement-item"
                >
                  <div className="achievement-header">
                    <strong>{achievement.title}</strong>
                    <span className="achievement-outcome">
                      {achievement.outcome}
                    </span>
                  </div>

                  <p className="achievement-description">
                    {achievement.description}
                  </p>

                  <div className="tag-container">
                    {achievement.technologies_used?.map(
                      (tech, index) => (
                        <span key={index} className="tag tech-tag">
                          {tech}
                        </span>
                      )
                    )}
                  </div>

                </div>
              ))}
            </div>
          )}

        </div>

      </div>

    </div>
  );
};

export default Profile;