from flask import Flask, request, jsonify, json, abort, render_template, url_for
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'todo_project'
app.config['MONGO_URI'] = 'mongodb://todo:todo123@ds119732.mlab.com:19732/todo_project'

mongo = PyMongo(app)

@app.route('/todo', methods = ['GET'])
def index():
    todo_data = {}
    todo_task = mongo.db.todos
    todo_count = todo_task.find({}).count();
    if not todo_count:
        return jsonify({'message':'No Found'})
    ta = todo_task.find({})
    for task in ta:
        todo_data[task['id']]=({'id': task['id'], 'title': task['title'], 'description': task['description'], 'done':bool(task['done'])})
    return (jsonify({'output': todo_data}))

@app.route('/todo/<int:id>', methods = ['GET'])
def get_task(id):
    todo_data={}
    todo_task = mongo.db.todos
    ta = todo_task.find({'id':id})
    if not ta.count():
        return jsonify({'message':'Nothing in the count'})
    todo_data={}
    for task in ta:
        todo_data[task['id']]={'id': task['id'], 'title': task['title'], 'description': task['description'], 'done':bool(task['done'])}
    return (jsonify({'output':todo_data}))

@app.route('/todo', methods = ['POST'])
def add():
   # id = request.json[id]
    title = request.json['title']
    description = request.json.get('description', '')
    done = bool(request.json['done'])
    todo_task = mongo.db.todos
    todo_count = todo_task.find({}).count();
    todo_task.insert({'id': todo_count + 1, 'title': title, 'description': description, 'done': done})
    return jsonify({'id': todo_count + 1, 'title': title, 'description': description, 'done': done})

@app.route('/todo/<int:id>', methods = ['PUT'])
def get_update(id):
    todo_data = {}
    todo_task = mongo.db.todos
    task = todo_task.find({'id': id})
    if not task.count():
       return 'No Found'
    else:
        title = request.json.get('title', task[0]['title'])
        description = request.json.get('description', task[0]['description'])
        done = bool(request.json.get('done', task[0]['done']))
        update_todo = todo_task.update_one(
            {'id': id},
                {
                    '$set' :{
                        'title': title,
                       'description': description,
                       'done': done
                       }
                 }
        )
    return jsonify({'message':'Successfully updated'})


@app.route('/todo/<int:id>', methods = ['DELETE'])
def get_delete(id):
    todo_data = {}
    todo_task = mongo.db.todos
    todo_task.delete_one({'id': id})
    return jsonify({'message' : 'Successfully deleted'})

@app.errorhandler(404)
def not_found_error(e):
    return "Not Found URL"

@app.errorhandler(500)
def not_found_error(e):
        return "Task not found"

app.run(debug = True, port = 4040)