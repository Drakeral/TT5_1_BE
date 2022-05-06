from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from src.api_logic import logic
from bson.json_util import ObjectId
import json
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)


# Initialize Flask App
app = Flask(__name__)
app.json_encoder = MyEncoder
CORS(app)

# ping
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"success": True}), 200

path_user = "/user"

# user_login /user/login
@app.route(path_user + "/login", methods=['POST'])
def user_login():
    return jsonify(logic.user_login(request.get_json())), 200

# user_create /user/create
@app.route(path_user + "/create", methods=['POST'])
def user_create():
    return jsonify(logic.user_create(request.get_json())), 200


    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False)