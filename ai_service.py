import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schemas import ActionItemList

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def transcribe_audio(file_path: str) -> str:
    """Uses Whisper on Groq for speech-to-text."""
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )
    return transcription.text

def extract_tasks_from_transcript(transcript: str) -> ActionItemList:
    """Uses openai/gpt-oss-20b on Groq to extract structured tasks."""
    system_prompt = (
        "You are a task extraction engine. Extract all actionable tasks from the transcript. "
        "Return ONLY a valid JSON object matching this structure:\n"
        "{\n"
        '  "tasks": [\n'
        "    {\n"
        '      "title": "Task description",\n'
        '      "priority": "High" or "Medium" or "Low",\n'
        '      "category": "Work" or "Personal" or "Urgent" or "Other",\n'
        '      "due_hint": "deadline or empty string",\n'
        '      "assignee": "name or Self"\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Transcript:\n\"{transcript}\""}
        ],
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return ActionItemList(**data)