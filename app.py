# IMPORTS
from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///table.db"
db = SQLAlchemy(app)

# A Todo named Sqlite Database


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# printing object should return meaningful value Task ID
    def __repr__(self):
        return "<Task %r>" % self.id


# Database created
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', "POST"])
def index():
    if (request.method == "POST"):
        task_content = request.form["task"]
        task_obj = ToDo(content=task_content)
        try:
            db.session.add(task_obj)
            db.session.commit()
        except:
            return "Sorry, can't process your query"
        return redirect("/")
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()

        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    try:
        new_task = ToDo.query.get_or_404(id)
        db.session.delete(new_task)
        db.session.commit()
        return redirect("/")
    except:
        return "Can't execute"


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task_taken = ToDo.query.get(id)
    if (request.method == "POST"):
        task_taken.content = request.form['task']
        db.session.commit()
        return redirect("/")
    else:
        return render_template('update.html', task_up=task_taken)


if (__name__ == "__main__"):
    app.run(debug=True)
