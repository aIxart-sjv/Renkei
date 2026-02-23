import { useEffect, useState, useMemo } from "react";
import StartupCard from "../components/StartupCard";
import api from "../services/api";
import "./Startups.css";

const Startups = () => {
  const [startups, setStartups] = useState([]);
  const [filteredStartups, setFilteredStartups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [domainFilter, setDomainFilter] = useState("all");

  // Fetch startups from backend
  useEffect(() => {
    const fetchStartups = async () => {
      try {
        setLoading(true);

        // expected endpoint: GET /startups
        const response = await api.get("/startups");

        const data = response.data || [];
        setStartups(data);
        setFilteredStartups(data);

      } catch (err) {
        console.error("Failed to fetch startups:", err);
        setError("Unable to load startups. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchStartups();
  }, []);

  // Extract unique domains
  const domains = useMemo(() => {
    const unique = new Set(startups.map(s => s.domain));
    return ["all", ...unique];
  }, [startups]);

  // Filter logic
  useEffect(() => {
    let result = startups;

    if (search) {
      result = result.filter(startup =>
        startup.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (domainFilter !== "all") {
      result = result.filter(startup => startup.domain === domainFilter);
    }

    setFilteredStartups(result);

  }, [search, domainFilter, startups]);

  if (loading) {
    return (
      <div className="startups-container">
        <p className="status-text">Loading startups...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="startups-container">
        <p className="error-text">{error}</p>
      </div>
    );
  }

  return (
    <div className="startups-container">

      {/* Header */}
      <div className="startups-header">
        <h1>Startups</h1>
        <p>Discover innovative startups from your network</p>
      </div>

      {/* Filters */}
      <div className="startups-filters">

        <input
          type="text"
          placeholder="Search startups..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />

        <select
          value={domainFilter}
          onChange={(e) => setDomainFilter(e.target.value)}
          className="filter-select"
        >
          {domains.map(domain => (
            <option key={domain} value={domain}>
              {domain === "all" ? "All Domains" : domain}
            </option>
          ))}
        </select>

      </div>

      {/* Startups Grid */}
      {filteredStartups.length === 0 ? (
        <p className="status-text">No startups found.</p>
      ) : (
        <div className="startups-grid">
          {filteredStartups.map(startup => (
            <StartupCard
              key={startup.id}
              startup={startup}
            />
          ))}
        </div>
      )}

    </div>
  );
};

export default Startups;