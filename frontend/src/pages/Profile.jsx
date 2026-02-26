function Profile() {
  return (
    <div className="page">
      <h1>Profile</h1>

      <div className="profile-card">
        <p><strong>Name:</strong> John Doe</p>
        <p><strong>Email:</strong> john@example.com</p>
        <p><strong>Role:</strong> Student</p>
        <p><strong>Interests:</strong> AI, Web Development, Startups</p>

        <button>Edit Profile</button>
      </div>
    </div>
  );
}

export default Profile;