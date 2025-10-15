from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uuid
import random
from pathlib import Path

app = FastAPI(title="Is it AI Generated")

BASE_DIR = Path(__file__).parent

# Serve static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# In-memory store mapping pair_id -> correct_label
pairs_store = {}


class Guess(BaseModel):
    pair_id: str
    chosen: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/pair")
async def get_pair():
    """Return a pair of images: one AI generated and one real. The client will display them randomly left/right."""
    # For this simple demo, we ship two sample images included in static/images.
    ai_image = "/static/images/ai_sample.svg"
    real_image = "/static/images/real_sample.svg"

    # Randomize order
    left_is_real = random.choice([True, False])
    if left_is_real:
        left = {"url": real_image, "label": "real"}
        right = {"url": ai_image, "label": "ai"}
    else:
        left = {"url": ai_image, "label": "ai"}
        right = {"url": real_image, "label": "real"}

    pair_id = str(uuid.uuid4())
    # Store the correct answer (which side is real)
    pairs_store[pair_id] = {
        "left": left["label"],
        "right": right["label"],
    }

    return JSONResponse({"pair_id": pair_id, "left": left, "right": right})


@app.post("/api/guess")
async def post_guess(guess: Guess):
    data = pairs_store.get(guess.pair_id)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired pair_id")

    # chosen should be 'left' or 'right'
    chosen = guess.chosen
    if chosen not in ("left", "right"):
        raise HTTPException(status_code=400, detail="chosen must be 'left' or 'right'")

    correct_label = data[chosen]
    is_correct = correct_label == "real"

    # Optionally delete the pair to avoid replay
    pairs_store.pop(guess.pair_id, None)

    return {"correct": is_correct, "correct_label": correct_label}
