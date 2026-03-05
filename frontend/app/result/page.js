"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar';

export default function ResultPage() {
  const [mcqData, setMcqData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const data = sessionStorage.getItem('mcqData');
    if (data) {
      try {
        const parsed = JSON.parse(data);
        // The data is directly parsed as { provider: "...", response: [...] }
        setMcqData(parsed);
      } catch (error) {
        console.error('Error parsing MCQ data:', error);
      }
    }
    setLoading(false);
  }, []);

  const handleNewGeneration = () => {
    sessionStorage.removeItem('mcqData');
    // Fallback standard routing since Next Router was causing compilation errors
    window.location.href = '/generate'; 
  };

  if (loading) {
    return (
      <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">⏳</div>
          <p>Loading results...</p>
        </div>
      </div>
    );
  }

  // FIXED: Check for mcqData.response instead of mcqData.mcqs
  if (!mcqData || !mcqData.response || mcqData.response.length === 0) {
    return (
      <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40 min-h-screen">
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <h1 className="text-3xl font-bold mb-4">No Results Found</h1>
          <p className="text-gray-600 mb-8">
            It seems no MCQs were generated or the results have expired.
          </p>
          <button
            onClick={handleNewGeneration}
            className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors"
          >
            Generate New MCQs
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Generated <span className="text-orange-600">MCQs</span>
              </h1>
              <p className="text-gray-600 font-medium">
                {mcqData.response.length} question{mcqData.response.length !== 1 ? 's' : ''} generated
                {/* Dynamically show the AI Provider */}
                {mcqData.provider && <span className="text-neutral-400 ml-2">| via {mcqData.provider}</span>}
              </p>
            </div>
            <button
              onClick={handleNewGeneration}
              className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors shadow-sm whitespace-nowrap"
            >
              Generate New
            </button>
          </div>
        </motion.div>

        {/* MCQs List */}
        <div className="space-y-6">
          {mcqData.response.map((mcq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: Math.min(index * 0.1, 0.5) }} // Cap animation delay
              className="bg-white shadow-sm rounded-xl p-6 border border-gray-200"
            >
              {/* Question */}
              <div className="mb-5">
                <div className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </span>
                  <h3 className="text-xl font-semibold text-gray-800 flex-1 leading-snug pt-1">
                    {mcq.question}
                  </h3>
                </div>
              </div>

              {/* Options */}
              <div className="ml-11 space-y-3">
                {mcq.options?.map((optionText, optIndex) => {
                  const isCorrect = optionText === mcq.correctAnswer;
                  const letter = String.fromCharCode(65 + optIndex); // Converts 0->A, 1->B, 2->C...

                  return (
                    <div
                      key={optIndex}
                      className={`p-3.5 rounded-lg border-2 transition-all ${
                        isCorrect
                          ? 'bg-green-50 border-green-500'
                          : 'bg-white border-gray-200'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={`flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm ${
                            isCorrect
                              ? 'bg-green-500 text-white'
                              : 'bg-gray-100 text-gray-600 border border-gray-300'
                          }`}
                        >
                          {letter}
                        </span>
                        <span className={`text-base ${isCorrect ? 'font-semibold text-green-900' : 'text-gray-700'}`}>
                          {optionText}
                        </span>
                        {isCorrect && (
                          <span className="ml-auto text-green-600 font-semibold text-sm bg-green-100 px-3 py-1 rounded-full">
                            ✓ Correct Answer
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center text-gray-400 font-medium text-sm pb-8"
        >
          Powered by AI • Generated in seconds
        </motion.div>
      </div>
    </div>
  );
}