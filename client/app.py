from flask import Flask, render_template, jsonify, request, abort
from models import generate_flash_fiction, replace_markers
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    # Grab silliness from ?silliness=…; default to 0.0 if missing
    silliness = request.args.get('silliness', default=0.0, type=float)
    if not 0.0 <= silliness <= 1.0:
        abort(400, description="silliness must be between 0.0 and 1.0")

    print(silliness)
    # Call your client function
    text = generate_flash_fiction(
        base_url="http://localhost:8000",
        silliness=silliness,
        timeout=1.0
    )
    text = replace_markers(text)
    return jsonify({"text": text})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

