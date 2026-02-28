// frontend/src/components/common/Card.jsx

import React from "react";

/**
 * =====================================
 * Reusable Card Component
 * =====================================
 *
 * Used across:
 * - Student cards
 * - Mentor cards
 * - Startup cards
 * - Dashboard widgets
 * - Analytics panels
 */

const Card = ({
  children,
  className = "",
  onClick,
  hover = false,
}) => {
  return (
    <div
      onClick={onClick}
      className={`
        bg-white
        rounded-2xl
        shadow-md
        p-5
        transition-all
        duration-200
        ${hover ? "hover:shadow-xl hover:-translate-y-1 cursor-pointer" : ""}
        ${className}
      `}
    >
      {children}
    </div>
  );
};

export default Card;