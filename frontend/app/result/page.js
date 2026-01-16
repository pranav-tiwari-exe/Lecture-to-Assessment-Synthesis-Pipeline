"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';
import { motion } from 'framer-motion';

export default function ResultPage() {
  const router = useRouter();
  const [mcqData, setMcqData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const data = sessionStorage.getItem('mcqData');
    if (data) {
      try {
        const parsed = JSON.parse(data);
        // Backend returns { success: true, data: { mcqs: [...], ... } }
        // So we need to extract the inner data object
        setMcqData(parsed.data || parsed);
      } catch (error) {
        console.error('Error parsing MCQ data:', error);
      }
    }
    setLoading(false);
  }, []);

  const handleNewGeneration = () => {
    sessionStorage.removeItem('mcqData');
    router.push('/generate');
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

  if (!mcqData || !mcqData.mcqs || mcqData.mcqs.length === 0) {
    return (
      <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40 min-h-screen">
        <Navbar />
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
    <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40 min-h-screen">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Generated <span className="text-orange-600">MCQs</span>
              </h1>
              <p className="text-gray-600">
                {mcqData.mcq_count} question{mcqData.mcq_count !== 1 ? 's' : ''} generated
                {mcqData.video_id && ` from YouTube video`}
              </p>
            </div>
            <button
              onClick={handleNewGeneration}
              className="bg-black text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition-colors"
            >
              Generate New
            </button>
          </div>
        </motion.div>

        {/* MCQs List */}
        <div className="space-y-6">
          {mcqData.mcqs.map((mcq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white shadow-lg rounded-xl p-6 border border-gray-200"
            >
              {/* Question */}
              <div className="mb-4">
                <div className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </span>
                  <h3 className="text-xl font-semibold text-gray-800 flex-1">
                    {mcq.question}
                  </h3>
                </div>
                
                {/* Difficulty and Type */}
                {(mcq.difficulty || mcq.question_type) && (
                  <div className="ml-11 mt-2 flex gap-2 flex-wrap">
                    {mcq.difficulty && (
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        mcq.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                        mcq.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {mcq.difficulty}
                      </span>
                    )}
                    {mcq.question_type && (
                      <span className="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
                        {mcq.question_type}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Options */}
              <div className="ml-11 space-y-2">
                {Object.entries(mcq.options || {}).map(([key, value]) => {
                  const isCorrect = key === mcq.correct_answer;
                  return (
                    <div
                      key={key}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        isCorrect
                          ? 'bg-green-50 border-green-500'
                          : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center font-bold text-sm ${
                            isCorrect
                              ? 'bg-green-500 text-white'
                              : 'bg-gray-300 text-gray-700'
                          }`}
                        >
                          {key}
                        </span>
                        <span className={isCorrect ? 'font-semibold text-green-900' : 'text-gray-700'}>
                          {value}
                        </span>
                        {isCorrect && (
                          <span className="ml-auto text-green-600 font-semibold text-sm">
                            ✓ Correct Answer
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Explanation */}
              {mcq.explanation && (
                <div className="ml-11 mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm text-blue-900">
                    <span className="font-semibold">Explanation: </span>
                    {mcq.explanation}
                  </p>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center text-gray-500 text-sm"
        >
          Powered by AI • Generated in seconds
        </motion.div>
      </div>
    </div>
  );
}
