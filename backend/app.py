from flask import Flask, request, Response
from agents import faq_agent
from flask_cors import CORS
import openai
import json

openai.api_key = "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"  # Replace with real key

app = Flask(__name__)
CORS(app)

@app.route("/ask-stream", methods=["POST"])
def ask_stream():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return Response(json.dumps({"error": "Query is required"}), mimetype="application/json"), 400

    # First check FAQ for instant answer
    faq_response = faq_agent(user_query)
    if faq_response:
        def generate_faq():
            yield f"data: {json.dumps({'agent': 'FAQ Agent', 'response': faq_response})}\n\n"
        return Response(generate_faq(), mimetype="text/event-stream")

    # Otherwise stream OpenAI chat
    def generate():
        yield f"data: {json.dumps({'agent': 'AI Agent', 'response': ''})}\n\n"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are BMAT Helpdesk AI assistant."},
                {"role": "user", "content": user_query}
            ],
            stream=True
        )
        for chunk in completion:
            if chunk.choices[0].delta.get("content"):
                yield f"data: {json.dumps({'token': chunk.choices[0].delta['content']})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
