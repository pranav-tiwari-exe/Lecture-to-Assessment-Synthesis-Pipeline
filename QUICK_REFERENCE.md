# Quick Reference - Interview Cheat Sheet

## 🎯 30-Second Elevator Pitch
"RPKP is an AI-powered MCQ generator that extracts YouTube video transcripts and automatically generates high-quality multiple-choice questions using advanced NLP models like T5 and RoBERTa. It's a full-stack microservices application built with Next.js, Express.js, and FastAPI."

## 📊 Architecture at a Glance

```
User → Frontend (Next.js:3000) 
    → Backend (Express:5000) 
    → ML Service (FastAPI:8000) 
    → MongoDB
```

## 🔑 Key Technologies

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 15, React 19 | SSR, fast routing, modern |
| Backend | Express.js 5, Node.js | Lightweight, RESTful APIs |
| ML Service | FastAPI, PyTorch | Fast, async, ML ecosystem |
| Database | MongoDB | Flexible schema, scalable |
| Models | T5, RoBERTa, Sentence Transformers | State-of-the-art NLP |

## 🔄 Complete Flow (1 Sentence Each)

1. **User Input**: User enters YouTube URL in frontend
2. **API Call**: Frontend sends POST request to backend
3. **Video ID Extraction**: Backend parses URL to get video ID
4. **Cache Check**: Backend checks MongoDB for existing MCQs
5. **Transcript Extraction**: Backend uses youtube-transcript library
6. **ML Request**: Backend sends transcript to ML service
7. **Preprocessing**: ML service cleans and chunks transcript semantically
8. **Question Generation**: T5 model generates questions from highlighted answers
9. **Validation**: RoBERTa validates question answerability
10. **Distractor Generation**: Multi-strategy approach (entity type, similarity, numeric)
11. **Storage**: Backend saves MCQs to MongoDB
12. **Response**: Backend returns MCQs to frontend
13. **Display**: Frontend shows results on result page

## 🧠 Key Concepts

### Answer Highlighting
- Wrap answer in `<hl>` tags
- T5 model trained for this format
- Guides question generation

### Semantic Chunking
- Group sentences by meaning (not size)
- Uses embeddings and cosine similarity
- Maintains topic coherence

### Multi-Strategy Distractors
1. Entity type matching (PERSON → PERSON)
2. Semantic similarity (0.2-0.8 range)
3. Numeric variations (half, double, ±1)

### Quality Validation
- Format check (ends with ?)
- Length check (minimum words)
- RoBERTa answerability (confidence >0.35)
- Semantic deduplication (similarity <0.90)

## 💾 Data Structures

### Backend Request
```json
{
  "youtubeUrl": "https://youtube.com/watch?v=abc123",
  "numQuestions": 5
}
```

### Backend Response
```json
{
  "success": true,
  "data": {
    "mcqs": [...],
    "mcq_count": 5,
    "video_id": "abc123",
    "saved_to_db": true
  }
}
```

### MCQ Object
```json
{
  "question": "Who created Python?",
  "options": {
    "A": "Guido van Rossum",
    "B": "James Gosling",
    "C": "Brendan Eich",
    "D": "Linus Torvalds"
  },
  "correct_answer": "A",
  "explanation": "Python was created by Guido van Rossum...",
  "difficulty": "Medium",
  "question_type": "Factual"
}
```

## 🎤 Common Questions & Answers

**Q: What does your project do?**
A: Generates MCQs from YouTube transcripts using AI. User provides URL, system extracts transcript, processes through NLP models, generates questions with distractors.

**Q: Why microservices?**
A: Separation of concerns, independent scaling, technology flexibility (Python for ML, Node.js for backend).

**Q: How does question generation work?**
A: Clean transcript → semantic chunking → extract answers → highlight answers → T5 generates questions → RoBERTa validates → generate distractors → format MCQs.

**Q: How do you ensure quality?**
A: Multi-step validation: format checks, RoBERTa answerability validation (confidence >0.35), semantic deduplication, distractor validation.

**Q: What's the biggest challenge?**
A: Ensuring question quality and generating plausible distractors. Solved with multi-strategy approach and validation pipeline.

**Q: How would you scale it?**
A: Load balancers, containerization (Docker), orchestration (Kubernetes), database replication, Redis caching, queue system for async processing.

## 🔧 Technical Details

### Models Used
- **T5-base-qa-qg-hl**: Question generation (highlighted answers)
- **RoBERTa-base-squad2**: Question answering/validation
- **all-MiniLM-L6-v2**: Semantic embeddings
- **spaCy en_core_web_sm**: Named entity recognition

### API Endpoints
- `POST /generate` (Backend): Main endpoint
- `POST /generate_mcqs` (ML): MCQ generation
- `GET /health`: Health checks

### Caching Strategy
- Check MongoDB by video ID first
- Return cached if exists
- Save after generation
- Reduces ML service load

## 🚀 Improvements to Mention
1. User authentication
2. Batch processing queue
3. Export features (PDF, CSV)
4. Multi-language support
5. Direct video upload
6. User feedback loop
7. Analytics dashboard

## 📈 Performance Metrics
- **Transcript Extraction**: ~5-10 seconds
- **MCQ Generation**: 2-5 minutes (depends on transcript length)
- **Cache Hit**: <1 second
- **First Request**: Slower (model loading)

## 🎯 Key Strengths to Emphasize
1. Full-stack development
2. AI/ML integration
3. Microservices architecture
4. Production-ready (error handling, caching)
5. Modern tech stack
6. Problem-solving (quality, distractors)

## ⚠️ Common Pitfalls to Avoid
- Don't say "I just followed a tutorial"
- Don't claim you did everything alone (mention learning resources)
- Don't oversell - be honest about limitations
- Don't forget to mention challenges and solutions

## 🎓 Technical Terms to Use
- Microservices architecture
- RESTful APIs
- Semantic similarity
- Embeddings
- Named Entity Recognition (NER)
- Question-Answering (QA)
- Natural Language Processing (NLP)
- Transfer learning
- Model fine-tuning
- Horizontal scaling
- Caching strategy
- Error handling
- Async processing

## 📝 Project Stats to Mention
- 3 services (Frontend, Backend, ML)
- 4 NLP models integrated
- Multiple validation steps
- Caching for performance
- Production-ready error handling

---

## 🎤 Opening Statement Template

"RPKP is a full-stack AI application I built that automatically generates Multiple Choice Questions from YouTube video transcripts. It uses a microservices architecture with three main components: a Next.js frontend for the user interface, an Express.js backend that orchestrates requests and handles YouTube transcript extraction, and a FastAPI-based ML service that uses advanced NLP models like T5 and RoBERTa to generate high-quality questions. The system includes intelligent distractor generation, quality validation, and MongoDB caching for performance. I chose this project to demonstrate my skills in full-stack development, AI/ML integration, and system design."

---

**Remember: Be confident, explain your thought process, and show enthusiasm!**
