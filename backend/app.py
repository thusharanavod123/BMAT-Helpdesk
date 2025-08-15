from flask import Flask, request, jsonify
from agents import bmat_router
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow React to call the API

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    result = bmat_router(user_query)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
