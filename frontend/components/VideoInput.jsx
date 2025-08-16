"use client";

import { useState } from "react";

export default function VideoInput() {
  const [videoLink, setVideoLink] = useState("");
  const [videoFile, setVideoFile] = useState(null);
  const [transcript,setTranscript] = useState("");

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
    }
  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Upload Lecture Video</h2>
      <form onSubmit={handleSubmit} className="space-y-4">

        {/* Conditional Input */}
              <div>
            <label className="block text-gray-700 mb-2">Transcript</label>
            <input
              type="text"
              placeholder="transcript..."
              value={transcript}
              onChange={handleTranscriptChange}
              className="text-black text-sm w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-gray-700 mb-2">YouTube Link</label>
            <input
              type="url"
              placeholder="https://youtube.com/..."
              value={videoLink}
              onChange={handleLinkChange}
              className="text-blue-500 text-sm w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        
          <div>
            <label className="block text-gray-700 mb-2">Upload MP4 File</label>
            <input
              type="file"
              accept="video/mp4"
              onChange={handleFileChange}
              className="w-full p-2 border rounded-lg"
            />
          </div>
    

        {/* Switch Button */}
       

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition"
        >
          Process Video
        </button>
      </form>
    </div>
  );
}
