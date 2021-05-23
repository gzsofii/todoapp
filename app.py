from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__) #depending on if it’s started as application or imported as module the name will be different ('__main__' versus the actual import name). Flask will know from this, where to look for templates, etc
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todoapp' # it needs to be created manually
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #not to get a warning when importing in interactive mode

migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.desc}>'

#db.create_all() # tables get created


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        descr = request.get_json()['description']
        todo = Todo(descr = descr)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.descr
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:    
        return jsonify(body)
    
@app.route('/')
def index(): # this is the controller in MVC
    return render_template('index.html', data=Todo.query.all()) # refreshes the page

