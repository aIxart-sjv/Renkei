import React from "react";
import "./AchievementsCard.css";

const AchievementsCard = ({ achievement }) => {
  if (!achievement) return null;

  const {
    title,
    description,
    category,
    outcome,
    technologies_used,
    event_name,
    date,
  } = achievement;

  const getOutcomeClass = (outcome) => {
    if (!outcome) return "outcome-default";

    const value = outcome.toLowerCase();

    if (value === "won") return "outcome-won";
    if (value === "runner-up") return "outcome-runner";
    if (value === "participated") return "outcome-participated";

    return "outcome-default";
  };

  return (
    <div className="achievement-card">
      {/* Header */}
      <div className="achievement-header">
        <h3 className="achievement-title">{title}</h3>

        {outcome && (
          <span className={`achievement-outcome ${getOutcomeClass(outcome)}`}>
            {outcome}
          </span>
        )}
      </div>

      {/* Event */}
      {event_name && (
        <p className="achievement-event">
          {event_name}
        </p>
      )}

      {/* Description */}
      {description && (
        <p className="achievement-description">
          {description}
        </p>
      )}

      {/* Tech Stack */}
      {technologies_used && technologies_used.length > 0 && (
        <div className="achievement-tech">
          {technologies_used.map((tech, index) => (
            <span key={index} className="tech-badge">
              {tech}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="achievement-footer">
        {category && (
          <span className="achievement-category">
            {category}
          </span>
        )}

        {date && (
          <span className="achievement-date">
            {new Date(date).toLocaleDateString()}
          </span>
        )}
      </div>
    </div>
  );
};

export default AchievementsCard;