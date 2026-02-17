"use client";

import { useState } from "react";
import { FaUser, FaEnvelope, FaCommentDots } from "react-icons/fa";

export default function FeedbackPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.email || !formData.message) {
      alert("Please fill all fields.");
      return;
    }

    setSubmitted(true);

    setTimeout(() => {
      setSubmitted(false);
    }, 3000);

    setFormData({ name: "", email: "", message: "" });
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-[#0f172a] overflow-hidden px-6">

      {/* Background Glow Effects */}
      <div className="absolute w-96 h-96 bg-purple-600/30 rounded-full blur-3xl -top-20 -left-20 animate-pulse"></div>
      <div className="absolute w-96 h-96 bg-pink-600/30 rounded-full blur-3xl bottom-0 right-0 animate-pulse"></div>

      <div className="relative bg-white/10 backdrop-blur-xl border border-white/20 shadow-2xl rounded-2xl p-10 w-full max-w-2xl">

        <h1 className="text-4xl font-bold text-center text-white mb-2">
          Share Your Feedback
        </h1>

        <p className="text-gray-300 text-center mb-8">
          Help us improve CivicResolve by sharing your thoughts and suggestions.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Name */}
          <div className="relative">
            <FaUser className="absolute left-4 top-4 text-gray-400" />
            <input
              type="text"
              name="name"
              placeholder="Your Name"
              value={formData.name}
              onChange={handleChange}
              className="w-full bg-transparent border border-gray-500 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            />
          </div>

          {/* Email */}
          <div className="relative">
            <FaEnvelope className="absolute left-4 top-4 text-gray-400" />
            <input
              type="email"
              name="email"
              placeholder="Your Email"
              value={formData.email}
              onChange={handleChange}
              className="w-full bg-transparent border border-gray-500 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 transition"
            />
          </div>

          {/* Message */}
          <div className="relative">
            <FaCommentDots className="absolute left-4 top-4 text-gray-400" />
            <textarea
              name="message"
              placeholder="Your Message..."
              rows={5}
              value={formData.message}
              onChange={handleChange}
              className="w-full bg-transparent border border-gray-500 text-white pl-12 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="
              relative w-full py-3 rounded-lg
              bg-gradient-to-r from-purple-500 to-pink-500
              text-white font-semibold text-lg
              hover:scale-105
              hover:shadow-xl hover:shadow-purple-500/40
              transition-all duration-300
              overflow-hidden
            "
          >
            <span className="relative z-10">Submit Feedback</span>
            <span className="absolute inset-0 bg-white/10 opacity-0 hover:opacity-100 transition"></span>
          </button>

        </form>

        {/* Success Modal */}
        {submitted && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/60 rounded-2xl backdrop-blur-md animate-fadeIn">
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6 rounded-xl shadow-xl text-center">
              <h2 className="text-2xl font-bold mb-2">Thank You! 🚀</h2>
              <p>Your feedback has been successfully submitted.</p>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
