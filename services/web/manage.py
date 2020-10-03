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
    user_1 = User(email="teacher@gmail.com", password="test",
                  role="teacher", first_name="qq", last_name="qq", school="uq")
    user_2 = User(email="student@gmail.com", password="test",
                  role="student", first_name="qq", last_name="qq", school="uq")
    user_3 = User(email="student1@gmail.com", password="test",
                  role="student", first_name="qq", last_name="qq", school="uq")
    user_4 = User(email="student2@gmail.com", password="test",
                  role="student", first_name="qq", last_name="qq", school="uq")
    user_5 = User(email="student3@gmail.com", password="test",
                  role="student", first_name="qq", last_name="qq", school="uq")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.add(user_4)
    db.session.add(user_5)

    teacher = Teacher(email="teacher@gmail.com")
    student = Student(email="student@gmail.com")
    student1 = Student(email="student1@gmail.com")
    student2 = Student(email="student2@gmail.com")
    student3 = Student(email="student3@gmail.com")
    db.session.add(teacher)
    db.session.add(student)
    db.session.add(student1)
    db.session.add(student2)
    db.session.add(student3)

    class_1 = TeacherClasses(
        class_name="2K", class_code="2KJVC", teacher=teacher)
    class_2 = TeacherClasses(
        class_name="2J", class_code="6JUIO", teacher=teacher)
    class_3 = TeacherClasses(
        class_name="6K", class_code="0KFPR", teacher=teacher)
    db.session.add(class_1)
    db.session.add(class_2)
    db.session.add(class_3)

    class_members_1 = ClassMembers(class_=class_1, student=student)
    db.session.add(class_members_1)
    class_members_2 = ClassMembers(class_=class_1, student=student1)
    db.session.add(class_members_2)
    class_members_3 = ClassMembers(class_=class_1, student=student2)
    db.session.add(class_members_3)
    class_members_3 = ClassMembers(class_=class_3, student=student3)
    db.session.add(class_members_3)

    resource_1 = Resource(resource_title="Deforestation",
                          resource_detail="Every day...")
    resource_2 = Resource(resource_title="Pollution",
                          resource_detail="9999 tonnes of rubbish...")
    db.session.add(resource_1)
    db.session.add(resource_2)

    task_1 = Task(task_name="Collect rubbish", task_detail="Collect rubbish...",
                  task_reason="Just because", points=10, class_=class_1, resource=resource_2, teacher=teacher)
    task_2 = Task(task_name="Plant a tree", task_detail="Choose a tree seed...",
                  task_reason="Just because", points=5, class_=class_1, resource=resource_1, teacher=teacher)
    db.session.add(task_1)
    db.session.add(task_2)

    # badge_1 = Badge(badge_id=1, badge_location="/static/badge_images/badge1.PNG", student=student)
    badge_1 = Badge(badge_name="test1", badge_comment="badge_comment",
                    badge_location="/static/badge_images/badge1.PNG", student=student)
    db.session.add(badge_1)
    # badge_99 = Badge(badge_id=99, badge_location="/static/badge_images/badge1.PNG", student=student)
    badge_99 = Badge(badge_name="test2", badge_comment="badge_comment2",
                     badge_location="/static/badge_images/badge1.PNG", student=student)
    db.session.add(badge_99)

    db.session.commit()


if __name__ == "__main__":
    cli()
