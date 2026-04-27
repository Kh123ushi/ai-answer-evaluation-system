import React, { useState } from "react";
import axios from "axios";

const UploadBox = ({ setResult }) => {
  const [teacherFile, setTeacherFile] = useState(null);
  const [studentFiles, setStudentFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  //  Handle multiple file upload (FIXED)
  const handleStudentFiles = (e) => {
    const newFiles = Array.from(e.target.files);

    setStudentFiles((prevFiles) => [...prevFiles, ...newFiles]);

    e.target.value = null; 
  };

  //  Submit
  const handleSubmit = async () => {
    if (!teacherFile || studentFiles.length === 0) {
      alert("Upload teacher + student files");
      return;
    }

    const formData = new FormData();
    formData.append("teacher_file", teacherFile);

    studentFiles.forEach((file) => {
      formData.append("student_files", file);
    });

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/evaluate-with-teacher",
        formData
      );

      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error uploading files");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Answers</h2>

      {/* Teacher File */}
      <input
        type="file"
        onChange={(e) => setTeacherFile(e.target.files[0])}
      />

      <br /><br />

      {/* Student Files */}
      <input type="file" multiple onChange={handleStudentFiles} />

      {/*show uploaded files */}
      <ul>
        {studentFiles.map((file, index) => (
          <li key={index}>{file.name}</li>
        ))}
      </ul>

      {/* Button */}
      <button onClick={handleSubmit}>
        {loading ? "Processing..." : "Evaluate"}
      </button>
    </div>
  );
};

export default UploadBox;