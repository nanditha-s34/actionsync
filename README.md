# ActionSync: Voice-to-Task Engine

ActionSync is an asynchronous voice-to-action application that transcribes audio notes and converts unstructured speech into structured, prioritized action items using FastAPI, Groq-hosted Whisper, and LLMs.

## Features
- **Speech-to-Text**: Fast audio transcription powered by Whisper on Groq.
- **Task Extraction**: Parses context into deterministic tasks with title, assignee, priority, and category.
- **Strict Typing**: Enforces JSON structure via Pydantic schemas.
- **Responsive UI**: Tailwind CSS interface for uploading recordings and inspecting action items.

## Architecture
1. Client submits audio via multipart form-data to `/api/process-audio`.
2. Audio stream is buffered temporarily and dispatched to Groq Whisper.
3. Transcript is analyzed by Groq LLM inference with structured JSON formatting.
4. Output is validated against Pydantic schemas and returned to the client.
5. Temporary audio buffers are cleaned up safely in a `finally` block.

## Tech Stack
- **Backend**: Python 3.12+, FastAPI, Uvicorn, Pydantic, python-dotenv
- **AI / Cloud**: Groq Cloud SDK (Whisper-large-v3, OpenAI-compatible chat endpoints)
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS

## Local Setup
1. Clone the repository and navigate into it:
   ```bash
   git clone <your-repo-url>
   cd actionsync