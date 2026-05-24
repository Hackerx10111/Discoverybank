"""
server.py — Discovery Bank AI Assistant
Full Flask server with Groq AI proxy endpoint.

The /api/chat route keeps your Groq API key server-side
so it is NEVER exposed in the browser.

Hosting:
  Render.com   → connect GitHub repo, it reads render.yaml automatically
  Railway.app  → connect GitHub repo, set GROQ_API_KEY env var
  Heroku       → git push heroku main (Procfile handles gunicorn)
  VPS / local  → python server.py

Install & run locally:
  pip install -r requirements.txt
  cp .env.example .env          # then fill in your GROQ_API_KEY
  python server.py

Production:
  gunicorn server:app
"""

import os
import json
import requests
from flask import Flask, send_from_directory, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app, origins="*")

# ── Config ─────────────────────────────────────────────────────────────
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL     = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_TOKENS     = int(os.environ.get("MAX_TOKENS", 1024))
PORT           = int(os.environ.get("PORT", 3000))
FLASK_ENV      = os.environ.get("FLASK_ENV", "production")


# ══════════════════════════════════════════════════════════════════════
# STATIC FILES
# ══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Serve the main single-page app."""
    return send_from_directory(".", "discovery-bank-final.html")

@app.route("/<path:path>")
def static_files(path):
    """Serve CSS, JS, images and other assets."""
    return send_from_directory(".", path)


# ══════════════════════════════════════════════════════════════════════
# GROQ AI PROXY  →  POST /api/chat
# ══════════════════════════════════════════════════════════════════════

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Proxy endpoint — receives messages from the frontend,
    forwards them to Groq, and streams the response back.

    Request body (JSON):
    {
      "messages": [
        {"role": "user", "content": "What is my balance?"},
        ...
      ],
      "system": "You are the Discovery Bank AI assistant..."   (optional)
    }

    Response (JSON):
    {
      "reply": "Your Transaction Account balance is R 24,380.50..."
    }
    """

    # ── Validate API key is configured ──────────────────────────────
    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY is not set. Add it to your .env file or hosting environment variables."
        }), 500

    # ── Parse request ────────────────────────────────────────────────
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Invalid JSON body"}), 400

    messages     = body.get("messages", [])
    system_msg   = body.get("system", "")
    temperature  = float(body.get("temperature", 0.7))
    max_tokens   = int(body.get("max_tokens", MAX_TOKENS))

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    # ── Build Groq request payload ───────────────────────────────────
    groq_messages = []

    # Prepend system message if provided
    if system_msg:
        groq_messages.append({
            "role": "system",
            "content": system_msg
        })

    # Add conversation history
    for msg in messages:
        role    = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant", "system") and content:
            groq_messages.append({"role": role, "content": content})

    payload = {
        "model":       GROQ_MODEL,
        "messages":    groq_messages,
        "max_tokens":  max_tokens,
        "temperature": temperature,
    }

    # ── Call Groq API ────────────────────────────────────────────────
    try:
        groq_response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type":  "application/json",
            },
            json=payload,
            timeout=30,
        )

        groq_data = groq_response.json()

        # Handle Groq errors
        if groq_response.status_code != 200:
            error_msg = groq_data.get("error", {}).get("message", "Groq API error")
            status    = groq_response.status_code

            if status == 401:
                return jsonify({"error": "Invalid Groq API key. Check your GROQ_API_KEY."}), 401
            elif status == 429:
                return jsonify({"error": "Rate limit reached. Please try again in a moment."}), 429
            elif status == 400:
                return jsonify({"error": f"Bad request: {error_msg}"}), 400
            else:
                return jsonify({"error": error_msg}), status

        # Extract the reply text
        reply = (
            groq_data
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not reply:
            return jsonify({"error": "Empty response from Groq"}), 500

        # Return usage stats too (useful for debugging)
        usage = groq_data.get("usage", {})

        return jsonify({
            "reply": reply,
            "model": groq_data.get("model", GROQ_MODEL),
            "usage": {
                "prompt_tokens":     usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens":      usage.get("total_tokens", 0),
            }
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Groq timed out. Please try again."}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reach Groq API. Check your internet connection."}), 503
    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500


# ══════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════

@app.route("/health")
def health():
    """Health check endpoint required by Render / Railway / Heroku."""
    return jsonify({
        "status":    "ok",
        "app":       "Discovery Bank AI Assistant",
        "model":     GROQ_MODEL,
        "api_ready": bool(GROQ_API_KEY),
    }), 200


@app.route("/api/models")
def list_models():
    """Returns available Groq models."""
    return jsonify({
        "current_model": GROQ_MODEL,
        "available_models": [
            {"id": "llama-3.3-70b-versatile",  "name": "Llama 3.3 70B (Recommended — fast & smart)"},
            {"id": "llama-3.1-8b-instant",     "name": "Llama 3.1 8B (Fastest — lower quality)"},
            {"id": "mixtral-8x7b-32768",       "name": "Mixtral 8x7B (Good for long context)"},
            {"id": "gemma2-9b-it",             "name": "Gemma 2 9B (Google — lightweight)"},
        ]
    }), 200


# ══════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    debug = FLASK_ENV == "development"

    print("=" * 55)
    print("  🏦  Discovery Bank AI Assistant")
    print("=" * 55)
    print(f"  URL     : http://localhost:{PORT}")
    print(f"  Model   : {GROQ_MODEL}")
    print(f"  API Key : {'✅ Set' if GROQ_API_KEY else '❌ NOT SET — add to .env'}")
    print(f"  Mode    : {'development' if debug else 'production'}")
    print("=" * 55)

    if not GROQ_API_KEY:
        print("\n  ⚠️  WARNING: GROQ_API_KEY is not set!")
        print("  Get a free key at https://console.groq.com/keys")
        print("  Then add it to your .env file:\n")
        print("    GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx\n")

    app.run(host="0.0.0.0", port=PORT, debug=debug)
