from flask.cli import FlaskGroup

from project import app, db
from project.models import *


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("create_db_prod")
def create_db():
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="test@gmail.com"))
    db.session.commit()


@cli.command("seed_tasks")
def seed_tasks():
    user_1 = User(email="teacher@gmail.com", password="teacher",
                  role="teacher", first_name="Chris", last_name="Fagan", school="University of Queensland")
    user_2 = User(email="student1@gmail.com", password="student",
                  role="student", first_name="Harris", last_name="Andrews", school="University of Queensland")
    user_3 = User(email="student2@gmail.com", password="student",
                  role="student", first_name="Dustin", last_name="Martin", school="University of Queensland")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)

    teacher = Teacher(email="teacher@gmail.com")
    student_1 = Student(email="student1@gmail.com")
    student_2 = Student(email="student2@gmail.com")
    db.session.add(teacher)
    db.session.add(student_1)
    db.session.add(student_2)

    class_1 = TeacherClasses(
        class_name="2K", class_code="2KJVC", teacher=teacher)
    class_2 = TeacherClasses(
        class_name="2J", class_code="6JUIO", teacher=teacher)
    class_3 = TeacherClasses(
        class_name="6K", class_code="0KFPR", teacher=teacher)
    db.session.add(class_1)
    db.session.add(class_2)
    db.session.add(class_3)

    class_members_1 = ClassMembers(class_=class_1, student=student_1, student_status="accepted")
    class_members_2 = ClassMembers(class_=class_1, student=student_2, student_status="pending")

    db.session.add(class_members_1)
    db.session.add(class_members_2)

    resource_1 = Resource(resource_title="Deforestation",
                          resource_detail="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque...")
    resource_2 = Resource(resource_title="Pollution",
                          resource_detail="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque...")
    db.session.add(resource_1)
    db.session.add(resource_2)

    task_1 = Task(task_name="Collect rubbish", task_detail="Collect rubbish...",
                  points=10, class_=class_1, resource=resource_2, teacher=teacher, required_approval= True)
    task_2 = Task(task_name="Plant a tree", task_detail="Choose a tree seed...",
                  points=5, class_=class_1, resource=resource_1, teacher=teacher, required_approval= False)
    db.session.add(task_1)
    db.session.add(task_2)

    db.session.commit()


if __name__ == "__main__":
    cli()
