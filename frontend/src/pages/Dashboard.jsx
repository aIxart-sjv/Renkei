function Dashboard() {
  return (
    <div className="page">
      <h1>Welcome Back 👋</h1>

      <div className="card-grid">
        <div className="info-card">
          <h3>Total Connections</h3>
          <p>24</p>
        </div>

        <div className="info-card">
          <h3>Startup Matches</h3>
          <p>8</p>
        </div>

        <div className="info-card">
          <h3>Mentor Requests</h3>
          <p>3 Pending</p>
        </div>

        <div className="info-card">
          <h3>Recommendations</h3>
          <p>5 New</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;