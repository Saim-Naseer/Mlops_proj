"use client";
import { motion } from "framer-motion";
import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    GRE_Score: "",
    TOEFL_Score: "",
    University_Rating: "",
    SOP: "",
    LOR: "",
    CGPA: "",
    Research: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const submitForm = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setPrediction((data.prediction * 100).toFixed(2));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const inputs = [
    { name: "GRE_Score", label: "GRE Score", min: 260, max: 340 },
    { name: "TOEFL_Score", label: "TOEFL Score", min: 0, max: 120 },
    { name: "University_Rating", label: "University Rating", min: 1, max: 5 },
    { name: "SOP", label: "SOP Strength", min: 1, max: 5 },
    { name: "LOR", label: "LOR Strength", min: 1, max: 5 },
    { name: "CGPA", label: "CGPA", min: 0, max: 10, step: 0.01 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#05080f] via-[#0a1a33] to-[#0d1220] text-white py-12 px-6">
      {/* HERO */}
      <section className="text-center mb-12">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-white"
        >
          University Admission Predictor
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-4 text-lg text-blue-200"
        >
          Smart, AI-powered probability estimation
        </motion.p>
      </section>

      {/* FORM */}
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {inputs.map((input) => (
          <motion.div
            key={input.name}
            className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl border border-white/20 hover:scale-105 transition-transform duration-300"
            whileHover={{ scale: 1.05 }}
          >
            <label className="text-blue-200 font-medium flex justify-between">
              {input.label}
              <span className="text-sm text-blue-400">
                {input.min}-{input.max}
              </span>
            </label>
            <input
              type="number"
              name={input.name}
              min={input.min}
              max={input.max}
              step={input.step || 1}
              required
              value={formData[input.name]}
              onChange={handleChange}
              className="mt-2 w-full bg-white/10 border border-white/20 rounded-xl p-3 text-white placeholder:text-blue-300 focus:ring-2 focus:ring-blue-400 outline-none"
              placeholder={`Enter ${input.label}`}
            />
          </motion.div>
        ))}

        {/* RESEARCH */}
        <motion.div
          className="bg-white/10 backdrop-blur-lg p-5 rounded-2xl border border-white/20 hover:scale-105 transition-transform duration-300"
          whileHover={{ scale: 1.05 }}
        >
          <label className="text-blue-200 font-medium flex justify-between">
            Research Experience
          </label>
          <select
            name="Research"
            required
            value={formData.Research}
            onChange={handleChange}
            className="mt-2 w-full bg-white/10 text-white border border-white/20 rounded-xl p-3 focus:ring-2 focus:ring-blue-400 outline-none"
          >
            <option value="" disabled className="text-blue-300">
              Select
            </option>
            <option value="1" className="text-black">Yes</option>
            <option value="0" className="text-black">No</option>
          </select>
        </motion.div>

        {/* SUBMIT */}
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={submitForm}
          className="col-span-full py-4 rounded-2xl bg-gradient-to-r from-blue-500 to-blue-300 text-black font-bold shadow-lg text-lg"
        >
          {loading ? "Predicting..." : "Get Admission Prediction"}
        </motion.button>

        {/* PREDICTION RESULT */}
        {prediction !== null && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="col-span-full p-6 rounded-2xl bg-white/10 border border-white/20 text-center"
          >
            <h3 className="text-xl font-semibold text-blue-300">Prediction Result</h3>
            <p className="mt-3 text-2xl font-bold text-blue-400">
              🎯 Chance of Admission: {prediction}%
            </p>
          </motion.div>
        )}
      </div>
    </div>
  );
}