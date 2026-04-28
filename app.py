import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from utils.scoring import rank_diseases
from utils.response_builder import build_response

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "disease_database.json"

app = FastAPI(title="Skin Disease Chatbot")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

with open(DATA_PATH, "r", encoding="utf-8") as f:
    DISEASE_DB = json.load(f)

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(req: ChatRequest):
    text = req.message.strip()

    if not text:
        return {
            "reply": "Please type your symptoms in text."
        }

    ranked = rank_diseases(text, DISEASE_DB)

    if not ranked or ranked[0]["score"] <= 0:
        return {
            "reply": (
                "I could not identify a likely condition from the text.\n\n"
                "Try adding details such as:\n"
                "- itchy or painful\n"
                "- red, dry, scaly, white, or purple\n"
                "- exact location on the body\n"
                "- whether it is spreading\n\n"
                "This is for educational use only and is not a diagnosis."
            )
        }

    top = ranked[0]
    second_score = ranked[1]["score"] if len(ranked) > 1 else 0.0
    reply = build_response(top, second_score)

    return {"reply": reply}