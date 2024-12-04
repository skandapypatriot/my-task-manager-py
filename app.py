# Imports
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# SQLite database file in the current working directory
DATABASE_URI = "sqlite:///client_tasks.db"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Task model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)  # Ensure tables are created

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Task(content=task_content)
        session.add(new_task)
        session.commit()
        return redirect("/")
    else:
        tasks = session.query(Task).order_by(Task.created.desc()).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = session.query(Task).get(id)
    if task:
        session.delete(task)
        session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = session.query(Task).get(id)
    if request.method == "POST":
        task.content = request.form["content"]
        session.commit()
        return redirect("/")
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
