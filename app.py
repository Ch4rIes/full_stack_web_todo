from hashlib import new
from flask import Flask , render_template , request , redirect , url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://czqz@localhost:5432/CRUD_TODO'
db = SQLAlchemy(app)
migrate = Migrate(app , db)



#build a SQL database to store all the todo items

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer , primary_key = True)
    description = db.Column(db.String() , nullable = False)
    completed = db.Column(db.Boolean , nullable = False)

db.create_all()
for d in Todo.query.all():
        print(d.description , d.completed)

@app.route('/todos/delete' , methods=['POST'])
def delete():
    try:
        todoid = request.get_json()['todoid']
        todotask = Todo.query.get(int(todoid))
        print(todotask)
        db.session.delete(todotask)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/set_state' , methods=['POST'])
def change_state():
    try:
        new_state = request.get_json()['completed']
        todoid = request.get_json()['todoid']
        print(new_state , todoid)
        todotask = Todo.query.get(int(todoid))
        print(todotask)
        todotask.completed = new_state
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/create' , methods=['POST'])
def create_listing():
    data1=Todo.query.all()
    new_description = request.get_json()['description']
    new_task = Todo(description = new_description , completed = False , id = len(data1) + 1)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'description': new_task.description
    })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())