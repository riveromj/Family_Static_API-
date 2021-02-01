"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['POST'])
def create_members():
    try:
        body = request.get_json()
        if body is None:
            return 'body is Null',400
        member ={
            "id": body["id"],
            "first_name" : body["first_name"],
            "age" : body["age"],
            "lucky_numbers": body["lucky_numbers"]
        }
        print(member)
        new_member = jackson_family.add_member(member)
        print(new_member,"---------------------")
        #if(new_member == 200):
         #   return jsonify('Everything ok!'), 200
        #jackson_family.add_member(body) 
        return jsonify(member),200
        #body = request.get_json()
        #jackson_family.add_member(body)
        return 'ok', 200
    except:
        return jsonify("resp.status_code") , 400


@app.route('/members', methods=['GET'])
def handle_hello():
    try:
    # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
        response_body = members
       
        return jsonify(response_body), 200
    except:
        return jsonify('Internal server error'), 500

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    user = jackson_family.get_member(id)
    if user:
        return jsonify(user), 200
    return 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    user = jackson_family.delete_member(id)
    print(user)
    if user:
        return jsonify({"done":True}), 200
    return jsonify({"done":False}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
