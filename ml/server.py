from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re
from urllib.parse import urlparse, parse_qs
from scripts.TranscriptQAGenerator import TranscriptQAGenerator

app = FastAPI()

class LinkRequest(BaseModel):
    link: str

class TranscriptRequest(BaseModel):
    transcript: str
    max_mcqs: int = 100 
    min_distractors: int = 1

def is_youtube_url(url: str) -> bool:
    youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    return bool(re.match(youtube_pattern, url))

def extract_video_id(url: str) -> str:
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        parsed_url = urlparse(url)
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/') or parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

@app.post("/extract_transcript")
def extract_transcript(request: LinkRequest):
    try:
        if not is_youtube_url(request.link):
            raise HTTPException(status_code=400, detail="Invalid YouTube URL. Please provide a valid YouTube video link.")

        video_id = extract_video_id(request.link)
        if not video_id:
            raise HTTPException(status_code=400, detail="Could not extract video ID from the provided URL.")

        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id, languages=['en'])

        # Combine transcript text from snippet.text instead of entry['text']
        full_transcript = " ".join([snippet.text for snippet in transcript_data])

        return {
            "success": True,
            "video_id": video_id,
            "url": request.link,
            "transcript": full_transcript,
            "transcript_segments": len(transcript_data)
        }

    except NoTranscriptFound:
        raise HTTPException(
            status_code=404,
            detail="Transcript is not available in English. Currently, this application supports only English transcripts."
        )
    except TranscriptsDisabled:
        raise HTTPException(
            status_code=403,
            detail="Transcripts are disabled for this video or no transcript is available."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching the transcript: {str(e)}"
        )

@app.post("/generate_mcqs")
def generate_mcqs(request: TranscriptRequest):
    if not request.transcript or len(request.transcript.strip()) == 0:
        raise HTTPException(status_code=400, detail="Transcript text is required.")

    try:
        mcqs = TranscriptQAGenerator().generate_qa_pairs(
            transcript=request.transcript,
            max_mcqs=request.max_mcqs,
            min_distractors=request.min_distractors
        )
        return {
            "success": True,
            "mcq_count": len(mcqs),
            "mcqs": mcqs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating MCQs: {str(e)}")