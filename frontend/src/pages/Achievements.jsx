import React, { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

const Achievements = () => {
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const token = localStorage.getItem("renkei_token");
  useEffect(() => {
    const fetchAchievements = async () => {
      try {
        if (!token) throw new Error("No token");

        // STEP 1: get current user
        const userRes = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!userRes.ok) throw new Error("Failed to fetch user");

        const user = await userRes.json();

        // STEP 2: get all students
        const studentRes = await fetch(`${API_BASE}/students/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!studentRes.ok) throw new Error("Failed to fetch students");

        const students = await studentRes.json();

        // STEP 3: find matching student by email
        const student = students.find(
          (s) => s.email === user.email
        );

        if (!student) throw new Error("Student profile not found");

        // STEP 4: fetch achievements
        const achRes = await fetch(
          `${API_BASE}/achievements/student/${student.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!achRes.ok) throw new Error("Failed achievements fetch");

        const achData = await achRes.json();

        setAchievements(achData);

      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAchievements();
  }, [token]);

  if (loading)
    return (
      <div className="p-6 text-center">
        Loading achievements...
      </div>
    );

  if (error)
    return (
      <div className="p-6 text-center text-red-500">
        {error}
      </div>
    );

  if (achievements.length === 0)
    return (
      <div className="p-6 text-center">
        No achievements found
      </div>
    );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        Your Achievements
      </h1>

      {achievements.map((ach) => (
        <div key={ach.id} className="border p-4 mb-3 rounded">
          <h2 className="font-bold">{ach.title}</h2>
          <p>{ach.description}</p>
          <p>Category: {ach.category}</p>
          <p>Outcome: {ach.outcome}</p>
          <p>
            Tech: {ach.technologies_used?.join(", ")}
          </p>
        </div>
      ))}
    </div>
  );
};

export default Achievements;