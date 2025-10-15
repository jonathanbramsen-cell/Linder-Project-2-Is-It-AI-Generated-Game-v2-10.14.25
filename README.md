# Is it AI Generated — minimal FastAPI demo

This is a small demo app that shows two images (one AI-generated, one real). The user must pick which is real.

Run locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

To add your own images, place them in `static/images/` and update the `get_pair` function in `main.py` to select from your pool.
