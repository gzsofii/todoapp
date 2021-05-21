from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #depending on if it’s started as application or imported as module the name will be different ('__main__' versus the actual import name). Flask will know from this, where to look for templates, etc
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todoapp' # it needs to be created manually
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #not to get a warning when importing in interactive mode

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.desc}>'


db.create_all() # tables get created

@app.route('/todos/create', methods=['POST'])
def create_todo():
    descr = request.get_json()['description']
    todo = Todo(descr = descr)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.descr
    })

@app.route('/')
def index(): # this is the controller in MVC
    return render_template('index.html', data=Todo.query.all()) # refreshes the page

