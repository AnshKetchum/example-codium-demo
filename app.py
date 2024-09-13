from flask import Flask, jsonify
from flask_cors import CORS
from logger import extract_response_content

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, world!'})

if __name__ == '__main__':
    app.run()