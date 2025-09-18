from flask import Flask, jsonify, request
from flask_cors import CORS
from routes import book_bp
 
app = Flask(__name__)
 
# Configure the CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(book_bp)
 
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask API!.  This is Jay Bounsavy."
 
if __name__ == '__main__':
    app.run(debug=True)
 
