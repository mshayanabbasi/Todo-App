from flask import Flask, jsonify , json, render_template, session, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    done = db.Column(db.Boolean)



db.create_all()

@app.route('/todo' , methods=['GET'])
def get_all_todo():
    todo = Todo.query.all()

    result=[]
    for todos in todo:
        todos_data={}
        todos_data['id']=todos.id
        todos_data['title']=todos.title
        todos_data['description']=todos.description
        todos_data['done'] = todos.done
        result.append(todos_data)

    return jsonify({'todos':result})

@app.route('/todo/<id>', methods=['GET'])
def get_one_todo(id):
    todos = Todo.query.filter_by(id=id).first()
    if not todos:
        return jsonify({'message':'Nothing in the dictionary'})

    todos_data = {}
    todos_data['id'] = todos.id
    todos_data['title'] = todos.title
    todos_data['description'] = todos.description
    todos_data['done'] = todos.done
    return jsonify(todos_data)

@app.route('/todo' , methods=['POST'])
def create_todo():
    data = request.get_json()

    new_todo =Todo(title=data['title'], description=data['description'], done=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify ({'message':'Add sucessufully'})

@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    if not todo:
        return jsonify({'message': 'Nothing in the dictionary'})

    todo.done=True
    db.session.commit()
    return jsonify({'message':'Updated Sucessfully'})

@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = Todo.query.filter_by(id=todo_id).first()
    if not todos:
        return jsonify({'message': 'Nothing in the dictionary'})
    else:
        db.session.delete(todos)
        db.session.commit()
    return jsonify({'message':'Deleted Sucessfully'})

app.run(debug=True)
