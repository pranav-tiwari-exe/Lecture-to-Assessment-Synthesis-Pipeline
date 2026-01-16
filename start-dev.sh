#!/bin/bash

# Start all services for development

echo "🚀 Starting RPKP Development Environment..."
echo ""

# Start MongoDB (if not running)
echo "📊 Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB manually."
    echo "   On Windows: Start MongoDB service"
    echo "   On Linux/Mac: mongod"
else
    echo "✅ MongoDB is running"
fi

# Start Backend
echo ""
echo "🔧 Starting Backend Server..."
cd backend
npm start &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start ML Service
echo ""
echo "🤖 Starting ML Service..."
cd ml
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
uvicorn server:app --reload --port 8000 &
ML_PID=$!
cd ..

# Wait a bit for ML service to start
sleep 3

# Start Frontend
echo ""
echo "🎨 Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Services:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:5000"
echo "   ML Service: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $ML_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
