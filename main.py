import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_service import transcribe_audio, extract_tasks_from_transcript

app = FastAPI(title="ActionSync API")

# Allow browser frontend to connect without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...)):
    # Create a temporary file path preserving the original extension
    file_ext = os.path.splitext(file.filename)[1] or ".m4a"
    temp_file_path = f"temp_upload{file_ext}"

    try:
        # Save uploaded audio locally
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Transcribe using Whisper
        transcript_text = transcribe_audio(temp_file_path)

        # Step 2: Extract structured tasks using Groq
        task_data = extract_tasks_from_transcript(transcript_text)

        return {
            "transcript": transcript_text,
            "tasks": task_data.tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Always clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)