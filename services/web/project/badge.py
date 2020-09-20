
from project.models import *
from project import app, db



def get_all_badges(id):
    badge_owned = Badge.query.filter_by(student_id=id).all()
    return badge_owned

def badge1(id):
    
    # check if already owned badge
    badge_owned = Badge.query.filter_by(student_id=id).all()
    # for first task complete
    if (len(badge_owned) == 0): #add new badge
        badge = 1
        # badge_1 = Badge(badge_image=badge, badge_id=1, student_id=id)
        badge_1 = Badge(badge_id=1, badge_location="/static/badge_images/badge1.PNG", student_id=id)
        db.session.add(badge_1)


def badge2(id):
    badge_owned = Badge.query.filter_by(student_id=id).all()
    badge_id = 2
    owned = False
    for x in badge_owned:
        if x.badge_id == badge_id:
            owned = True

    if not owned:
        badge= 2
        # badge_2 = Badge(badge_image=badge, badge_id=2, student_id=id)
        badge_2 = Badge(badge_id=2, badge_location = "/static/badge_images/badge1.PNG", student_id=id)

        db.session.add(badge_2)
