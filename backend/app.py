from flask import Flask, request, jsonify
from flask_cors import CORS
from executor import execute_code

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "TechSpark Multi-Language Compiler Backend Running"

@app.route("/run", methods=["POST"])
def run():

    try:

        data = request.get_json()

        language = data["language"]

        code = data["code"]

        user_input = data.get("input", "")

        result = execute_code(language, code, user_input)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )