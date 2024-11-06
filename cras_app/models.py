# cras_app/models.py

from datetime import date, datetime
from cras_app.extensions import db
from cras_app.extensions import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    class_shift = db.Column(db.String(20), nullable=False)
    attendance_status = db.Column(db.String(10), nullable=True)  # Presente ou Ausente

    def __repr__(self):
        return f'<Student {self.name}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)  # Data do registro de presença
    attendance_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)  # Hora do registro de presença

    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))