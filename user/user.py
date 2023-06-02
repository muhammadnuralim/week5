from flask import Blueprint, render_template, request, jsonify
import os
import json

userBp = Blueprint("user", __name__)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# user json
user_file = os.path.join(__location__, "../data/user.json")

# read json data
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

# write json data
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# generate id
def id_maker(file_path):
    data = read_json(file_path)
    id = len(data["data"]) + 1
    return id

@userBp.route("", methods=['GET'], strict_slashes = False)
def get_user():
    # ganti ini jadi ngambil user
    return "ini user"

