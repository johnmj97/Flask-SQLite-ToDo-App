from flask import Flask,render_template,url_for, request , redirect
from flask_sqlalchemy import SQLAlchemy
import urllib
from datetime import datetime
import uuid
import logging
app = Flask(__name__)

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                   "SERVER=")
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///list.db'
with app.app_context():
     db=SQLAlchemy(app)

class todo(db.Model):
     id = db.Column(db.Uuid(), primary_key = True)
     content = db.Column(db.String(), nullable = False)
     completed = db.Column(db.Integer, default = 0)
     date_created = db.Column(db.DateTime, default =datetime.now)

     def __repr__(self): 
          return f'task {id}'

@app.route('/',methods=['POST','GET'])

def index():
     if request.method == "POST":
          task_content = request.form['content']
          if task_content == "":
               return redirect('/')
          new_task = todo()
          new_task.content = task_content
          new_task.id = uuid.uuid4()
          try:
               db.session.add(new_task)
               db.session.commit()
               return redirect('/')
          except Exception as e:
               print(f'error{e}') 
     else:
          #pass
          tasks= db.session.execute(db.select(todo).order_by(todo.date_created)).all()
          app.logger.warning(tasks)
          return render_template('index.html',tasks=tasks)

@app.route('/delete/<id>')
def delete(id):
     task_to_delete = db.session.execute(db.select(todo).filter_by(id=uuid.UUID(id))).scalar_one()
     print(task_to_delete)
     try:
          db.session.delete(task_to_delete)
          db.session.commit()
          return redirect('/')
     except:
          print(f"Error in deleting id {id}")
     
@app.route('/update/<id>', methods= ['GET','POST'])
def update(id):
     task_to_update = db.session.execute(db.select(todo).filter_by(id=uuid.UUID(id))).scalar_one()
     print(task_to_update)
     if request.method == "POST":
          task_to_update.content = request.form['content']
          db.session.commit()
          return redirect('/')
     else:
          return render_template('update.html',task=task_to_update)
     


if __name__ == "__main__":
    app.run(debug=True)
