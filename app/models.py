from app import db

class Users(db.Model):
    __tablename__ = 'users'  # explicitly set table name
    username = db.Column(db.String(100), unique=True, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan")

class Task(db.Model):
    __tablename__ = 'tasks'  # explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    user_id = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)