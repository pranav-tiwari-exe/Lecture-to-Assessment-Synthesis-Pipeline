# Backend Server

Express.js backend server for the RPKP project that handles YouTube transcript extraction, MCQ generation, and MongoDB storage.

## Features

- ✅ Receive YouTube URL from frontend
- ✅ Extract transcript using `youtube-transcript` library
- ✅ Send transcript to ML service for MCQ generation
- ✅ Store generated MCQs in MongoDB
- ✅ Cache existing MCQs to avoid regenerating

## Setup

1. Install dependencies:
```bash
npm install
```

2. Make sure MongoDB is running:
```bash
# Default MongoDB connection: mongodb://localhost:27017
```

3. Configure environment variables (optional):
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Start the server:
```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

## API Endpoints

### POST `/generate`
Generate MCQs from YouTube URL or transcript text.

**Request Body:**
```json
{
  "youtubeUrl": "https://www.youtube.com/watch?v=VIDEO_ID",
  "numQuestions": 5
}
```

Or with transcript text:
```json
{
  "text": "Your transcript text here...",
  "numQuestions": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "mcqs": [...],
    "mcq_count": 5,
    "video_id": "VIDEO_ID",
    "youtube_url": "https://...",
    "saved_to_db": true,
    "db_id": "MONGODB_ID"
  }
}
```

### GET `/health`
Health check endpoint.

## Configuration

- **MongoDB URI**: `mongodb://localhost:27017` (default)
- **Database Name**: `rpkp_db` (default)
- **ML Service URL**: `http://localhost:8000` (default)
- **Server Port**: `5000` (default)

## Dependencies

- `express` - Web server framework
- `mongodb` - MongoDB driver
- `youtube-transcript` - YouTube transcript extraction
- `axios` - HTTP client for ML service
- `cors` - CORS middleware
