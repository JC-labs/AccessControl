from app import db
from app.models import User

db.create_all()
user = User(username="admin", email="admin@mail.com", role=0)
user.set_password("admin")
db.session.add(user)
db.session.commit()