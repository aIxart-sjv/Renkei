import React from "react";
import "./StudentCard.css";

const StudentCard = ({ student, onViewProfile }) => {
  if (!student) return null;

  const {
    id,
    name,
    email,
    department,
    year,
    skills = [],
    interests = [],
    innovation_score,
    performance_score,
  } = student;

  return (
    <div className="student-card">
      {/* Header */}
      <div className="student-card-header">
        <div className="student-avatar">
          {name?.charAt(0).toUpperCase()}
        </div>

        <div className="student-info">
          <h3 className="student-name">{name}</h3>
          <p className="student-email">{email}</p>
        </div>
      </div>

      {/* Academic Info */}
      <div className="student-academic">
        <span className="student-department">{department}</span>
        <span className="student-year">Year {year}</span>
      </div>

      {/* Skills */}
      {skills.length > 0 && (
        <div className="student-section">
          <p className="student-label">Skills</p>
          <div className="student-tags">
            {skills.slice(0, 5).map((skill, index) => (
              <span key={index} className="tag skill-tag">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Interests */}
      {interests.length > 0 && (
        <div className="student-section">
          <p className="student-label">Interests</p>
          <div className="student-tags">
            {interests.slice(0, 5).map((interest, index) => (
              <span key={index} className="tag interest-tag">
                {interest}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Scores */}
      <div className="student-scores">
        {innovation_score !== undefined && (
          <div className="score-box">
            <span className="score-label">Innovation</span>
            <span className="score-value">
              {innovation_score.toFixed(2)}
            </span>
          </div>
        )}

        {performance_score !== undefined && (
          <div className="score-box">
            <span className="score-label">Performance</span>
            <span className="score-value">
              {performance_score.toFixed(2)}
            </span>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="student-card-footer">
        <button
          className="view-profile-btn"
          onClick={() => onViewProfile?.(id)}
        >
          View Profile
        </button>
      </div>
    </div>
  );
};

export default StudentCard;