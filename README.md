# Lecture-to-Assessment Synthesis Pipeline (RPKP)

A full-stack application that automatically generates Multiple Choice Questions (MCQs) from YouTube video transcripts using advanced AI/ML models. This project reduces manual effort for educators by automating assessment generation and enabling scalable, intelligent learning workflows.

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
- 🤖 Generate high-quality MCQs using AI models (T5, RoBERTa, Sentence Transformers)
- 💾 Store MCQs in MongoDB with caching
- 🎨 Modern, responsive UI with dark mode support
- ⚡ Fast generation with semantic similarity
- 📊 Display results with explanations and difficulty levels
- 🔄 Modular and extensible architecture
- 🧠 NLP-based text processing and analysis

## 🚀 Quick Start

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB (running locally or connection string)
- npm or yarn

### 1. Clone the Repository

```bash
git clone https://github.com/pranav-tiwari-exe/Lecture-to-Assessment-Synthesis-Pipeline.git
cd Lecture-to-Assessment-Synthesis-Pipeline
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
Lecture-to-Assessment-Synthesis-Pipeline/
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

## 👥 Team Contribution

This project was developed as part of a collaborative team effort. Contributions include:

- **Backend Integration**: Express.js API development, MongoDB integration, YouTube transcript extraction
- **ML Pipeline**: NLP model integration (T5, RoBERTa), question generation, distractor creation
- **Frontend Development**: Next.js UI, user interface design, API integration
- **System Architecture**: Microservices design, service communication, error handling
- **Testing & Debugging**: End-to-end testing, bug fixes, performance optimization

This experience provided hands-on experience with:
- NLP-based applications and transformer models
- Multi-module project architecture
- Backend–ML integration
- Collaborative development workflows

## 🎓 Learning Outcomes

- Hands-on experience with NLP-based applications
- Exposure to multi-module project architecture
- Practical understanding of backend–ML integration
- Experience working in a collaborative development environment
- Full-stack development with modern technologies
- AI/ML model integration and optimization

## 🚀 Future Enhancements

- Improve question quality using advanced NLP or transformer-based models
- Add support for audio-to-text processing
- Introduce dashboards for instructors and students
- Enhance evaluation metrics for generated assessments
- Multi-language support
- Batch processing capabilities
- Export features (PDF, CSV)
- User authentication and personalization

## 📄 License

This project is open source and available under the MIT License. Intended for educational and academic purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

For support, please open an issue in the repository.
