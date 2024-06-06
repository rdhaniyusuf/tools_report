from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
from tools import *


app = Flask(__name__)
CORS(app)
@app.route('/upload', methods=['POST'])
def upload_file():
    # code upload file here
    return jsonify({"message": "File Upload Success"}), 200

def process_file():
    # code processing here
    return jsonify({"message" : "File Processing"}), 200


if __name__ == '__main__':
    app.run(debug=True)