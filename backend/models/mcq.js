import { getDB } from '../config/db.js';

const COLLECTION_NAME = 'mcqs';

export async function saveMCQs(data) {
  try {
    const db = await getDB();
    const collection = db.collection(COLLECTION_NAME);
    
    const document = {
      youtubeUrl: data.youtubeUrl,
      videoId: data.videoId,
      transcript: data.transcript,
      mcqs: data.mcqs,
      mcqCount: data.mcqs?.length || 0,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    const result = await collection.insertOne(document);
    console.log(`✅ Saved ${data.mcqs?.length || 0} MCQs to MongoDB with ID: ${result.insertedId}`);
    
    return {
      id: result.insertedId,
      ...document
    };
  } catch (error) {
    console.error('❌ Error saving MCQs to MongoDB:', error);
    throw error;
  }
}

export async function getMCQsByVideoId(videoId) {
  try {
    const db = await getDB();
    const collection = db.collection(COLLECTION_NAME);
    
    const result = await collection.findOne({ videoId });
    return result;
  } catch (error) {
    console.error('❌ Error fetching MCQs from MongoDB:', error);
    throw error;
  }
}

export async function getAllMCQs(limit = 50) {
  try {
    const db = await getDB();
    const collection = db.collection(COLLECTION_NAME);
    
    const results = await collection
      .find({})
      .sort({ createdAt: -1 })
      .limit(limit)
      .toArray();
    
    return results;
  } catch (error) {
    console.error('❌ Error fetching all MCQs from MongoDB:', error);
    throw error;
  }
}
