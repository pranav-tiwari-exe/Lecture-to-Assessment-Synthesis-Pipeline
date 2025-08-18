import express from "express";
import cors from "cors";
import axios from "axios";
import { YoutubeTranscript } from "youtube-transcript";

const app = express();
app.use(cors());
app.use(express.json());

// ML service endpoint (running FastAPI on 8001)
const ML_SERVICE_URL = "http://localhost:8001/generate";

// Route: Generate questions
app.post("/generate", async (req, res) => {
  try {
    const { youtubeUrl, text, numQuestions = 5 } = req.body;

    if (!youtubeUrl && !text) {
      return res.status(400).json({ success: false, error: "Provide youtubeUrl or text" });
    }

    let script = text;

    // If YouTube URL → fetch transcript
    if (youtubeUrl) {
      const videoId = new URL(youtubeUrl).searchParams.get("v");
      if (!videoId) {
        return res.status(400).json({ success: false, error: "Invalid YouTube URL" });
      }

      const transcript = await YoutubeTranscript.fetchTranscript(videoId);
      script = transcript.map((t) => t.text).join(" ");
    }

    // Call ML microservice
    const response = await axios.post(ML_SERVICE_URL, {
      text: script,
      num_questions: numQuestions,
    });

    res.json({ success: true, data: response.data });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ success: false, error: "Something went wrong" });
  }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Backend running at http://localhost:${PORT}`);
});
