from flask.cli import FlaskGroup

from project import app, db
from project.models import User, TeacherClasses, Task


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="test@gmail.com"))
    db.session.commit()

@cli.command("seed_tasks")
def seed_tasks():
    user = User(email="test@gmail.com")
    class_1 = TeacherClasses(class_name="Year 10", teacher=user)
    class_2 = TeacherClasses(class_name="Year 11", teacher=user)
    class_3 = TeacherClasses(class_name="Year 12", teacher=user)
    db.session.add(class_1)
    db.session.add(class_2)
    db.session.add(class_3)

    task_1 = Task(task_name="Collect rubbish", task_detail="Collect rubbish...",
    task_reason="Just because", points=10, class_=class_1)
    task_2 = Task(task_name="Plant a tree", task_detail="Choose a tree seed...",
    task_reason="Just because", points=5, class_=class_1)
    db.session.add(task_1)
    db.session.add(task_2)

    db.session.commit()

if __name__ == "__main__":
    cli()
