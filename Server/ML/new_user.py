from meety_orm import User
from meety_config import db

test = User(email='test@test.com', password_hash = '1'*32, active = 1)
db.session.add(test)
db.session.commit()

