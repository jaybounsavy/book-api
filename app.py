from flask import Flask, jsonify, request
from flask_cors import CORS
 
app = Flask(__name__)
 
# Configure the CORS
CORS(app, resources={r"/*": {"origins": "*"}})
 
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask API!"
 
if __name__ == '__main__':
    app.run(debug=True)
 