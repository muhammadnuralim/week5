from flask import Blueprint, render_template, request, jsonify
import os
import json

taskBp = Blueprint("task", __name__)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# task json
task_file = os.path.join(__location__, "../data/task.json")

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

@taskBp.route("", methods=['GET'], strict_slashes = False)
def get_all_task():

    tasks = read_json(task_file)

    response = jsonify({
        "success" : True,
        "data" : tasks})

    return response, 200

@taskBp.route("<int:id>", methods=['GET'], strict_slashes = False)
def get_one_task(id):
    
    tasks = read_json(task_file)

    task = [task for task in tasks['data'] if task['_id'] == id]

    if not task:
        return jsonify({'message' : 'No task found!'})
    
    response = jsonify({
        "success" : True,
        "data" : task[0]
    })

    return response, 200

@taskBp.route("", methods=['POST'], strict_slashes = False)
def create_task():
    
    data = request.get_json()

    new_task = {
        "_id" : id_maker(task_file),
        "description" : data['description'],
        "title" : data["title"],
    }
    temp_data = read_json(task_file)

    temp_data["data"].append(new_task)

    write_json(task_file, temp_data)

    response = jsonify({
        "success" : True,
        "message" : "New Task created!",
        "data" : {
            "task_id" : new_task['_id']}
    })

    return response, 201

@taskBp.route("<int:id>", methods=['PUT'], strict_slashes = False)
def edit_task(id):
    
    data = request.get_json()

    temp_data = read_json(task_file)

    for task in temp_data["data"]:
        if task["_id"] == id:
            task["description"] = data["description"]
            task["title"] = data["title"]
            break
    
    write_json(task_file, temp_data)

    response = jsonify({
        "success" : True,
        "message" : "data update successfully",
    })

    return response, 200

@taskBp.route("<int:id>", methods=['DELETE'], strict_slashes = False)
def delete_task(id):

    temp_data = read_json(task_file)

    for task in temp_data["data"]:
        if task["_id"] == id:
            temp_data["data"].remove(task)
            break

    write_json(task_file, temp_data)

    response = jsonify({
        "success" : True,
        "message" : "data delete successfully",
    })

    return response, 200


# untuk penamaan url PUT atau delete tinggal tambahkan /<id>
