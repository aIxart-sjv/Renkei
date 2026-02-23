import React from "react";
import "./MentorCard.css";

/**
 * MentorCard Component
 *
 * Props:
 * mentor: {
 *   mentor_id: number,
 *   name: string,
 *   organization: string,
 *   designation: string,
 *   expertise: string[],
 *   match_score?: number
 * }
 *
 * onClick?: function
 */

const MentorCard = ({ mentor, onClick }) => {
  if (!mentor) return null;

  const {
    name,
    organization,
    designation,
    expertise = [],
    match_score,
  } = mentor;

  return (
    <div className="mentor-card" onClick={onClick}>
      
      {/* Header */}
      <div className="mentor-card-header">
        <div className="mentor-avatar">
          {name?.charAt(0)?.toUpperCase() || "M"}
        </div>

        <div className="mentor-info">
          <h3 className="mentor-name">{name}</h3>

          {designation && (
            <p className="mentor-designation">{designation}</p>
          )}

          {organization && (
            <p className="mentor-organization">{organization}</p>
          )}
        </div>
      </div>

      {/* Expertise */}
      {expertise.length > 0 && (
        <div className="mentor-expertise">
          {expertise.map((skill, index) => (
            <span key={index} className="expertise-tag">
              {skill}
            </span>
          ))}
        </div>
      )}

      {/* Match Score */}
      {match_score !== undefined && (
        <div className="mentor-match">
          <span className="match-label">Match Score</span>
          <span className="match-value">
            {(match_score * 100).toFixed(0)}%
          </span>
        </div>
      )}
      
    </div>
  );
};

export default MentorCard;