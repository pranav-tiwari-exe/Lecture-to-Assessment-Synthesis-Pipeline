"use client";

import { useState } from "react";
import { motion } from 'framer-motion';

export default function VideoInput() {
  const [videoLink, setVideoLink] = useState("");
  const [videoFile, setVideoFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [activeInput, setActiveInput] = useState("transcript");

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
      setVideoLink("");
      setTranscript("");
      setActiveInput("file");
    }
  };

  const handleLinkChange = (e) => {
    setVideoLink(e.target.value);
    setVideoFile(null);
    setTranscript("");
    setActiveInput("link");
  };

  const handleTranscriptChange = (e) => {
    setTranscript(e.target.value);
    setVideoFile(null);
    setVideoLink(null);
    setActiveInput("transcript");
  }; 

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!videoLink && !videoFile && !transcript) {
      alert("Please provide a transcript, YouTube link, or upload a video file");
      return;
    }

    console.log("Video Link:", videoLink);
    console.log("Video File:", videoFile);
    console.log("Transcript:", transcript);
  };

  return (
    <motion.div 
      className="max-w-4xl mx-auto px-4 py-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      {/* Header */}
      <motion.div 
        className="text-center mb-12"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
          Process Your <span className="text-orange-600">Learning</span> Content
        </h1>
        <p className="max-w-2xl mx-auto text-lg">
          Upload transcripts, files or YouTube links to generate insightful questions.
        </p>
      </motion.div>

      {/* Main Input Container */}
      <motion.div 
        className="bg-white shadow-lg border-0 rounded-xl border-neutral-200 overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4 }}
      >
        {/* Input Type Selector */}
        <div className="flex border-b border-neutral-200">
          <button
            type="button"
            onClick={() => setActiveInput("transcript")}
            className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
              activeInput === "transcript"
                ? "bg-black text-white"
                : "text-neutral-600 hover:text-black hover:bg-neutral-50"
            }`}
          >
            📝 Transcript
          </button>
          <button
            type="button"
            onClick={() => setActiveInput("file")}
            className={`flex-1 px-6 py-4 text-sm font-medium transition-colors border-x border-neutral-200 ${
              activeInput === "file"
                ? "bg-black text-white"
                : "text-neutral-600 hover:text-black hover:bg-neutral-50"
            }`}
          >
            📁 Upload File
          </button>
          <button
            type="button"
            onClick={() => setActiveInput("link")}
            className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${
              activeInput === "link"
                ? "bg-black text-white"
                : "text-neutral-600 hover:text-black hover:bg-neutral-50"
            }`}
          >
            🔗 YouTube Link
          </button>
        </div>

        {/* Input Area */}
        <form onSubmit={handleSubmit} className="relative text-zinc-600">
          <motion.div 
            className="p-6"
            key={activeInput}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
          >
            {activeInput === "transcript" && (
              <div className="relative">
                <textarea
                  placeholder="Paste your transcript here and we'll generate questions from it..."
                  value={transcript}
                  onChange={handleTranscriptChange}
                  rows={6}
                  className="w-full resize-none border-0 text-lg placeholder-neutral-400 focus:outline-none focus:ring-0 bg-transparent"
                  style={{ fontFamily: 'Outfit, sans-serif' }}
                />
              </div>
            )}

            {activeInput === "file" && (
              <div className="relative">
                <div className="border-2 border-dashed border-neutral-300 rounded-xl p-8 text-center hover:border-neutral-400 transition-colors">
                  <input
                    type="file"
                    accept="video/*"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  <div className="flex flex-col items-center">
                    <div className="text-4xl mb-4">📝</div>
                    <p className="text-lg text-neutral-600 mb-2">
                      {videoFile ? videoFile.name : "Click to upload a file"}
                    </p>
                    <p className="text-sm text-neutral-400">
                      Supports *.pdf and *.txt formats
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeInput === "link" && (
              <div className="relative">
                <input
                  type="url"
                  placeholder="https://youtube.com/watch?v=..."
                  value={videoLink}
                  onChange={handleLinkChange}
                  className="w-full text-lg border-0 placeholder-neutral-400 focus:outline-none focus:ring-0 bg-transparent py-2"
                  style={{ fontFamily: 'Outfit, sans-serif' }}
                />
              </div>
            )}
          </motion.div>

          {/* Submit Button */}
          <div className="px-6 pb-6">
            <motion.button
              type="submit"
              className="w-full bg-black text-white py-4 rounded-xl font-semibold text-lg shadow-md hover:bg-neutral-800 transition-all duration-300 flex items-center justify-center gap-2"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={!transcript && !videoFile && !videoLink}
            >
              <span>🚀 Process Content</span>
            </motion.button>
          </div>
        </form>
      </motion.div>

      {/* Footer Text */}
      <motion.p
        className="text-center text-neutral-500 mt-6 text-sm"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.8 }}
      >
        Powered by AI • Generate insightful questions in seconds
      </motion.p>
    </motion.div>
  );
}
