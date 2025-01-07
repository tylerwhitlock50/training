from app.extensions import db, logger
from flask_login import UserMixin
from datetime import datetime
from app.extensions import bcrypt
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    
class User(UserMixin, db.Model):
    
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    role = db.Column(db.Enum(Role), default=Role.EMPLOYEE, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    user_status = db.Column(db.Integer, db.ForeignKey('user_status.id'), nullable=False)
    
    assigned_trainings = db.relationship('AssignedTraining', backref='user', lazy=True)
    completed_trainings = db.relationship('Training_log', backref='user', lazy=True)
    
    
    def get_assigned_trainings(self):
        return AssignedTraining.query.filter_by(user_id=self.id, is_completed=False).all()

    def get_completed_trainings(self):
        return self.completed_trainings
    
    def has_roles(self, roles):
        if isinstance(roles, str):
            return self.role.value == roles
        if isinstance(roles, list):
            return self.role.value in roles
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'



    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
        
class Training_log(db.Model):
    __tablename__ = 'training_log'
    
    id = db.Column(db.Integer, primary_key=True)
    training_template_id = db.Column(db.Integer, db.ForeignKey('training_template.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #trainings = db.relationship('TrainingTemplate', backref='training_templates.id', lazy=True)
    #training_results = db.relationship('TrainingResult', backref='logs', lazy=True)
    training_results = db.Column(db.Integer, db.ForeignKey('training_result.id'), nullable=False)

    def __repr__(self):
        return f'<Training {self.training_template.title} for {self.user.username}>'

class TrainingTemplate(db.Model):
    __tablename__ = 'training_template'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    validity_period = db.Column(db.Integer, nullable=False)  # in days
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    trainings = db.relationship('Training_log', backref='training_template', lazy=True)
    evaluation_type_id = db.Column(db.Integer, db.ForeignKey('evaluation_type.id'), nullable=False)

    def __repr__(self):
        return f'<TrainingTemplate {self.title}>'

    
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    users = db.relationship('User', backref='department', lazy=True, foreign_keys='User.department_id')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def get_team(self):
        return self.users
    
    def get_training_matrix(self):
        team = self.get_team()
        matrix = []
        for user in team:
            completed = [{'template': training.training_template.title, 'completion_date': training.completion_date} for training in user.completed_trainings]
            assigned = [{'template': assigned.training_template.title, 'due_date': assigned.due_date} for assigned in AssignedTraining.query.filter_by(user_id=user.id, is_completed=False)]
            matrix.append({
                'user': f'{user.username}',
                'completed_trainings': completed,
                'assigned_trainings': assigned
            })
        return matrix
    
    def __repr__(self):
        return f'<Department {self.name}>'
    
class AssignedTraining(db.Model):
    __tablename__ = 'assigned_training'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    training_template_id = db.Column(db.Integer, db.ForeignKey('training_template.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AssignedTraining User: {self.user_id}, Training: {self.training_template_id}>'
    
    def mark_completed(self):
        try:
            self.is_completed = True
            self.due_date = None
            db.session.commit()
        except Exception as e:
            logger.error(f'Error marking training as completed: {e}')
            db.session.rollback()
        
        
class TrainingResult(db.Model):
    __tablename__ = 'training_result'
    # This models stores the possible results of the training
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class EvaluationType(db.Model):
    __tablename__ = 'evaluation_type'
    # This model stores the types of evaluations that can be done on a training
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

class UserStatus(db.Model):
    __tablename__ = 'user_status'
    # This model stores the status of the user
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    