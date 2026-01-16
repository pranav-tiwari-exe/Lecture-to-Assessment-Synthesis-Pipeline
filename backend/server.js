import express from "express";
import cors from "cors";
import axios from "axios";
import { YoutubeTranscript } from "youtube-transcript";
import { connectDB } from "./config/db.js";
import { saveMCQs, getMCQsByVideoId } from "./models/mcq.js";

const app = express();
app.use(cors());
app.use(express.json());

// ML service endpoint (running FastAPI on port 8000)
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://localhost:8000";

// Helper function to extract video ID from YouTube URL
function extractVideoId(url) {
  try {
    const urlObj = new URL(url);
    if (urlObj.hostname.includes('youtu.be')) {
      return urlObj.pathname.slice(1).split('?')[0];
    } else if (urlObj.hostname.includes('youtube.com')) {
      return urlObj.searchParams.get('v');
    }
    return null;
  } catch (error) {
    // Try regex approach as fallback
    const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
  }
}

// Connect to MongoDB on startup
connectDB().catch(console.error);

// Route: Generate questions from YouTube URL
app.post("/generate", async (req, res) => {
  try {
    const { youtubeUrl, text, numQuestions = 5 } = req.body;

    if (!youtubeUrl && !text) {
      return res.status(400).json({ 
        success: false, 
        error: "Please provide either a YouTube URL or transcript text" 
      });
    }

    let transcript = text;
    let videoId = null;

    // If YouTube URL provided → extract transcript
    if (youtubeUrl) {
      try {
        videoId = extractVideoId(youtubeUrl);
        
        if (!videoId) {
          return res.status(400).json({ 
            success: false, 
            error: "Invalid YouTube URL. Please provide a valid YouTube video link." 
          });
        }

        console.log(`📹 Extracting transcript for video ID: ${videoId}`);
        
        // Fetch transcript using youtube-transcript library
        const transcriptData = await YoutubeTranscript.fetchTranscript(videoId);
        transcript = transcriptData.map((t) => t.text).join(" ");
        
        if (!transcript || transcript.trim().length === 0) {
          return res.status(400).json({ 
            success: false, 
            error: "Could not extract transcript from this video. Transcript may not be available." 
          });
        }

        console.log(`✅ Transcript extracted (${transcript.length} characters)`);
        
        // Check if MCQs already exist for this video
        const existingMCQs = await getMCQsByVideoId(videoId);
        if (existingMCQs) {
          console.log(`📋 Found existing MCQs for video ${videoId}`);
          return res.json({
            success: true,
            data: {
              mcqs: existingMCQs.mcqs,
              mcq_count: existingMCQs.mcqCount,
              video_id: videoId,
              youtube_url: youtubeUrl,
              cached: true
            }
          });
        }
      } catch (error) {
        console.error("❌ Error extracting transcript:", error.message);
        return res.status(400).json({ 
          success: false, 
          error: `Failed to extract transcript: ${error.message}` 
        });
      }
    }

    if (!transcript || transcript.trim().length === 0) {
      return res.status(400).json({ 
        success: false, 
        error: "Transcript is empty. Please provide valid content." 
      });
    }

    // Call ML microservice to generate MCQs
    console.log(`🤖 Sending transcript to ML service for MCQ generation...`);
    
    try {
      const mlResponse = await axios.post(`${ML_SERVICE_URL}/generate_mcqs`, {
        transcript: transcript,
        max_mcqs: numQuestions,
        min_distractors: 2
      }, {
        timeout: 300000 // 5 minutes timeout for ML processing
      });

      const mcqsData = mlResponse.data;

      if (!mcqsData.success || !mcqsData.mcqs || mcqsData.mcqs.length === 0) {
        return res.status(500).json({ 
          success: false, 
          error: "ML service did not generate any MCQs. Please try again." 
        });
      }

      console.log(`✅ Generated ${mcqsData.mcq_count} MCQs from ML service`);

      // Store MCQs in MongoDB
      let savedData = null;
      if (videoId || youtubeUrl) {
        try {
          savedData = await saveMCQs({
            youtubeUrl: youtubeUrl || null,
            videoId: videoId || null,
            transcript: transcript,
            mcqs: mcqsData.mcqs
          });
          console.log(`💾 MCQs saved to MongoDB`);
        } catch (dbError) {
          console.error("⚠️ Warning: Failed to save to MongoDB:", dbError.message);
          // Continue even if DB save fails
        }
      }

      // Return response to frontend
      return res.json({
        success: true,
        data: {
          mcqs: mcqsData.mcqs,
          mcq_count: mcqsData.mcq_count,
          video_id: videoId || null,
          youtube_url: youtubeUrl || null,
          saved_to_db: savedData !== null,
          db_id: savedData?.id || null
        }
      });
    } catch (mlError) {
      console.error("❌ ML service error:", mlError.message);
      
      if (mlError.code === 'ECONNREFUSED') {
        return res.status(503).json({ 
          success: false, 
          error: "ML service is not available. Please ensure it's running on port 8000." 
        });
      }
      
      if (mlError.response) {
        return res.status(mlError.response.status || 500).json({ 
          success: false, 
          error: mlError.response.data?.detail || mlError.response.data?.error || "ML service error" 
        });
      }
      
      return res.status(500).json({ 
        success: false, 
        error: `ML service error: ${mlError.message}` 
      });
    }
  } catch (err) {
    console.error("❌ Server error:", err);
    return res.status(500).json({ 
      success: false, 
      error: err.message || "Internal server error" 
    });
  }
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ 
    success: true, 
    message: "Backend server is running",
    timestamp: new Date().toISOString()
  });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Backend running at http://localhost:${PORT}`);
  console.log(`📊 MongoDB: ${process.env.MONGODB_URI || 'mongodb://localhost:27017'}`);
  console.log(`🤖 ML Service: ${ML_SERVICE_URL}`);
});
