from flask import Blueprint, render_template, request, jsonify
import os
import json

# membuat blueprint object
taskBp = Blueprint("task", __name__)

# mendapatkan file path project
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# path file task
task_file = os.path.join(__location__, "../data/task.json")

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

# route GET all tasks
@taskBp.route("", methods=['GET'], strict_slashes = False)
def get_all_task():
    """
    Fungsi untuk mendapatkan semua task

    args:
        -

    return
        response (json object): pesan response
    """
    
    # membaca data task json
    tasks = read_json(task_file)

    # membuat response dalam bentuk object json
    response = jsonify({
        "success" : True,
        "data" : tasks})

    return response, 200

# route GET tasks/<id>
@taskBp.route("<int:id>", methods=['GET'], strict_slashes = False)
def get_one_task(id):
    """
    Fungsi untuk mendapatkan task berdasarkan id

    args:
        id (int): id task

    return
        response (json object): pesan response
    """
    
    # membaca file task json
    tasks = read_json(task_file)

    # list comprehension untuk mencari task berdasarkan id
    task = [task for task in tasks['data'] if task['_id'] == id]
    
    # kondisi jika task tidak ditemukan
    if not task:
        return jsonify({'message' : 'No task found!'})
    
    # membuat response dalam bentuk object json
    response = jsonify({
        "success" : True,
        "data" : task[0]
    })

    return response, 200

# route POST /tasks
@taskBp.route("", methods=['POST'], strict_slashes = False)
def create_task():
    """
    Fungsi untuk membuat task baru

    args:
        -

    return
        response (json object): pesan response
    """
    
    # mendapatkan request json dari client
    data = request.get_json()
    
    # dictionary task baru
    new_task = {
        "_id" : id_maker(task_file),
        "description" : data['description'],
        "title" : data["title"],
    }
    
    # membaca file task.json
    temp_data = read_json(task_file)

    # menambahkan task baru ke variable hasil baca task.json
    temp_data["data"].append(new_task)
    
    # write data json ke dalam file task
    write_json(task_file, temp_data)

    # membuat response
    response = jsonify({
        "success" : True,
        "message" : "New Task created!",
        "data" : {
            "task_id" : new_task['_id']}
    })

    return response, 201

# route PUT tasks/<id>
@taskBp.route("<int:id>", methods=['PUT'], strict_slashes = False)
def edit_task(id):
    """
    Fungsi untuk edit seluruh detail task

    args:
        id (int) : id task

    return
        response (json object): pesan response
    """
    
    # mendapatkan request json dari client
    data = request.get_json()
    
    # membaca file task.json     
    temp_data = read_json(task_file)
    
    # mendapatkan data berdasarkan id task
    # melakukan overwrite description dan title
    for task in temp_data["data"]:
        if task["_id"] == id:
            task["description"] = data["description"]
            task["title"] = data["title"]
            break
    
    # write data yang sudah di edit
    write_json(task_file, temp_data)
    
    # membuat response
    response = jsonify({
        "success" : True,
        "message" : "data update successfully",
    })

    return response, 200

# route DELETE tasks/id
@taskBp.route("<int:id>", methods=['DELETE'], strict_slashes = False)
def delete_task(id):
    """
    Fungsi untuk hapus task berdasarkan id

    args:
        id (int) : id task

    return
        response (json object): pesan response
    """
    
    # membaca file task.json     
    temp_data = read_json(task_file)
    
    # mendapatkan data task berdasarkan id
    # kemudain remove task tersebut
    for task in temp_data["data"]:
        if task["_id"] == id:
            temp_data["data"].remove(task)
            break
    
    # write data json 
    write_json(task_file, temp_data)
    
    # membuat response
    response = jsonify({
        "success" : True,
        "message" : "data delete successfully",
    })

    return response, 200


# untuk penamaan url PUT atau delete tinggal tambahkan /<id>
