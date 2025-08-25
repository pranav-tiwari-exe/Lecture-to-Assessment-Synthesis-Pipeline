"use client";

import { useState } from "react";

export default function VideoInput() {
  const [videoLink, setVideoLink] = useState("");
  const [videoFile, setVideoFile] = useState(null);
  const [transcript, setTranscript] = useState("");

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
      setVideoLink(""); // Clear link if file selected
    }
  };

  const handleLinkChange = (e) => {
    setVideoLink(e.target.value);
    setVideoFile(null); // Clear file if link entered
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!videoLink && !videoFile) {
      alert("Please provide a YouTube link or upload a video file");
      return;
    }

    // Send to backend
    console.log("Video Link:", videoLink);
    console.log("Video File:", videoFile);
  };

  const handleTranscriptChange = (e) => {
    setTranscript(e.target.value);
  };

  return (
    <div
      className="max-w-lg mx-auto p-8 shadow-xl rounded-2xl border"
      style={{
        background: "linear-gradient(to bottom right, #F5E6CC, #FAF1E3)",
        borderColor: "#E6CFA7",
      }}
    >
      <h2
        className="text-2xl font-extrabold mb-6 text-center"
        style={{ color: "#3A4B41" }}
      >
        🎥 Upload Lecture Video
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Transcript Input */}
        <div>
          <label
            className="block font-medium mb-2"
            style={{ color: "#3A4B41" }}
          >
            Transcript
          </label>
          <textarea
            placeholder="Enter transcript..."
            value={transcript}
            onChange={handleTranscriptChange}
            rows={3}
            className="text-sm w-full p-3 border rounded-lg focus:outline-none focus:ring-2 resize-none"
            style={{
              borderColor: "#E6CFA7",
              color: "#3A4B41",
              backgroundColor: "#FAF1E3",
              focusRingColor: "#3A4B41",
            }}
          />
        </div>

        {/* File Upload */}
        <div>
          <label
            className="block font-medium mb-2"
            style={{ color: "#3A4B41" }}
          >
            Or Upload File
          </label>
          <input
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="block w-full text-sm border rounded-lg cursor-pointer file:mr-4 file:py-2 file:px-4 
            file:rounded-lg file:border-0 file:text-sm file:font-semibold"
            style={{
              borderColor: "#E6CFA7",
              color: "#3A4B41",
              backgroundColor: "#F5E6CC",
            }}
          />
        </div>

        {/* YouTube Link Input */}
        <div>
          <label
            className="block font-medium mb-2"
            style={{ color: "#3A4B41" }}
          >
            YouTube Link
          </label>
          <input
            type="url"
            placeholder="https://youtube.com/..."
            value={videoLink}
            onChange={handleLinkChange}
            className="text-sm w-full p-3 border rounded-lg focus:outline-none focus:ring-2"
            style={{
              borderColor: "#E6CFA7",
              color: "#3A4B41",
              backgroundColor: "#FAF1E3",
            }}
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full py-3 rounded-xl font-semibold shadow-md transition-all duration-300"
          style={{
            backgroundColor: "#3A4B41",
            color: "#F5E6CC",
          }}
        >
          🚀 Process Video
        </button>
      </form>
    </div>
  );
}
