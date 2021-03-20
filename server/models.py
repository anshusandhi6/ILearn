from app import db,ma
import datetime
from marshmallow import Schema, fields, ValidationError, pre_load

class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)   
    first_name = db.Column(db.String(20),nullable=False)
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(70), unique = True) 
    password = db.Column(db.String(80)) 
    register_date = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())

    def __repr__(self):
         return f"User('{self.first_name}', '{self.email}', '{self.register_date}')"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True)