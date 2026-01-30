from flask import Flask, request, jsonify, session
import time
from flask_cors import CORS
from router import conduct_router
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
app.secret_key = "dev-secret-key"
CORS(app, supports_credentials=True)

def youtube_id(url: str) -> str | None:
    qs = parse_qs(urlparse(url).query)
    return qs.get("v", [None])[0]

def to_content_blocks(output):
    blocks = []

    if output.Text:
        blocks.append({
            "type": "text",
            "value": output.Text
        })

    for img in output.ImageLinks:
        blocks.append({
            "type": "image",
            "src": img
        })

    for yt in output.YoutubeLinks:
        vid = youtube_id(yt)
        if vid:
            blocks.append({
                "type": "youtube",
                "videoId": vid
            })

    return blocks


@app.route("/chat", methods=["POST"])
def chat():
    if 'conversation_history' not in session:
        session['conversation_history'] = ""


    data = request.get_json()
    user_message = data.get("message", "")
    session['conversation_history'] += "\nUser: " + user_message

    response = conduct_router(session['conversation_history'])
    session['conversation_history'] += "\nRespondent: " + session['conversation_history']

    print(response)

    json_res = jsonify({
        "role": "assistant",
        "content": to_content_blocks(response)
    })

    print(json_res.get_json())

    return json_res
