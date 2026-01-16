# RPKP - YouTube MCQ Generator

A full-stack application that generates Multiple Choice Questions (MCQs) from YouTube video transcripts using advanced AI/ML models.

## 🏗️ Architecture

```
Frontend (Next.js) → Backend (Express.js) → ML Service (FastAPI) → MongoDB
```

1. **Frontend**: Next.js React application with modern UI
2. **Backend**: Express.js API server handling requests and MongoDB operations
3. **ML Service**: FastAPI service using NLP models to generate MCQs
4. **Database**: MongoDB for storing generated MCQs

## ✨ Features

- 📹 Extract transcripts from YouTube videos
- 🤖 Generate high-quality MCQs using AI models
- 💾 Store MCQs in MongoDB with caching
- 🎨 Modern, responsive UI with dark mode support
- ⚡ Fast generation with semantic similarity
- 📊 Display results with explanations and difficulty levels

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB (running locally or connection string)
- npm or yarn

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RPKP
```

### 2. Backend Setup

```bash
cd backend
npm install

# Optional: Create .env file
# MONGODB_URI=mongodb://localhost:27017
# DB_NAME=rpkp_db
# PORT=5000
# ML_SERVICE_URL=http://localhost:8000

npm start
```

Backend will run on `http://localhost:5000`

### 3. ML Service Setup

```bash
cd ml

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (if needed)
python -m spacy download en_core_web_sm

# Start ML service
uvicorn server:app --reload --port 8000
```

ML Service will run on `http://localhost:8000`

### 4. Frontend Setup

```bash
cd frontend
npm install

# Optional: Create .env.local file
# NEXT_PUBLIC_API_URL=http://localhost:5000

npm run dev
```

Frontend will run on `http://localhost:3000`

## 📖 Usage

1. Open `http://localhost:3000` in your browser
2. Navigate to the Generate page
3. Enter a YouTube URL or paste a transcript
4. Click "Process Content"
5. Wait for MCQs to be generated (may take a few minutes)
6. View results on the Result page

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
MONGODB_URI=mongodb://localhost:27017
DB_NAME=rpkp_db
ML_SERVICE_URL=http://localhost:8000
PORT=5000
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 📁 Project Structure

```
RPKP/
├── frontend/          # Next.js frontend application
│   ├── app/          # Next.js app router pages
│   ├── components/   # React components
│   └── lib/          # Utility functions and API clients
├── backend/          # Express.js backend server
│   ├── config/       # Configuration files (DB, etc.)
│   ├── models/       # MongoDB models
│   └── server.js     # Main server file
└── ml/               # FastAPI ML service
    ├── scripts/      # ML scripts and models
    └── server.py     # FastAPI server
```

## 🛠️ Technologies Used

### Frontend
- Next.js 15
- React 19
- Tailwind CSS
- Framer Motion
- Axios

### Backend
- Express.js 5
- MongoDB
- Axios
- youtube-transcript

### ML Service
- FastAPI
- PyTorch
- Transformers (Hugging Face)
- spaCy
- Sentence Transformers

## 📝 API Endpoints

### Backend (`http://localhost:5000`)

- `POST /generate` - Generate MCQs from YouTube URL or transcript
- `GET /health` - Health check

### ML Service (`http://localhost:8000`)

- `POST /generate_mcqs` - Generate MCQs from transcript
- `POST /extract_transcript` - Extract transcript from YouTube URL
- `GET /health` - Health check

## 🐛 Troubleshooting

### Backend Issues
- Ensure MongoDB is running
- Check if port 5000 is available
- Verify ML service is accessible

### ML Service Issues
- Ensure all Python dependencies are installed
- Download spaCy model: `python -m spacy download en_core_web_sm`
- Check if port 8000 is available
- First run will download ML models (may take time)

### Frontend Issues
- Clear browser cache
- Check if backend is running
- Verify API URL in environment variables

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For support, please open an issue in the repository.
