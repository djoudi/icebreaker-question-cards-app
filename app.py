"""Standalone trainer-led question-card version of the icebreaker platform."""
import json
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

APP_DIR = Path(__file__).resolve().parent
BANKS = {
    "general": json.loads((APP_DIR / "general-questions.json").read_text(encoding="utf-8")),
    "cyber": json.loads((APP_DIR / "cyber-questions.json").read_text(encoding="utf-8")),
    "day1": json.loads((APP_DIR / "day1-questions.json").read_text(encoding="utf-8")),
}
app = Flask(__name__, static_folder=None)


@app.get("/")
def index():
    return send_from_directory(APP_DIR, "index.html")


@app.get("/school-logo.png")
def school_logo():
    return send_from_directory(APP_DIR, "school-logo.png", mimetype="image/png")


@app.get("/api/banks")
def banks():
    return jsonify({key: {"title": bank["title"], "description": bank.get("description", ""), "questions": bank["questions"]}
                    for key, bank in BANKS.items()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
