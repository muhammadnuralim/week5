from flask import Blueprint, render_template, request, jsonify
import os
import json

# membuat blueprint object
userBp = Blueprint("user", __name__)

# mendapatkan file path project
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# path file user json
user_file = os.path.join(__location__, "../data/user.json")

# read json data
def read_json(file_path):
    """
    Fungsi untuk read data json

    args:
        file_path (str): path file json

    return:
        data (json object): data json
    """
    
    # membuka file json
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

# write json data
def write_json(file_path, data):
    """
    Fungsi untuk write data json

    args:
        file_path (str): path file json
        data (dict) : data baru yang akan dimasukkan

    return:
        -
    """
    
    # buka data json dengan mode write
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# generate id
def id_maker(file_path):
    """
    Fungsi untuk membuat id 

    args:
        file_path (str): path file json

    return
        id (int): id hasil fungsi
    """
    
    # membaca data yang akan dibuat id
    data = read_json(file_path)
    
    # mendapatkan panjang data dan menambahkan dengan 1
    id = len(data["data"]) + 1
    
    return id

# route GET users
@userBp.route("", methods=['GET'], strict_slashes = False)
def get_user():
    """
    Fungsi mendapatkan user

    args:
        -

    return
        response (json object) : pesan response
    """
    
    # membaca data user json
    users = read_json(user_file)

    # membuat response dalam bentuk object json
    response = jsonify({
        "success" : True,
        "data" : users
    })

    return response, 200
