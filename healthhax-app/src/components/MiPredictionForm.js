import React, { useState } from "react";
import "./MiPredictionForm.css"; // Add a CSS file for custom styling

const MiPredictionForm = () => {
  const [formData, setFormData] = useState({
    Age: "",
    Sex: "",
    Chest_Pain: "",
    Dizziness: "",
    Shoulder_Pain: "",
    Fatigue: "",
    ECG_Abnormality: "",
    Troponin_Level: "",
    Hypertension: "",
    Diabetes: "",
    Prior_Heart_Disease: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.Age || isNaN(formData.Age) || formData.Age < 0 || formData.Age > 120) {
      alert("Please enter a valid Age (0-120)." );
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          Age: parseInt(formData.Age),
          Sex: parseInt(formData.Sex),
          Chest_Pain: parseInt(formData.Chest_Pain),
          Dizziness: parseInt(formData.Dizziness),
          Shoulder_Pain: parseInt(formData.Shoulder_Pain),
          Fatigue: parseInt(formData.Fatigue),
          ECG_Abnormality: parseInt(formData.ECG_Abnormality),
          Troponin_Level: parseFloat(formData.Troponin_Level),
          Hypertension: parseInt(formData.Hypertension),
          Diabetes: parseInt(formData.Diabetes),
          Prior_Heart_Disease: parseInt(formData.Prior_Heart_Disease),
        }),
      });
      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
    setLoading(false);
  };

  return (
    <div className={`container ${darkMode ? "dark-mode" : ""}`}>
      <div className="card">
        <h2 className="title">HealthHax MI Prediction</h2>
        <h3 className="subtitle">Myocardial Infarction Prediction</h3>
        <form onSubmit={handleSubmit} className="form">
          {Object.keys(formData).map((key) => (
            <div key={key} className="form-group">
              <label className="form-label">{key.replace("_", " ")}</label>
              {key === "Sex" || key === "Chest_Pain" || key === "Hypertension" || key === "Diabetes" ? (
                <select name={key} value={formData[key]} onChange={handleChange} className="form-input">
                  <option value="">Select</option>
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              ) : (
                <input
                  type="text"
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  className="form-input"
                  required
                />
              )}
            </div>
          ))}
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? <span className="loader"></span> : "Get Prediction"}
          </button>
        </form>
        {prediction && (
          <div className="result">
            <h3 className="result-title">Prediction Result:</h3>
            <p className="result-text"><strong>MI Prediction:</strong> {prediction.MI_Prediction === 1 ? "Likely Heart Attack" : "Unlikely"}</p>
            <p className="result-text"><strong>Probability:</strong> {prediction.Probability.toFixed(2)}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MiPredictionForm;
