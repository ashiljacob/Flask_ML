from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow, Schema

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Todo(db.Model):
   __tablename__ = "todos"
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(20))
   todo_description = db.Column(db.String(100))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, title, todo_description):
       self.title = title
       self.todo_description = todo_description

   def __repr__(self):
       return f"{self.id}"



class TodoSchema(ma.Schema):
   class Meta:
       model = Todo
       sqla_session = db.session
       fields = ("id","title","todo_description")

   # id = fields.Number(dump_only=True)
   # title = fields.String(required=True)
   # todo_description = fields.String(required=True)



@app.route('/todo', methods = ['POST'])
def create_author():
    data = request.get_json()
    title = data['title']
    todo_description = data['todo_description']
    todo = Todo(title,todo_description).create()
    todo_schema = TodoSchema()


    result = todo_schema.jsonify(todo).data
    print(result)
    return make_response(result)


@app.route('/todo', methods = ['GET'])
def index():
    get_todo = Todo.query.all()
    todo_schema = TodoSchema(many=True)
    todo = todo_schema.jsonify(get_todo)
    return make_response(todo)

if __name__ == "__main__":
    app.run(debug=True)
