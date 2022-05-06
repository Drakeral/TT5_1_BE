from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# ping
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"success": True}), 200
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False)