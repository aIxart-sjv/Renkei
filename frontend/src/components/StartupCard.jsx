import React from "react";
import "./StartupCard.css";

/**
 * StartupCard Component
 *
 * Props:
 * - startup: {
 *     id: number
 *     name: string
 *     domain: string
 *     stage: string
 *     tech_stack: string[]
 *     funding_received?: number
 *     innovation_score?: number
 *   }
 *
 * - onView?: function(startup)
 */

const StartupCard = ({ startup, onView }) => {
  if (!startup) return null;

  const {
    name,
    domain,
    stage,
    tech_stack = [],
    funding_received,
    innovation_score,
  } = startup;

  const formatFunding = (amount) => {
    if (!amount) return "Not disclosed";

    if (amount >= 1_000_000)
      return `$${(amount / 1_000_000).toFixed(1)}M`;

    if (amount >= 1_000)
      return `$${(amount / 1_000).toFixed(1)}K`;

    return `$${amount}`;
  };

  return (
    <div className="startup-card">
      {/* Header */}
      <div className="startup-card-header">
        <h3 className="startup-name">{name}</h3>
        <span className="startup-stage">{stage}</span>
      </div>

      {/* Domain */}
      <p className="startup-domain">{domain}</p>

      {/* Tech Stack */}
      {tech_stack.length > 0 && (
        <div className="startup-tech-stack">
          {tech_stack.map((tech, index) => (
            <span key={index} className="tech-badge">
              {tech}
            </span>
          ))}
        </div>
      )}

      {/* Stats */}
      <div className="startup-stats">
        <div className="startup-stat">
          <span className="stat-label">Funding</span>
          <span className="stat-value">
            {formatFunding(funding_received)}
          </span>
        </div>

        {innovation_score !== undefined && (
          <div className="startup-stat">
            <span className="stat-label">Innovation</span>
            <span className="stat-value">
              {innovation_score.toFixed(2)}
            </span>
          </div>
        )}
      </div>

      {/* Action */}
      {onView && (
        <button
          className="startup-view-btn"
          onClick={() => onView(startup)}
        >
          View Details
        </button>
      )}
    </div>
  );
};

export default StartupCard;