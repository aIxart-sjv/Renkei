// =============================
// FORMATTERS
// =============================

export const truncateText = (text, maxLength = 80) => {
  if (!text) return "";
  return text.length > maxLength
    ? text.substring(0, maxLength) + "..."
    : text;
};

export const capitalize = (value) => {
  if (!value) return "";
  return value.charAt(0).toUpperCase() + value.slice(1);
};

export const formatNumber = (num) => {
  if (num === null || num === undefined) return "0";
  return new Intl.NumberFormat().format(num);
};


// =============================
// DATE HELPERS
// =============================

export const formatDate = (date) => {
  if (!date) return "-";

  return new Date(date).toLocaleDateString("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export const timeAgo = (date) => {
  if (!date) return "";

  const seconds =
    Math.floor((new Date() - new Date(date)) / 1000);

  const intervals = [
    { label: "year", seconds: 31536000 },
    { label: "month", seconds: 2592000 },
    { label: "day", seconds: 86400 },
    { label: "hour", seconds: 3600 },
    { label: "minute", seconds: 60 },
  ];

  for (const i of intervals) {
    const count = Math.floor(seconds / i.seconds);
    if (count >= 1)
      return `${count} ${i.label}${count > 1 ? "s" : ""} ago`;
  }

  return "Just now";
};


// =============================
// SCORE HELPERS
// =============================

export const scoreColor = (score) => {
  if (score >= 80) return "#22c55e";
  if (score >= 50) return "#f59e0b";
  return "#ef4444";
};

export const normalizeScore = (score, max = 100) => {
  if (!score) return 0;
  return Math.min((score / max) * 100, 100);
};


// =============================
// GRAPH HELPERS
// =============================

export const groupNodesByType = (nodes = []) => {
  return nodes.reduce((acc, node) => {
    const type = node.type || "unknown";

    if (!acc[type]) acc[type] = [];
    acc[type].push(node);

    return acc;
  }, {});
};


// =============================
// STORAGE HELPERS
// =============================

export const saveToStorage = (key, value) => {
  localStorage.setItem(key, JSON.stringify(value));
};

export const getFromStorage = (key) => {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
};

export const removeFromStorage = (key) => {
  localStorage.removeItem(key);
};


// =============================
// RANDOM HELPERS
// =============================

export const generateAvatar = (name = "User") => {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(
    name
  )}&background=0f172a&color=fff`;
};

export const sleep = (ms) =>
  new Promise((resolve) => setTimeout(resolve, ms));