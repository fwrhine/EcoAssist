from flask.cli import FlaskGroup

from project import app, db
from project.models import *


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
    user_1 = User(email="test@gmail.com", password="test", role="teacher", first_name="qq", last_name="qq",school="uq")
    user_2 = User(email="test2@gmail.com", password="test", role="teacher", first_name="qq", last_name="qq",school="uq")
    db.session.add(user_1)
    db.session.add(user_2)

    teacher = Teacher(email="test@gmail.com")
    student = Student(email="test2@gmail.com")
    db.session.add(teacher)
    db.session.add(student)

    class_1 = TeacherClasses(class_name="2K", teacher=teacher)
    class_2 = TeacherClasses(class_name="2J", teacher=teacher)
    class_3 = TeacherClasses(class_name="6K", teacher=teacher)
    db.session.add(class_1)
    db.session.add(class_2)
    db.session.add(class_3)

    class_members_1 = ClassMembers(class_=class_1, student=student)
    db.session.add(class_members_1)

    resource_1 = Resource(resource_title="Deforestation", resource_detail="Every day...")
    resource_2 = Resource(resource_title="Pollution", resource_detail="9999 tonnes of rubbish...")
    db.session.add(resource_1)
    db.session.add(resource_2)

    task_1 = Task(task_name="Collect rubbish", task_detail="Collect rubbish...",
    task_reason="Just because", points=10, class_=class_members_1, resource=resource_2)
    task_2 = Task(task_name="Plant a tree", task_detail="Choose a tree seed...",
    task_reason="Just because", points=5, class_=class_members_1, resource=resource_1)
    db.session.add(task_1)
    db.session.add(task_2)

    db.session.commit()

if __name__ == "__main__":
    cli()
