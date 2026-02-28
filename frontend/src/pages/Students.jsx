// frontend/src/pages/Students.jsx

import { useEffect, useState } from "react";
import "./Students.css";

import { getStudents } from "../api/students";
import Card from "../components/common/Card";

const Students = () => {

  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      const data = await getStudents();
      setStudents(data);
    } catch (err) {
      console.error("Failed to fetch students");
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return <div className="students-loading">Loading students...</div>;

  return (
    <div className="students-page">

      <h1 className="students-title">
        Student Innovation Network
      </h1>

      <p className="students-subtitle">
        Talent discovered through graph intelligence
      </p>

      <div className="students-grid">

        {students.map((student) => (

          <Card key={student.id}>

            <div className="student-card">

              <h3>{student.name}</h3>

              <p className="student-domain">
                {student.domain || "General"}
              </p>

              <p className="student-bio">
                {student.bio || "No bio available"}
              </p>

              {/* Innovation Score */}
              <div className="innovation-section">

                <span>Innovation Score</span>

                <div className="innovation-bar">
                  <div
                    className="innovation-fill"
                    style={{
                      width: `${student.innovation_score * 10}%`
                    }}
                  />
                </div>

              </div>

              {/* Skills */}
              <div className="student-skills">
                {(student.skills || "")
                  .split(",")
                  .slice(0, 4)
                  .map((skill, i) => (
                    <span key={i}>{skill.trim()}</span>
                  ))}
              </div>

              {/* Meta */}
              <div className="student-meta">

                <span>
                  🎓 Year: {student.year || "N/A"}
                </span>

                <span>
                  🧠 Projects: {student.project_count || 0}
                </span>

              </div>

            </div>

          </Card>

        ))}

      </div>

    </div>
  );
};

export default Students;